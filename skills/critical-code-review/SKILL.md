---
name: critical-code-review
description: "Review a branch before push through four lenses, with scope audit and corrections. Use for a very critical code review or a review before pushing; reviewing an existing PR as a reviewer is a separate skill."
---

# Critical code review

The review happens BEFORE the push. A push without review has to be apologized for later.

This is the author-side critical review before push. For a review of an existing PR and its comments, use a
PR-review skill. Retain applicable safety and authorization requirements.

## 1. Scope

Define the base (the PR's target branch) and list the diff (`git diff --stat <base>...HEAD`). If another
branch was merged in, separate what came from it from what belongs to this task.

## 2. Review lenses

When authorized subagents are available, each receives the file list, task goal and repository instructions. Otherwise review the lenses sequentially and disclose the lack of independent review. Each lens yields
findings with file:line, severity, a concrete failure scenario and a suggested fix.
- **CR1 bugs and behavior**: error paths, fail-open, per-run state not cleaned, concurrency, test
  regressions, regex erasing a response.
- **CR2 architecture (Google eng-practices)**: design, layers, duplication, names, complexity, tests that test
  what matters, dead code. Test oracles must be independent: expected values come from a hand-derived literal or
  an independent source; a value recomputed the way the code computes it proves nothing, and a fixture whose
  expected value mirrors the implementation is a finding. Apply the `ub-mode` metrics to the files in the diff when the tools are available.
- **CR3 prompts and rules**: contradictions between prompt, condensed rules, tool docstrings and code;
  instructions the model cannot follow; prompt size.
- **CR4 scope, security and hygiene**: does each hunk belong to the task (branch holds only the task's scope)?
  Instrumentation, lab artifacts, `.env`, secrets, real data in tests, needlessly formatted files, changes from
  another branch. A subtraction the change requires, pinned by a test and with the suite proving behavior did
  not change, belongs to the task (ub-mode, Subtract Before You Add); loose refactoring remains a finding.
  Spec check: list the ticket or spec requirements and mark each as met, partial, missing or wrong, quoting the
  spec line for every item that is not met. Follow a requirement beyond the diff to its callers, config and docs.
  An inherited gap unrelated to the requested outcome becomes a follow-up note and does not block the push. An
  unmet requirement, or an existing weakness that the change now exposes or depends on, is judged by its impact
  like any other finding, whoever wrote the old code. When every requirement is met, say so with the mapping and
  add no gap of your own; without a spec, note that.

## 3. Triage and correction

- Verify each finding (read the code) before accepting it; discard false positives and say why.
- For each accepted finding, ask why it got through and where it originates (skill `root-cause` if installed; otherwise reproduce and test competing causes): the same
  pattern in several files is fixed at the source (helper, template, prompt), and the finding gets a guard
  (lint or test).
- Fix what belongs to this task. What belongs to another task: revert it here and record it as a separate task.
- Product decisions with no obvious answer: follow the production behavior and record it.
- Parallel fixes by subagents only with disjoint file scopes.
- Format/lint only the changed parts (the base may already be dirty; formatting everything pollutes the diff).
- Run focused tests and the full suite.

## 4. Report

Short table: finding → severity → done / discarded (reason) / deferred (where it is recorded). List the
architecture follow-ups not done. Local commit follows the user's rules; push and publication require
authorization.

## Related

- `ub-mode` (Uncle Bob's, from https://github.com/unclebob/ub-mode): metrics (CRAP, duplication, mutation) and what counts as subtraction in scope
- `root-cause`: tracing a finding back to its origin
- Stop a review cycle that does not converge: if two fixes with the same premise fail the same gate, or each new reviewer finds new problems for 2 rounds, write the premise in one sentence, show the numbers per round and ask before fixing anything else.
- A recurring finding becomes a lint or a test.
