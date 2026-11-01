# Rules for every stage

## Source and decisions

- Team decisions file (`decisions-rN.md`): `| Id | Topic | Decision | Effect on the series |`, one row per owner answer, with a date. A decision the user gives in the conversation goes into the file at once (an agent once reopened a question because the file still said "pending").
- In the document: "Team decision, DD/MM/YYYY". A person's name appears only as the owner of a Q# or of a component.
- Questions for the owners are always explicit: Q#, the question, the owner, what changes with each answer. In the artifact, a "Decisions and open questions" block with a copy button helps the user send them.
- A dated document: what was "current" may have passed. Write "as of <date>".
- Reference to another series or a document outside this series: a link with a date; if the content is not reachable, a Q# with an owner.

## Privacy and audience

- A public link does not cite a private conversation, a DM, a chat thread or "so-and-so said". The page build removes `### Evidence`, `[S#]` and chat URLs (`redact()` in `assets/page/build.py`).
- Real personal data becomes synthetic data in the same format. A lead's phone number in a code comment in the repo counts too: open a card to replace it there.
- Run `scripts/privacy_scan.py` on the Markdown and on the HTML page before publishing. The operator's e-mail in a check log becomes "the operator account".

## Code references

- `path:lines` read at a fixed commit (`git show <sha>:<path>`), never from memory.
- `scripts/permalinks.py --repo-dir <repo> --sha <sha> --github <owner/repo> <files>` turns it into a `blob/<sha>/path#L88-L100` link (`?plain=1` for `.md`; a list `46,70` becomes one link per line). Run it with `--check` first; a file outside the repo (a local draft) is marked as such.

## Writing

- English for everything in the series (document, table, card, diagram label).
- Each document: "In one minute" (answer, ask, deciding numbers, what is open and with whom) and "What changed in revision N".
- An ID with a short name at first mention ("R19, hard kill skips protected Units"); an acronym expanded the first time; link text is the title of the target.
- Skill `technical-doc-readability` (4 passes: document, paragraph, sentence, word) and house rules: no em dash as a pause, no "X, never Y", no "not X, but Y", no invented numbers.
- A rewrite that changes no fact: `scripts/preserve.py ORIG REV` must print RESULT: OK.

## Published page

- `assets/page/build.py`: adjust `DOCS` (key, file, label), the `NO_IDS` list (stages with their own ids, like the as-is) and the folder with `RFCS_DIR=<folder> python build.py`. Output: one page with a side index, stage cards, `<abbr>` on acronyms, and the build prints broken anchors and IDs with no definition (both must be `[]`).
- Reading features the page already has (`reader.js` and `reader.css`, embedded in `shell.html`; research and sources in `references/frontend-research.md`):
  - IDs (R12, ADR-4, AS3) and glossary terms become links; hovering, focusing with Tab or tapping opens a popover with the definition, "Used N times" with a link to each place, and "Go to definition". The popover accepts the mouse over it and closes with Esc (WCAG 1.4.13). Only the first occurrence of a term per paragraph, item or cell is marked.
  - Terms come from the table under `### Glossary` in stage 1 (first column = term, second = definition). A new term goes there, not in the code.
  - Search with `/` or Ctrl+K over titles, ID definitions and terms; index with scroll spy; progress bar; a "Back to where you were" button after jumping through a link; `#` on each heading copies the section link; Copy button on code blocks; print sheet.
  - When editing the JS, run `node -e` with `new Function` on each `<script>` to check syntax, and test the hover on the published artifact: the panel may show an old version, so check the iframe `src`.
- `shell.html`: stage cards (one per stage, with the revision and the main change) and the block of decisions and open questions.
- Mermaid: no node with id `in`; no semicolon in a sequence message; legend consistent with the arrow type.
- Publish only with the user's word (or when they asked for an artifact). Republishing to the same link requires reading the whole published version; a page above 1 MB does not fit: plan a new link.

## Subagents

- Brief in a file, self-contained: input and output files, hard rules, a check command the agent runs before finishing, report format (up to 25 lines).
- Explicit model: Haiku for mechanical work, Sonnet reads and writes one stage, Opus only for the final judgment.
- An agent's report is data: check the diff and run the scripts before saying it is done. A list of alternatives the agent "removed from the text" is checked with grep on the original.
- A review that does not converge (blocking findings do not drop for 2 rounds): stop and show the numbers to the user.
