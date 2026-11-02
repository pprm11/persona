# Three gates per stage: well written, correct, optimized

A stage closes only when it passes all three. They are different questions, with different reviewers, and one does not cover another: the text can be impeccable and the design wrong; the design can be right and too expensive or too complicated. The user's rule: it is not enough to be well written, the solution must be correct and well written, and also optimized.

| Gate | Question | Reviewer | Evidence that counts |
|---|---|---|---|
| **Well written** | Can a cold reader understand, check and decide without asking? | Sonnet applying the `artifact-routing` writing rules + a cold reader (another agent, no context) | The cold reader's answers to the stage checklist; `preserve.py`; traceability; a source on every number |
| **Correct** | Does it do what it must, including when something goes wrong? | Adversarial Opus per area + a second opinion from another model (Codex) | Counterexample, script that explores interleavings, recomputation, POC with a negative control, official documentation with URL and date |
| **Optimized** | Is it the simplest and cheapest way to give the same guarantees, including swapping the technology or removing the piece? | Opus "what can be removed, merged or made cheaper" + a measurement script | Before and after numbers (cost, calls per message, latency per hop, nodes, tests), the simpler alternative tested and why it loses |

Pass rule, the same for the three: zero *blocking* findings; each *major* fixed or accepted by the owner as a limit L# with a reason; *minor* becomes an item in the README. A fix that touched a stage reruns the gate of that area and the cascade of the following stages. If the number of blocking findings does not drop for 2 rounds, stop and show the numbers to the user.

Finding format (all three gates): Id · Gate · Severity · Where (file, section, ID) · What · Evidence · Smallest fix. A conflict with a team decision becomes a question for the owners, never a correction. Each reviewer closes with "Checked and passes": what was verified and passed, so it is clear what was covered.

## Criteria per stage

### 1 Problem domain
- **Well written**: "In one minute" with answer and ask; glossary with market names and one term per concept; every R# in EARS with BCP 14; each Q# with an owner and the effect of each answer; a cold reader answers "what must be true and how do we know".
- **Correct**: requirements consistent with each other and with the team decisions; together they reach the goals (no business counterexample breaks any); each AC would fail if the requirement broke; stage criteria with statistical power at the stated volume (minimum detectable effect at alpha 0.05 and power 0.8, computed in a script); assumptions the as-is may overturn are marked.
- **Optimized**: no requirement without a goal or decision behind it (gold plating leaves or becomes a non-goal); scope cut by value; each AC is the cheapest observable signal that proves the requirement; questions ordered by how much they unlock.

### 2 As-is
- **Well written**: state words with one meaning; every statement tagged; "what this means for the design" as AS# constraints; a cold reader knows where each piece runs.
- **Correct**: each fact reproduces from its tag (file at the commit, read command); NOT VERIFIED only where no check was possible, with the command that would verify it; no stage 1 assumption contradicted without a question; the recheck did not change the main facts.
- **Optimized**: depth of checking proportional to how much the fact changes a decision (a fact that changes nothing gets no expensive check); the cheapest, read-only check; the stage carries the summary and points to the full report instead of repeating it.

### 3 Market study
- **Well written**: each practice with source, date and label; adopted / adapted / rejected table with "where in the series" and "why".
- **Correct**: the source says what the series claims (reopened); right label (page read in full or search only); a number used the way the source measures it.
- **Optimized**: reuses what the market and the team already have before building (each "build" says why nothing ready fits); only benchmarks that a decision uses; research effort proportional to the risk of the decision.

### 4 Solution domain
- **Well written**: contexts, aggregates, invariants, commands and policies with IDs and a trace to R# and AS#; who may issue each command.
- **Correct**: every invariant holds under concurrency, failure, redelivery and clock skew (invariant × event table, interleaving script); the model covers every R#; no policy contradicts another.
- **Optimized**: each stateful piece is questioned: does the requirement really need stored state, or does a deterministic computation (hash, rule) give the same guarantee? Where can the state live at lower cost (in a system that already exists, in the event itself)? Then the smallest model that meets every R# (fewer contexts, aggregates, commands and states); no orphan element; the simplest consistency mechanism that suffices (conditional write before transaction, transaction before lock); placement with fewer hops and fewer ownership changes.

### 5 HLA
- **Well written**: "We will" ADRs with the strongest alternative and negative consequences; a diagram of what passes and what does not; cost 1-3-1 with price and volume sources.
- **Correct**: platform limits and timeouts fit the whole chain (official documentation); alarms fire on the failure they claim to catch; cutover and bypass with no loss or duplication; the cost recomputed in a script matches the table; ADRs do not contradict each other.
- **Optimized**: each technology compared with at least one real alternative and with the option of not having the piece (another database, another runtime, a service the team already operates, no new component), with cost, latency and operation measured; minimum cost today and at target, with the crossover point and what would change the choice; fewer pieces to operate (managed service before server, a component the team already operates before a new one); latency per hop within budget with measured headroom; reversible decisions where possible.

### 6 HLD
- **Well written**: every route with a full example; items with keys and fields; algorithms with written conditions (ALG#); failure modes with detection and recovery; a coverage table.
- **Correct**: write conditions are right (each ConditionExpression reviewed against the invariant); POCs with a negative control prove what they claim; error handling and redelivery are idempotent; no personal data in logs, traces or keys.
- **Optimized**: database reads and writes per message counted per path (and as few as possible); network calls in the synchronous path only where needed; cold start and package size measured; log and trace volume costed; configuration with the fewest keys.

### 7 Test plan
- **Well written**: each case Given / When / Then with the ID it proves; coverage matrix; environments, data and blockers with an owner; entry and exit criteria per environment and stage.
- **Correct**: each test would fail if the behavior were wrong (negative control executed or manual mutation); covers every AC, QS, invariant, failure mode, alarm and stage criterion; the environments and data exist or the blocker is named; no test touches a real production API.
- **Optimized**: each risk tested at the cheapest level that catches it (pyramid: unit and property before integration, integration before production); no duplicate case; suite time measured; each stage's sample at the minimum that gives the decision; what runs in CI on every PR separated from what runs before each stage.

## How to run with several agents

- Well written: one Sonnet applies the `artifact-routing` writing rules and `preserve.py`; another agent, with no context, answers the stage checklist (questions a cold reader must answer) from the document alone.
- Correct: one Opus per area with `correctness-brief.md` (algorithms and concurrency; architecture, limits and cost; requirements against the as-is; evidence and POCs) and one Codex with the same scope, without seeing the other findings.
- Optimized: one Opus with the question "what can be removed, merged, moved to another technology or made cheaper while keeping every R#, AC and invariant", starting with the question most expensive to get wrong: does this piece need to exist? With a measurement script (cost per line, DynamoDB calls and capacity units per path, hops and latency, test suite time).
- The three run in parallel; the findings are merged into one table; fixes per stage; a new round only on the areas touched.
