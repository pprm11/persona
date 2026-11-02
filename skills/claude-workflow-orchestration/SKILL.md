---
name: claude-workflow-orchestration
description: "Prepare Claude Sonnet and Haiku briefs and Workflows, including long handoffs and failure recovery. Use when delegating to cheaper Claude models or authoring a Workflow script. Cross-harness coordination lives in cross-harness-orchestration."
---

# Claude Workflow orchestration (Sonnet and Haiku)

Model tier follows the rule of explicit models per subagent (cheap for mechanical work, mid for reading and writing,
top for judgment) and `cross-harness-orchestration`; the Sonnet, Haiku and Opus names below are the Claude defaults.
A cheap model fails for lack of context, not lack of intelligence: the brief must carry everything.

`cross-harness-orchestration` owns cross-harness coordination and model selection; this skill provides Claude
Workflow mechanics and brief-writing details. Keep any safety and authorization requirements that apply.

## 1. The brief must stand alone

A subagent does not see the conversation. Every prompt carries:
- **Who asked and why**, in one line: "The user asked in this session: <short quote>." Without it, Haiku and
  Sonnet refuse tasks that look "outside the request" (two agents refused to fill in a document because the user's
  last message was about CI).
- **Absolute paths** with forward slashes, exact ids (node, block, PR, branch) and the exact command.
- **What success is**, in one verifiable sentence, and the output schema with `ok` plus `note` or evidence.
- **What never to do** in that task (push to shared branches, force-push, change hosting or repo settings, read
  `.env`, call a customer's production system).
- **A blocked call means stop.** Every brief says: "if a call is blocked by the permission classifier, stop and
  report; never reach the same result by another route."
- **New tests pass the whole static gate** (strict type checking plus the repo's sensors), not just the linter: the
  brief says to run the full static check before pushing.
- **Do not dodge a sensor.** A helper that returns the raw object (for example `_state(ctx)` returning the session
  state) hides the access from the sensor and is a workaround. The brief says to use the typed owner or stop and
  list what is missing.
- **The repo's merge rules**, when the agent will merge or open a PR: point to the repo's merging and CI
  failure-mode docs. The errors that cost the most rounds came from stale bases, not from code: a baseline merged by
  hand, another person's edit lost in a moved file, a removed branch rule copied to another branch, a test reading a
  CI environment variable, a secret-scanner false positive on test data.
- **Before merging a batch of PRs**, simulate the cross merge: pairwise text conflicts between PRs (with a merge
  commit) and a cumulative merge that runs the gates at each step.

## 2. Large text: a file, never retyped

A cheap model breaks JSON and truncates text when it retypes a long payload.
- Generate the content with a script into a file; the agent only **reads the file and passes it whole**.
- **Per-call ceiling**: a document-write tool may refuse writes above a size limit. Cut files below the limit,
  splitting at a blank line. One file per agent, one `pending` block per file (planted beforehand, in order), and
  each agent replaces its own block: the order stays guaranteed.
- Rule in the prompt: "the whole file in one write or nothing; if the server refuses, stop and report the
  code, never write part of it." Retry only for malformed JSON of your own.
- Content with `\` (regex, grep) is where Haiku errs most: use Sonnet for those files.
- Afterwards, **verify** (count the remaining `pending` blocks, reread the tab). An agent's "ok" is not proof.

## 3. Which model for what

See the policy line above. Practical rule: Haiku only for a single call with a payload under 5 KB; copying a file of
5 to 25 KB or touching `\` (regex, grep) is Sonnet.

## 4. Task execution, cost and cross-PR breakage

The pipeline (worktree per task, gate, commit, review, acceptance, cost, cross-merge simulation, merge order) belongs
to the wave runner of the project. This skill covers only the brief and the Workflow mechanics.

## 5. Workflow mechanics (real pitfalls)

- `args` is real JSON; a string placeholder becomes a list of characters.
- **Resume loses the cache** when any earlier prompt or the order of calls changes. To skip finished work, prefer a
  new run with `args.pre = {ID: result}` and skip those tasks.
- A wave with no executable task: `continue` before integration, PR and QA (otherwise agents are spent for nothing).
- To wait for a specific agent, filter the journal by **label** (`"label":"impl F100"` plus result), never by the
  count of `result` entries (a reviewer finishing first misleads the counter).
- Cap simultaneous agents at what the machine handles; large waves take hours.
- **The run lives with the session.** If the app closes or restarts, the Workflow stops without notice. The journal
  stays in the folder of the session that launched it: only that session can `resumeFromRunId`. Rule: **one
  conductor per run**; when launching or resuming, tell the sibling sessions the run id; whoever is not the
  conductor does not resume.
- **Do not edit the script while the run is alive** if you plan to resume: any changed prompt (even the shared RULES
  or the base) invalidates the cache from that point on. Batch the changes for the next run.
- **The base of a stacked PR** is the dependency that already contains the others (the transitive closure of the
  hard dependencies), not the first one in the list. With the wrong base, the diff shows frozen files from the other
  PR and the frozen-files check fails.

## 6. Ask first

A change to repository settings, a write to the deployment platform, or creating or deleting something in the issue
tracker: ask the user right before. An issue deleted on purpose cannot be recreated; use the reference copy from the
wave report.

## 7. Fixed preamble for every brief that touches code

Paste this at the start of every implementation or fix brief, filling in the <>:

```
Task: <ID>, ticket at <path to JSON>. The ticket's file plan is what you may touch.
Rules that are not negotiable:
1. Touch only what the task asks. Do not reformat, rename, translate or "improve in passing"
   a file owned by another task (owner listed in the repo's ownership file). Needed to touch
   something outside the plan? List it in the PR body with the reason.
2. Never make the gate pass by hiding something from the sensor: no splitting a literal, no helper
   that hides a forbidden access, no rewriting a comment to lower a count, no code created only to
   silence the sensor, no colliding name to make a finding disappear.
3. Do not touch exemption lists, baselines owned by others, existing sensors, or ported-behavior
   tests (only repoint imports). If the gate requires it, STOP and report: "needs owner decision".
4. Do not delete code, tests or functionality that the ticket does not tell you to delete.
5. If a call is blocked by the classifier, or the gate does not close without violating 1-4: stop and
   report. Escalating is the right answer; forcing is not.
6. Before the push: run the full check (not only static) on the merged tree; the PR body must match
   the diff (list deviations from the ticket; do not write "does not touch src/" if it does).
7. Everything you start (container, database, kind cluster, server, background process) carries
   <ID>-<first 8 chars of the session> in its name and is torn down before the final report. The report
   lists what stayed alive and why. File searches start from the repo or the config directory; never `find /`.
```

Why item 7: sessions that end without cleanup leave unhealthy validation containers and orphaned whole-disk searches
holding system handles.

Why the rest: review of agent-written PRs found scope leaks in most open PRs, exemptions widened by the task itself,
sensor workarounds, deleted tests and false PR bodies. Research shows agents cheat on the evaluator (editing the test
almost every time); asking "do not cheat" barely changes it, while giving an escalation exit cuts it sharply.

## 8. Orchestration confusions that cost hours

- **Integration only merges.** Never fix a task's code inside the integration PR or branch. A red sensor after a
  merge sends the fix back to the PR that owns it.
- **No long-lived integration branch.** Each PR enters the target branch through the queue as soon as it is green;
  a child PR points to its OPEN parent PR or to the target branch, never to a branch already merged.
- **One conductor per run.** Two sessions resuming the same Workflow in the same worktrees is a collision. Before
  resuming: list agents and tell the siblings; only the launcher resumes. A Workflow dies with its session.
- **Resume reuses the cache only with identical prompt and args.** Editing RULES after launch re-runs everything.
  Pass the same args as the launch.
- **A DRAFT PR or one with a known failure does not enter the integration.**
- **"Applied" means the drift check ran with exit 0**, not "file written".
- **A declared trigger is a tested trigger** (push, merge queue and schedule triggers broke after merge).

## Related

- `cross-harness-orchestration`: the same pattern with children from another harness

When `cross-harness-orchestration` is unavailable, choose an available model, write a self-contained brief, isolate writers, and enforce the agreed budget directly.
