# Stage 5: high level architecture (HLA) with ADRs

Reader: the platform reviewer who approves the architecture. arc42 + C4 structure, lean.

## Skeleton

```
# High level architecture (HLA): <system>
Series: ...
## In one minute            decision, ask to reviewers (approve the architecture and ADRs), key numbers, open items
## What changed in revision N
## Goals · ## Constraints   constraints cite AS# and team decisions
## Context and scope        C4 context diagram (mermaid)
## Traffic through the <component>   every webhook, event and destination that passes AND that does not pass, diagram + table
## Solution strategy · ## Building blocks (C4 containers)
## Runtime views            one subsection per scenario: happy path, reverse events, kills, outage, bypass, scheduled sends...
## Deployment               per environment (dev / test / prod)
## Cross-cutting concepts · ## Observability and monitoring   logs (no PII, retention), metrics, alarms → destination, dashboard, tracing
## Cost and hosting decision   1-3-1: one problem, three options, one recommendation; price list with date; volume basis with source; crossover
### Public benchmarks (summary)   3 rows + link to the market study
## Technology choices (summary)   language, runtime, IaC, test tools: options, criteria, decision; detail in the HLD; a consequential decision becomes an ADR, a routine one goes to the decisions file (see ADR or decisions file)
## Decisions to record as ADRs     only those that pass the ADR test below; table ADR-#: "We will ..." · basis · alternatives and why they lose · negative consequences
## Quality scenarios · ## Risks and technical debt (K#) · ## Assumptions added · ## Open questions · ## Future possibilities
```

## Cost 1-3-1

1. Public provider price per region (e.g. `curl` the AWS price list JSON and keep the file with its date). No prices from memory.
2. Volume today and at target, with a source (business data, a capacity file at a commit). Derived units stated explicitly (e.g. requests per user per day × downstream calls per request).
3. Three options with the cost per line (compute, requests, gateway, database, logs, metrics and alarms) today and at target, the crossover point and what would change the decision. Each line has a price or NOT PRICED with a ceiling and a Q#. The priced topology is the one in the Deployment section (number of tasks, load balancer, NAT, database, outbound traffic). Without a target volume from the owners, use 1×, 10× and 100× of today's volume. Cite the price list file and the SKU of each price. Use the first on-demand tier, no free tier, and say whether the target volume crosses a tier. The table totals come from the saved cost script, with no hand calculation. AWS price list codes: `AWSLambda`, `AmazonApiGateway`, `AmazonDynamoDB`, `AmazonCloudWatch`, `AmazonECS` (Fargate), `AWSELB`, `AmazonRDS`, `AmazonSQS`, `AmazonSNS`, `AWSSecretsManager`; NAT Gateway and outbound traffic live in `AmazonEC2` (large file: filter by `usagetype` with `NatGateway` and `DataTransfer-Out`).
4. Decide (when the user asks for a decision) and write the ADR.

## ADR or decisions file

Record an ADR for a consequential trade-off, for a decision the team or an external constraint requires, or when the rationale is worth keeping for the next reader. This covers product and design rules as well as technology. A routine choice (small, revertible, reusing what exists, rationale in one clause) gets one row in the decisions file (`decisions-rN.md`, format in `cross-cutting.md`) with its date, who can revert it and the linked open question. Three questions help tell the two apart: is it hard to reverse, would it surprise a reader without context, was it a real trade-off between alternatives? They guide the judgment and do not all have to hold. When an existing ADR already settles the choice, record it in the decisions file with a citation and keep an ADR only for the local trade-off around it.

## How to choose technology (goes into the Technology choices section)

Compare language, runtime, framework, libraries, IaC and test tools by stated criteria (cold start, maturity, what the team already uses, operating cost) and decide; the detail goes to the HLD; apply the ADR test above to decide whether the choice becomes an ADR or a log line.

## Done when

Each ADR says "We will ...", has the strongest alternative and why it loses, and the negative consequence; routine decisions sit in the decisions file and have no ADR; the cost has a price source and a volume source; the traffic diagram covers everything that passes and everything that does not.
