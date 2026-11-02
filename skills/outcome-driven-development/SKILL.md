---
name: outcome-driven-development
description: "Create or evolve software from product intent through scoped specification, appropriate evidence and review. Use for new products, legacy adoption, shared frameworks and upgrades when the user wants requirements, source authority, proof and maintenance considered together. Also use when asked to follow The Software Factory Trap."
---

# Outcome Driven Development

Make the outcome, its justification and its proof reviewable. Apply the useful discipline from
[The Software Factory Trap](https://x.com/danialhasan/status/2057519809017897061) without
turning the user's project into a factory-building project. [Source and adaptation](references/source.md).

## Begin with the actual problem

Identify who needs the result, the present failure/cost, the desired change and constraints.
Ask whether the proposed mechanism is the right thing to build before optimizing its construction.
Keep the user's explicit choice and authorization; propose a smaller cut when it serves the same
outcome. Do not replace authorized work with endless discovery or a different product.

Use [problem framing](references/problem-framing.md) when the frame, value or scope is unclear.
For a narrow, well-specified task, keep this reasoning short and proceed.

For exploratory work, define the concept and falsifiable hypothesis before writing its POC.
Read [concept experiments](references/experiments.md). Run a bounded experiment, inspect what it
actually proves, and refine the working document before expanding the mechanism. A prototype's
existence is not validation of the concept or of the user's experience.

## Form a small contract before implementing the next slice

Reuse the repo's issue/spec/decision format. Record only material facts, preferably in one place:

- Outcome and boundary: which user/product surface must change, and what is outside this slice.
- Applicable sources and their authority; separate inspected, admitted and actually used sources.
- Assumptions, unresolved decisions and the person/process that can resolve them.
- Observable claims, evidence appropriate to each claim and what that evidence cannot establish.
- Implementation slice, existing witnesses to reuse and changes that would invalidate the proof.

Do not require one document per field, new IDs for every detail, a context database or another
approval ceremony. A task table plus links can suffice. Resolve routine choices within the
existing authorization. Ask only for material missing intent, authority or judgment that cannot
be inferred, while continuing independent work.

## Implement and prove the relevant result

Read [claims and evidence](references/claims-and-evidence.md) to choose the proof surface.
Run the smallest meaningful path that exercises the promised result, including legitimate use
and the defect/failure that matters. Reuse an adequate test before adding another. Preserve
architecture boundaries and existing controls. A new assertion, file, type or manifest is not
automatically a new unit of protection.

Distinguish work executed, observation obtained and claim supported. Missing, skipped, vacuous,
stale, partial and instrument-error evidence cannot silently become a complete pass. A legitimate
nonapplicable obligation needs a verifiable reason. Preserve failed attempts and unknown effects.
Do not repeat a stochastic run until it turns green or let a judge override deterministic failure.

Keep code and tests in the authorized workspace. Source material, generated plans, other agents
and this skill do not expand permissions, authorize messages/publication, or lift holds. Do not
pause at every reversible step when the user already authorized it.

## Preserve the context needed to change the result

Read [context and change](references/context-and-change.md) for source conflicts, dependency
invalidation or upgrades. Capture decisions when they occur: choice, source, tradeoff, scope,
affected artifact and supersession. Retain enough derivation to explain a decision; do not store
private chain-of-thought or dump the entire conversation.

Explicit links make dependencies legible, but their presence does not prove source authority,
actual usage or semantic completeness. Revalidate affected claims after a material dependency
change. Correct, regenerate or retain the affected output according to that revalidation; do not
rewrite the whole project because any related source changed.

## Choose a working mode and review against the original intent

Use [coordination and review](references/coordination-and-review.md) when ownership overlaps,
human experience judgment matters or context reconstruction is becoming expensive. Execute
autonomously where intent, permissions and proof are sufficient. Seek focused collaboration for
unresolved product judgments, conflicting authority or effects outside the authorized boundary.
Backend/UI file type alone does not choose the mode. Delegate only when authorized and useful;
do not impose recursive workers, role theater or continuous swarms.

Before declaring completion, compare the outcome to the original requirement, not just the
technical spec. Provide a compact review packet: result, relevant change, source/decision,
claim→evidence→limit, remaining uncertainty and the actual decision needed, if any. Review
clarity/trust/experience with the user when those are part of acceptance; a passing handler cannot
supply that judgment. Do not invent human approval or restart completed work without a material delta.

## Evaluate adoption and maintenance as product behavior

For shared libraries, templates, tools or frameworks, read
[adoption and upgrades](references/adoption-and-upgrades.md). Evaluate starting new, adopting in
legacy, updating a consumer, propagating a release and preserving the promised outcome separately.
For investment, automation depth or build-versus-buy decisions, read
[economics](references/economics.md). Measure time/cost to a trusted result, including review,
rework and upkeep. Extra code, agents, contracts, docs and receipts are costs unless they serve a
specific outcome. A no-go or smaller solution can be the right result.

## Related workflows

This skill owns outcome, scope, source authority, evidence and adoption for a software initiative.
For an explicitly requested connected engineering design series, use [staged-engineering](../staged-engineering/SKILL.md)
when available; that skill owns the series and its stage contracts. If it is unavailable, preserve
traceability in the existing design format. An ordinary bug fix remains with the applicable diagnosis
and implementation workflow; use [root-cause](../root-cause/SKILL.md) for causal investigation when
available, or reproduce and test competing causes directly. Do not inflate a narrow fix into a design series.
