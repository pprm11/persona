# Components

Building blocks any Diataxis type may use. A type reference says which components its tabs need. Take a component only when its "Use when" holds. Each component has one shape, so readers learn it once.

| Component | Tutorial | How-to | Reference | Explanation |
|---|---|---|---|---|
| In one minute | goal and result | outcome and time | scope and version | answer and ask |
| As of date, What changed | when the steps were last run | when last run | always | when it decides something |
| Conventions block | rarely | rarely | always | when IDs or keywords exist |
| Stable IDs | no | for steps others cite | always | when claims are traced |
| Open questions, decisions | no | no | rarely | always |
| Evidence and citations | for expected output | for commands | always | for every number |
| Success check, failure table | every step | every procedure | no | no |

## In one minute

Use when: first block of every page. Shape: 4 to 6 plain sentences, no bullets. On a multi-type page the one block at the top covers the whole page, and each tab opens with a lead paragraph of one to three sentences that answers the same questions for that tab.
- Explanation: the answer, the ask, the deciding numbers, what is open and with whom.
- Tutorial and how-to: what the reader will have at the end, what they need before starting, how long it takes if you measured it.
- Reference: what the page covers, which version it describes, where to look first.

Example: "We will route messages through one gateway. We ask the platform owner to approve by the end of the month. The deciding number is 40 ms added latency (measured, section 4). Q3 is open with the security owner."

## As of date and What changed in revision N

- Put one line under the title: `As of 2026-11-01 · Revision 4 · Owner: <role>`. Use absolute ISO dates (YYYY-MM-DD) in one format across the page.
- Anything time bound carries "as of <date>" at the claim, not only in the header.
- `What changed in revision N` follows In one minute, newest first, one bullet per change. Name the IDs a bullet touches. Skip it on revision 1.

## Conventions block

Use when the page has IDs, requirement keywords or evidence tags. Shape: a short table or list under the page head.
- ID prefixes and what each means (`G` goal, `R` requirement, `Q` open question, `L` accepted limit).
- Keyword meaning: "MUST, SHOULD, MAY are used as in BCP 14 (RFC 2119 and RFC 8174) and only in capitals."
- Source tag formats (see Evidence and citations) and the meaning of each state word.
- How a decision is attributed (see Owner decisions).

## Stable IDs

- Give every item that other text cites an ID and a short name at its definition: `R19. Hard kill skips protected units.` Define it once, in a list line `- R19. Name. Sentence.` or a table row `| R19 | Name | ... |`.
- At first mention in a paragraph write the ID with its name: "the retry rule (R19)". Never start a sentence with an ID, never write a sentence that is only a chain of IDs.
- Never renumber. A new item takes the next number. A removed item stays as `Removed in revision 5: duplicate of R4.`
- Link text and popover text come from the short name, so write it as a title.
- IDs from another source that collide with yours (a prior report using `A1`) stay plain text on that page, or get a prefix.

## Open questions block

Use when something blocks or changes the content. Shape: one list, one item per question, and a copy button that copies the list with the IDs.

| Field | Content |
|---|---|
| Q | `Q7` and the question in one sentence |
| Owner | a role or a named owner of the question |
| Effect | what changes with each answer: "If A, section 4 drops the cache. If B, it stays." |

Order by how much the answer unlocks. Pending items also appear in In one minute. Apply an answer to the content and to the decisions block at once, then close the Q with "Removed in revision N". A stale list makes agents reopen closed questions.

## Decisions block

Use when decisions exist. Shape: ordered list "Decided on <date>" next to "Still open", or one table.

| Id | Topic | Decision | Status | Effect |
|---|---|---|---|---|
| D4 | Hosting | Managed database | Accepted | Removes the self-run cluster |

Status chips use fixed words with an icon or label, never color alone: Proposed, Accepted, Amended, Superseded, Removed.

## Decision record

Use for a choice someone will question years later. Shape, in this order:
1. `ADR-12. Title` and the line `Status · Date · Decided by · Supersedes or superseded by`.
2. Context: the forces, as facts with numbers and sources.
3. Decision: starts "We will" and covers one choice.
4. Options compared: a table with the strongest alternative and why it loses. Include "do nothing".
5. Consequences: positive and negative, each with who is affected.
6. Revisit when: a condition you can observe.

Never renumber or delete. A changed decision is a new record, and the old one reads "Superseded by ADR-15". Write the record while the choice is open, so it keeps the deliberation.

## Owner decisions

- An answer from an owner is source. Do not reword it. Record it in a decisions file with a date and apply it at once.
- Attribute with "Team decision, YYYY-MM-DD". A person's name appears only as owner of a question or component.
- A conflict between the draft and a decision becomes a question for its owner. It is never a silent correction.
- A shareable page never cites private chat, direct messages or "X said". Strip chat links and `[S#]` source markers before publishing.

## Evidence and citations

| Kind | Shape |
|---|---|
| Code | `path:lines` read at a fixed commit, rendered as a permalink `blob/<sha>/path#L88-L100`. Never a branch link. Markdown files take `?plain=1`. |
| Command | The exact command, then the output or the part that matters |
| Web page | Title, publisher, URL, access date. Save a snapshot for a page a decision depends on |
| Standard | Persistent identifier: DOI as `https://doi.org/...`, RFC number, standard number with year |
| Not verified | `[NOT VERIFIED: <command that would verify it>]` |
| Assumption | `[ASSUMED: <what changes if it is wrong>]` |
| Untested step | `[UNTESTED]` before the step, and say what would test it |

Every number and every claim of fact has one of these within a sentence. State words (LIVE, STALE, ABSENT, NOT VERIFIED, ASSUMED) each get one meaning, defined once in the Conventions block. Use short tags such as `[RFC9110]` linked to a References list, and one citation system per page.

### A claim with no source

This table is the one rule. Every other file points here.

| The claim is... | Do this |
|---|---|
| Checkable, and you can name the command or file that would check it | Keep it and tag `[NOT VERIFIED: <command>]` |
| A premise you choose to proceed on, with no way to check it now | Keep it and tag `[ASSUMED: <what changes if it is wrong>]` |
| Waiting for an owner's answer, or a source you could not reach | Make it an open question with an owner and the effect of each answer, and write "pending" at the claim |
| None of these, or nobody can say where it came from | Delete it |

When you edit someone else's text, do not guess: apply the table to the claim and ask the author in your reply.

## Privacy

- Personal data becomes synthetic data in the same format (a phone number keeps its length and country prefix). Check comments and fixtures in the source repository too.
- Commands never print secrets. Read them from the environment: `echo "${#API_KEY} characters set"`, not `echo $API_KEY`. Use a placeholder in capitals and explain it under the command.
- Logs and output samples are redacted before they enter the page.
- Run `privacy_scan.py` on the Markdown and on the built HTML before publishing.

## Pending notice

Use when a section cannot be finished. Shape: one line at the top of the section, `Pending: <what is missing>. Owner: <role>. Needed for: <section or decision>.` Mirror it in the open questions block. Remove the notice when the content lands.

## Success check

Use when: every tutorial step and every how-to procedure. Shape: one line after the action, `You should see: <exact output or visible state>.` A step the reader cannot verify gets a way to verify it. The last step ends with the check that the goal is met.

## Failure table

Use under a procedure. Key the rows by the exact message, because readers paste it into search. One shape everywhere: the columns You see, Cause, Do this. Add a first column Id (`F1`) when other text cites a row; the Id then follows the anchor convention in `linking.md`.

| Id | You see | Cause | Do this |
|---|---|---|---|
| F1 | `connection refused` | The service is still starting | Wait 30 s and repeat step 4 |

Put a one-line recovery next to the step that can fail, and the table at the end for the rest.

## Overview cards

Use when a page has three or more parts the reader may enter at different points (a multi-tab artifact, a series). Shape: one card per part with a label, a title, one sentence on what the reader gets, and a footer with the as-of date or revision. Each card links to its tab or section with an anchor. Do not use cards on a single-purpose page.

## Keeping a document true

- Stamp the page with the date or version it was last checked against the system.
- Test the examples, commands and links where you can. A tutorial or how-to that was never run says so.
- Change the document in the same change as the code it describes. Delete pages nobody maintains.

## Scripts

Run from the skill folder. Python 3 with the standard library only. Mermaid checks need Node.

| Script | Does | Command |
|---|---|---|
| `scripts/preserve.py` | Reads Markdown or HTML and compares the tokens of two versions, not the prose: headings, code, link URLs, IDs, tags and numbers. Prints LOST and ADDED. Exit 1 if anything was lost in headings, code, tags, URLs or IDs, or a number was added. `--prefixes` sets the ID prefixes (default `G A Q D L P`), `--tags` the evidence tags to track (default none, for example `UNTESTED`), `--legacy` the older behavior. Use after any rewrite that must not change facts | `python -I scripts/preserve.py ORIGINAL REVISED [--prefixes CMD OPT] [--tags UNTESTED]` |
| `scripts/privacy_scan.py` | Reads Markdown or HTML and finds e-mail addresses, phone numbers, payment card numbers (Luhn checked), keys and tokens, private keys and URLs with credentials. `--pack br` adds CPF, CNPJ and Brazilian phone formats. `--allow-prefix P` (repeatable) lets synthetic numbers that start with P pass. Exit 1 if anything is found | `python -I scripts/privacy_scan.py [--pack br] [--allow-prefix P] FILE ...` |
| `scripts/permalinks.py` | Turns `` `path:lines` `` in Markdown into GitHub permalinks at one commit. Reports paths missing from the tree, lines past the end and cited lines that differ from the checkout. `--check` only reports, `--show` prints the cited lines | `python -I scripts/permalinks.py --repo-dir <repo> --sha <commit> --github <owner/repo> [--check] [--show] FILE.md ...` |
| `scripts/svg_gate.py` | Reads an HTML page and estimates the width of every `<text>` in hand-written `<svg>` figures. Lists each label that runs past its box or the viewBox. Exit 1 if any | `python -I scripts/svg_gate.py PAGE.html` |
| `scripts/mermaid/check.mjs` | Parses every mermaid block of one or more files, fenced Markdown or `<pre class="mermaid">` in HTML. Prints `N/M parse OK` and the failing block numbers; a file with zero blocks gives a warning | `cd scripts/mermaid && npm install` once, then `node check.mjs FILE ...` |
| `scripts/mermaid/extract.py` | Writes `diagrams.json` with every mermaid block of the given files (Markdown or HTML), for measuring. A file with zero blocks gives a warning | `python -I scripts/mermaid/extract.py FILE ...` |
| `scripts/mermaid/measure.html`, `search.js` | In a browser, `await measure({tight: true})` returns id, width and height per block. `await best(1000, 1300)` picks the best direction per flowchart for a column width and height | `python -m http.server` in `scripts/mermaid`, open `measure.html`, run in the console |

The permalink script matches GitHub URLs only. The privacy scan patterns are generic and cannot know every identifier, so add a pack or patterns for the data your pages carry (street addresses and national IDs are not covered by default). `extract.py` creates `diagrams.json` on each run; it is not shipped. `check.mjs` and `measure.html` both pin mermaid 11.4.1; when the host renders another version, change both pins together.
