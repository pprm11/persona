# Diagrams

A diagram earns its place when it shows a relationship that prose or a table shows worse: flow, structure, sequence, state. If a table says it, use the table. One diagram answers one question.

## Which diagram for which type

| Type | Use | Avoid |
|---|---|---|
| Tutorial | A small flowchart or screenshot of the state the learner should see after a step | A full architecture before the learner has built anything |
| How-to | A decision flowchart for branches ("which path applies"), a sequence of steps across tools | Diagrams that explain why instead of what to do |
| Reference | Structure diagrams (components, data model, state machine) with every element labeled and tied to a dated source | Decorative layouts, any edge not found in the source of truth |
| Explanation | Sequence diagrams for causality, flowcharts for tradeoffs, one picture per claim | A diagram that lists settings while claiming to explain a cause |

## Rules for each diagram

- **Caption line first.** A paragraph right before the diagram: `**Figure: <short title>.** <what it shows and where to look> (Legend: <color or shape> is <role>, ...)`. The page reads the bold part as the figure title for the figure index and the full-screen view. A how-to may phrase it as the question the figure answers.
- **Only facts from the text.** Same participants, edges, directions and groups. Redrawing must not add or drop a claim. Every node can be found in the page's text or source.
- **Legend, not color alone.** Each role differs by shape or border style as well as color, so it survives grayscale and color blindness. The legend names every class used.
- **`classDef` per role** (service, database, person, external system, new, old). Use mid-tone fills and a strong stroke, set the text color explicitly, and check that text on its block reads at 4.5:1 in both light and dark. Light text on light blocks is the usual failure.
- **Direction.** TB for chains and layers, LR only with up to 4 levels. Choose the one that gives the shortest edges. Measure both.
- **Splitting.** A diagram whose edges cross the whole figure becomes two, for example what passes through a component and what passes around it. A subgraph only where the text already groups.
- **Size limits.** Up to 14 nodes and 3 subgraphs per figure. Rendered width up to 1,250 px and height up to 1,400 px. Larger shrinks to unreadable text on an empty background. Beyond the limits, split.
- **Labels.** Up to 26 characters per line and 2 lines per node, up to 16 characters per edge. Break with `<br/>`. Shortening labels gains about 20 percent of width, the rest comes from structure.
- **Tight layout.** Start flowcharts with `%%{init: {"flowchart": {"nodeSpacing": 22, "rankSpacing": 30, "padding": 6, "diagramPadding": 4}}}%%`.
- **Sequence diagrams** start with `autonumber`, so the text can cite "step 4". Add a numbered step list under complex ones.
- **IDs and terms in labels.** Keep stable IDs and glossary terms in node labels (`R12`, `Router`), so the page can attach the definition on hover.

## Hand-drawn SVG figures

Use mermaid when it can draw the figure. When a figure is hand-written `<svg>` with `<text>`, labels do not wrap and nothing warns when one runs past its box. A published tutorial shipped three such figures with labels wider than their boxes, because nobody looked at the render.

- Budget each label before drawing. A monospace glyph is about 0.62 em, so at 11 px a label of N characters needs about 6.8 × N px plus 8 px of padding. A 560 px box holds about 80 characters at 11 px.
- A longer label becomes two lines (raise the box 14 px per line) or a shorter label. Never go below 11 px.
- A label beside an arrow or outside every box counts against the viewBox width.
- Run `python -I scripts/svg_gate.py PAGE.html` before publishing. It estimates each label's width and lists every overflow of its box or the viewBox. Treat the list as blocking.
- Look at the render once with real glyphs. Serve the file with `<meta charset="utf-8">`, because without it the preview shows broken accents that the published page does not have.

## Accessibility

- Add `accTitle:` and `accDescr:` (or `accDescr { ... }`) as the first lines of every diagram. They produce the SVG title and description for screen readers.
- For a complex figure add a text version in a collapsed `<details>` under the caption: nodes and edges as a short list or small table. Keep it in the same source block, so it goes stale together with the diagram.
- Do not rely on hover for meaning. A node's meaning lives in its label and the text version, and the popover only repeats it.

## Measure and validate

1. `python -I scripts/mermaid/extract.py <files>` (Markdown or the built HTML page) writes `diagrams.json` to the current working directory. Copy `measure.html` and `search.js` there before serving it; do not write into the installed skill directory.
2. Serve that working directory (`python -m http.server`), open `measure.html`, run `await measure({tight: true})` for width and height of each block. Run `await best(1000, 1300)` for the best direction per flowchart.
3. Parse check: Copy `package.json` and `check.mjs` to a working directory, install its dependencies there, then run `node check.mjs <files>`. All blocks must pass, and a file with zero blocks is a warning to read.
4. Look at each figure in the final page at about 1,000 px wide and at 400 px, in light and dark.

## Mermaid gotchas

- No node with id `end` or `in`. Use `endNode` or `input`.
- No semicolon inside a sequence message, it ends the statement.
- Legend and arrow type agree: dashed arrows in the legend are dashed in the source.
- Background `box` colors in sequence diagrams need `rgb()` or `rgba()`, hex reads as a comment.
- The host renders with a strict security level. `click`, `href`, `callback` and tooltip directives inside the diagram are ignored. Do not rely on them. Put links in the text, and let the page script work on the rendered SVG.
- Render with the host's mermaid version. Internal class and id names (`g.node`, `flowchart-<id>-<n>`, `LS-`/`LE-` edge classes) change between versions, so scripts must tolerate a miss.
- Mermaid reads theme colors as hex, not CSS variables. Fixed `classDef` hexes are safer than variables, and they must read in both themes.
- Diagrams render natively from `<pre class="mermaid">`. In a Markdown source, a fenced block is copied into that element by hand when you build the page.

## What the page does with a figure

The reader script (see the reader-page reference) wraps each `.diagram`:

| Feature | Behavior |
|---|---|
| Figure bar | `Figure N · caption`, from the caption line |
| Expand | Full-screen view with wheel and button zoom, drag to pan, double-click to open, Esc to close, focus returns to the opener |
| Copy link | Copies a link to `#figure-N`. The number follows document order, so inserting a diagram renumbers later links |
| Node popover | A node whose label holds an ID or glossary term shows the same popover as the text, on hover, focus or tap. Click or Enter goes to the definition |
| Edge highlight | Hovering a flowchart node highlights its edges and dims the rest. The dimming respects reduced motion |
| Figure index | A collapsed "Figures" entry in the contents lists every figure with its caption |
| Small-text hint | When the rendered width falls under 65 percent of the drawn width, a notice reads "Text is small: expand to read" |

Design for it. A caption line that is missing breaks the bar and the index. A label that mixes two IDs gets one popover. A diagram wider than the limits triggers the hint, which is a sign to split, not to ignore.

## Dependencies

The optional Mermaid parser in `scripts/mermaid/check.mjs` requires Node.js and the `jsdom` and `mermaid` packages declared in the adjacent `package.json`. Install them in an isolated local copy when needed. `measure.html` loads Mermaid from a CDN and requires network access and a browser; verify access and third-party terms before use. The Python extraction and other page checks do not require these packages.
