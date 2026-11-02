# Concept before POC

Use this loop for uncertain product/architecture/DX decisions, not for every mechanical edit.

Before implementing the experiment, define the concept in terms of the problem it resolves,
its boundary and alternative interpretations. Then state a falsifiable hypothesis: which change
should improve which observable result, for whom, under what constraints? State what outcome
would reject or narrow the idea. Existing exploratory code is a candidate, not retrospective proof
that this hypothesis was defined earlier.

Choose the smallest POC and evidence that can distinguish those outcomes. Include legitimate use
and a relevant failure/control. Identify the comparison baseline, target, context and limits.
Name the cost/time boundary and an exit condition. Avoid building the complete framework merely
to discover whether one interaction is useful.

After executing, record observed result, unexpected friction, unsupported claims and the decision:
retain, change, defer or reject. Update the concept/spec where the evidence changes it. Keep the
old result and rationale linked rather than rewriting history to fit the candidate.

For beautiful developer experience, explicitly examine cognitive load, coherent vocabulary,
discoverability, number of choices/edits, first useful result, error recovery and upgrade
predictability. Presentation can improve clarity, but visual polish does not repair a confusing
model. Show the actual flow. Distinguish automated step/time evidence from human judgment of
clarity, trust and delight; invite focused user feedback when useful without blocking unrelated work.

One small table can hold concept, hypothesis, POC, result/limit and refinement. Split artifacts
only when their lifetime or audience differs. A growing stack of plans is itself a cost to inspect.
