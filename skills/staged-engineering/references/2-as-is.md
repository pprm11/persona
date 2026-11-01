# Stage 2: as-is

Reader: an engineer or tech lead who needs to know where each piece runs today before reading the design. It records facts with proof and decides nothing. It comes right after the problem domain because it confirms or overturns the domain's assumptions.

## Collection (read-only)

- No deploy, no new resource, no config change, no message, no secret printed. Each check is a read command with an id (`[LIVE X1]`), a time, and its output kept in `evidence/`.
- Code and manifests at a fixed commit per repo, with a prefix (`v2:` = repo X at commit Y). Prefix table at the start.
- State words with one meaning each: **LIVE** (answered a probe or showed status SUCCESS/Healthy on the date; says nothing about traffic), **STALE** (present but not serving properly, or stopped since a date), **ABSENT** (declared and not present, or present and never run), **NOT VERIFIED** (no check was possible; say what would verify it and who unlocks it). A fact read only from a file carries no state word: it carries the `[FILES]` tag and, when the runtime state matters, an NV#.
- Tags: `[LIVE id]`, `[FILES prefix:path:lines]` (in the text of the series stages, cite code as `path:lines` in backticks, which `permalinks.py` turns into a link; the prefix stays in the prefix table only), `[RENDER ref overlay]`, `[PLATFORM <date>]` (a team statement, not verified by a command), `[NOT VERIFIED: ...]`.

## Full report (its own artifact, parts A1 to A7)

A1 structure (C4 context and containers) · A2 deploy and environments · A3 pipelines · A4 path of a request · A5 flags and levers · A6 data · A7 drift (rows DR-xx in DECISION, CANARY, INFO; D# is for team decisions) and questions. Each part has a checklist (questions a cold reader must answer) and goes through the cold reader → reviewer loop until zero blocking findings.

## The stage in the series (summary)

```
# <Topic>: as-is of <systems> (<snapshot date>)
Series: ...
<one paragraph: what this stage records, link to the full as-is report>
## In one minute            4 to 6 sentences, answer first, the ask (who confirms which NOT VERIFIED item), with tags
## What changed in revision N
## What the as-is means for <the design>   AS1, AS2...: one constraint each, with the fact's tag and the BR#/R#/A# it touches
## 1 Orientation · 2 Product by environment · 3 Facts that most change decisions · 4 Top risks, stated as facts
## 5 Questions for <owner> · 6 Not verified · 7 Recheck of <date> · 8 How to read the full report · 9 More views (diagrams)
```

The as-is ids (A1, P2, X1...) collide with the series ids, so the build does not auto-link in this stage. The AS# constraints are what the later stages cite.

## No live access

When live checks are not permitted: `evidence/` keeps the file reads (the `git show` command and the excerpt) and the NOT VERIFIED list, each item with the read command that would verify it and who can run it. The A1 to A7 report and the recheck stay as an accepted limit L# in the README. In a one-day run, the recheck is a re-read of the files at the end of the day, recorded as such. Sections 1, 2 and 7 still apply, with what the files show and NOT VERIFIED for the rest.

## Done when

Each assumption A# and each requirement that depends on the current state has a fact that confirms it, contradicts it, or stays NOT VERIFIED with who unlocks it; every fact has a tag; a short recheck of the main facts on another date changed nothing (or what changed is recorded).
