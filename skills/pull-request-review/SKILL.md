---
name: pull-request-review
description: "Review an existing pull request as a reviewer and prepare actionable, evidence-backed findings."
---

# Pull Request Review

## Inspect first

Read the PR description, commits, complete requested diff, relevant surrounding callers, linked acceptance criteria and CI logs before commenting. Identify the exact head and base. Compare claimed parity against the actual authoritative source; inspect related open or recently merged changes when they can conflict or silently undo behavior.

Check scope, correctness, failure paths, concurrency, authorization and sensitive data, architecture, tests and negative controls, deployment and rollback. For a purported fix ask whether evidence supports the root cause. When the diff removes or loosens a validation, authorization check or other protection, read the history of those lines on the base ref (for example `git log -L <start>,<end>:<file> <base>`, `git log -S '<removed text>'` or `git blame <base> -- <file>`) to learn what it guarded, then look for the same invariant at another boundary and for a test that pins it. A finding needs an execution path, its preconditions, the impact and evidence that no equivalent protection remains. A protection that moved and is tested, or one removed by a recorded decision that cites its source and accepts the residual risk, goes in the summary as checked, with where it lives now or the decision. A removal the author marks as open or provisional still needs a finding. Distinguish failed checks, missing evidence and untested behavior from verified defects. If [root-cause](../root-cause/SKILL.md) is unavailable, reproduce and compare competing explanations yourself.

## Findings

Report only actionable findings supported by a location and concrete trigger, impact and smallest fix. Use one point per comment; mark blocking issues, questions and suggestions clearly. Put issues without an appropriate diff line in the summary. State what was checked, CI state, acceptance gaps, conflicts and limitations; avoid claims about the author's intent.

## Authorized publication

Only post comments or a formal review when the user's authorization covers that action. Reconfirm head immediately before submission, anchor to valid old or new diff lines on that commit, and reread the posted result. If the head changed, reassess affected findings rather than attaching stale comments. Report failed or rejected publication honestly. A request for review text alone does not authorize publishing it. Author-side review and publication belong to [critical-code-review](../critical-code-review/SKILL.md) and [publish-pull-request](../publish-pull-request/SKILL.md), when installed.
