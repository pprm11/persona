---
name: root-cause
description: "Diagnose an error, bug, CI failure or recurring rework: reproduce it, use an Ishikawa diagram and causal questions, prove the root cause, and separate correction, containment and prevention. Use for root cause analysis, Ishikawa or 5 whys."
---

# Root cause (Ishikawa)

Fixing the symptom makes the problem come back in another form. The order is fixed: problem, fishbone, whys, proof,
root fix, guard. A solution appears only at step 5. Before that, every solution idea is rewritten as a cause
("missing retry" becomes "the call does not handle a 503").

`root-cause` owns diagnosis and proof.

## 1. Problem (the fish head)

One observable sentence with what, where, since when and how much (cases, %), with a source. No cause and no
solution in it. "CI fails" is not enough; "the `test-domain` check fails in 4 of 10 runs since PR #212, with a
Postgres timeout" is. Reproduce the problem before going on: without a reproduction, step 4 has no proof. Record
the command or sequence, the input, the observed symptom and the criterion that tells a correct result. A command
that fails with a different error does not reproduce this bug. When useful, shrink the case one element at a
time, and rerun the original case after the fix. The exemption at the end of this skill still applies: a stack
trace that already proves the single cause needs no reproduction harness.

## 2. Fishbone (6 categories)

| Category | In software and agents |
|---|---|
| Method | process, flow, order of steps, business rule, prompt, brief |
| Machine | code, tool, dependency, infrastructure, model |
| Material | input data, state, config, fixture, the batch of conversations |
| People | who executed (person, agent, subagent): missing context, handoff, knowledge |
| Measurement | test, eval, judge, rubric, metric, monitoring (includes a wrong test) |
| Environment | environment (dev / staging / production), network, version, time of day, concurrency, CI |

In each category, list the candidate causes or write "nothing found". Mark each one as **fact** (with file and
line, commit, log or command) or **hypothesis**. Read before assuming: code, diff, logs, history.

## 3. Whys

For the 1 to 3 causes with the most evidence, ask "why?" until you reach a cause that:
- is under the team's control;
- if removed, prevents this problem and similar ones from coming back;
- is not just "human error" or "the agent got it wrong": ask why the process let the error through.

It usually takes 3 to 5 levels. If the chain leaves the team's control (vendor, customer), stop there and record it.

When two or more causes stay plausible, write for each the observation that would weaken it, then choose one probe
that tells them apart and change one thing per probe. The number of hypotheses follows the evidence. Two techniques,
only when they fit: in a chain of components, log once at each boundary to see where the value goes wrong; when a
test passes alone and fails in the suite, bisect the test order to find the one that pollutes shared state.

## 4. Proof

Before fixing, prove the root: reproduce it, find the commit that introduced it, count how many cases it explains. A
root that explains fewer than half of the cases is not the only one: go back to the fishbone. Several roots are
legitimate; order them by cases. A change that happened at the same time as the problem is correlation, not proof.

## 5. Correction

Classify each proposed action:
- **root**: removes the proven cause.
- **containment**: holds the symptom while the root is not fixed (retry, longer timeout, regex, `skip`, an `if` for
  the case, rollback). Only with the label "containment" and a recorded task for the root. A guard that only hides
  the error (an `except` that swallows it, an `if` that skips the case without logging) is not containment: it is a
  patch and counts as a finding.
- **guard**: prevents the return (lint, test, gate, written rule). Every fixed root gets a guard.

A delivery with containment only is a failure, unless the root is out of scope or out of control: say so and record
it. Option menus follow the same rule: each option says whether it is root or containment, and the recommendation
attacks the root.

## 6. Delivery

The problem; the fishbone as a table (category, cause, fact or hypothesis, source), or as a diagram in an inline
widget when there are 3 or more causes; the chain of whys; the root and its proof; the actions with their label.
Scale to the size: a small bug fits in 5 lines, an incident or a test-battery result needs the full table.

Exempt: a typo, or an error whose single cause the stack trace or log itself proves. That needs no reproduction
harness and no list of hypotheses. Even then, answer "why did this get
through?" to decide the guard.

## Pitfalls

- Stopping at the first why ("the test failed because the mock was wrong").
- A diagram that is a list of solutions in disguise.
- Grouping by symptom and calling it a cause (ten "wrong city" errors can have three different roots).
- Fixing the same pattern file by file when the origin is one (generator, template, prompt, helper).

## Related

- `inline-widgets`: fishbone diagram
