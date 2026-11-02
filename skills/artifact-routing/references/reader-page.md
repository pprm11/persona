# Reader page: build, markup contract and checks

The page is one HTML file published as an Artifact. This file is the one place that says how to build it. Every other file points here.

You write a lean source: content and page CSS, with the reader markers empty. `scripts/build_page.py` inlines the reader (`assets/reader/reader.js` and `reader.css`) and runs the auto-linker. You publish the built file and keep the lean one as the source you edit. Keep the markup contract below, and every reading aid works without further code.

## Files

| File | Role |
|---|---|
| `assets/templates/shell.html` | Lean skeleton with `{{...}}` placeholders, tokens, base styles and empty reader markers. Start a new page here |
| `assets/templates/<type>.html`, `multi-type.html` | Lean worked examples. Content and page CSS only, reader markers empty |
| `assets/templates/driftwood-facts.md` | The one fact sheet behind the sample product used by every example |
| `assets/reader/reader.js`, `reader.css` | Sources of the reading aids. Edit them here only. Uses only shell tokens |
| `scripts/build_page.py` | Fills the reader markers from `assets/reader/`, optionally runs `autolink.py`, writes the publishable page |
| `scripts/autolink.py` | Links IDs, glossary terms and abbreviations, and checks IDs, anchors and outside links |

## Build and publish

1. Copy a template (the type's own, or `shell.html`). Keep both marker pairs empty: `/* reader.css */` then `/* /reader.css */`, and `// reader.js` then `// /reader.js`.
2. Fill the content (next sections). Delete every unused optional block and every comment. Search the file for `{{` and for `<!--` last.
3. Build, then check the built file:

```bash
python -I scripts/build_page.py page.html -o page.built.html --autolink
python -I scripts/autolink.py page.built.html --check --internal-only
```

4. Both tools read the ID grammar from `data-id-prefixes` on `<main>`. Pass `--prefixes` only to override it. Rebuilding a built page is safe, because anything between the markers is replaced.
5. Run `privacy_scan.py` on the built file, the type checklist and the gates in `quality-gates.md`.
6. Run the checks at the end of this file, then publish the built file. Never publish the lean source.

After a change to `reader.js` or `reader.css`, rebuild every page that uses them, `shell.html` included.

## Fill the shell

| Placeholder | Fill with |
|---|---|
| `TITLE` | Two to four words. Used in `<title>` and the `h1` |
| `LANG` | Language code of the page, on the outermost wrapper (the host owns `<html>`) |
| `EYEBROW` | Short context line above the title (project, kind, status) |
| `ONE_MINUTE` | Always fill it. Answer first: the point, the ask, the deciding numbers, what is open and with whom |
| `AS_OF`, `REVISION`, `META` | ISO date, revision number, optional extra facts starting with ` · ` |
| `ID_PREFIXES` | Comma list such as `R,Q,ADR-`. Empty when the page has no IDs |
| `CARD_*` | One `a.card` per part. Delete the block for a single-type page |
| `TABS_LABEL`, `TAB_ID`, `TAB_LABEL`, `TAB_ID_2`, `TAB_LABEL_2`, `PANEL_CONTENT*` | One `button[role=tab]` and one `div[role=tabpanel]` per Diataxis type. Repeat the pair, so the bar has as many buttons as there are panels. Keep the bar order Tutorial, How-to, Reference, Explanation. The default tab is the reader's main job: give it `aria-selected="true"` and leave its panel without `hidden`, wherever it sits in the bar. Delete the bar and the extra panels for one type |
| `TERM`, `TERM_DEFINITION` | Glossary items; repeat the `dt`/`dd` pair. Delete the section when there are no terms |
| `DECIDED_*`, `OPEN_*` | Items of the decisions block; repeat `li`. Delete the section when unused |
| `FOOTER_NOTE` | One line: scope, owner, how to report an error |

## Anchor convention

One rule for every link target. `linking.md` owns it; the markup is below.

| Target | Anchor |
|---|---|
| A defined ID (`R12`, `CFG2`, `ADR-4`) | `#def-<ID>` |
| A glossary term | `#term-<slug>` |
| A heading, figure or step | Its own `id` |

A reference row carries an ID in its first column (`CMD1`, `OPT3`), so it gets a `#def-` anchor and a popover. Other tabs link to the row, never to the tab as a whole.

## Markup contract

Everything is optional. A feature does nothing when its markup is missing.

| Feature | Markup the reader looks for |
|---|---|
| Root | `div.reader-root[lang]` wraps `div.page`. Overlays (popover, search, viewer, pills) are appended inside it so they inherit `lang` |
| Language | The reader UI follows the closest `lang` of the root: `pt` or `pt-BR` gives Portuguese, anything else gives English. `data-reader-strings` on `div.reader-root` takes a JSON object that overrides single strings, for example `{"copy":"Copy text"}`. Keys are in the `STRINGS` object at the top of `reader.js` |
| Page grid | `div.page` with `nav.index` and `main`. Add class `page--solo` when there is no `nav.index` |
| Main | `<main id="main" data-reader="all" data-id-prefixes="R,Q,ADR-">` |
| Skip link | `a.skip[href="#main"]` first in the root |
| Contents menu | `nav.index` with a `button#searchbtn`. Leave it without a `ul` and the reader builds the list from `h2[id]` and `h3[id]`, grouped by tab. Add `data-nomenu` to a heading to leave it out. A hand-written `ul` is kept as written |
| Heading ids | Every `h2` to `h4` gets a slug id when it has none. Write your own for stable links. Use only letters, digits, `-` and `_` |
| Tabs | `.tabs[role=tablist]` holding one `button[role=tab][id=tab-x][aria-controls=x][aria-selected]` per panel; `div#x[role=tabpanel][aria-labelledby=tab-x]`, `hidden` on all but the default one |
| Defined ID | `<span class="defid" id="def-R12">R12</span>` at the start of its definition line, followed by `. Short name. Sentence.` The popover shows the line. In a table, the ID is the first cell |
| Linked ID | `<a class="ref" href="#def-R12" data-tip="R12 · Short name. Sentence.">R12</a>`. The build writes it; write the plain ID in text |
| Glossary term (default) | `<dl class="glossary"><dt class="defterm">Variant</dt><dd>Definition</dd></dl>`. The build adds `id="term-variant"`. Optional `data-aliases="a, b"` on the `dt` |
| Glossary term (table) | `table[data-glossary]` also works: first cell term, second cell definition. Aliases come from an optional column headed Aliases (comma separated). See `ubiquitous-language.md` |
| Linked term | `<a class="term" href="#term-variant" data-tip="Variant · Definition">Variant</a>`. The build writes it |
| Abbreviation | `<abbr title="Architecture decision record">ADR</abbr>`, or a `table[data-abbr]`. The reader moves the title into the popover and makes it focusable |
| Code | `<pre><code>`. The reader adds a Copy button. Mermaid `pre` is skipped |
| Table | Plain `<table>`. The reader wraps it in `.tablewrap` and makes a scrolling wrapper reachable with the keyboard |
| Figure | `<p><strong>Figure: Short title.</strong> What to look at. Legend.</p>` then `<div class="diagram"><pre class="mermaid">...</pre></div>`. Optional `id` on the div and `data-caption`. Add `<details class="figtext"><summary>Text version</summary>...</details>` inside the div for a complex figure. The caption may start with `Figure:` or `Figura:` (case-insensitive) |
| Open questions | `ol#open-list > li` with `.q`, `.a`, `.tag`; `button.copy[data-target="open-list"]`. The copied text keeps each ID: `1. [Q4] Question. Owner and effect` |
| Evidence link | `a.src[data-tip][data-action="Open the file ↗"]` opens a new tab; never needed for in-page links |
| Footer | `footer.pagefoot` with a `#top` link |

Rules for `data-tip`: header, then ` · `, then body. The header is bold. Never put the tip in `aria-label`, because it replaces the visible link text for screen readers; the popover is announced on focus through `aria-describedby`.

### Automatic linking

The build step (`autolink.py`) is the main linker. The reader script repeats the same job at run time as a fallback, so a page that skipped the build still works. Both follow the rules in `linking.md`: first mention per paragraph, list item or cell; matching rules; what is skipped. An ID that matches the prefixes but has no definition gets class `ref missing` and a console warning. Links already written by hand or by the build count as the first mention. Mark text `data-no-link` to leave it alone; the build and the reader skip the same elements.

### ID grammar

`data-id-prefixes` on `<main>` is the one place the grammar lives. The reader, `build_page.py` and `autolink.py` all read it; `autolink.py` falls back to `G A Q D L P` only when neither `--prefixes` nor the attribute exists. Each prefix is followed by digits and an optional lowercase letter (`R12`, `Q13b`, `ADR-4`). An ID is not matched inside a longer word or after a hyphen.

### Switching features

`data-reader` takes `all`, a list of names, or `all -name` to remove some. Names: `progress menu spy filter drawer permalinks codecopy tables autolink abbr popover back search slash tabs figures copyopen`. Remove `slash` to turn the bare `/` shortcut off (Ctrl+K stays). Constants for timings and thresholds are at the top of `reader.js` in the object `T`.

## What the reader does

- Reading progress bar. Contents menu with scroll spy (`aria-current`, the menu scrolls to the active item; headings of hidden tabs never count). Filter box with count and Esc to clear. Search button.
- Phones (960 px and narrower): the menu becomes a drawer opened by a Contents button, with search and filter inside, Esc and a Close button. The page keeps bottom padding equal to the height of the floating buttons, so they never cover the last line.
- Heading permalinks (`#` button, copies the link; visible on touch). Copy on code. Copy fallback selects the text; there is no `window.prompt`.
- Popover on `a.term`, `a.ref`, `abbr` and diagram nodes: opens on hover, focus or tap, stays open while the pointer is over it (250 ms close delay), closes on Esc or an outside click, "Used N times" grouped by section with "N more", "Go to definition". On touch the first tap opens it and the second follows the link. Tab from an open trigger enters its links.
- Back pill after an in-page jump (not after menu or search), restores the tab and position, hides when you return.
- Search with `/` or Ctrl+K: every word must match; exact ID or term first, headings before definitions; matches are marked.
- Tabs: any link, search hit or initial hash into a hidden tab opens it; arrows, Home, End; the hash is the panel id. Jumps mark the target with `.is-target` because `replaceState` does not update `:target`.
- Figures: bar with number and caption from the legend line, Expand to a viewer (wheel, pinch, buttons, drag, double-click, `+ - 0`, Esc), Copy link, "Text is small" hint, figure index in the menu, node popovers, edge highlight on flowchart hover.
- Print: all tabs shown with their names, light colors, no controls, external URLs written out. Diagrams keep the theme they were rendered with.

## Artifact limits

- No `<!doctype>`, `<html>`, `<head>` or `<body>`; the host wraps the file. `<title>` and the viewport-fit meta come first, then `<style>`.
- Scripts load only from cdnjs, jsdelivr or unpkg; fonts only from Google Fonts. The templates load none besides fonts. Mermaid renders natively from `<pre class="mermaid">`.
- `window.prompt`, `alert` and `confirm` never show; `window.print` does nothing; only plain `#token` hashes reach `location.hash`. `localStorage` needs try/catch (the reader does not use it).
- Tokens on `:root`, dark under `@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {...} }` and again under `:root[data-theme="dark"]`. `body` has an explicit background.
- Side gutter `padding-left: max(16px, env(safe-area-inset-left, 0px))`, same on the right. Work at 400 px.
- Size 16 MB at most. A page over 1 MB needs a full read of the published version before republishing, and an in-place republish can be refused: plan a new link.

## Check before publishing

1. Syntax: `node --check assets/reader/reader.js`. For a built page, extract the last `<script>` body to a temp file and run `node --check` on it, or run `new Function(code)` on each inline script.
2. Open the page once in light, once in dark and once at 400 px. No horizontal page scroll; the Contents button opens the drawer and does not cover the last line.
3. Hover an ID and a term; move the pointer into the popover; press Esc. Focus one with Tab and press Tab again.
4. Click a link into another tab; the tab opens, the back pill shows, pressing it returns.
5. Press `/`, type an ID, press Enter; the target is marked.
6. Open a figure, expand it, zoom, close with Esc; hover a node.
7. Look for `{{`, for `<!--` and for `ref missing` in the DOM; read the console for the missing-ID warning.
8. After publishing, open the live page and test one hover. The panel can show an old version: check the iframe `src` for the new version.

Mermaid gotchas that break a figure silently (no node with id `in`, no semicolon in a sequence message, legend matching the arrow style) are in `diagrams.md`.

## Features and the types that gain most

| Feature | Tutorial | How-to | Reference | Explanation |
|---|---|---|---|---|
| Progress, steps with copyable code | high | high | low | low |
| Contents menu, scroll spy, filter | low | medium | high | high |
| Search, permalinks | low | medium | high | medium |
| Popovers for IDs and terms, used-in list | low | low | high | high |
| Back pill | low | low | medium | high |
| Tabs between types | high | high | high | high |
| Figures with expand and node popovers | medium | medium | high | high |
| Open questions with copy | none | none | low | high |
| Table scroll and sticky tab bar at 400 px | medium | medium | high | medium |
