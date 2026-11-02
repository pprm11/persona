---
name: pull-request-description
description: "Write or revise a pull request description that explains behavior, evidence and risk to reviewers."
---

# Pull Request Description

Read the current diff, linked requirements, existing description and validation receipts. Identify the reviewer and retain accurate useful context. Describe observable behavior, the concrete problem and why it matters; use before/after examples when helpful. Cite the actual source of consequential claims. Do not infer a design decision or test result that is not evidenced.

Follow the repository template where applicable. A useful body normally contains problem and behavior change, review path for non-obvious parts, exact tests and results, material risks and rollback, and relevant out-of-scope work. If stacked, identify the base and prerequisite. Mark tests not run and distinguish local results from CI on the exact commit. Explain unfamiliar domain terms for a reader without the originating conversation.

Before handoff compare the body against the current diff and checks, remove stale status claims, and preserve valid prior context. Writing a body does not itself authorize an external update. [publish-pull-request](../publish-pull-request/SKILL.md) owns authorized author publication if installed; otherwise use the repository’s publication procedure.
