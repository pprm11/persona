---
name: measured-correction
description: "Run a measured correction cycle for evaluation failures, including options and before/after comparison."
---

# Measured Correction

## Diagnose

Record the baseline, rubric, sample, costs and conditions needed for a comparable rerun. Cluster failures, count cases and their weight in the metric, and show representative paraphrased evidence. A symptom cluster may have several causes. Use [root-cause](../root-cause/SKILL.md), if installed, to reproduce and test causal hypotheses; otherwise test competing causes directly. Label unproven causes as hypotheses.

## Decide

For each material cause compare feasible options: what changes, affected cases, risk, cost and whether it addresses the cause or contains the symptom. Include a root correction when feasible. Recommend only when requested or appropriate to the decision; obtain the user's choice when it belongs to them. Follow established product behavior when that is the governing source, and surface an unresolved decision rather than inventing one.

## Implement and measure

Make scoped changes and meaningful offline tests; do not expose real examples. Run focused and required full tests before an expensive evaluation. Repeat the affected cases and a reproducible regression sample under equivalent conditions; record seed, versions, rubric and both results. More rounds are useful where variance matters. Report improvements, regressions and uncertainty; investigate or revert a worsening change within the user’s authorization. Do not claim an improvement solely from a changed setting. Provide a before/after table and remaining failures.
