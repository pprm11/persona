# Document skeletons

Use this file when the document has a known genre and no genre skill supplies its content contract. A genre fixes the reader, the first paragraph and the section names readers expect. The Diataxis type of each section still comes from `SKILL.md`: the genre says what the document contains, the type says how each part is written and accepted.

A genre is a bundle of parts, and each part has one type. Write each part to its type file (`tutorial.md`, `how-to.md`, `reference.md`, `explanation.md`) and keep the genre's section names as headings. Under each heading, make the first sentence the claim (`writing.md`).

| Genre | Reader and job | Types it holds | Skeleton |
|---|---|---|---|
| README | A newcomer deciding whether and how to use the project | Explanation (what, why), Tutorial or How-to (quickstart), Reference (links) | below |
| Install guide | Someone who needs the tool working on their machine | How-to | below |
| Runbook | An on-call person under pressure | How-to | below |
| API reference | An integrator looking up one field | Reference | below |
| CLI reference | A user looking up a command, flag or message | Reference | below |
| RFC | A reviewer deciding whether to approve | Explanation, with Reference for facts | below |
| ADR | An engineer asking, years later, why | Explanation | below, and Decision record in `components.md` |
| Postmortem | A team and its leaders learning from an incident | Explanation | below |

In every skeleton the stamp (`As of <date>`, version or revision, owner role) sits under the title, and every number has a source (`components.md`).

## README

- **First paragraph.** What the project is, in one sentence, and for whom. The next sentence says why it exists and its status (active, maintenance only, deprecated).
- **Sections.**
  1. Quickstart: the shortest path to a working result, with commands and the output to expect (a Tutorial in miniature, or a How-to when the reader is not new to the field).
  2. Where to go next: links to how-to guides, reference and design notes, one line each.
  3. Status and versions: what is stable, what is not, supported platforms.
  4. Owner, support channel, how to contribute.
- **Common failure.** A feature list of adjectives with no purpose, no status and no runnable example. Fix: state the purpose first, then show one command and its output.

## Install guide

- **First paragraph.** What will be installed, on which systems, how long it takes if measured, and what the reader needs first.
- **Sections.**
  1. Before you start: requirements as a table with version, check command and expected output.
  2. Steps: one action each, one block per supported system, `You should see:` after each.
  3. Verify: an independent check that the tool works.
  4. If something fails: failure table keyed by exact message.
  5. Upgrade and uninstall: each with its own check.
- **Common failure.** Commands that need editing before they run, or a missing verify step. Fix: placeholders in capitals explained under the block, and a verify that reads state.
- **Type.** How-to. Link to the Reference for each option and to the Explanation only where a step looks wrong without a reason.

## Runbook

- **First paragraph.** The alert or symptom that leads here, its impact, and a link to the dashboard that confirms it. A reader who holds a different symptom must see at once that this is the wrong page.
- **Sections.**
  1. Is this the right runbook: symptom, alert name, confirming check.
  2. Mitigate first: rollback, failover or traffic shift, before any investigation.
  3. Investigate: a decision table or flowchart for branches, never nested prose.
  4. Steps: one checkable action each, the condition before any destructive action, expected output, recovery note next to the step that can fail.
  5. Confirm recovery: how to know it worked.
  6. Escalate: whom, and after how long.
- **Common failure.** Explanation between steps, or commands that need mental arithmetic. Fix: one sentence and a link, and commands that run as pasted.
- **Type.** How-to, kept on one page.

## API reference

- **First paragraph.** What the API or endpoint does, the version, the base address and the authentication it needs.
- **Sections.**
  1. Conventions: ID prefixes, error format, pagination, rate limits, versioning.
  2. Per endpoint: purpose in one sentence, method and path, authentication, every parameter (type, required or not, default, allowed values), a complete request that runs as pasted, the full response, and each error with its cause and the action the caller takes.
  3. Errors and codes: one table keyed by the exact code or message.
  4. Changes by version: since, deprecated in, removed in.
  5. Verification: how the entries were checked against the schema or the running service.
- **Common failure.** An architecture essay inside the reference, or errors listed without the action to take. Fix: move the essay to an Explanation tab, and add a Do this cell per error.
- **Type.** Reference. One table shape per kind of thing (`reference.md`).

## CLI reference

- **First paragraph.** The tool, the version described, what the page covers and what it leaves out.
- **Sections.**
  1. Conventions: ID prefixes, column meanings, source format.
  2. Overview: one table of commands, plus a structure diagram when commands share files.
  3. Per command: synopsis, options table (ID, Name, Meaning, Type, Default, Allowed values, Since, Source), exit codes, an example with its exact output.
  4. Configuration keys, environment variables and files: one table each.
  5. Exit codes and error messages: tables keyed by the exact text.
  6. Glossary and verification: entry counts against `--help` or the schema.
- **Common failure.** Options described by advice ("most teams use 7"). Fix: state the default and the range, and move advice to a How-to or Explanation.
- **Type.** Reference.

## RFC

- **First paragraph.** The proposal, the ask, who must approve and by when, and the feedback you want. Pages of context before the proposal are the usual failure.
- **Sections.**
  1. Summary: situation, complication, question, answer, ask, in a few sentences.
  2. Context and goals: forces as facts with numbers and sources; goals and non-goals with IDs.
  3. Proposal: the design from overview to detail, with a diagram when more than three parts interact.
  4. Alternatives considered: one subsection each, including "do nothing", each with the observable reason it loses.
  5. Risks and negative consequences: what gets worse, for whom, how it will be detected.
  6. Rollout and rollback: steps, flags, how long rollback takes.
  7. Open questions: each with an owner and the effect of each answer.
  8. Decision requested and references.
- **Common failure.** No alternatives, or a strawman alternative. Fix: state the strongest alternative as its best advocate would, then refute it with a mechanism or a number.
- **Type.** Explanation. Tables of options or limits that readers look up are Reference and link in.

## ADR

- **First paragraph.** The decision as "We will ...", with its status and date.
- **Sections.** The decision record shape in `components.md`: Context, Decision, Options compared, Consequences, Revisit when.
- **Common failure.** Options listed without a choice, only positive consequences, or a record written after the fact so the deliberation is lost. Fix: write it while the choice is open, list the rejected path, and give each consequence a payer.
- **Rules.** One decision per record. Never renumber or delete; a changed decision is a new record and the old one reads "Superseded by ADR-N".
- **Type.** Explanation.

## Postmortem

- **First paragraph.** The impact (who, how much, how long, in UTC) and the cause, in one or two sentences.
- **Sections.**
  1. Summary: what broke, the impact, the fix.
  2. Impact with numbers.
  3. Contributing causes in systems and processes. Describe what failed, never who failed.
  4. Wrong turns: each hypothesis or action pursued and then dropped, with what it looked like, why it was wrong, the evidence that dropped it and what to check first next time. List only turns the sources support. When there were none, write one line starting "None" and invent nothing.
  5. What went well and what was lucky.
  6. Action items: one owner, one ticket, one checkable end state each.
  7. Timeline last, with the source of each entry.
- **Common failure.** A timeline before the summary, or blame on a person. Fix: lead with impact and use system subjects ("the pipeline had no schema validation"). A related failure is a straight line from incident to fix that hides the misleading signals, so the next responder repeats the detour. Fix: record each dropped path under Wrong turns, as a misleading signal with a system subject. A rejected fix that was weighed as an option belongs in contributing causes or action items.
- **Type.** Explanation. The action items are a How-to list owned by the team.
