"""Check that a rewrite kept every fact token of the original.

Usage:
    python -I preserve.py ORIGINAL REVISED [--prefixes G A Q D L P] [--tags UNTESTED SAMPLE] [--legacy]

ORIGINAL and REVISED are Markdown or HTML files (.html and .htm are read as HTML, anything else as
Markdown; a file whose first non-blank character is "<" is also read as HTML). Compares, as multisets:
  heading   Markdown # lines, or the text of h1 to h6;
  code      fenced blocks, or the text of <pre>;
  inline    `code` spans, or <code> outside <pre>;
  tag       bracketed evidence tags such as [UNTESTED] or [SAMPLE: x]; only the tag names given by --tags
            are tracked (default none), each a regular expression fragment, so "NOT VERIFIED" works;
  url       Markdown link targets, or href values of <a> (in-page "#..." hrefs are ignored, because the
            auto-linker adds and removes them);
  id        defined-ID tokens built from --prefixes (default G A Q D L P): a prefix, digits and an
            optional lower-case letter, so Q13b, CMD2 and ADR-12 are IDs. Prefixes may end with a dash;
  number    numbers in the visible text (HTML: text outside script, style, pre and code).
Visible prose is not compared word by word, since a rewrite changes it on purpose.
Prints LOST (in original, missing or fewer in revised) and ADDED (new in revised). Exit 1 if anything is
LOST in headings, code, tags, URLs or IDs, or if a number was ADDED.

--legacy restores the first version of this script: the ID grammar of one project
(ADR-n, BRn, QSn, ACn and single letters R P G N A Q L I C K D U T) and the tags LIVE, FILES, PLATFORM,
NOT VERIFIED, RENDER and "?". Explicit --prefixes or --tags still override its parts.
"""
import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser

DEFAULT_PREFIXES = ["G", "A", "Q", "D", "L", "P"]
LEGACY_ID = r"(?<![\w-])(?:ADR-\d{1,2}(?!\d)|BR\d+|QS\d+|AC\d+|[RPGNAQLICKDUT]\d+[a-z]?)(?![\w])"
LEGACY_TAGS = ["LIVE", "FILES", "PLATFORM", "NOT VERIFIED", "RENDER", r"\?"]
NUMBER = r"(?<![\w.])\d[\d.,:]*\d%?|(?<![\w.])\d%?"
HEADINGS = {"h1", "h2", "h3", "h4", "h5", "h6"}


def id_regex(prefixes):
    alts = "|".join(re.escape(p) for p in sorted(prefixes, key=len, reverse=True))
    return r"(?<![\w-])(?:" + alts + r")\d+[a-z]?(?![\w])"


def tag_regex(tags):
    return r"\[(?:" + "|".join(tags) + r")[^\]]*\]"


def _finish(kinds, bare, id_rx, tag_rx, tag_text):
    kinds["tag"] = Counter(re.findall(tag_rx, tag_text)) if tag_rx else Counter()
    kinds["id"] = Counter(re.findall(id_rx, bare))
    kinds["number"] = Counter(re.findall(NUMBER, bare))
    return kinds


def markdown_tokens(text, id_rx, tag_rx):
    fences = re.findall(r"```.*?```", text, flags=re.S)
    prose = re.sub(r"```.*?```", "", text, flags=re.S)
    out = {
        "heading": Counter(l.strip() for l in prose.splitlines() if re.match(r"^#{1,6} ", l)),
        "code": Counter(fences),
        "inline": Counter(re.findall(r"`[^`\n]+`", prose)),
        "url": Counter(re.findall(r"\]\(([^)\s]+)\)", prose)),
    }
    bare = re.sub(r"`[^`\n]+`", "", prose)
    bare = re.sub(r"\]\([^)]*\)", "]", bare)
    return _finish(out, bare, id_rx, tag_rx, prose)


class _Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.headings, self.pre, self.code, self.urls = [], [], [], []
        self.visible, self.alltext = [], []
        self._stack = []          # open tags we care about
        self._buf = {}            # tag -> collected text of the innermost open one

    def _in(self, *tags):
        return any(t in self._stack for t in tags)

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href") or ""
            if href and not href.startswith("#"):
                self.urls.append(href)
        if tag in HEADINGS | {"pre", "code", "script", "style"}:
            self._stack.append(tag)
            self._buf[tag] = []

    def handle_endtag(self, tag):
        if tag in self._stack:
            while self._stack:
                top = self._stack.pop()
                text = "".join(self._buf.pop(top, []))
                if top in HEADINGS:
                    self.headings.append(f"{'#' * int(top[1])} {re.sub(chr(32) + '+', chr(32), ' '.join(text.split()))}")
                elif top == "pre":
                    self.pre.append(text)
                elif top == "code" and not self._in("pre"):
                    self.code.append(f"`{text}`")
                if top == tag:
                    break

    def handle_data(self, data):
        if self._in("script", "style"):
            return
        for t in self._stack:
            self._buf[t].append(data)
        self.alltext.append(data)
        if not self._in("pre", "code"):
            self.visible.append(data)


def html_tokens(text, id_rx, tag_rx):
    p = _Page()
    p.feed(text)
    p.close()
    out = {
        "heading": Counter(p.headings),
        "code": Counter(s.strip("\n") for s in p.pre),
        "inline": Counter(p.code),
        "url": Counter(p.urls),
    }
    bare = " ".join(p.visible)
    return _finish(out, bare, id_rx, tag_rx, "".join(p.alltext))


def is_html(path, text):
    return path.lower().endswith((".html", ".htm")) or text.lstrip().startswith("<")


def tokens(path, text, id_rx, tag_rx):
    return (html_tokens if is_html(path, text) else markdown_tokens)(text, id_rx, tag_rx)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check that a rewrite kept every fact token of the original.")
    ap.add_argument("original")
    ap.add_argument("revised")
    ap.add_argument("--prefixes", nargs="+", help="ID prefixes (default: G A Q D L P)")
    ap.add_argument("--tags", nargs="+", help="evidence tag names tracked inside [...] (default: none)")
    ap.add_argument("--legacy", action="store_true", help="the first version's project-specific IDs and tags")
    args = ap.parse_args(argv)
    if args.prefixes:
        id_rx = id_regex([p for v in args.prefixes for p in v.split(",") if p])
    elif args.legacy:
        id_rx = LEGACY_ID
    else:
        id_rx = id_regex(DEFAULT_PREFIXES)
    tags = args.tags if args.tags else (LEGACY_TAGS if args.legacy else [])
    tag_rx = tag_regex(tags) if tags else None
    pa, pb = args.original, args.revised
    ta, tb = read(pa), read(pb)
    a, b = tokens(pa, ta, id_rx, tag_rx), tokens(pb, tb, id_rx, tag_rx)
    bad = False
    for kind in a:
        lost = a[kind] - b[kind]
        added = b[kind] - a[kind]
        strict_lost = kind in ("heading", "code", "tag", "url", "id")
        if lost:
            print(f"LOST {kind} ({sum(lost.values())}):", list(lost.items())[:40])
            bad = bad or strict_lost
        if added and kind in ("number", "id", "tag", "url", "code"):
            print(f"ADDED {kind} ({sum(added.values())}):", list(added.items())[:40])
            bad = bad or kind == "number"
    print("RESULT:", "FAIL" if bad else "OK")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
