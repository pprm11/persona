# Round 1 of the skill evals

Each run is graded against `evals/rubric.md`, with a `grade.md` next to the run (run A and run B).

## Totals

| Run | Seed | Total | Result |
|---|---|---|---|
| A | outbound message queue | 63.5 | Fail (below 85) |
| B | LLM gateway with model A/B | 87.5 | Pass (no blocking skill defect) |

Run A lost most of its points to execution: an incomplete cost table for the recommended option (C8, 6), invented "series target" measures (C3, 6), wrong citations (C11, 4), a verify command that prints secrets (C5, 5). Run B lost points to POCs that pass by construction, missing asks and two unsourced numbers.

## Skill defects, merged and ordered by points lost

| # | Defect | Points lost | Runs | Exact edit |
|---|---|---|---|---|
| 1 | A POC criterion does not have to be able to fail. Both runs shipped one: A's POC-4 (800 reservations can never break 1,000 a minute), B's race under one Python lock and its injection check on a one-element set. | 7.0 (A 3.5, B 3.5, C10) | A, B | `references/6-hld.md`, in the POC rules, after "write the hypothesis and the pass criterion before running.", append: "The criterion must be able to fail: run a negative control that breaks without the protection under test (no shared lock in the harness, no result built to pass) and a load that can exceed the limit the POC claims to prove." |
| 2 | The ask is missing from three stage templates while `references/cross-cutting.md` requires it in every "In one minute". | 4.5 (B 3, A 1.5, C2) | A, B | `references/2-as-is.md`: `## In one minute            4 to 6 sentences, answer first, the ask (who confirms which NOT VERIFIED item), with tags`. `references/3-market-study.md`: `## In one minute            verdict, the ask, what the market covers, what it does not, the numbers that drive decisions`. `references/6-hld.md`: `## In one minute            answer, the ask to implementers and reviewers, the numbers the POCs proved`. |
| 3 | A# is the id of assumptions, and the HLD template gave algorithms no prefix, so both runs numbered algorithms A1 and up, colliding with assumptions. | 4.0 (A 2, B 2, C12) | A, B | `references/6-hld.md`: `## Algorithms               one subsection each, id ALG# (A# is reserved for assumptions), pseudo-code in fenced blocks, conditions (e.g. DynamoDB ConditionExpression) written out`. |
| 4 | The order "questions before answers" leaves no trace and the revision numbering of the draft is unspecified. Run A could not show the order and mislabelled its revision heading; run B invented the protocol and was the only one to prove it. | 3.0 (A, C4) | A (B passed by its own initiative) | `references/1-problem-domain.md`, append: "Save the draft with the questions as revision 1 (`evidence/<stage>-r1-before-answers.md`) and record when the answers were read (`evidence/answers-read-at.txt`). Apply the answers as revision 2 and list each D# in What changed in revision 2." |
| 5 | "A vendor talking about itself is a vendor claim" reads as overriding search-only, so A labelled summary-only pages as vendor claims. | 2.0 (A, C6) | A | `references/3-market-study.md`, append: "A page read only through a summary or snippet is search-only, whoever the publisher is; a vendor claim requires the page to be read." |
| 6 | `scripts/privacy_scan.py` flags the synthetic number the skill prescribes in `SKILL.md`, so a clean scan is impossible. | 0 (content was right) | A | `scripts/privacy_scan.py`: skip matches that start with the synthetic prefix. `SKILL.md`, after the example: "A synthetic number starts with the reserved prefix; the scanner ignores it." |
| 7 | The as-is tag `[FILES prefix:path:lines]` never matches the regex in `scripts/permalinks.py`; both runs had to drop the prefix. | 0 | A, B | `references/2-as-is.md`: ``Tags: `[LIVE id]`, [FILES `path:lines`] (prefix only in the prefix table), ...``. Or extend the regex in `scripts/permalinks.py` to accept `prefix:path:lines`. |
| 8 | The as-is assumes live checks: `evidence/` with command output, the A1 to A7 report, a recheck on another date. Nothing says what to write when no live check is allowed. | 0 | A, B | `references/2-as-is.md`, append: "No live access: `evidence/` keeps the file reads and the NOT VERIFIED list; the A1 to A7 report and the recheck stay as L# in the README." |
| 9 | The page build is a verification step in `SKILL.md` but sits next to publishing; both runs skipped it. | 0 | A, B | `SKILL.md`, append: "The build runs locally even when publishing is not allowed." |
| 10 | Cost lines: the skill lists the lines (`references/5-hla.md`) but not that the priced topology must match the Deployment table, nor what to write for an unpriced line. Run A's C8 loss is execution; this edit makes it detectable. | 0 (A's 6 points are execution) | A | `references/5-hla.md`, append: "Each line has a price or NOT PRICED with a ceiling and a Q#. The priced topology is the one in the Deployment section (number of tasks, load balancer, NAT, database). Without a target volume from the owners, use 1×, 10× and 100× of today's volume." |

No skill defect was classed blocking.

## REPORT.md complaints judged valid

Run A:

| Id | Verdict |
|---|---|
| S1 revision numbering of the draft | Valid (defect 4) |
| S2 FILES tag vs permalinks | Valid (defect 7) |
| S3 scanner flags the synthetic number | Valid (defect 6) |
| S4 database POCs, downloads | Valid |
| S5 negative controls | Valid (defect 1) |
| S6 price files, free tier, target volume | Partly valid (target volume; defect 10) |
| S7 compare premises with files | Partly valid (the as-is reference already covers A#) |
| S8 evidence with no live access | Valid (defect 8) |
| S9 single-agent declaration | Valid, trivial |
| S10 requirement found later | Partly valid |
| S11 D# closes which Q# | Valid, minor |
| S12 build when publishing is forbidden | Valid (defect 9) |

Run B:

| Id | Verdict |
|---|---|
| S1 decision contradicts its own source | Partly valid (`SKILL.md` covers conflicts in general) |
| S2 FILES tag vs permalinks | Valid (defect 7) |
| S3 checkout not at the fixed commit | Not valid (`cross-cutting.md` already requires `git show <sha>:<path>`) |
| S4 recheck with no live facts | Valid (defect 8) |
| S5 later stage revising an earlier one | Valid |
| S6 stand-in when mock tools are missing | Valid |
| S7 trace format vs HLD coverage | Valid, minor |
| S8 single-agent declaration | Valid, trivial |
| S9 build when publishing is forbidden | Valid (defect 9) |
| S10 production owner name | Not valid (`SKILL.md` allows a component owner) |
| S11 cost checklist | Valid (defect 10) |

Complaints raised by both runs: FILES tag vs permalinks, single-agent declaration, build when publishing is forbidden, cost checklist. These four plus defects 1 to 3 are the edits for round 2.
