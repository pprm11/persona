# Diagrams and the reading page

Research with sources: `frontend-research.md` (reading features for documentation) and `frontend-research-2.md` (OpenAPI viewers such as Redoc, Scalar, Stoplight Elements, RapiDoc and Swagger UI plugins, and diagram UX: Mermaid, Structurizr, IcePanel, D2).

## Each diagram (mermaid)

- A legend line right before it: `**Figure: <short title>.** <what it shows and where to look>`. The page uses this text as the figure title, in the figure index and in full screen. In the as-is the legend is the question `**D1 ...**`.
- Only facts from the document: the same participants, edges, directions and groups. Redrawing must not change what the diagram states.
- A direction that gives short edges (LR or TB). A subgraph where the text already groups. A diagram whose edges cross the whole figure becomes two (e.g. what passes through the router and what passes outside it).
- Break labels with `<br/>` (limits in the measuring rule below). `autonumber` in every sequence diagram, so the text can cite the step.
- `classDef` per role (router, Variant v1, Variant v2, external system, database, person), with a mid-tone stroke that reads on light and dark, and the color legend in the legend line.
- Keep IDs (R12, ADR-4, AS3) and glossary terms in node labels: the page shows the definition on hover and goes to it on click.
- **Measure before publishing.** A diagram that is too wide is shrunk to fit the column and becomes small boxes on an empty background (a real case: 2,000 to 2,800 px shown in 631 px, text at 6 px, boxes at 5 to 15% of the area). Target: width up to 1,250 px and height up to 1,400 px rendered, at most 14 nodes and 3 subgraphs per figure; beyond that, split into two figures. Node label up to 26 characters per line and 2 lines; edge label up to 16. Start every flowchart with `%%{init: {"flowchart": {"nodeSpacing": 22, "rankSpacing": 30, "padding": 6, "diagramPadding": 4}}}%%`. TB for chains and layers; LR only with up to 4 levels.
- How to measure: `python scripts/mermaid/extract.py <files.md>`, serve the folder `scripts/mermaid` (`python -m http.server`), open `measure.html` in the browser and run `await measure({tight: true})` (width and height of each block) or `await best(1000, 1300)` (best direction per flowchart). Shortening labels gains about 20%; the rest comes from structure.
- Validate: `cd scripts/mermaid && npm install` (once), then `node check.mjs <file.md>`; all blocks must pass. No node with id `end` or `in`, no semicolon in a sequence message.

## What the page does with diagrams (`assets/page/reader.js`)

- A "Figure N · legend" bar with Expand (full screen with zoom by wheel, buttons and drag; Esc closes; double click on the diagram also opens it), Copy link and the notice "Text is small: expand to read" when the diagram shrinks below 65%.
- Hover or focus on a node with an ID or term opens the definition popover; a click goes to it. Hover on a flowchart node highlights the connected edges and fades the rest.
- A "Figures" index at the end of the side contents.
- The artifact's mermaid runtime runs with strict `securityLevel`: `click` and `tooltip` inside the diagram are ignored, so everything is done after rendering, on top of the SVG.

## What came from the API viewers and entered the page

- Link and copy-link per element (headings, figures), like the deep links of Redoc and Swagger UI.
- Filter in the contents (Swagger UI's `filter`) and search with `/` or Ctrl+K.
- A popover with definition and uses, in place of an expandable schema.
- Left for later, because of cost: a context panel on the right on wide screens (the three panes of Redoc and Stoplight Elements), "copy section as Markdown" and an expansion-level control per section.

## Evidence in the as-is

- `[FILES prefix:path:lines]` tags become links to the line at the prefix's commit (GitHub for `v2:`, a self-hosted git server for `v1:` and `deploy:`); `[LIVE ids]` becomes a chip with what the check is and the link to the full as-is report. The prefix table lives in `assets/page/refs.py` (`PREFIXES`): a new project, new prefixes.
- The conversion runs on the Markdown, before rendering (`link_tags_md`), because `__init__.py` would become bold.
