#!/usr/bin/env python3
"""Auto-link IDs, glossary terms and abbreviations in a finished HTML page.

Usage:
    python -I autolink.py IN.html -o OUT.html [--prefixes G A Q D L P] [--internal-only] [--check]

ID prefixes: --prefixes wins; otherwise the data-id-prefixes attribute of <main> (the same
attribute the reader reads); only when neither exists the default G A Q D L P applies.

Inputs read from the page itself:
  * defined IDs: elements with class "defid" (explicit), list lines "ID. text"
    and the first cell of a table row "ID | text" (automatic); when the table has a
    column headed Meaning, Description or Definition, the hover also carries it;
  * glossary terms: rows of a table with the attribute data-glossary
    (first column term, second column definition, optional column headed Aliases with
    comma-separated synonyms, header case-insensitive) and <dt class="defterm"> items of a
    definition list (the next <dd> is the definition; data-aliases adds synonyms);
  * abbreviations: rows of a table with the attribute data-abbr
    (first column abbreviation, second column expansion).

Output: mentions become <a class="ref" href="#def-ID" data-tip="ID \u00b7 short name \u00b7 meaning">
and <a class="term" href="#term-slug" data-tip="term \u00b7 short definition">; the first
use of an abbreviation gets <abbr title>. A link already in the page (hand-written or from an
earlier run) counts as the first mention in its block, so a second run changes nothing.
Exit code 1 when an ID is used without a definition, an in-page anchor has no target, or
(--internal-only) a link leaves the page.
Prefixes may have several letters and end with one dash (ADR-, CMD, OPT, ERR-).

Never linked at build time (the same set the browser-side linker in assets/reader/reader.js skips):
  tags: a, code, pre, h1-h6, abbr, button, script, style, textarea, select, nav, svg, title, kbd, samp;
  classes: .defid, .defterm, .tag, .hlink, .copy, .pop, .mermaid, .diagram, .figbar, plus
  .ref and .term (links already made);
  attribute: [data-no-link] on the element or any ancestor.
Standard library only.
"""
import argparse
import html as H
import re
import sys

DEFAULT_PREFIXES = ["G", "A", "Q", "D", "L", "P"]
SKIP_TAGS = {"code", "pre", "a", "h1", "h2", "h3", "h4", "h5", "h6", "abbr", "script", "style",
             "title", "button", "textarea", "select", "nav", "svg", "kbd", "samp"}
SKIP_CLASSES = {"diagram", "defid", "defterm", "ref", "term", "mermaid", "tag", "hlink", "copy", "pop", "figbar"}
SKIP_ATTR = "data-no-link"
BLOCK_TAGS = {"p", "li", "td", "th", "dd", "dt"}
DEF_BLOCKS = {"li", "p", "dd", "dt", "td", "th", "h1", "h2", "h3", "h4", "h5", "h6"}
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
P_CLOSERS = {"div", "ul", "ol", "table", "h1", "h2", "h3", "h4", "h5", "h6", "pre", "blockquote",
             "section", "dl", "figure", "form", "hr"}

TOKEN_RE = re.compile(
    r"""<!--.*?-->|<!\[CDATA\[.*?\]\]>|<(script|style)\b[^>]*>.*?</\1\s*>"""
    r"""|</?[A-Za-z][^\s>/]*(?:[^>"']|"[^"]*"|'[^']*')*>|<![^>]*>""",
    re.S | re.I)
ATTR_RE = re.compile(r"""([^\s"'<>/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'>]+)))?""")


def tokenize(src):
    """Split HTML into tokens. Returns (tokens, kinds); kinds: text open close void comment raw."""
    tokens, kinds, pos = [], [], 0
    for m in TOKEN_RE.finditer(src):
        if m.start() > pos:
            tokens.append(src[pos:m.start()])
            kinds.append("text")
        tok = m.group(0)
        tokens.append(tok)
        kinds.append(_classify(tok, m.group(1)))
        pos = m.end()
    if pos < len(src):
        tokens.append(src[pos:])
        kinds.append("text")
    tokens.append("")  # sentinel: closes anything still open at the end
    kinds.append("text")
    return tokens, kinds


def _classify(tok, raw_tag):
    if raw_tag:
        return "raw"
    if tok.startswith("<!"):
        return "comment"
    m = re.match(r"<(/?)([A-Za-z][^\s>/]*)", tok)
    tag = m.group(2).lower()
    if m.group(1):
        return "close"
    if tok.endswith("/>") or tag in VOID:
        return "void"
    return "open"


def tag_of(tok):
    return re.match(r"</?([A-Za-z][^\s>/]*)", tok).group(1).lower()


def page_prefixes(src):
    """Prefixes from data-id-prefixes on the <main> element, or an empty list."""
    m = re.search(r"""<main(?=[\s>])[^>]*?\sdata-id-prefixes\s*=\s*(?:"([^"]*)"|'([^']*)')""", src, re.I)
    if not m:
        return []
    raw = H.unescape(m.group(1) if m.group(1) is not None else m.group(2))
    return [p for p in re.split(r"[\s,]+", raw) if p]


def parse_attrs(tok):
    inner = re.sub(r"^</?[A-Za-z][^\s>/]*", "", tok)
    inner = re.sub(r"/?>$", "", inner)
    attrs = {}
    for m in ATTR_RE.finditer(inner):
        val = m.group(2) if m.group(2) is not None else m.group(3) if m.group(3) is not None else m.group(4)
        attrs[m.group(1).lower()] = H.unescape(val) if val is not None else ""
    return attrs


class Node:
    __slots__ = ("tag", "attrs", "open", "close", "children", "parent")

    def __init__(self, tag, attrs, open_idx, parent):
        self.tag, self.attrs, self.open, self.close = tag, attrs, open_idx, open_idx
        self.children, self.parent = [], parent

    @property
    def classes(self):
        return set(self.attrs.get("class", "").split())


def build_tree(tokens, kinds):
    root = Node("#root", {}, -1, None)
    root.close = len(tokens)
    cur = root

    def close_chain(node, target, idx):
        n = node
        while True:
            n.close = idx
            if n is target:
                return n.parent
            n = n.parent

    def implied(node, tag, idx):
        stops = {"li": ("ul", "ol"), "td": ("tr", "table"), "th": ("tr", "table"),
                 "tr": ("table", "tbody", "thead", "tfoot"), "dd": ("dl",), "dt": ("dl",)}
        if tag in stops:
            same = {"li": ("li",), "td": ("td", "th"), "th": ("td", "th"), "tr": ("tr",),
                    "dd": ("dd", "dt"), "dt": ("dd", "dt")}[tag]
            n = node
            while n is not None and n.tag != "#root" and n.tag not in stops[tag]:
                if n.tag in same:
                    return close_chain(node, n, idx)
                n = n.parent
        if tag in P_CLOSERS and node.tag == "p":
            return close_chain(node, node, idx)
        return node

    for i, (tok, kind) in enumerate(zip(tokens, kinds)):
        if kind == "text":
            if tok:
                cur.children.append(i)
        elif kind == "open":
            tag = tag_of(tok)
            cur = implied(cur, tag, i)
            node = Node(tag, parse_attrs(tok), i, cur)
            cur.children.append(node)
            cur = node
        elif kind in ("void", "raw"):
            node = Node(tag_of(tok), parse_attrs(tok), i, cur)
            cur.children.append(node)
        elif kind == "close":
            tag = tag_of(tok)
            n = cur
            while n is not None and n.tag != "#root" and n.tag != tag:
                n = n.parent
            if n is not None and n.tag == tag:
                cur = close_chain(cur, n, i)
    while cur is not None and cur.tag != "#root":
        cur.close = len(tokens) - 1
        cur = cur.parent
    return root


def walk_nodes(node):
    for ch in node.children:
        if isinstance(ch, Node):
            yield ch
            yield from walk_nodes(ch)


def text_of(node, tokens, kinds, stop_lists=False):
    """Text content of a node, tags removed, entities decoded, spaces collapsed."""
    return norm(_collect(tokens, kinds, node.open + 1, node.close, stop_lists))


def _collect(tokens, kinds, start, end, stop_lists=False, first=""):
    parts = [first] if first else []
    for i in range(start, min(end, len(tokens))):
        if kinds[i] == "text":
            parts.append(tokens[i])
        elif kinds[i] == "open" and stop_lists and tag_of(tokens[i]) in ("ul", "ol"):
            break
    return "".join(parts)


def norm(text):
    return re.sub(r"\s+", " ", H.unescape(text)).strip()


def short(text, n=110):
    t = re.sub(r"`|\*\*|\[|\]\([^)]*\)", "", text).strip()
    t = re.split(r"(?<=[a-z0-9)])\. ", t, maxsplit=1)[0] if len(t) > n else t
    return (t[: n - 1] + "\u2026") if len(t) > n else t


def slug(term):
    """Same as slug() in assets/reader/reader.js: lower case, runs of [^a-z0-9] become one dash
    (accented letters are not kept), dashes trimmed, empty becomes 'section'."""
    return "term-" + (re.sub(r"[^a-z0-9]+", "-", str(term).lower()).strip("-") or "section")


MEANING_HEADERS = {"meaning", "description", "definition"}
TIP_MAX = 160
PREFIX_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*-?$")


def parse_prefixes(values):
    """Validate ID prefixes: letters and digits, first a letter, optionally one trailing dash.
    Each value may hold several prefixes separated by commas. Raises ValueError."""
    out = []
    for v in values:
        for p in v.split(","):
            p = p.strip()
            if not PREFIX_RE.match(p):
                raise ValueError(f"invalid ID prefix {p!r}: use letters and digits, starting with a letter, "
                                 "with at most one trailing dash (G, ADR-, CMD)")
            if p not in out:
                out.append(p)
    return out


def trim(text, n=TIP_MAX):
    return (text[: n - 1].rstrip() + "\u2026") if len(text) > n else text


class Def:
    def __init__(self, id_, anchor, short_, prio, order):
        self.id, self.anchor, self.short, self.prio, self.order = id_, anchor, short_, prio, order


class AutoLinker:
    def __init__(self, src, prefixes=None, internal_only=False):
        self.src = src
        self.prefixes = prefixes or page_prefixes(src) or DEFAULT_PREFIXES
        self.internal_only = internal_only
        pfx = "|".join(re.escape(p) for p in sorted(self.prefixes, key=len, reverse=True))
        self.id_full = re.compile(r"^(?:" + pfx + r")\d+[a-z]?$")
        self.id_start = re.compile(r"^(\s*)((?:" + pfx + r")\d+[a-z]?)\.(?=\s|$)")
        self.id_pat = (r"(?<![\w\[#/.&-])(?P<id>(?:" + pfx + r")\d+[a-z]?)(?![\w-])"
                       r"(?! (?:context|container|model|deployment|style|n\b|\d))")
        self.tokens, self.kinds = tokenize(src)
        self.out = list(self.tokens)
        self.root = build_tree(self.tokens, self.kinds)
        self.defs = {}
        self.dups = []
        self.anchor_at = {}       # text token index -> (start, end, id, anchor id)
        self.skip_nodes = set()   # nodes whose content must not be linked (wrapped cells)
        self.terms = {}           # term -> (anchor id, short)
        self.aliases = {}         # alias -> term
        self.term_of_anchor = {}  # anchor id -> term
        self.slug_owner = {}      # generated anchor -> term, to warn about collisions
        self.pre_seen = {}        # block node (or None for the page) -> keys already linked in it
        self._meaning_col = {}    # table node -> index of its Meaning column, or None
        self.abbrs = {}           # abbreviation -> expansion
        self.abbr_used = set()
        self.undefined = set()
        self.referenced = set()
        self.external = []
        self.warnings = []

    # ---------------------------------------------------------------- collection
    def in_skip(self, node):
        n = node.parent
        while n is not None and n.tag != "#root":
            if n.tag in SKIP_TAGS or SKIP_ATTR in n.attrs or (n.classes & (SKIP_CLASSES - {"defid", "defterm"})):
                return True
            n = n.parent
        return False

    def _table_of(self, node):
        n = node
        while n is not None and n.tag != "table":
            n = n.parent
        return n

    def _cells(self, tr):
        return [c for c in tr.children if isinstance(c, Node) and c.tag in ("td", "th")]

    def collect(self):
        t, k = self.tokens, self.kinds
        cands = []  # (prio, order, id, anchor, short, edit)
        order = 0
        nodes = list(walk_nodes(self.root))
        # glossary and abbreviation tables first
        for tbl in (n for n in nodes if n.tag == "table"):
            if "data-glossary" in tbl.attrs:
                self._glossary(tbl)
            elif "data-abbr" in tbl.attrs:
                self._abbreviations(tbl)
        for dt in (n for n in nodes if n.tag == "dt" and "defterm" in n.classes):
            self._dl_term(dt)
        for node in nodes:
            if self.in_skip(node):
                continue
            tbl = self._table_of(node)
            in_special = tbl is not None and ("data-glossary" in tbl.attrs or "data-abbr" in tbl.attrs)
            order += 1
            # 1. explicit class defid
            if "defid" in node.classes:
                text = text_of(node, t, k)
                if not self.id_full.match(text):
                    self.warnings.append(f"element with class defid does not contain an ID: {text[:40]!r}")
                    continue
                anchor = node.attrs.get("id") or f"def-{text}"
                edit = ("add_id", node, anchor) if "id" not in node.attrs else None
                cands.append((0, order, text, anchor, self._short_after(node), edit))
            # 2. list line "ID. text"
            elif node.tag == "li" and not in_special:
                hit = self._li_def(node)
                if hit:
                    idx, m, rest_first = hit
                    i = m.group(2)
                    anchor = f"def-{i}"
                    text = short(norm(_collect(t, k, idx + 1, node.close, True, rest_first)))
                    cands.append((1, order, i, anchor, text, ("text", idx, m.start(2), m.end(2), i, anchor)))
            # 3. table row whose first cell is exactly the ID
            elif node.tag == "tr" and not in_special:
                cells = self._cells(node)
                if len(cells) < 1 or any(self._is_header_cell(c) for c in cells[:1]):
                    continue
                first = cells[0]
                if any("defid" in d.classes for d in walk_nodes(first)) or "defid" in first.classes:
                    continue
                text = text_of(first, t, k)
                if self.id_full.match(text):
                    anchor = f"def-{text}"
                    sh = self._row_desc(cells, 1, self._table_of(node)) if len(cells) > 1 else ""
                    cands.append((2, order, text, anchor, sh, ("wrap", first, text, anchor)))
        # winners: lowest (priority, document order) per ID
        seen_ids = {}
        for c in sorted(cands, key=lambda c: (c[0], c[1])):
            prio, _o, i, anchor, sh, edit = c
            if i in seen_ids:
                self.dups.append(i)
                continue
            seen_ids[i] = True
            self.defs[i] = Def(i, anchor, sh, prio, _o)
            self._apply_edit(edit)

    def _is_header_cell(self, cell):
        n = cell.parent
        while n is not None and n.tag not in ("table", "#root"):
            if n.tag == "thead":
                return True
            n = n.parent
        return False

    def _meaning_index(self, tbl):
        """Index of the column headed Meaning, Description or Definition (case-insensitive), or None."""
        if tbl is None:
            return None
        if tbl not in self._meaning_col:
            idx = None
            for tr in (n for n in walk_nodes(tbl) if n.tag == "tr"):
                cells = self._cells(tr)
                if cells and (self._is_header_cell(cells[0]) or all(c.tag == "th" for c in cells)):
                    for i, c in enumerate(cells):
                        if text_of(c, self.tokens, self.kinds).lower() in MEANING_HEADERS:
                            idx = i
                            break
                    break
            self._meaning_col[tbl] = idx
        return self._meaning_col[tbl]

    def _row_desc(self, cells, name_idx, tbl):
        """Hover text after the ID: the short name in cell name_idx, plus the Meaning column if the table has one."""
        t, k = self.tokens, self.kinds
        m_idx = self._meaning_index(tbl)
        if m_idx == name_idx:
            return trim(short(text_of(cells[name_idx], t, k), TIP_MAX))
        name = short(text_of(cells[name_idx], t, k))
        if m_idx is not None and m_idx < len(cells) and cells[m_idx] is not cells[name_idx]:
            meaning = short(text_of(cells[m_idx], t, k), TIP_MAX)
            if meaning:
                return trim(f"{name} \u00b7 {meaning}" if name else meaning)
        return name

    def _li_def(self, li):
        """First non-blank text of the list item, before any nested list, starting with 'ID.'"""
        t, k = self.tokens, self.kinds
        for i in range(li.open + 1, li.close):
            if k[i] == "open" and tag_of(t[i]) in ("ul", "ol"):
                return None
            if k[i] == "text" and t[i].strip():
                m = self.id_start.match(t[i])
                return (i, m, t[i][m.end():]) if m else None
        return None

    def _short_after(self, node):
        """Text that follows an explicit defid element inside its row or block."""
        t, k = self.tokens, self.kinds
        if node.tag in ("td", "th") and node.parent is not None and node.parent.tag == "tr":
            cells = self._cells(node.parent)
            pos = cells.index(node) if node in cells else -1
            if 0 <= pos < len(cells) - 1:
                return self._row_desc(cells, pos + 1, self._table_of(node))
            return ""
        n = node.parent
        while n is not None and n.tag not in DEF_BLOCKS and n.tag != "#root":
            n = n.parent
        if n is None or n.tag == "#root":
            return ""
        text = norm(_collect(t, k, node.close + 1, n.close, True))
        if not text and n.tag in ("td", "th"):
            return self._short_after(n)
        return short(text.lstrip(" .:-\u2013\u2014\u00a0"))

    def _apply_edit(self, edit):
        if edit is None:
            return
        kind = edit[0]
        if kind == "add_id":
            _, node, anchor = edit
            self.out[node.open] = re.sub(r"^<([A-Za-z][^\s>/]*)", lambda m: f'<{m.group(1)} id="{anchor}"',
                                         self.tokens[node.open], count=1)
        elif kind == "text":
            _, idx, s, e, i, anchor = edit
            self.anchor_at[idx] = (s, e, i, anchor)
        elif kind == "wrap":
            _, cell, i, anchor = edit
            self._wrap_cell(cell, "defid", anchor)

    def _wrap_cell(self, cell, cls, anchor):
        self.out[cell.open] = self.tokens[cell.open] + f'<span class="{cls}" id="{anchor}">'
        self.out[cell.close] = "</span>" + self.tokens[cell.close]
        self.skip_nodes.add(cell)

    def _aliases_index(self, tbl):
        """Index of the column headed Aliases (case-insensitive) in the header row, or None."""
        for tr in (n for n in walk_nodes(tbl) if n.tag == "tr"):
            cells = self._cells(tr)
            if cells and (self._is_header_cell(cells[0]) or all(c.tag == "th" for c in cells)):
                for i, c in enumerate(cells):
                    if text_of(c, self.tokens, self.kinds).lower() == "aliases":
                        return i
                return None
        return None

    def _glossary(self, tbl):
        t, k = self.tokens, self.kinds
        a_idx = self._aliases_index(tbl)
        for tr in (n for n in walk_nodes(tbl) if n.tag == "tr"):
            cells = self._cells(tr)
            if len(cells) < 2 or cells[0].tag == "th" or self._is_header_cell(cells[0]):
                continue
            term = text_of(cells[0], t, k)
            if not term or term in self.terms:
                continue
            existing = next((d for d in walk_nodes(cells[0]) if "defterm" in d.classes), None)
            anchor = (existing.attrs.get("id") if existing else None) or self._new_anchor(term)
            aliases = [existing.attrs.get("data-aliases", "") if existing else ""]
            if a_idx is not None and 0 < a_idx < len(cells):
                aliases.append(text_of(cells[a_idx], t, k))
            self._add_term(term, anchor, short(text_of(cells[1], t, k), TIP_MAX), ",".join(aliases))
            if existing:
                self.skip_nodes.add(cells[0])
            else:
                self._wrap_cell(cells[0], "defterm", anchor)

    def _dl_term(self, dt):
        """A <dt class="defterm"> of a definition list; the next <dd> sibling is its definition."""
        t, k = self.tokens, self.kinds
        term = text_of(dt, t, k)
        if not term or term in self.terms:
            return
        anchor = dt.attrs.get("id")
        if not anchor:
            anchor = self._new_anchor(term)
            self.out[dt.open] = re.sub(r"^<([A-Za-z][^\s>/]*)", lambda m: f'<{m.group(1)} id="{anchor}"',
                                       self.tokens[dt.open], count=1)
        sibs = dt.parent.children if dt.parent is not None else []
        after = sibs[sibs.index(dt) + 1:] if dt in sibs else []
        dd = next((s for s in after if isinstance(s, Node) and s.tag == "dd"), None)
        self._add_term(term, anchor, short(text_of(dd, t, k), TIP_MAX) if dd is not None else "",
                       dt.attrs.get("data-aliases", ""))
        self.skip_nodes.add(dt)

    def _new_anchor(self, term):
        a = slug(term)
        if a in self.slug_owner and self.slug_owner[a] != term:
            self.warnings.append(f"terms {self.slug_owner[a]!r} and {term!r} share the anchor {a!r}; "
                                 "give one of them an explicit id")
        self.slug_owner.setdefault(a, term)
        return a

    def _add_term(self, term, anchor, desc, aliases=""):
        self.terms[term] = (anchor, desc)
        self.term_of_anchor.setdefault(anchor, term)
        for a in (x.strip() for x in aliases.split(",")):
            if a and a not in self.terms and a not in self.aliases:
                self.aliases[a] = term

    def _abbreviations(self, tbl):
        t, k = self.tokens, self.kinds
        for tr in (n for n in walk_nodes(tbl) if n.tag == "tr"):
            cells = self._cells(tr)
            if len(cells) < 2 or cells[0].tag == "th" or self._is_header_cell(cells[0]):
                continue
            ab = text_of(cells[0], t, k)
            if ab and ab not in self.abbrs:
                self.abbrs[ab] = text_of(cells[1], t, k)

    # ------------------------------------------------------------------- linking
    def _build_regex(self):
        parts = []
        if self.prefixes:
            parts.append(self.id_pat)
        if self.terms:
            names = "|".join(re.escape(x) for x in sorted([*self.terms, *self.aliases], key=len, reverse=True))
            parts.append(r"(?<![\w-])(?P<term>" + names + r")(?:s|es)?(?![\w-])")
        if self.abbrs:
            names = "|".join(re.escape(x) for x in sorted(self.abbrs, key=len, reverse=True))
            parts.append(r"(?<![\w-])(?P<abbr>" + names + r")(?![\w-])")
        self.rx = re.compile("|".join(parts)) if parts else None

    def _tip(self, name, desc):
        return H.escape(f"{name} \u00b7 {desc}" if desc else name, quote=True)

    def _repl(self, m, seen):
        if m.groupdict().get("id"):
            i = m.group("id")
            if i not in self.defs:
                self.undefined.add(i)
                if ("id", i) in seen:
                    return m.group(0)
                seen.add(("id", i))
                return f'<span class="ref missing" title="No definition found">{i}</span>'
            self.referenced.add(i)
            if ("id", i) in seen:
                return m.group(0)
            seen.add(("id", i))
            d = self.defs[i]
            return f'<a class="ref" href="#{d.anchor}" data-tip="{self._tip(i, d.short)}">{i}</a>'
        if m.groupdict().get("term"):
            term = m.group("term")
            canon = self.terms.get(term) and term or self.aliases.get(term, term)
            if ("term", canon) not in seen:
                seen.add(("term", canon))
                anchor, desc = self.terms[canon]
                return f'<a class="term" href="#{anchor}" data-tip="{self._tip(canon, desc)}">{m.group(0)}</a>'
            if term not in self.abbrs:
                return m.group(0)
            ab = term
        else:
            ab = m.group("abbr")
        if ab in self.abbr_used:
            return m.group(0)
        self.abbr_used.add(ab)
        return f'<abbr title="{H.escape(self.abbrs[ab], quote=True)}">{ab}</abbr>'

    def link_text(self, text, seen):
        if self.rx is None or not text:
            return text
        out, pos = [], 0
        for m in self.rx.finditer(text):
            out.append(text[pos:m.start()])
            out.append(self._repl(m, seen))
            pos = m.end()
        out.append(text[pos:])
        return "".join(out)

    def _is_external(self, href):
        return bool(re.match(r"(?i)^(?:https?:|ftp:|//)", href))

    def _leaves_page(self, href):
        if href.startswith("#") or not href:
            return False
        return not re.match(r"(?i)^(?:mailto:|tel:|javascript:|data:)", href)

    def _mark_external(self, node):
        href = node.attrs.get("href", "")
        if self._leaves_page(href):
            self.external.append(href)
        if not self._is_external(href) or self.internal_only:
            return
        tok = self.out[node.open]
        if "target" not in node.attrs:
            tok = tok[:-1] + ' target="_blank">'
        rel = node.attrs.get("rel")
        if rel is None:
            tok = tok[:-1] + ' rel="noopener">'
        elif "noopener" not in rel.split():
            tok = re.sub(r"""(rel\s*=\s*)(["'])(.*?)\2""", lambda m: f'{m.group(1)}{m.group(2)}{m.group(3)} noopener{m.group(2)}',
                         tok, count=1)
        self.out[node.open] = tok

    def _visit(self, node, skip, seen):
        classes = node.classes
        nskip = (skip or node.tag in SKIP_TAGS or bool(classes & SKIP_CLASSES) or node in self.skip_nodes
                 or "data-abbr" in node.attrs or SKIP_ATTR in node.attrs)
        nseen = set(self.pre_seen.get(node, ())) if node.tag in BLOCK_TAGS else seen
        if node.tag == "a" and node.attrs.get("href") is not None:
            self._mark_external(node)
        if {"ref", "missing"} <= classes:
            self.undefined.add(text_of(node, self.tokens, self.kinds))
        if node.tag == "abbr":
            self.abbr_used.add(text_of(node, self.tokens, self.kinds))
        self._walk(node, nskip, nseen)

    def _walk(self, node, skip, seen):
        for ch in node.children:
            if isinstance(ch, Node):
                self._visit(ch, skip, seen)
                continue
            tok = self.tokens[ch]
            if ch in self.anchor_at:
                s, e, i, anchor = self.anchor_at[ch]
                before = tok[:s] if skip else self.link_text(tok[:s], seen)
                after = tok[e:] if skip else self.link_text(tok[e:], seen)
                self.out[ch] = before + f'<span class="defid" id="{anchor}">{i}</span>' + after
            elif not skip:
                self.out[ch] = self.link_text(tok, seen)

    def _existing_links(self):
        """A link already in the page to a defined ID or term (or one of its aliases or plurals)
        counts as the first mention in its block, wherever it sits in that block."""
        for a in (n for n in walk_nodes(self.root) if n.tag == "a"):
            href = a.attrs.get("href", "")
            if href.startswith("#def-"):
                i = next((d.id for d in self.defs.values() if d.anchor == href[1:]), None)
                key = ("id", i) if i else None
            elif href.startswith("#term-"):
                term = self.term_of_anchor.get(href[1:])
                key = ("term", term) if term else None
            else:
                key = None
            if key is None:
                continue
            blk = a.parent
            while blk is not None and blk.tag != "#root" and blk.tag not in BLOCK_TAGS:
                blk = blk.parent
            self.pre_seen.setdefault(blk if blk is not None and blk.tag != "#root" else None, set()).add(key)

    def run(self):
        self.collect()
        self._build_regex()
        self._existing_links()
        # abbreviations already expanded in the source count as first use
        for n in walk_nodes(self.root):
            if n.tag == "abbr":
                self.abbr_used.add(text_of(n, self.tokens, self.kinds))
        self._walk(self.root, False, set(self.pre_seen.get(None, ())))
        return "".join(self.out)


def check_anchors(result):
    """Return (broken in-page anchors, ids defined)."""
    tokens, kinds = tokenize(result)
    ids, hrefs = set(), set()
    for tok, kind in zip(tokens, kinds):
        if kind in ("open", "void"):
            attrs = parse_attrs(tok)
            if "id" in attrs:
                ids.add(attrs["id"])
            if tag_of(tok) == "a" and "name" in attrs:
                ids.add(attrs["name"])
            href = attrs.get("href", "")
            if tag_of(tok) in ("a", "area") and href.startswith("#") and len(href) > 1 and not href.startswith("#:~:"):
                hrefs.add(href[1:])
    return sorted(h for h in hrefs if h not in ids)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Auto-link IDs, glossary terms and abbreviations in an HTML page.")
    ap.add_argument("input")
    ap.add_argument("-o", "--output", help="output file (required unless --check)")
    ap.add_argument("--prefixes", nargs="+", default=None,
                    help="ID prefixes, one or more letters, optionally ending with a dash, e.g. ADR- CMD "
                         "(default: data-id-prefixes of <main>, else G A Q D L P)")
    ap.add_argument("--internal-only", action="store_true", help="report every link that leaves the page as an error")
    ap.add_argument("--check", action="store_true", help="only report, write nothing")
    args = ap.parse_args(argv)
    if not args.check and not args.output:
        ap.error("-o is required unless --check is given")
    with open(args.input, encoding="utf-8", newline="") as f:
        src = f.read()
    try:
        prefixes = parse_prefixes(args.prefixes or page_prefixes(src) or DEFAULT_PREFIXES)
    except ValueError as e:
        ap.error(str(e))
    linker = AutoLinker(src, prefixes, args.internal_only)
    result = linker.run()
    if not args.check:
        with open(args.output, "w", encoding="utf-8", newline="") as f:
            f.write(result)
    broken = check_anchors(result)
    undefined = sorted(linker.undefined)
    external = sorted(set(linker.external)) if args.internal_only else []
    print(f"IDs defined: {len(linker.defs)}; referenced: {len(linker.referenced)}; "
          f"glossary terms: {len(linker.terms)}; abbreviations: {len(linker.abbrs)}")
    print("undefined IDs:", undefined)
    print("broken anchors:", broken)
    if args.internal_only:
        print("links that leave the page:", external)
    if linker.dups:
        print("warning, IDs defined more than once (first wins):", sorted(set(linker.dups)))
    for w in linker.warnings:
        print("warning:", w)
    return 1 if (undefined or broken or external) else 0


if __name__ == "__main__":
    sys.exit(main())
