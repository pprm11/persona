# Reference

[Diataxis: Reference](https://diataxis.fr/reference/) describes information-oriented material users consult for reliable descriptions. Applying it to any medium is this skill's adaptation. This file is the content contract for a Reference page or tab. Shared parts live in `components.md`, `writing.md`, `ubiquitous-language.md`, `linking.md`, `diagrams.md`, `reader-page.md` and `quality-gates.md`; this file points to them. A worked page is `assets/templates/reference.html`.

## 1. Purpose and acceptance

- **Reader's need:** look up one fact about a thing (a command, option, key, field, error, file, role, component) while doing other work, then leave. The reader already knows what the thing is for.
- **The one question:** "What exactly is X, and what are its values, limits and defaults?"
- **Acceptance check (observable):** a reader who holds a name or an exact message finds its entry in under three actions (contents, search or ID link) and states type, default, allowed values, version and source without reading any other entry. Test with five lookups from the answer key.
- **Neighbor types, and what to move out:**
  - Tutorial: any "first, do this". Move steps to the Tutorial or How-to tab and link from the entry.
  - How-to: any recovery procedure. The entry says what the error means; the fix steps live in a How-to.
  - Explanation: any "why it works this way", history of the design, or comparison with alternatives. Link to the claim in Explanation; keep one neutral sentence of scope.
  - Opinion and advice ("we recommend") do not belong. A default is a fact; a recommendation is an Explanation or How-to.

## 2. When several types share one artifact

- This tab owns facts: names, shapes, values, versions, sources. It never owns steps or reasons.
- Every entry may carry one link out: to the How-to that uses it, or to the Explanation of its reason. The other tabs link in by stable ID (`#def-CFG2`), never by tab name alone.
- Default tab: Reference when the reader arrives mid-task with a name in hand (an error message, a flag). Make it the second tab after Tutorial or How-to when the reader is new; the tab bar stays sticky so the switch costs one click.
- The page stamp (version, as-of date) is the Reference tab's job; other tabs repeat only the version.

## 3. Skeleton

Order for lookup, not for reading. The API reference and CLI reference skeletons in `skeletons.md` add the genre's section names.

| # | Section | Status | Content | Component |
|---|---|---|---|---|
| 1 | Title, eyebrow, as-of line | Required | Product, version described, date, revision, owner role | As of date |
| 2 | In one minute | Required | Scope, version, what is not covered, where to look first (4 to 6 sentences) | In one minute |
| 3 | What changed in revision N | Conditional (from revision 2) | One bullet per change, naming IDs | As of date and What changed |
| 4 | Conventions | Required | ID prefixes, column meanings, source format, state words, capitalized terms | Conventions block |
| 5 | Overview and map | Required when 4 or more kinds of thing | One table of commands or resources, plus one structure diagram | Diagrams |
| 6 | Commands or resources | Required | One subsection per command: synopsis, options table, exit codes, runnable example with output | Stable IDs, Evidence |
| 7 | Configuration keys | Conditional | File location and search order, key table, cross-key rules, a complete valid file | Stable IDs |
| 8 | Environment variables, files, exit codes | Conditional | One table each, same shape rules as below | Stable IDs |
| 9 | Errors and messages | Required when the product prints any | Table keyed by the exact message | Stable IDs, Evidence |
| 10 | Changes by version, deprecations | Conditional | Per entry: since, deprecated in, removed in | As of date |
| 11 | Glossary and abbreviations | Required when 5 or more terms | Glossary as a definition list (or a `data-glossary` table when a Related entries column helps) and a `data-abbr` table | `ubiquitous-language.md` |
| 12 | Verification and gaps | Required | What was checked, with what command, when; `[NOT VERIFIED]` and Pending notices | Evidence, Pending notice |
| 13 | Footer | Required | Scope, owner role, how to report an error | none |

One table shape per kind of thing, reused everywhere:

| Kind | Columns, in this order |
|---|---|
| Option, config key, environment variable | ID, Name, Meaning, Type, Default, Allowed values, Since, Source |
| Command | ID, Command, Purpose, Synopsis, Exit codes, Since, Source |
| File | ID, Path, Role, Created by, Read by, Since, Source |
| Exit code | ID, Code and name, Raised when, Commands, Since |
| Error | ID, Exact message, Exit code, Raised when, Command, Since, Source |

The second column is the lookup name; the reader script shows it as the popover title, so keep it short and exact.

## 4. Content depth

A complete Reference page contains:
- **Version and date** on the page and on the entry when it changed: "Since 2.2". Default and allowed values in separate cells. A range has units ("1 to 365", "1KB to 10GB").
- **Every entry the product exposes**, not only the common ones: hidden flags, deprecated names (kept with "Deprecated in", "Removed in" and the replacement), every exit code, every message the code can print. Count entries against the source (`--help` output, schema, grep of message strings) and write the counts in Verification.
- **Exact spelling** of names, flags and messages in code font, byte for byte, including capitalization and punctuation. Placeholders in capitals, explained below the block.
- **Types with precision:** "integer", not "number"; "string, one of"; "path, must exist"; units; whether the value is case sensitive.
- **Cross-entry rules** (conflicts, precedence, "whichever comes first") in a short list under the table, each citing the IDs it ties.
- **Examples that run as pasted** with the exact output, one per command, plus one complete valid configuration file. Mark an untested example `[UNTESTED]`.
- **Source on every row** as `path:lines` at one commit named in Conventions, or a command that reproduces the fact. Gaps get `[NOT VERIFIED: <command>]`.
- **Scope statement:** what the page does not cover (other products, internals) and where it lives.
- **Structure diagram** when the product has relations a table hides (which command touches which file, state transitions, data model). Every node and edge is in the source or the tables.
- **Glossary**, one definition sentence per term, genus plus difference, with the ID of the entry it relates to (in the definition, or in a Related entries column of a `data-glossary` table).
- **Stable IDs** that never change, so every row has a permalink and other tabs can cite it.
- **Pending notices** for rows that cannot be finished, mirrored in Verification.

## 5. Writing emphasis

Follow `writing.md`; add only this:
- Neutral third person, present tense, fragments allowed. "Number of Generations kept." not "You can use this to choose how many files to keep".
- No "should", no advice, no adjectives. Say what happens, then stop. Use MUST, SHOULD and MAY only if the source is a specification and the keywords are defined in Conventions.
- Same words in the same column order in every row. A cell is a final answer or an identifier, never "see below" or "depends". Repeat a critical limit in prose under the table.
- One term per concept (`ubiquitous-language.md`): the Name column, the synopsis, the example and the error table spell a flag the same way.
- Section headings are plain noun phrases the reader holds (`driftwood run`, "Exit codes"). No claim headings here.
- State what is true, then the exception, then the version: "Default 7. Allowed 1 to 365. Since 1.0."

## 6. Front end

- `data-reader="all"`. Turn on `menu` and `spy` (long page), `filter` and `search` (lookup is the main job), `permalinks`, `codecopy`, `tables` (wide tables scroll inside their own wrapper), `autolink`, `abbr`, `popover`, `back`, `figures`, `tabs` (only with several types). `progress` stays on but matters little. Turn off `copyopen` unless the page has an open questions list.
- Layout: left contents menu with filter, one `h2` per kind of thing, one `h3` per command. Tables are the main structure. Cards only for a multi-tab artifact.
- Row permalinks: the ID in the first column is the row anchor (`#def-CMD2`). Search finds it by ID and by name; the jump marks the row.
- IDs in prose link to the row and show its name in a popover. Glossary terms in prose show the definition. The glossary (a definition list or a `data-glossary` table) and the abbreviations table are read by `scripts/autolink.py`.
- Prefix list in `data-id-prefixes` (for example `CMD,OPT,CFG,ENV,FIL,EXIT,ERR`). A prefix is a short code of capitals.
- Diagrams: structure diagrams only (components, data model, state machine, "who touches what"), caption line first, legend, `accTitle` and `accDescr`, a collapsed text version for complex ones. See `diagrams.md`.
- Dense tables at 400 px: keep the ID and Name columns short and let the table scroll in its wrapper; repeat critical facts in prose.
- As-of stamp in the `meta` line and the footer.

## 7. Evidence and gates

| Gate | What it checks for a Reference page |
|---|---|
| Well written | One shape per kind of thing. Names match what readers hold. Units, defaults, scope on each row. Headings are lookup names. No procedure or reasoning sits inside an entry. |
| Correct | Version and as-of date are on the page. Each row matches the source of truth at the named commit. A script or a read confirms entry counts, defaults, allowed values and message strings. Every example ran. Gaps are tagged. |
| Optimized | No entry that only repeats another source without adding a fact (link instead). No prose that belongs in Explanation or How-to. Order serves lookup. |

- **Cold-reader answer key (five to eight questions, each answerable from one row):** What is the default of X? Which values does X accept? Since which version does Y exist? Which exit code does message M carry? Which file does command C write? Which commands read file F? What does term T mean here? What does the page not cover?
- **Test the facts:** diff the tables against machine output (`<tool> --help`, schema dump, `grep` of messages) with a script; run each example in a clean environment; run `autolink.py --check --internal-only`; compare entry counts with the source and record them.
- The stop rule for repeated rounds is in `quality-gates.md`.

## 8. Common failures

| Failure | Fix |
|---|---|
| Entries explain why or how ("to rotate daily, first...") | Cut to the fact; move the steps to How-to and the reason to Explanation; link by ID |
| Default and allowed values merged in one cell, or missing | Separate cells; write "none, required" when there is no default |
| Several table shapes for the same kind of thing | Pick one column order and apply it to every row |
| Message paraphrased in the error table | Copy the message byte for byte; readers search for it |
| Entries missing (hidden flags, rare errors) | Count entries in the source and compare; list the diff in Verification |
| No version or date, or "currently" and "new" | Stamp the page and each changed row ("Since 2.2"); use absolute dates |
| Claims with no source | Add `path:lines` at one commit or a command; else `[NOT VERIFIED: ...]` |
| Same thing under two names | One term per concept; add a collisions row; rename in every table and diagram |
| Diagram with edges not in the source | Redraw from the tables; every node and edge appears in text |
| Recommendations in cells ("use 7 for most cases") | Delete or move to How-to or Explanation |
| Rows cannot be linked | Give every row a stable ID in the first column; never renumber |
| Glossary terms defined twice with different words | One glossary table is the single source; inline text shrinks to a pointer |
| Examples that were never run | Run them, paste exact output, or mark `[UNTESTED]` |

## 9. Positive and negative example

Positive (one row, all facts, no advice):

> `CFG2` · `keep` · Number of Generations kept per Live log · integer · default `7` · allowed 1 to 365 · since 1.0 · `config/schema.py:21-28`

Negative (reads like advice and hides the facts):

> `keep` lets you decide how many old files to hold on to. Most teams find a handful enough, but you may want more if your disks allow it.

The negative has no type, default, range, version or source, and it gives advice.

## 10. Pre-publish checklist

- [ ] The title, version described and as-of date are on the page and in the footer.
- [ ] In one minute states scope, version, exclusions and where to look first.
- [ ] Every kind of thing uses one table shape; column order is identical across tables.
- [ ] Every row has a stable ID in the first column and a short exact name in the second.
- [ ] Every row has type, default, allowed values and since (or says "none").
- [ ] Every row has a source at one named commit, or a `[NOT VERIFIED]` tag with its command.
- [ ] Entry counts match the source; counts are written in Verification.
- [ ] Every message in the error table is copied byte for byte from the source.
- [ ] No row contains steps, advice or reasons; links out use stable IDs.
- [ ] Every example ran as pasted; outputs are exact or the example is marked `[UNTESTED]`.
- [ ] Diagrams have a caption line, a legend, `accTitle`, `accDescr`, and nothing outside the tables.
- [ ] Glossary and abbreviation tables exist; `autolink.py --check --internal-only` reports `[]` for undefined IDs, broken anchors and outside links.
- [ ] Capitalized glossary terms are used the same way in every table, diagram and example.
- [ ] Privacy scan passes; no secrets or personal data in samples.
- [ ] Hover, search by ID, filter and the 400 px layout were tried on the built page, in light and dark.
