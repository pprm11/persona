# Quality gates

An artifact ships only after it passes three gates. They ask different questions and need different reviewers, and one does not cover another. A page can read well and be wrong, or be right and carry parts nobody needs.

| Gate | Question | Reviewer | Evidence that counts |
|---|---|---|---|
| Well written | Can the intended reader understand, check and use it without asking? | A reviewer who applies `writing.md` (and a readability skill, if you have one), plus a cold reader (another agent with no context) holding an answer key | The cold reader's answers against the key, `preserve.py` after rewrites, a source on every number, links and IDs that resolve |
| Correct | Does it say and do what is true, including when something goes wrong? | An adversarial reviewer per area, plus a second model that has not seen the first findings | A counterexample, a re-run command, a recomputation, a test with a negative control, official documentation with URL and access date |
| Optimized | Is it the smallest piece that does the job for this reader? | A reviewer asked what can be removed, merged or shortened | Before and after measures (words, steps, clicks, nodes, time to complete), and the simpler alternative with the reason it loses |

Optimized starts with one question: does this piece need to exist, or does an existing page, tool or default already serve the reader? Only then trim.

## Finding format

One row per finding: **Id · Gate · Severity · Where · What · Evidence · Smallest fix**. The criteria each gate applies to a type are in that type's file, section "Evidence and gates".

| Field | Content |
|---|---|
| Id | `RV-3` (not `F`, which is a failure row in a how-to) |
| Gate | Well written, Correct or Optimized |
| Severity | Blocking (the reader fails or is misled), Major (the reader is slowed or may err), Minor (polish) |
| Where | file or tab, section, ID |
| What | one sentence |
| Evidence | the quote, the command and its output, the source |
| Smallest fix | the least change that removes the finding |

A conflict with an owner decision is never a fix. It becomes a question for the owner. Each reviewer closes with **Checked and passes**: what was examined and held. Without it, nobody knows what was covered.

## Pass rule

- Zero blocking findings on all three gates.
- Each major finding is fixed, or accepted by the owner as a limit with a reason (an ID such as `L4`).
- Minor findings go in a list on the page or in the hand-off.
- A fix reruns the gate of the area it touched. Rewrites run `preserve.py` again.

## Stop rule

When the number of blocking findings does not fall for 2 rounds, or two fixes built on the same premise fail the same gate, stop fixing. Write the premise in one sentence, show the counts per round, draw a cause diagram (people, method, material, tool, environment, measure) with the whys down to a proven root, and ask the owner to choose. Do not start another round before the choice. A new reviewer that finds new problems for 2 rounds in a row is the same signal.

## Running the gates with agents

- **Well written.** One agent applies the readability passes (document, paragraph, sentence, word) and your style skill (for example `humanize`, if installed). A second agent gets only the finished page and the answer key, no brief, no history. It answers the key's questions from the page alone. Every wrong or missing answer is a finding. Keep the key out of the page so it cannot leak.
- **Complete** (part of Correct). One reviewer walks each tab through its type's Content depth list and Pre-publish checklist, item by item, and marks Present, Partial or Missing with a quote. A Missing item the reader needs is Blocking. Diagrams go through `diagrams.md` the same way. A cold reader and an adversarial reviewer both pass a page that is right but thin, so this check is not optional.
- **Correct.** One adversarial reviewer per area (for a page: facts and numbers, commands and examples, links and IDs, claims about behavior). Tell each to try to break the page, not to approve it. Run a second model on the same scope without showing it the first findings. Merge into one table.
- **Optimized.** One reviewer asks first whether the piece needs to exist, then what can be cut, merged or moved to a place that already exists. It measures before and after.
- Run the three in parallel with explicit models: cheap for mechanical checks, mid for reading and writing, top for judgment.
- An agent report is data. Open the diff, run the scripts and the page, and check any "I removed X" claim with a search on the original.

## Testing a skill or template

A skill or template is tested like code, in fresh sessions.
1. Write 2 or more seeds, each a realistic request with its context and a hidden answer key. Give each fresh session only its seed, never the key or earlier output.
2. Score every output against a rubric of about 10 criteria with points, for example type fit, content contract, evidence, IDs, rendering, accessibility, hygiene. Set the pass line before running.
3. Read the lowest criteria, change the skill for those, rerun the same seeds and compare totals. A rise on one seed with a fall on another is a regression.
4. Stop by the stop rule above. Keep seeds and scores with the skill so the next change can be compared.
