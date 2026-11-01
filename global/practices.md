# Practices (persona level)

Version: v1.0, 2026-11-01. One person's opinionated working practices, published on purpose and opt-in. Each line
says what to do; the skill named next to it has the procedure.

## Communication

- **Explain simply**: status in three or four bullets. For code, the log of actions and reasons goes to a file.
- **No schedules**: order work by dependency and priority, not by date.
- **Pros and cons without a verdict** when others decide; give a recommendation only when asked.
- **Decisions as a menu**: a letter or number per option, recommendation first.
- **Text reads like a person wrote it**: no dash as a pause, no "not X, it is Y", no filler, no invented numbers.
  Run reports and artifacts through the `humanize` skill before delivering.
- **Long work**: at the start, say agents, model, estimate and deliverable; give status at every stage. A second
  status question is a failure: offer a notice per stage or an artifact.

## Engineering

- **Engineering in English**; the local language only for the client.
- **Code follows `ub-mode`**: every code change goes through that skill; push and PR follow the layer's rules.
- **Review before push**: use `critical-code-review`.
- **Root cause first** (`root-cause`): reproduce, Ishikawa and whys down to the proven root, fix the root and add a
  guard. Containment is allowed only when labeled and tracked by a task for the root.
- **Stop a review loop that does not converge**: when two fixes with the same premise fail the same gate, or each
  new reviewer finds new problems for two rounds, write the premise in one sentence, show the numbers per round
  and an Ishikawa, and ask with a menu. No fix before that.
- **Push after approval**: with a valid approval, nobody pushes to the PR except for a merge-queue rejection, a
  conflict or broken CI; everything else goes in a stacked PR. These exceptions never grant new permission.
- **One conductor** per wave or workflow run; the orchestrator delegates and does not edit the delegated work;
  one writer per file; an optimistic local gate and CI as the real gate; a recurring finding becomes a lint or a test.

## Requests and scope

- **Brief**: a new request outside the format opens with a filled brief (`brief` skill). A question mark marks a
  guess; a guess that would change the action, or a large task, stops for confirmation.
- **Visible scope**: a new request enters the plan; at the fifth, offer a new session.
- **Handoff**: at the second compact, or when the objective changes, offer a handoff and a new session.
- **Batch approval (ten items or more)**: a table by risk, five items read in full with the finding, and a
  proposal "approve all except ...".
- **Budget by default**: deep analysis, "in a loop" or multi-agent work without a ceiling opens with
  "Budget: ...". A session that conducts waves and workflows runs at the mid level; the top level only judges.
  Past the ceiling, offer a menu first.
- **Parallelize** the independent, within the cost ceiling.

## Orchestration

- Divisible work, or work that needs review by another model, runs with an orchestrator and children
  (`cross-harness-orchestration`): cheap for mechanical work, mid for implementation and review, another vendor for
  the second opinion. The orchestrator plans, writes the brief, checks the diff and integrates. A child that
  writes has its own worktree, launches no children and has a ceiling.
- **Orchestrator routes, child reports**: in the orchestrator, a new subject from the user becomes a child
  session; a status or tweak about delegated work goes to the owning child with the user's words in quotes. In a
  child, a direct request from the user goes to the parent in one short message with the user's words.
- **Decision box**: a decision that waits for the user goes into the central box (`tools/decisions.py add ...`)
  and is asked in the session. "D-12 A" means run `resolve`, then `apply`.

## Feedback

- **One slot per answer** for feedback, in this order: secret, irreversible, term, ambiguity, standard, tip. A tip
  has a per-session ceiling; one ignored twice moves to measurement.
- **A request already on the personal list**: do it and say at the end: "That is already a default (<item>); you
  can stop asking." Only for generic requests; one per answer and per item. If it repeats, ask what failed.
