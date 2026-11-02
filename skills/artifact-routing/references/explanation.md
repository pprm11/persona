# Explanation

[Diataxis: Explanation](https://diataxis.fr/explanation/) describes understanding-oriented treatment that connects ideas and context. Applying it to any medium is this skill's adaptation. Shared building blocks are in `components.md`, writing rules in `writing.md`, vocabulary in `ubiquitous-language.md`, links in `linking.md`, figures in `diagrams.md`, the page contract in `reader-page.md`, the gates in `quality-gates.md`. A worked page is `assets/templates/explanation.html`.

## Purpose and acceptance

- **Reader's need:** to understand why something is the way it is, so they can predict it, judge it or decide about it. They are not doing a task and not looking up a fact.
- **The one question:** a bounded "why" or "why this and not that". Write it in the first sentence of In one minute. A page with two questions is two pages.
- **Acceptance check (observable):** a cold reader, after reading, (1) states the key relationship in their own words, (2) names the strongest alternative and why it loses, (3) names two limits, and (4) predicts the outcome of one new case that the page never mentions. Record the answers against a key.
- **Neighbors, and what to move out:**

| Neighbor | Signal that the content belongs there | Move it to |
|---|---|---|
| Tutorial | "Run this", a numbered learning path | Tutorial tab, link from the context section |
| How-to | A procedure, a command the reader must type to reach a goal | How-to tab, one link at the claim it supports |
| Reference | A full table of options, flags, defaults, error codes | Reference tab, link to the row, quote only the fact the argument needs |

An explanation may show a command or an output as evidence. It never asks the reader to follow along.

## When several types share one artifact

- This tab owns the reasons, the alternatives, the trade-offs, the limits, the decision record and the open questions. Nothing else in the artifact carries them.
- Link out at each claim that depends on a fact: to the Reference row for the exact option (`#def-<ID>`, see `linking.md`), to the How-to only where a limit has a remedy. Link text is the title of the target. Do not repeat the target's content.
- Other tabs link in: a how-to step with a non-obvious reason and a reference entry with a surprising default each carry one link to the claim here.
- Default tab: this one only when the occasion is a decision or a review (an RFC reader, a design review). When the reader's main job is to do or to look up, the Explanation tab comes last.
- One glossary for the whole artifact, placed here when the concepts are what the page explains, otherwise in Reference. Cards on the overview point to this tab with the as-of date or revision in the footer.
- Terms and IDs defined in this tab stay valid for every tab. Never define the same term twice.

## Skeleton

Use the RFC skeleton in `skeletons.md` for a proposal, the Decision record in `components.md` for an ADR, and the postmortem skeleton (impact first, systems not people) when the page explains an incident.

| # | Section | Status | Content | Component |
|---|---|---|---|---|
| 1 | Head: title, eyebrow, as-of line | Required | Title is a claim or the question. Line: `As of <date> · Revision N · Owner: <role>` | As of date |
| 2 | In one minute | Required | The answer, the ask, the deciding numbers, what is open and with whom. 4 to 6 sentences | In one minute |
| 3 | What changed in revision N | Conditional (revision 2 and later) | One bullet per change, naming the IDs it touches | What changed |
| 4 | Conventions | Conditional (IDs or keywords exist) | ID prefixes, keyword meaning, evidence tags | Conventions block |
| 5 | Context | Required | The forces as facts with numbers and sources, goals and non-goals with IDs (`G1`) | Stable IDs, Evidence |
| 6 | Mechanism | Required | How it works, by cause. One diagram per claim, caption first | Diagrams |
| 7 | Alternatives | Required | Table with "do nothing", the strongest alternative and the chosen path. Below it, one refutation paragraph | Table |
| 8 | Trade-offs and limits | Required | Positive and negative consequences with who is affected, accepted limits (`L1`), where the claim stops holding | Stable IDs |
| 9 | Decision record | Conditional (a choice someone will question) | Status, context, "We will", options, consequences, revisit when | Decision record |
| 10 | Decisions and open questions | Required when anything is open | Decided next to still open, owner and effect per question, copy button | Open questions, Decisions |
| 11 | Glossary | Conditional (three or more terms used in two sections) | Genus plus difference, one sentence | `ubiquitous-language.md` |
| 12 | References | Conditional | One citation system, persistent identifiers, access dates | Evidence and citations |
| 13 | Footer | Required | Scope, owner, how to report an error | none |

Order inside the page: answer, then reasons, then evidence, then open items. Headings from section 5 on state the claim ("A burst between two runs fills the disk"). Keep names such as In one minute and Glossary where readers expect them.

## Content depth

A complete explanation has all of these. Missing one is a finding.

- **Bounded question.** Stated once, with a non-scope line: what this page does not explain and where that lives.
- **Answer first.** The claim, its main reason, the number that decides, and the ask (approve, review, learn). Pending items appear here too.
- **Context as facts.** Each force has a number or an observation and a source tag. Facts and interpretation sit in separate sentences, and interpretation is labeled ("We read this as...").
- **Goals with IDs.** Each goal has a name and a way to tell it was met. Goals that conflict are said to conflict.
- **Mechanism by cause.** Every "ensures", "enables", "handles" gets the mechanism and the condition under which it fails (`writing.md`, mechanism check). Where useful, a formula with two sample inputs and the recomputation command.
- **At least one diagram** per causal claim: sequence for cause over time, flowchart for a decision or trade-off. Caption line, legend, accessible title and text version for a complex figure.
- **Alternatives.** At least: do nothing, the strongest alternative stated in the form its best advocate would use, the chosen path. Each row says what it gives, what it costs, and the observable reason it loses.
- **Refutation.** One paragraph that answers the strongest alternative on its own terms, with a mechanism or a number, and admits what the alternative does better.
- **Trade-offs.** Each consequence says who pays. Positive and negative are both present. A page with only upsides is incomplete.
- **Limits and counterexamples.** Cases where the claim stops being true, as accepted limits with IDs. At least one case where the mechanism never triggers, and one where it triggers wrongly. Run the counterexample test: invent a case the facts allow and check that no universal claim breaks.
- **Assumptions** with what changes if each is wrong.
- **Evidence.** A tag on every number and causal claim: command and output, source at a fixed version, measurement with date, or `[NOT VERIFIED: <command>]`. Sample or invented data is labeled as such on the page.
- **Decision record** when the choice is contested: status, date, decider, supersedes, "We will...", options, consequences, revisit when (an observable condition). Never renumbered; a change is a new record.
- **Open questions** with a role as owner and the effect of each answer ("If A, section 4 changes; if B, it stays").
- **Glossary and IDs.** Terms defined by genus plus difference, one sentence, same wording in popover and glossary. IDs defined once with a short name.
- **Transfer case** (optional, strong): one worked case that applies the relationship to a new input, with the answer hidden in a collapsed `<details>`. It becomes the cold-reader test.

## Writing emphasis

Follow `writing.md`. Specific to this type:
- State the claim in the first sentence of every section and paragraph; the rest supports it.
- Prose carries reasoning. Use a table only when every cell is a final answer. A bullet without a "because" belongs in prose.
- Name the strongest alternative before you refute it. Refute with a mechanism, not with an adjective.
- Never write balance without a position ("both have pros and cons"). Give the deciding criterion, or say no decision exists and who decides.
- Give each trade-off a price and a payer, in numbers where you have them. No invented numbers; label samples.
- Separate observed from inferred: "Measured: ... Inferred: ...".
- No procedure steps, no option tables, no marketing. Those are other types.
- Keep terms fixed; a variant word reads as a second concept.

## Front end for this type

- `data-reader="all"`. Why: long page read in jumps, so contents menu, scroll spy, filter, search, permalinks, popovers, back pill, figures and `copyopen` all pay off (`reader-page.md`, features table). Turn `progress` off only if the page is short.
- Set `data-id-prefixes` (for example `G,L,Q,D,ADR-`). Define each ID once on its own line with `span.defid`. The popover then shows the definition wherever the ID is mentioned.
- Glossary as `dl.glossary` with `dt.defterm`, a heavy use of popovers: link every concept the argument turns on. Add `<abbr title>` for ADR, RFC and similar on first use.
- Layout: In one minute card at the top, claim headings, tables for alternatives and consequences, callouts for the ask and for accepted limits, the asks block (Decided and Still open, copy button) near the end.
- Evidence blocks as `<pre><code>` with the copy button, labeled with the command.
- Diagrams: sequence for causality, flowchart for a decision or trade-off, one picture per claim (`diagrams.md`). Avoid a diagram that only lists settings.
- Cross-tab links are plain `#id` anchors; the back pill returns the reader to the claim they left.
- At 400 px the tables scroll inside their wrapper; keep alternatives to 4 columns.

## Evidence and gates

| Gate | Checks for an explanation |
|---|---|
| Well written | In one minute holds the answer and the ask. Each section opens with its claim. Terms defined once and used the same way. A cold reader states the key relationship and its limits in their own words. The headings test passes: from the title, first paragraph and headings a reader says what is claimed, what is asked and where the detail lives. `autolink.py --check` prints `[]` for undefined IDs and broken anchors |
| Correct | Every causal and comparative claim has a mechanism and a source. Numbers recompute from the stated inputs. The strongest alternative is stated fairly. Counterexample test finds no broken universal claim. Samples are labeled |
| Optimized | Every section serves the bounded question. No recap, no repeated summary, no option nobody would pick. The page has not turned into a procedure or a lookup list. Long reasoning becomes a table only when each cell is a final answer. Before and after word counts recorded |

Cold-reader answer key (keep it out of the page):
1. What is the question the page answers, in one sentence?
2. What is the answer, and what is the main reason?
3. What is the strongest alternative, and why does it lose?
4. Name two accepted limits.
5. What does the choice cost, and who pays?
6. Given a new case (state it), what happens, and which part of the mechanism decides it?
7. What is still open, with whom, and what changes with each answer?

Every wrong or missing answer is a finding that points to hidden context. Test facts by running the commands shown, recomputing each number, and having a second model attack each causal claim without seeing the first findings.

## Common failures

| Failure | Fix |
|---|---|
| Starts with background and buries the answer | Move the answer, ask and deciding number into In one minute |
| Lists settings while claiming to explain a cause | Show the mechanism: inputs, rule, outcome, and where it fails |
| Procedure creeps in ("first run...") | Move the steps to the How-to tab and leave one link |
| Option table copied from the reference | Keep only the fact the argument needs and link to the row |
| Straw-man alternative | State it as its best advocate would, then refute with a mechanism or number |
| Only upsides | Add consequences with a payer, and accepted limits with IDs |
| Universal claim ("always", "never") | Find the counterexample, narrow the claim, record the limit |
| Fact and opinion mixed | Label measured, inferred and assumed; add `[NOT VERIFIED: command]` |
| Invented or unsourced number | Source it, recompute it, or mark it as a sample |
| One term, two names | Pick the glossary term and apply it everywhere, diagrams and captions included |
| Balance without a position | State the deciding criterion, or name who decides and by when |
| Open question without owner or effect | Add a role and the effect of each answer |
| Decision record written after the fact | Record the options and the rejected path while the choice is open |
| Diagram without caption or legend | Caption line first, legend names every shape and color |
| Two questions in one page | Split into two tabs or two artifacts |
| Closes with a moral | Close on the next action or the open item |

## Positive and negative example

**Positive.** "Driftwood rotates when a file reaches `max_size` or when the schedule is due, whichever comes first. A time-only rule lets a file grow by the write rate times the whole schedule period; the size rule caps growth at `max_size` plus one check interval of writes. The cost is that archive names carry a timestamp, not a calendar period (L1)." Claim, mechanism, price and payer in three sentences, and each is checkable.

**Negative.** "Driftwood uses a robust, flexible rotation strategy that ensures logs stay manageable. Both approaches have pros and cons." No mechanism, no number, no position, nothing to disprove. A table of the four options with their defaults, under a heading that says "why", is the other failure: it is Reference.

## Pre-publish checklist

- [ ] The page answers one bounded question, stated in In one minute, with a non-scope line.
- [ ] In one minute has the answer, the ask, the deciding numbers and what is open with whom.
- [ ] Each section's first sentence is its claim; the headings test passes.
- [ ] Every causal claim names its mechanism and where it stops holding.
- [ ] Every number has a source tag or is labeled as a sample, and recomputes.
- [ ] The strongest alternative is stated fairly and refuted with a mechanism or number.
- [ ] Trade-offs show who pays; accepted limits have IDs; one counterexample is tested.
- [ ] Facts, inference and assumptions are labeled apart.
- [ ] Each diagram has a caption line, legend, accessible title, and only facts from the text.
- [ ] Decision record exists for the contested choice, with an observable revisit condition.
- [ ] Open questions have owner and effect; the same items appear in In one minute.
- [ ] Terms and IDs defined once; `autolink.py --check --internal-only` prints `[]` on all three lists.
- [ ] No procedure and no option table in the body; links go to the other tabs by anchor.
- [ ] Style skill run; `{{`, comment markers and `ref missing` absent; private data scan clean.
- [ ] Cold reader passed the answer key, or the untested state is stated on the page.
