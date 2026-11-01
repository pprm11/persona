# Stage 6: high level design (HLD) and POCs

Reader: whoever will implement. Exact: routes, payloads, items, write conditions, algorithms and failures. Condition before action.

## Skeleton

```
# High level design (HLD): <system>
Series: ...
## In one minute            answer, the ask to implementers and reviewers, the numbers the POCs proved
## What changed in revision N
## Components
## Interfaces               routes with method, path, auth, full request and response, errors with the caller's action
## Data                     the table, every item with keys and fields, retention/TTL, IAM least privilege
## Algorithms               one subsection each, id ALG# (A# is reserved for assumptions), pseudo-code in fenced blocks, conditions (e.g. DynamoDB ConditionExpression) written out
## Sequences                mermaid sequence per key scenario
## Failure modes            table: failure · detection · behaviour · recovery
## Configuration · ## Observability (log line, metrics, alarms, tracing, dashboard) · ## Security · ## Cost
## <Rollout>                stages, entry/exit criteria per stage (from BR#), kill switches, rollback
## Migration from the current state   steps by dependency, each with what blocks it (Q#)
## Tests                    unit, contract, load; what each proves
## Coverage                 table: R# / AC# / I# → where in this HLD → which test
## Technology choices       language and runtime, framework, libraries, IaC and delivery, tracing, test tools: options, criteria, choice
## Proof of concept results one subsection per POC + "What the proofs of concept leave open"
## Next steps · ## Assumptions · ## Open questions · ## Sources
```

## POCs

- A POC proves a concept, not a feature: write the hypothesis and the pass criterion before running. The criterion must be able to fail: run a negative control that breaks without the protection under test (no shared lock in the harness, no result built to pass) and a load that can exceed the limit the POC claims to prove. Without the mock tool (moto, a local database), use a stand-in and say which one and what it does not prove. A POC with several checks has one control per check, and the summary says how many checks have a control. Synthetic data follows the HLD formats (key, id, log line); with another format the POC proves something else.
- Local, no cloud: mocks (moto for DynamoDB, respx for HTTP, k6 for load), synthetic data, no real phone numbers. moto proves the shape of the call, not atomicity: concurrent conditional writes go to DynamoDB Local, or to a local database declared as a stand-in.
- Cap of 5 minutes per POC; if it exceeds that, reduce the load and say by how much.
- Result with a measured number, the command to reproduce it and what stayed open. Examples: stable draw across stages (chi-square), first write wins with 40 threads, added p95 latency without a database, new routes with a sale × message race.
- A POC finding that changes the design goes back to the right stage (invariant in stage 4, ADR in stage 5) and enters the cascade.

## Done when

The coverage table links every R#, AC# and I# to a part of the HLD and to a test or POC; every route has a full example; every failure mode has detection and recovery.
