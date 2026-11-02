# Ubiquitous language: build and keep a document's vocabulary

Use this file when an artifact introduces more than a handful of domain terms, or when several artifacts and tabs share terms. A document that uses two names for one thing, or one name for two things, makes the reader guess. The mechanics of links, popovers and anchors live in `linking.md`; this file covers the vocabulary itself.

## 1. Choose names

- **Prefer the market-standard name over an invented one.** Search how established tools and standards name the concept before you coin a term. Example: an experimentation design called a "group" and an "arm" in house speech should use the vendor-neutral terms the field uses, such as Variant for the option under test, Unit for the thing assigned, Allocation for the split of traffic and Canary release for a staged rollout.
- **Rename when your term collides with another system.** If "pause" already means something in a provider you integrate, give your concept a new name (soft kill and hard kill), and record the old name in the collisions table.
- **Check the side effects of a rename.** After renaming, read the diff for broken grammar ("an Variant"), broken compounds and tool names that contain the old word, and for identifiers that must keep their form.
- **Never rename identifiers.** Branches, repos, tools, flags, code and API fields keep their spelling. Write them in code font and explain them with the standard term.

## 2. One term per concept

- One concept has one name everywhere: prose, headings, tables, diagrams, code samples, captions and alt text.
- Never vary a term for style. A reader treats a new word as a new thing.
- Run a MECE check on the vocabulary before you publish a glossary of more than about 10 terms.

| MECE question | Action on a "no" |
|---|---|
| Is every term used for exactly one concept? | Split the term or add a collision row |
| Is every concept named by exactly one term? | Merge the synonyms into one standard term |
| Do any two definitions overlap? | Sharpen the difference clause of each |
| Does any term in use lack a definition? | Define it or stop using it |
| Do the terms of one class cover the whole class? | Add the missing members or narrow the class |

- Record the result of the check next to the glossary (one line is enough: date, what changed).

## 3. Write definitions

- **Genus plus difference, one sentence.** Say what kind of thing it is, then what separates it from its neighbors. Start with the genus, not with the term.
- Before: "Allocation is when we do the thing with the traffic."
- After: "Allocation: the rule that assigns each Unit to one Variant and keeps that assignment stable."
- **Contrast with the nearest neighbor** when two terms are easy to confuse: "test: offline, with no model. eval: a suite that calls a real model."
- **Keep it short.** A popover truncates long text, so the first 110 to 160 characters must carry the meaning. Put detail in a second sentence.
- **Give a source** when the definition comes from a standard, a vendor document or a decision: a link, a clause number, a date.
- **Do not use the term inside its own definition,** and do not define with a term that is itself undefined.
- **State scope** when the term has a narrower meaning here than in general use ("in this artifact, 'session' means a login session").

## 4. Inline definition or glossary entry

| Situation | Where the definition goes |
|---|---|
| Used once, and only in one section | Inline, at the first use, in a clause or sentence |
| Used in two or more sections or tabs | Glossary entry; link the first use per paragraph |
| Used by every reader on every page (HTTP, URL) | Nowhere |
| A project-specific identifier (flag, endpoint, field) | Reference tab entry, not the glossary |
| A concept the whole document turns on | Glossary entry plus a short explanation in the Explanation tab |

- A term defined inline and again in the glossary must use identical wording, or the glossary wins and the inline text shrinks to a pointer.
- A new term goes into the glossary, never into code or into the page script.

## 5. The glossary table is the single source

- Keep one glossary per artifact, in one of two shapes the scripts read. Recommended: a definition list, `<dl class="glossary">` with `<dt class="defterm">Term</dt><dd>One-sentence definition</dd>`. Alternative: a `table[data-glossary]` with the term in the first column and the definition in the second, when readers also need columns such as related entries or a source. Do not mix the shapes.
- Aliases go in the `data-aliases="a, b"` attribute on the `dt`, or in a column headed Aliases (any case, comma separated) of a `data-glossary` table. The build and the reader script read both.
- The glossary feeds hover and focus popovers, in-page search, the abbreviation list and the "used N times" list. The page build reads it and nothing else; see `linking.md` for the markup.
- Terms are matched by whole word, longest term first, with a plural suffix allowed. Matching skips code, preformatted blocks, links, headings and abbreviations.
- Slugs: lowercase, with every run of non-alphanumeric characters turned into a hyphen. The build writes the anchor `term-<slug>`; do not hand-write anchors for terms.
- Group entries by theme when there are more than about 15 (for example work and decisions, testing, delivery). The table order does not change the build.
- A term in the table with zero uses is a smell: delete it or find where it belongs.

## 6. Collisions table

One row for every word that means different things in your domain.

| Word | Senses | Standard term for each |
|---|---|---|
| session | a login session; a working conversation with a coding agent | **login session**; **agent session** |
| environment | a deployment target; a shell variable set | **environment**; **variable set** |
| rule | an engineering rule (lint, review); a business rule of the product | **engineering rule**; **business rule** |

- Every sense gets its own distinct standard term, so a reader can always disambiguate by wording.
- Use the standard term in running text. Use the bare word only inside a sentence where the context removes any doubt.
- Add a row when a reader, a reviewer or a search finds the same word used for two things. Do not wait for a complaint.

## 7. Synonyms, corrections and interpretation

- **Declare tolerated synonyms** at the top of the glossary (alternate spellings, nicknames, an informal name for an environment). Never correct them.
- **Never correct** accents, case, typos, nicknames, pasted quotations or the reader's harmless synonym.
- **Correct a term only when two readings would change the action.** The correction goes first and is short: "You said X; I understood Y (standard term: Z)." One correction per reply.
- If the action is irreversible or reaches outside the document, ask before acting.
- A "how to read requests" section maps ambiguous phrases to actions ("deploy: take a version to an environment", "run: execute a test or script"). Add it when readers ask for things in shorthand.
- Retired terms stay in the glossary as a mapping row: "old name: read as new name".

## 8. Version the glossary

- The header carries a version and a date ("v1.2, 2026-03-01").
- Add a term, swap a term or change a definition: bump the version, and write the change in a log file or in a "What changed" line.
- Ask before changing a term other people use ("add X to the glossary?" or "swap X for Y?"), and edit after the yes.
- When several glossaries stack (a general one, a team one, a personal one), load them from general to specific. On conflict the most specific one wins, and the override is listed.

## 9. Abbreviations list

- Keep the abbreviation list next to the glossary, as a second table: abbreviation, expansion. It is a data file, not a hard-coded dictionary in the page script.
- Expand on first use in each artifact, and mark the page text with `<abbr title="expansion">`.
- Add an abbreviation to the list when the artifact uses it twice or more. Drop the abbreviation and write the full name when it appears once.
- When a term and its abbreviation both exist, the glossary defines the term and the abbreviation list points to it.
- Review the list whenever the glossary version changes.

## 10. Linking summary

Point to `linking.md` for the mechanics. The rules that affect vocabulary:

- Click on a term goes to its definition. Hover and keyboard focus show a short definition. The popover stays open under the pointer and closes with Esc.
- Link only the first occurrence of a term per paragraph, list item or table cell.
- An identifier that other sections cite (a requirement, a decision) is defined once, has a short name at its first mention, and is never the first word of a sentence.
- Link text is the title of the target.
- Links stay inside the artifact, and they may cross tabs.

## 11. Terms in diagrams, code and headings

- **Diagrams:** node labels use the glossary term, spelled as in the table. Hover on a node shows the same definition as the text. The caption lists any term the diagram introduces. Do not abbreviate in a diagram what the text spells out.
- **Code samples:** identifiers stay as they are. Explain an identifier with the standard term in the sentence before or after the block, and never rename a variable to match the glossary inside a sample that must run.
- **Headings:** use the standard term; do not link inside a heading. The first use in the body is the linked one.
- **Captions and alt text:** use the standard term, and spell it the same way as the table.
- **Titles and tab labels:** a tab named after a glossary term must use its exact spelling.

## 12. Checks

| Check | Pass condition |
|---|---|
| Every glossary row has exactly one definition sentence | yes |
| No term in text lacks a glossary row (for terms used in two or more sections) | none missing |
| No two rows define the same concept | none |
| Collisions table covers every word with two senses | yes |
| Every identifier cited in text has exactly one definition | yes, and the build prints no missing or broken ones |
| Glossary version and date are current | yes |
| Cold reader can answer "what does X mean here" from the artifact alone | yes |
