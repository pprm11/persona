# Tutorial

[Diataxis: Tutorials](https://diataxis.fr/tutorials/) defines a learning-oriented experience through guided practice. Applying it to any medium is this skill's adaptation. Shared building blocks are in `components.md`; the worked example is `assets/templates/tutorial.html`.

## 1. Purpose and acceptance

- **Reader's need:** to learn a skill by doing it once, with someone else in charge of the path. The reader does not yet know what to ask.
- **The one question the page answers:** "Can I do this, and what does it look like when it works?"
- **Promise:** one outcome, stated before step 1, reached in a safe place the reader can throw away (a sandbox: a scratch folder, a test account, a fixture file).
- **Acceptance check (observable):** a learner who follows the steps in order, without skipping, reaches the promised outcome, sees the stated output after every action, and then repeats the skill on a small novel case without the page.
- **Evidence:** every expected output comes from a run in a clean environment, or the step carries `[UNTESTED]`. A walkthrough by an agent or a script shows the path works. Only a real learner shows that learning happened. Never claim the second from the first.

| If the reader wants to... | It is not a tutorial. Move it to |
|---|---|
| Get a real task done on their own data | How-to guide: link at the end |
| Look up a flag, default or error code | Reference: link at the step, never copy the table in |
| Know why the tool works this way | Explanation: one link at most, after the learner has seen it work |
| Choose between several ways | How-to or Explanation. A tutorial has one path |

## 2. When several types share one artifact

- This tab owns the guided path, its sandbox and its checkpoints. It owns no option tables, no decision logic and no rationale.
- It is the **default tab** for a first-time reader who must learn a skill: a newcomer to the tool, a product launch. Make the How-to tab the default when the reader's main job is a task such as installing or configuring, or when most visitors already know the product. An onboarding page whose job is to get the tool installed opens on the How-to; installation is never a Tutorial.
- Link from each step to the exact Reference entry of the option or command it uses (`#def-CFG2`, the anchor convention in `linking.md`), not to the Reference tab as a whole. Link to the How-to tab for the real-world version of the task, and for installation when a prerequisite is missing. Link to an Explanation entry only after the outcome is reached.
- A step that needs a paragraph of theory is a sign the paragraph belongs in Explanation. Replace it with one sentence and a link.
- Tab label: the outcome or the word Tutorial, matching the exact spelling used in the other tabs (see `ubiquitous-language.md`).

## 3. Skeleton

Builds on the quickstart skeleton in `skeletons.md` (what it is, shortest path to a working result with commands and expected output, links onward) and adds guided practice.

| # | Section | Status | What goes in it | Component |
|---|---|---|---|---|
| 1 | Title, eyebrow | Required | Outcome as a 2 to 4 word title. Eyebrow: product, version, type | shell header |
| 2 | In one minute | Required | 4 to 6 sentences: what the learner will have at the end, what is needed first, what is touched (only the sandbox), time if measured | In one minute |
| 3 | As-of line | Required | Date, product version, systems the steps were last run on. "Never run" if so | As of date |
| 4 | Before you start | Required | Prerequisites as a table: item, version, check command, expected output. A statement of what the tutorial does not touch. A link to the how-to for a missing prerequisite | Success check |
| 5 | What you will do | Conditional (six or more steps) | One line per step with a step ID, so other tabs and failure rows can cite "step S3" | Stable IDs |
| 6 | Steps | Required | Numbered list. Per step: verb heading, "Changes:" line, one action, the reason in one sentence, "You should see", a one-line recovery. Warning box before any real side effect | steps, Success check |
| 7 | Checkpoint figure | Conditional | A small diagram of the state after a key step, with caption and legend | Diagrams |
| 8 | What you learned | Required | 3 to 5 sentences naming the skills, each tied to the step where it happened. No new facts | none |
| 9 | Try it yourself | Conditional | One novel case that reuses the skill, with the expected result to compare. Not a second tutorial | Success check |
| 10 | Clean up | Required when files, accounts or processes remain | Warning, command, check that it is gone | Warning box |
| 11 | If something goes wrong | Required | Failure table keyed by exact message | Failure table |
| 12 | Where to go next | Required | Links to How-to (real task), Reference (exact entries), Explanation (why). Link text is the destination title | `linking.md` |
| 13 | Terms | Conditional | Glossary of terms first met here, so popovers work | Glossary |

Order matters: the outcome and the sandbox rule come before step 1. Do not add an overview of the sections, a recap of the steps or a "key takeaways" box.

## 4. Content depth

A complete tutorial contains all of these. Missing items are the usual reason a page feels thin.

- **Outcome sentence** in the title or first line: what exists at the end that did not exist at the start (an archive, a deployed page, a passing test).
- **Audience line:** who it is for and what they are assumed to know, once.
- **Prerequisites with versions** and a command that proves each one, with its exact output. Include operating system and shell.
- **Sandbox statement:** the one folder, account or dataset the steps touch, and that nothing else changes. Provide the sample data inline or with a command that creates it. Never require the reader's real data.
- **Per-OS blocks** when a command differs (shell, path separator, quoting). Label each block. A command identical everywhere appears once.
- **One action per step.** A step with two commands needs two checks, so split it.
- **Reason in one sentence** per step, only if the reader could not guess it. Never a paragraph.
- **"Changes:" line** per step: what the step creates, edits or deletes. It tells the reader which steps are safe to repeat.
- **Expected output after every action,** copied from a real run, with the variable parts named ("your sizes differ by a few bytes; the names and their order matter").
- **Warning before any step with a real side effect:** deleting, overwriting, sending, spending, writing outside the sandbox. State what it does, then the command. The condition comes before the command.
- **A recovery line** next to each step that can fail, then the failure table for the rest.
- **Checkpoint figure** after the step where the state is hardest to picture.
- **Reversal:** at least one step shows the learner can undo what they did. It builds confidence to try on real data.
- **Clean up** steps that remove what the tutorial created, with a check.
- **What you learned:** the skills, not the steps.
- **Transfer case:** a small task with a known answer that the learner can do without the page.
- **Versioned and dated:** product version, date, systems tested. Untested steps are tagged `[UNTESTED]` with the check that would test them.
- **Safe values:** placeholders in capitals, secrets read from the environment, no real names or data in samples (see Privacy in `components.md`).

## 5. Writing emphasis

Use `writing.md` for everything general. Specific to a tutorial:

- Second person, imperative, present tense: "Run `driftwood init`." "You now have a config file." Use "we" only for work done together.
- Promise one outcome. Do not list features, offer choices or say "you can also".
- Name each step by what it achieves, with a verb: "Create the sandbox", not "Setup".
- Tell the reader what to expect before they act when the result could surprise them, and what they should see after.
- Teach by showing. Defer definitions to a popover and reasons to a link; a tutorial that explains is a lecture.
- Choose the plain default at every fork and say nothing of the alternatives.
- Keep the tone steady and reassuring. When something fails, say what the message means and what to do next, never "just" or "simply".
- Use the same names for files, folders and commands from the first mention to the last (`ubiquitous-language.md`).

## 6. Front end for this type

| Choice | Setting and reason |
|---|---|
| Reader features | `data-reader="all"`. Keep **progress** on: the learner sees how far they are. Keep **codecopy** on: commands are pasted. Keep **popover** and **autolink** for terms and step IDs. **search** and **filter** stay on but matter little |
| Layout | One narrow column. Contents menu lists the sections and the steps (each step heading has an `id`). Numbered steps with `ol.steps` |
| Tabs | The Tutorial tab first when the reader is new. The bar scrolls sideways at 400 px |
| Code | One `pre` per command or per output, never a command and its output in one block. Label OS blocks with a short line above |
| Success check | A line "You should see:" in the success style, followed by the output block |
| Warning | `callout callout--warn` with a visible label word "Warning", placed immediately before the risky command |
| Failure table | A plain table, keyed by exact message in code font |
| Diagrams (`diagrams.md`) | A small flowchart of the state after a step. Caption first, legend by shape and color, text version in `details.figtext`. No architecture overviews |
| IDs | Step IDs (`S1`...) for cross-tab and failure-table citations. `data-id-prefixes="S"`, plus the Reference prefixes (`CMD,CFG`) when the page carries the rows the steps link to |
| Glossary | Three to six terms as a definition list (`ubiquitous-language.md`), with lowercase `data-aliases` so running text links |
| Not used | Open questions, decisions, cards |

## 7. Evidence and gates

The three gates are defined in `quality-gates.md`; this is what each checks here.

| Gate | Checks for a tutorial |
|---|---|
| Well written | Outcome and sandbox rule appear before step 1. One action and one success check per step. Prerequisites listed once. Headings are verbs. A cold reader states what they will have built |
| Correct | Every step was run in a clean environment on each OS shown, in order, and the output matches. Versions are pinned and dated. Untested steps are tagged. The failure rows were produced by breaking the step on purpose |
| Optimized | Each step is needed for the outcome. No choices, digressions or theory. Count steps against the shortest working path and cut repeats of a skill already shown. Measure time to finish with a new learner when possible |

**Cold-reader answer key** (the reader gets only the page):
1. What will you have at the end?
2. Which folder do the commands touch, and does anything outside it change?
3. What do you need installed before step 1, and how do you check it?
4. After the config step, which file exists and what is in it?
5. Which step changes data, and what warns you?
6. You see the first error message in the failure table. What do you do?
7. How do you undo what the run did?
8. Where do you go to do this on your own files?

**Testing the path**
- Run it in a fresh container or user account per OS. Paste each block exactly as written, in order, and diff the output against the page.
- Run a negative control: skip one step, confirm the failure row quotes the message you actually get.
- Automate it: extract the code blocks and expected outputs, run them in CI, fail on a diff.
- Watch one real learner who did not write it. Record where they stop. Label a scripted run "simulated" in the hand-off.

## 8. Common failures with the fix

| Failure | Fix |
|---|---|
| Explains concepts between steps | Move to Explanation, leave one sentence and a link |
| Offers options ("you can also...") | Pick the default, delete the rest, link to How-to |
| Step without expected output | Add "You should see" with real output |
| Output invented, not from a run | Run it in a clean environment, paste the output, or tag `[UNTESTED]` |
| Works only on the author's machine | State OS, versions and shell, add per-OS blocks, run on a clean machine |
| Real side effect without warning | Add a Warning box before the command, with what it does and how to undo it |
| Needs the reader's real data | Supply sample data or a command that creates it |
| Two actions in one step | Split, one check each |
| Prerequisite hidden in step 4 | Move to Before you start with a check command |
| Ends with no sign of success | Add the final check and "What you learned" |
| Lecture on the reference table | Link to the exact entry instead |
| Recap of the steps at the end | Replace with skills learned, tied to steps |
| Leaves files behind | Add Clean up with a warning and a check |
| Copies a reference table | Delete, link to the entry |

## 9. Positive and negative example

**Positive:** "In this tutorial you rotate a log file in a scratch folder. You finish with a compressed archive and a config file. Step 1 creates the folder. You should see `app.log`." The outcome is named, the folder is safe, each action has a visible result.

**Negative:** "Driftwood supports four options: `keep`, `compress`, `max_size` and `schedule`. Choose the ones that suit your setup, then run it against your logs." This is a reference list with no path, no check and a risk to real files.

## 10. Pre-publish checklist

- [ ] The title names one outcome, and the first block says what exists at the end.
- [ ] The sandbox is stated, and no step writes outside it.
- [ ] Prerequisites have versions, a check command and expected output.
- [ ] Every action has one step and one "You should see" with real output.
- [ ] Commands that differ by OS have labeled blocks; all were run on each OS.
- [ ] A Warning box precedes every step with a real side effect.
- [ ] Each step that can fail has a recovery line; the failure table is keyed by exact message.
- [ ] Untested steps carry `[UNTESTED]`; the as-of line says which version and systems were run.
- [ ] Each option or command links to its exact Reference entry; the How-to link is present.
- [ ] No theory between steps, no alternatives, no recap of the steps.
- [ ] "What you learned" lists skills; a novel case is offered or the reason is stated.
- [ ] Clean up exists when anything remains.
- [ ] No secrets, personal data or machine paths in commands or outputs.
- [ ] `scripts/autolink.py --check --internal-only` reports `[]` on all three lines; inline scripts pass `node --check`.
- [ ] Looked at once in light, dark and at 400 px.
