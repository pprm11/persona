---
name: cross-harness-orchestration
description: "Coordinate parallel work or second opinions across Claude Code and Codex, with model selection, self-contained briefs, isolated writers and a budget ceiling. Use for portable or cross-harness orchestration."
---

# Cross-harness orchestration

The orchestrator plans, briefs, checks and integrates. Children do the work. Choose a model tier per task
(cheap for mechanical work, mid for reading, writing and review, top for judgment), using the model names of the
active harness, within task availability and the approved budget. Explicit model requests apply. Use a different
model for review when useful.

## Steps

1. **Split** the task into pieces that touch disjoint files and need no result from each other. Pieces that
   depend on each other run in sequence. Two children never write the same file.
2. **Brief** each piece in a file. A child knows only the brief:
   - Goal: what changes when it is done (one sentence).
   - Where: repo, branch, files to read and files allowed to change.
   - Acceptance: the command or observable signal (`make check`, a test name, "34 of 35").
   - Out of scope, and what to do when blocked (stop and report, do not improvise).
   - Facts it cannot rediscover cheaply: decisions, ids, constraints, with sources.
   For long briefs follow the `claude-workflow-orchestration` rules when that skill is available.
3. **Pick the model and tier.** Report the actual model and effort, including any substitution for an unavailable
   model. Writers need their own worktree.
4. **Run** with the harness's native child tool when it exposes the chosen model, or use a delegation helper for
   cross-harness work. In Codex, use native subagents for task pieces; open a new thread only for a separate
   session the user requested. Explicit model selection may require a self-contained, no-history child. Never
   assume a helper option exists without checking its help. A delegation helper should provide:
   - run: start a child from a brief file, in a given repo, with a tier, optionally in write mode (own worktree
     and branch) and in the background;
   - status: report on a run by id.

   Pass the target harness deliberately instead of relying on a default. Verify the recorded command before
   naming the model a child used. Stop Claude children at a budget and Codex children at a timeout. Use background
   mode for anything over a couple of minutes, and do not poll in a tight loop: check when you have nothing else to
   do, or once per few minutes.
5. **Verify** before reporting. The child's final message is a claim, not proof: read the diff in its
   worktree, run the acceptance command yourself, and say what you checked.
6. **Integrate**: merge or cherry-pick the child's branch into the working branch only within what the user
   allowed. Local commits on the task branch are fine; push and publication require authorization. Remove finished
   worktrees (`git worktree remove`).

## Limits

- Depth 1: children cannot delegate. Enforce it in the helper if it supports it; native-child briefs must prohibit
  further delegation explicitly.
- Ceiling: at most 10 children per task unless the user sets another number. Say up front how many children
  will run, in which harness and tier, and what the user gets at the end.
- Switching model or harness does not reset or increase an approved child, cost or time ceiling.
- If two rounds of child fixes do not reduce the open problems, stop and ask. Write the premise in one sentence,
  show the numbers per round and a root-cause analysis (`root-cause`), then offer a menu. Make no further
  correction before that.
- Keep run records (brief, command, log, final message, changed files) outside version control. They may hold code
  and customer data.

## Orchestration and session rules

- One conductor per wave or workflow run; pass the run id to sibling sessions when launching or resuming. A session
  that is not the conductor does not resume the run or push to the run's branches.
- Long runs: keep the app open; do not edit the script while the run is alive.
- The orchestrator delegates: CI failures, conflicts and review comments go to the session that owns the branch.
- Archive a finished child session without asking. On each child notice, list the linked sessions and archive the
  ones that finished. A child is finished when its PR is merged or closed, its question is answered, or it only
  waits for an external event that a new session can resume.
  - Before archiving, check the worktree: `git status` shows only untracked build output and no commit is missing
    from upstream. Copy anything worth keeping first, because archiving deletes the worktree.
  - Do not archive a child that waits for the user or has unsaved work. A child of another session is archived by
    its parent: pass the request on.
  - Report each archival in one line.
  - Where the harness has no archive tool, list the finished threads for the user to archive.
- Before editing a shared repo: run git status and list sessions; one writer per file.

## Push and approval

- Optimistic gate: static checks and the tests of the touched area locally; CI is the real gate.
- Protect CI: few pipelines, one push per round, no repeated CI without a change, PR body edits in a batch.
- After a valid approval, nobody pushes to the PR except for a merge queue rejection, a conflict or broken CI.
  Everything else goes into a stacked PR. These exceptions depend on the current publication authorization and
  grant no new permission.

## Code quality

- A recurring review comment or finding becomes a lint or a test.
- Answer each point with its id, commit and the path of the lint or test.
- Do not work around a block or a sensor: stop and run `make check`.
- Simulate the batch of PRs before merging.

## Models and cost

- Cheap for mechanical work, mid for reading and writing, top for judgment.
- Self-contained brief: the user's request and an instruction to report what was read and what was skipped.
- Fix the acceptance criterion before launching; after changing the prompt, do not resume.
- A base failure does not take down its dependents; with no blocking finding after 3 rounds, open the PR with a
  checklist.
- One session per phase; a short status per subagent.

## Related

- `claude-workflow-orchestration`: self-contained briefs for the children
