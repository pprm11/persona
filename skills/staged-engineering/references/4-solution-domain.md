# Stage 4: solution domain (RFC)

Reader: an engineer who checks the domain model before the architecture. Still no technology: contexts, aggregates, invariants, commands, policies and where the piece sits (placement).

## Skeleton

```
# RFC: <topic>, solution domain
Series: ...
## In one minute · ## What changed in revision N · ## Conventions
## From subdomains to bounded contexts   one context per subdomain, or the reason for merging
## Context map              upstream/downstream, conformist, anticorruption layer; who calls whom
## Ownership by context     matrix: context × data it owns × who may write
## Aggregates               one subsection each: purpose, fields, invariants I#, lifecycle
### Removed aggregates      "Removed in revision N: <reason>"
## Commands and domain events   command → aggregate → events; who may issue it (e.g. only the owning Variant)
## Policies                 forward, tracing, outage, kill, sale end, pin: each as WHEN/IF ... THEN
## Measurement              exposure log, comparison report, who builds it
## Decision: placement (ADR-# or D#)   options A to E with pros and cons; the decision and why; Background: the options compared
## Prior art (summary)      3 lines + link to the market study
## Assumptions · ## Open questions · ## Next steps
```

## How to do it

1. Trace: each BR# and R# from stage 1 and each AS# from the as-is → an aggregate, invariant, command or policy. A requirement with no home is a hole; an element with no requirement is an orphan (remove it or justify it).
2. Testable invariants: each I# later becomes a test or a write condition in the HLD (e.g. "first write wins", "a sale-ended Assignment never comes back").
3. Neutral placement options when others decide. With a team decision, record "Team decision, date" and move the options to Background.
4. Explicit concurrency policy: what happens when two events arrive together (sale × new message, late status × newer one).

## Done when

Every R# has a model element, every command says who may issue it, and every invariant has a way to be verified.
