# Brief: cascade re-derivation of a series (template)

Fill every `<...>` before handing this to a subagent. One subagent per stage, in order.

Scratchpad root (R): <scratchpad>

The series designs <one sentence: the system and the question it answers>. It has six stages, each built on the previous one:
1 problem domain RFC → 2 as-is → 3 market study → 4 solution domain RFC → 5 HLA (with ADRs) → 6 HLD.
Files live in `R/r<N>/new/` (`<series>-1-problem-domain.md`, `-1a-as-is.md`, `-1b-market-study.md`, `-2-solution-domain.md`, `-3-hla.md`, `-4-hld.md`, `-README.md`). Stages before yours are already final for this revision: treat them as the source. Untouched copies of revision <N-1> are in `R/r<N>/base/`.

What changed in the source since the last revision: <one line per change>. Your job is to re-derive YOUR stage from the stages above it, and change its decisions where they no longer follow.

## Source of truth, in this order

1. Team decisions: `R/decisions-r<N>.md`. Never change one. If your stage or an upstream stage conflicts with one, do not resolve it: write an open question (next free Q number in the README / problem domain) and list it in your report.
2. The upstream stages in `R/r<N>/new/`.
3. Your stage as it is now.

## What to do

1. Read the team decisions, every upstream stage completely, and your stage completely.
2. Build a trace table in `R/r<N>/trace-<stage>.md`: for each upstream item your stage must answer (business rule BR#, requirement R#, acceptance check AC#, quality scenario QS#, as-is constraint AS#, invariant I#, ADR, as relevant to your stage), the element of your stage that answers it, and a status: covered, stale (answers an older version of the item), missing, contradicts, or orphan (an element of your stage that answers nothing upstream).
3. Fix every stale, missing and contradicts row in your stage, and remove or justify every orphan. A design decision of your stage that no longer follows from upstream gets changed: you decide it (the user delegated reversible design decisions), and record it.
4. Keep IDs stable. A new item takes the next free number of its kind. An item you remove stays as a row or line "Removed in revision <N>: <reason>" in the same place. Update the "In one minute" section and add a "What changed in revision <N>" section right after it (replacing nothing else), with one bullet per change.
5. House rules: English only; no em dash or en dash as a pause; no invented numbers (a number needs a source in the series, the team decisions or a cited file); fenced code and mermaid blocks change only when the design they show changes; do not cite private conversations or name who said what beyond the owner of a question.
6. Repository references: write them as inline code `path:lines` for code read at commit `<sha>` of `<owner/repo>`. A final script turns each one into a permalink with that commit hash, so do not write repository URLs yourself and do not cite a file you have not read at that commit (`git show <sha>:<path>`).
7. Edit only your own stage file(s), the trace file and the change log. Do not run git, do not publish.

## Change log (mandatory): `R/r<N>/changes-<stage>.md`

One row per decision you changed, added or removed:

| Id | Before | After | Why (upstream id that forces it) |

Then a list "Questions raised" (new Q numbers with owner taken from the team decisions or the README owner lists) and "Left as is on purpose" (items you considered and kept, one line each).

## Report (final message, at most 20 lines)

Counts from the trace table (covered / stale / missing / contradicts / orphan, before your fixes), the decision changes in one line each, the questions raised, and anything you could not fix.
