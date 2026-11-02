# How-to guide

[Diataxis: How-to guides](https://diataxis.fr/how-to-guides/) describes goal-oriented guidance for a real task. Applying it to any medium is this skill's adaptation. Worked example: `assets/templates/how-to.html`.

## Purpose and acceptance

- **Reader.** Someone who knows the basics and has a real task now. They skim for the step they are on, copy commands and come back after an interruption.
- **Question the page answers.** "How do I reach this goal from this starting state?" One goal per guide, named in the title with the starting condition ("Rotate and compress one app's logs with Driftwood on Linux, macOS or Windows").
- **Acceptance check.** A reader with the stated prerequisites, who follows the steps in order, reaches the "done when" state, sees the expected output at each step, and can undo the change or was warned before the irreversible step. Test it by running the path in a clean environment (see Evidence and gates).
- **Not a tutorial.** A tutorial teaches a skill in a safe sandbox and may take detours. A how-to assumes competence and has no detours. Move "what is a rotation" to Explanation or the glossary, and "what you learned" out.
- **Not a reference.** Do not list every option. Show the options this task needs, with the value to use, and link to the reference entry for the rest.
- **Not an explanation.** Do not justify design choices between steps. Give a reason only when the step looks wrong without it, in one sentence, with at most one link.

## When several types share one artifact

- The how-to tab owns: goal, prerequisites, ordered steps, verify, failures, rerun safety, rollback.
- It links out, never in-line: to the Tutorial for a reader who lacks the skill, to a Reference entry for each option or message it names, to an Explanation for a non-obvious reason. Use in-page anchors on the exact entry (`#def-CFG2`, the anchor convention in `linking.md`), never on the tab as a whole.
- Reference entries link back to the how-to that uses them.
- Default tab: this one, when the artifact serves operators or people with a task to finish. A first-time reader of a product gets the Tutorial first. Keep the tab order Tutorial, How-to, Reference, Explanation.
- A page that holds only a how-to drops the tab bar and the cards and keeps the sections below.

## Skeleton

Builds on the runbook and install-guide skeletons in `skeletons.md`: right-runbook check first, mitigate before investigate, one checkable action per step, recovery notes next to the step that can fail, explicit ending.

| # | Section | Status | What goes in it | Component |
|---|---|---|---|---|
| 1 | Title, eyebrow, as-of line | required | Task and starting condition in the title. Version and OS covered in the eyebrow. `As of <date> · Revision N · Tested on <versions and systems>` | As of date |
| 2 | In one minute | required | What the reader has at the end, what they need before, how long it takes if measured | In one minute |
| 3 | Pending notice | conditional | One line per untested or unfinished part: `Pending: <what>. Owner: <role>. Needed for: <step>.` | Pending notice |
| 4 | Goal and done when | required | The goal in one sentence. Done when: one observable state, with the command that shows it | Success check |
| 5 | Before you start | required | Table: requirement, exact version or permission, how to check, expected output. Include access rights, free disk, a backup of what the task changes | Table, Success check |
| 6 | Which path applies | conditional | Only when the task branches on a real state. Decision flowchart or decision table, with the step each branch enters | Figure with caption and legend |
| 7 | Steps | required | Numbered, imperative, one action each, condition before any destructive action. Each step: the command per OS, `You should see:` with exact output, a one-line recovery note when it can fail | Steps, copy buttons, Success check |
| 8 | Verify | required | Independent check that the goal is met, not the output of the last step repeated | Success check |
| 9 | If something fails | required | Failure table keyed by the exact message | Failure table |
| 10 | Run it again | required for any step that changes state | Per step: safe to repeat or not, what happens | Table |
| 11 | Undo | required when any step is reversible, and a stated "cannot be undone" when not | Rollback in reverse order, with the check that proves it worked. Uninstall or cleanup | Steps, Success check |
| 12 | Related | conditional | Links to the Reference entries, the Explanation and the next how-to. One line each | Cross-tab links |
| 13 | Glossary | conditional | Terms used in two or more sections, as a definition list | Glossary table |
| 14 | Footer | required | Scope, owner role, how to report a wrong step | Footer |

Order rule: prerequisites before step 1, undo after verify, failure table after the steps. Never put background before the steps.

## Content depth

A complete how-to holds every item below. A missing item is a finding in the Correct gate.

**Start**
- Title names the task and the starting condition. Goal in one sentence. A "done when" that is observable (a command and its output, a file, a status), never "you are finished".
- Prerequisites with versions, each with the command that checks it and the output it prints. Name permissions (user, group, admin shell), network access, free disk and time.
- The state the reader changes, named before step 1: which files, which services, what is overwritten.
- A backup step or a dry run first, when the task changes data.

**Steps**
- One action per step. Imperative verb first. Condition before the destructive action ("If `driftwood check` prints `ok`, run ...").
- Commands run as pasted. Placeholders in capitals, explained under the block. Secrets come from the environment, never printed (`components.md`, Privacy).
- A command block per supported OS (Linux, macOS, Windows PowerShell), labeled, same step numbers, same result. Say once which shell the blocks assume. Note path, quoting and permission differences in the block, not in prose.
- `You should see:` after each step, with the exact output or visible state. Redact paths and users that are not part of the lesson.
- A step the reader cannot verify gets a way to verify it.
- A recovery note beside any step with a common failure, pointing to the failure table row by ID.
- Time-consuming or blocking steps carry the wait ("takes up to 2 min").
- No theory between steps. A reason in one sentence, or a link.

**Verify and fail**
- Verify uses a different observation from the last step (read the state, not the command's own success line).
- Failure table rows keyed by the exact message, in code font, as the tool prints it, one row per message. Columns: Id, You see, Cause, Do this. "Do this" is a command or a concrete action and names the step to repeat.
- Include the failures of the environment (permission, missing file, lock, disk full), not only of the tool.
- Include "no error but nothing happened" cases when they exist, keyed by the symptom.

**Safety**
- Rerun safety: for each state-changing step, whether a second run is harmless, a no-op or harmful, and what it prints.
- Rollback or uninstall in reverse order, with its own check. A step that cannot be undone is flagged before it, in a warning callout, with the backup that covers it.
- Stop conditions: "If the output differs, stop and go to the failure table. Do not continue."
- Side effects named: services restarted, files deleted, data sent.

**Truth**
- `As of <date>`, the version tested, the systems tested. Steps that were not run carry `[UNTESTED]` and a pending notice with an owner.
- A source for each version-dependent fact: the release note or the reference entry, linked inside the document.
- A branch only for states that exist. Alternatives come after the main path, as a table, not as nested prose.

## Writing emphasis

Follow `writing.md`; the points below are specific to this type.
- Imperative, second person implied. "Run `driftwood check`." Not "You might want to run".
- Verb phrases in headings for the task ("Create the config"); noun phrases for sections ("Before you start").
- Use "must" for a hard requirement and "can" for an option. Avoid "should" in steps.
- Name the object each time ("the config file", then `driftwood.toml` in code). One term per concept; use the glossary term, not a synonym.
- Numbers with units ("50 MB", "7 files", "30 s"). No "a few", no "quickly".
- Put the reason after the instruction, never before. One link per step at most.
- Cut every sentence a reader in a hurry would skip and lose nothing.

## Front end for this type

| Choice | Value | Why |
|---|---|---|
| `data-reader` | `all`, and `all -spy` if the page has fewer than 5 headings | Back pill returns the reader to the step after a jump to a failure row or a term. Code copy is the main aid. Progress bar shows how far into the procedure they are |
| Layout | Single column, contents menu, `ol.steps` for the steps, `callout--warn` for destructive steps, `callout` for pending notices | Numbered circles let the reader find their place; the menu helps the return after an interruption |
| Code | One `pre > code` per command group per OS, copy button on. One command per line when the reader runs them in sequence | Copy gives them the text without prompts. Leave `$` and `>` out of the block |
| Output | A second `pre` right after, labeled by the line `You should see:` in a paragraph | The reader compares by eye |
| Tables | Prerequisites, failure table, rerun safety, glossary. Row IDs in the first column for the failure table (`F1`) | Permalinks, search and popovers find a failure by its ID or message |
| IDs | `data-id-prefixes="F"` for failures; add `S` for steps only when other documents cite them | Failure rows are cited from steps; steps are cited rarely |
| Popovers | Glossary terms used in two or more sections, and abbreviations at first use | The reader does not leave the step to learn a word |
| Figures | One decision flowchart when the task branches; one sequence across tools when several programs take part. Caption phrased as the question it answers (`diagrams.md`) | Orientation, not explanation |
| Pending notice | `callout` under the as-of line, mirrored in the step | Visible before the reader starts |
| Print | All tabs print with their names; keep each command on one line where it fits | Operators print runbooks |

Diagram kinds from `diagrams.md`: decision flowchart, sequence of steps across tools. Avoid diagrams that explain why.

## Evidence and gates

Gates are defined in `quality-gates.md`. For a how-to:

| Gate | Checks | Evidence |
|---|---|---|
| Well written | Title names task and start. Steps are imperative and ordered, with conditions before destructive actions. Failure table keyed by exact messages. Prerequisites listed once | Cold reader with the key. Headings test. `autolink.py --check` prints `[]` |
| Correct | Commands run as pasted, output matches. Branches match real states. Permissions and side effects named. Rollback works, or stop conditions exist where an action cannot be undone | Run the path on a clean machine per OS. Run each failure on purpose and compare the message. Run rollback and the verify step. Record the date and versions |
| Optimized | One path first. No theory between steps. Every step is needed | Count steps against the shortest working path. Remove steps the tool already does |

Cold-reader answer key for this type (the reader has only the page):
1. What is the goal, and how do you know you reached it?
2. What must be true before step 1, and how do you check each condition?
3. Which step changes data, and what covers you if it goes wrong?
4. A message appears that is not in the steps: where do you look, and what does the row tell you?
5. You ran step 5 twice by mistake: what happened?
6. How do you undo everything, and how do you check?

Testing the path: use a clean container or a fresh user per OS, paste each block unedited, save the output, diff it against the expected output on the page. Provoke each failure row (remove the file, drop the permission) and read the real message. Mark any step you could not run with `[UNTESTED]` and a pending notice.

## Common failures

| Failure | Fix |
|---|---|
| Starts with background or history | Move it to Explanation. First line is the goal and the starting state |
| Several goals in one guide | Split into guides, one goal each, linked |
| Steps hide decisions ("choose an appropriate value") | Give the value for this task, link the reference entry for other values |
| Command needs editing before it runs | Use capitals placeholders and explain them under the block, or use a safe sample path |
| No expected output | Add `You should see:` after every step, with the real output |
| Destructive step before its condition or backup | Move the condition and the backup before the step; add a warning callout |
| Failure table keyed by cause ("permissions problem") | Key by the exact message the tool prints, so a search for the message lands on the row |
| Only the tool's failures, not the environment's | Add permission, missing path, lock, disk space, wrong shell rows |
| No rollback, or rollback never run | Write it, run it, record the check. If impossible, say it before the step |
| Rerun behavior unknown | Run each step twice and write the result in the rerun table |
| OS commands differ in outcome | Test each OS block and align the expected output, or label the difference |
| Theory between steps | One sentence and a link, or cut |
| Versions missing or stale | Pin the tested version and the as-of date; review at each release |
| Verify repeats the last output | Observe the state another way (list the files, read the status) |
| Untested step looks like a tested one | Mark `[UNTESTED]` and add a pending notice with an owner |

## Positive and negative example

Positive: a task named "Rotate and compress one app's logs with Driftwood 2.4.0". It lists `driftwood --version` printing `driftwood 2.4.0`, a block per OS, `You should see:` after each step, a failure table with `error: config not found` and `error: permission denied on /var/log/app` as keys, a rerun table saying `driftwood run` twice in one period prints `nothing to rotate`, and `driftwood restore` as the rollback with its check.

Negative: a page titled "Log rotation" that opens with the history of log files, says "configure Driftwood appropriately", shows no output, lists errors by category ("permission issues") and has no way back. The reader cannot tell whether the task finished or how to undo it.

## Pre-publish checklist

- [ ] The title names one task and its starting condition.
- [ ] "Done when" is observable and has its command.
- [ ] In one minute states outcome, prerequisites and time (measured, or omitted).
- [ ] Every prerequisite has a version, a check command and the expected output.
- [ ] Every step has one action, a block per supported OS and `You should see:`.
- [ ] Every condition and backup comes before the step that needs it.
- [ ] Commands ran as pasted on each OS; date and versions recorded in the as-of line.
- [ ] The failure table is keyed by exact messages and each row was provoked.
- [ ] Rerun safety is written for every state-changing step.
- [ ] Rollback exists, was run and has a check; or the irreversible step is flagged.
- [ ] Untested steps carry `[UNTESTED]` and a pending notice with an owner.
- [ ] No theory between steps; reasons are one sentence with one link at most.
- [ ] Links point to exact entries inside the document; `autolink.py --check --internal-only` prints `[]`.
- [ ] No secret printed by a command; privacy scan clean.
- [ ] Style skill run on the prose; code blocks untouched; `{{` and comments gone from the page.
