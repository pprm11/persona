# Rules for every stage

## Source and decisions

- Team decisions file (`decisions-rN.md`): `| Id | Topic | Decision | Effect on the series |`, one row per owner answer, with a date. A decision the user gives in the conversation goes into the file at once (an agent once reopened a question because the file still said "pending").
- In the document: "Team decision, DD/MM/YYYY". A person's name appears only as the owner of a Q# or of a component.
- Questions for the owners are always explicit: Q#, the question, the owner, what changes with each answer. In the artifact, a "Decisions and open questions" block with a copy button helps the user send them.
- A dated document: what was "current" may have passed. Write "as of <date>".
- Reference to another series or a document outside this series: a link with a date; if the content is not reachable, a Q# with an owner.

## Privacy and audience

- A public link does not cite a private conversation, a DM, a chat thread or "so-and-so said". The page build removes `### Evidence`, `[S#]` and chat URLs (the `artifact-routing` page build does this).
- Real personal data becomes synthetic data in the same format. A customer's phone number in a code comment in the repo counts too: open a card to replace it there.
- Run `privacy_scan.py` (`artifact-routing`) on the Markdown and on the HTML page before publishing. The operator's e-mail in a check log becomes "the operator account".

## Code references

- `path:lines` read at a fixed commit (`git show <sha>:<path>`), never from memory.
- `permalinks.py` (`artifact-routing`) `--repo-dir <repo> --sha <sha> --github <owner/repo> <files>` turns it into a `blob/<sha>/path#L88-L100` link (`?plain=1` for `.md`; a list `46,70` becomes one link per line). Run it with `--check` first; a file outside the repo (a local draft) is marked as such.

## Writing, page and diagrams

How to write, build and check each document belongs to the `artifact-routing` skill (not bundled here): type per part, readability, the `preserve.py` check, the reader page, linking, diagrams and publishing. The series adds only these:

- English for everything in the series (document, table, card, diagram label).
- Each document: "In one minute" (answer, ask, deciding numbers, what is open and with whom) and "What changed in revision N".
- An ID with a short name at first mention ("R7, retries are idempotent"); an acronym expanded the first time.
- Terms for the page glossary come from the table under `### Glossary` in stage 1 (first column = term, second = definition). A new term goes there.
- Stage cards (one per stage, with the revision and the main change) and a block of decisions and open questions go on the page.
- Publish only with the user's word (or when they asked for an artifact).

## Subagents

- Brief in a file, self-contained: input and output files, hard rules, a check command the agent runs before finishing, report format (up to 25 lines).
- Explicit model: Haiku for mechanical work, Sonnet reads and writes one stage, Opus only for the final judgment.
- An agent's report is data: check the diff and run the scripts before saying it is done. A list of alternatives the agent "removed from the text" is checked with grep on the original.
- A review that does not converge (blocking findings do not drop for 2 rounds): stop and show the numbers to the user.
