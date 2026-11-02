# Linking rules

Links are how a reader gets from a claim to its source and from a word to its meaning. Apply these rules to any document. For a published page, `scripts/autolink.py` applies most of them mechanically.

## What becomes a link

| Mention | Link target | Shown on hover or focus |
|---|---|---|
| Stable ID (`Q3`, `D2`, `ADR-4`) | Its definition line | ID, middle dot, short name, and the meaning when the table has a Meaning column |
| Glossary term | Its row or item in the glossary | Term, middle dot, one-sentence definition |
| Abbreviation | No link; `<abbr title>` with the expansion | The expansion |
| Another section or tab of the same document | In-page anchor | Title of the target |
| Evidence in code | Permalink to the line at a fixed commit | Repository, commit, lines |
| External source | Its URL, opened in a new tab | Title and access date in the reference list |

- Define every ID once, on its own line: `Q3. Short name. Text.` or a table row whose first cell is the ID. The link goes to that line, never to a cell that only mentions the ID.
- Put the short name at the first mention, so the hover has something to show.
- Link text is the title of the destination ("the retry policy"), never "here", "this" or "see section 9".
- Keep the link text short enough to read as a phrase; the hover carries the detail.

## What never becomes a link

- Text inside code, preformatted blocks, headings, existing links, abbreviations, scripts, styles, `nav`, `select`, tags (`.tag`), heading permalinks, copy buttons, popovers, figure bars and anything marked `data-no-link`. The build step and the reader script skip the same set.
- Text inside diagrams (`.diagram`). A diagram label links through the figure's own controls, not through prose rules.
- The ID or term on its own definition line.
- A word that only looks like an ID: `A4 paper`, `C4 context`, `Q1 2026`. The tool skips an ID followed by a digit or by `context`, `container`, `model`, `deployment` or `style`. Rename the ID or reword the sentence if a real collision remains.
- Lower-case use of a glossary term. Matching is case sensitive on purpose.

## First occurrence

- Link a term or ID once per paragraph, list item or table cell. Repeats in the same block stay plain text.
- A link already in the block counts as that first mention, wherever it sits: one you wrote by hand, one from an earlier run, and a link to the term's plural or to one of its aliases. A second run therefore adds nothing.
- Link an abbreviation once per document, at its first use: `<abbr title="Time to live">TTL</abbr>`.
- A new paragraph starts again, so a reader who lands in the middle still gets a link.

## Anchor convention

One rule for every in-page link, in every type and template.

| Target | Anchor | Written by |
|---|---|---|
| A defined ID (`R12`, `CFG2`, `ADR-4`, a reference row) | `#def-<ID>` | the `defid` span; the build adds it to table rows and list lines |
| A glossary term | `#term-<slug>` | the build, from the term (see Slug below) |
| A heading, figure or step | its own `id` | you |

A reference row has an ID in its first column, so every option, command, key and message has a `#def-` anchor. Other tabs link to that anchor. Nobody invents a second scheme (`#ref-opt-keep`, `#opt-keep`) for the same thing.

## In-page anchors and external links

- Every `href="#x"` needs an `id="x"` or `name="x"` in the same page. A broken anchor is a defect, not a warning.
- Use plain `#token` anchors; the host page only forwards simple hashes.
- Keep headings, figures and definitions addressable: give each an `id`, and offer a copy-link control on headings.
- External links open with `target="_blank" rel="noopener"`. The tool adds both when missing and extends an existing `rel`.
- When the reader asks for links only inside the document, run with `--internal-only`. Every external or relative link is then listed and the run fails. Move the fact into the page, or cite the source as plain text with its access date.
- Links may cross tabs. A tab is a section of one document, so a link from the Tutorial tab to a Reference entry is an in-page anchor. Make the target tab visible on arrival (the reader script does this for `#id` hashes).

## Cross-tab links

- Link from a tutorial step to the reference entry for the exact option (`#def-CFG2`), not to the reference tab as a whole. Writing the plain ID in the step is enough; the build links it.
- Link from a how-to step to the explanation only when the step has a non-obvious reason; one link, at the step.
- Link from a reference entry to the how-to that uses it.
- Link from an explanation claim to the reference row the argument needs, and from a reference row with a surprising default to the claim that explains it.
- Do not repeat explanation inside the link text. The link says where, the target says why.

## Links to code

- Cite code as `path:lines` at a commit and link it to the permalink: `https://host/org/repo/blob/<full-sha>/path#L10-L20`. Never link a branch name; it moves.
- For Markdown files on GitHub add `?plain=1`, so the line anchor works.
- Show the repository and short commit in the hover.
- Read the cited lines at that commit before you write the claim. A script that compares the cited lines with the checkout catches drift (see `components.md`, Scripts, for `permalinks.py`).

## Persistent identifiers and access dates

- Prefer a DOI, an RFC number, a standard number or an archive URL over a bare page URL.
- Write the access date next to every web source: "accessed 2026-11-01". Without a date the reader cannot judge staleness.
- A source you could not reach follows the claim table in `components.md` (Evidence and citations), never a silent omission.
- Never link a private conversation, ticket or inbox from a shareable page. Write the fact and its date: "Team decision, YYYY-MM-DD".

## Link decay

- Every external link rots. Archive the sources a decision depends on and cite the archived copy next to the live one.
- Re-check external links when you publish a revision and when the document's stamp ("as of") is older than the reader's tolerance.
- Prefer a permalink to a moving page whenever the site offers one.
- Keep a single list of external sources (reference list) so decay is fixed in one place.

## Run the auto-linker

```
python -I scripts/autolink.py page.html -o page.linked.html [--prefixes CMD OPT ADR-] [--internal-only] [--check]
```

On a page you build with `build_page.py --autolink`, the build runs this for you (see `reader-page.md`). Run it by hand for `--check`, or for a page that has no reader.

Inputs, all read from the page:

| Source | Marked as |
|---|---|
| Defined IDs | Elements with class `defid`; list lines `ID. text`; a table row whose first cell is exactly the ID and whose second cell is the text |
| Glossary terms, default shape | A definition list `<dl class="glossary">` whose terms are `<dt class="defterm">` followed by the `<dd>` definition. The `id` is optional; the tool writes `term-<slug>` |
| Glossary terms, table shape | Table with attribute `data-glossary`: first column term, second column definition. An optional column headed Aliases (any case) holds comma separated synonyms. Other columns are ignored by the linker |
| Aliases | Optional `data-aliases="log file, journal"` on a `dt.defterm`, or a column headed Aliases in a `data-glossary` table (comma separated). Each alias links to the same term. The reader script reads the same column |
| Abbreviations | Table with attribute `data-abbr`; first column abbreviation, second expansion |

Use the definition list unless the glossary needs extra columns for readers (related entries, a source). Use one shape per artifact.

Rules the tool applies:

- ID grammar: one of the prefixes, digits, an optional lower-case letter (`Q13b` is one ID). The prefixes come from `--prefixes` when given, otherwise from `data-id-prefixes` on `<main>`. Only when the page has neither does the tool fall back to `G A Q D L P`.
- Prefixes may have several letters and may end with one dash: `--prefixes ADR- CMD OPT ERR-` matches `ADR-3`, `CMD2`, `OPT7`, `ERR-12`. Start with a letter; use letters and digits only (a comma also separates prefixes). The longest prefix wins, so `A` and `ADR-` can coexist. A bad prefix stops the run with an error.
- Anchor slug: `term-` plus the term in lower case with every run of characters outside `a-z0-9` replaced by one dash, dashes trimmed, `section` when nothing is left. This is the reader script's own function, so accented letters are dropped (`Cafe au lait` gives `term-cafe-au-lait`; an accented letter is dropped, not transliterated). Two terms with the same slug raise a warning; give one an explicit `id`.
- Popover text: `ID · short name`; when the table has a column headed Meaning, Description or Definition (any case) the tool appends it: `ID · short name · meaning`, cut to about 160 characters. A glossary term shows `term · definition`. The reader splits the text at the first middle dot, so the ID or term is always the bold heading.
- A definition-list term without an `id` gets the slug id; one with an `id` keeps it.
- Output: `<a class="ref" href="#def-ID" data-tip="ID · short name · meaning">`, `<a class="term" href="#term-slug" data-tip="term · definition">` and `<abbr title>`.
- Longest term first; a plural `s` or `es` after a term still links.
- Priority when one ID is defined twice: explicit `defid`, then a list line, then a table row. The first in document order wins inside a level. The others are listed as duplicates.
- Running the tool twice gives the same file (a test covers templates, plurals, aliases and repeated IDs).
- `--check` reports and writes nothing.

## Read the report

```
IDs defined: 12; referenced: 9; glossary terms: 7; abbreviations: 5
undefined IDs: []
broken anchors: []
```

| Line | Meaning | Fix |
|---|---|---|
| `undefined IDs` | Used in text, defined nowhere; shown as `span.ref.missing` | Add the definition line, or fix the typo |
| `broken anchors` | An `href="#x"` with no `id="x"` | Add the id or correct the link |
| `links that leave the page` (with `--internal-only`) | External or relative link | Remove it or write the source as text |
| `warning, IDs defined more than once` | Same ID has several definitions | Keep one; turn the others into mentions |
| `warning: terms ... share the anchor` | Two glossary terms give the same slug | Give one term an explicit `id` |

The run exits with 1 when `undefined IDs`, `broken anchors` or `links that leave the page` is not empty. Treat `[]` on all of them as a publishing gate. Add the style sheet rules for `a.ref`, `a.term`, `.ref.missing`, `.defid:target` and `.defterm:target` from the page template, and test the hover on the published page.
