# Stage 1: problem domain (RFC)

Reader: whoever decides whether the problem and the requirements are right (platform team, business owner). This stage is the source of all the others and does not choose technology.

## Skeleton (headings in English, in this order)

```
# RFC: <topic>, problem domain
Status · Date · Author · Decision owners
Series: 1 problem domain (this document) · 2 [as-is](...) · 3 [market study](...) · 4 [solution domain](...) · 5 [HLA](...) · 6 [HLD](...) · [README](...)

## In one minute            answer + ask + the 3 rules that matter + what is still open (with owner)
## What changed in revision N
## Conventions              BCP 14 keywords (MUST/SHOULD/MAY), EARS (WHEN, WHILE, IF ... THEN), ID kinds
## Motivation               what breaks today, who feels it, cost of doing nothing
## Goals and non-goals      G#, N#
## Assumptions              A#: working answers, each with what would change if wrong
## Context
### Current state           short; the detail lives in the as-is stage
### Decisions of <date> that shape the problem   "Team decision, DD/MM/YYYY", no quotes, no names
### <Flow around one unit of work>               e.g. traffic around one Conversation
## Problem domain
### Subdomains              core / supporting / generic
### Glossary                market-standard names first (Variant, Unit, Assignment, Allocation, Canary release...)
### Event classes           MECE: every event belongs to exactly one class
### Business rules          BR#: rule, then reason with its number and source
## Requirements             R#, in EARS, each tracing to a BR# or G#
### Quality scenarios       QS#: source, stimulus, environment, response, measure (with source for the number)
## Profiles                 contract + the first concrete profile (e.g. the order assistant) + its acceptance checks AC#
## Cross-cutting concerns   privacy, compliance, observability, retention
## Open questions           Q#: question, owner, what changes with each answer
## Next steps               next stage first, by dependency, no dates
```

## How to get there

1. Start with the questions for the owners. Save the draft with the questions as revision 1 (`evidence/problem-r1-before-answers.md`) and record when the answers were read (`evidence/answers-read-at.txt`). Apply the answers as revision 2, list each D# in "What changed in revision 2" and say which Q# each D# closes. The questions are what only the business or the platform can answer (assignment lifetime, volume, stage criteria, rollback). List them as Q# with an owner, tell the user to ask them, and record each answer in the decisions file. In an autonomous run (no user), the questions stay in stage 1 and in the decisions file as "pending", and the series goes on with working A# assumptions.
2. Glossary with market names (Statsig, LaunchDarkly and Argo Rollouts use Variant/Unit/Allocation/Canary). An in-house term that collides with another system gets a new name ("pause" collided with the messaging provider's pause: it became soft kill / hard kill).
3. MECE check: vocabulary (one term per concept, no overlap), subdomains and event classes (each event in exactly one class, none outside). Record the result in the README.
4. Internal traceability: each R# points to a BR# or G#; each BR# has at least one AC#; each Q# answered by a team decision leaves Open and enters Decided.
5. Volume and cost numbers come with a source (a repo file at a commit, or a business database with a date).

## Done when

A cold reader answers from the document alone: which problem, for whom, which rules hold, how to know it is right (AC#) and what still depends on whom.
