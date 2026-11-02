---
name: publish-pull-request
description: "Publish an explicitly authorized author-side pull request or update and follow its checks."
---

# Publish Pull Request

## Prepare the exact candidate

Confirm the user's instruction and repository policy authorize the intended external action. Review the branch, base, diff and any existing PR state. Scope the branch to the task without discarding unrelated user work. Apply the required author-side review and repository gates; [critical-code-review](../critical-code-review/SKILL.md) can assist when installed, otherwise perform the review directly. Run required checks on the integrated candidate, not just an earlier branch state. Preserve failed results and explain limitations.

Reconcile base changes and conflicts according to repository policy; verify moved tests and structured configuration remain intact. Do not force push or overwrite others' work unless separately authorized. For a stacked PR identify its dependency and current base.

## Publish and verify

Prepare or refresh the body from actual behavior and receipts using [pull-request-description](../pull-request-description/SKILL.md), if installed, or the repository template. Commit and push only within the authorized scope, then create or update the PR as requested. Do not add an approval step when the existing instruction already authorizes the action.

Observe the actual remote head, base, relevant run and attempt after publication. Match required check results to that exact candidate and event; a local passing suite does not establish CI success, and stale or absent receipts remain unknown. Refresh outdated body claims only when that update is authorized. Report the PR link, commit, checks and remaining risks. Draft removal, merge and deployment require the authorization and gates applicable to each action; they are not implied by writing a description.
