---
name: staged-engineering
level: persona
description: "Drive a traceable six-stage engineering design series: problem domain and as-is, market study, solution domain, HLA with ADRs, then HLD. Use for RFC to HLA to HLD work, a design series with traceability, or cascading revisions when an earlier stage changes."
---

# Staged engineering

A design series answers one engineering question (for example, "where should the new notification service run?") in 6 chained documents. Each stage decides only what the previous one allows. The problem domain is the source, and a change to it forces you to re-derive every later stage. The template for each stage is in `references/`.

Terms: **stage** (one document of the series), **source** (the previous stage plus the team decisions), **team decision** (an owner's answer, with a date), **Q#** open question, **D#/ADR-#** decision, **trace** (a table: source item, stage element, status).

This skill covers the connected design series and its traceability. If your organization has its own procedure for this, follow that and use this one as the generic fallback, or when the user asks for it. Keep any safety and authorization rules that apply. For a single team RFC, use your RFC skill if you have one. When an RFC is one stage of a series, use both and keep the stage contract.

This skill owns the genre: which documents the series has and what each must contain. For writing, building and checking each document (type per part, reader page, linking, diagrams, the three gates), use an `artifact-routing` skill (writing, page build and check scripts; not bundled here, bring your own): pass it this skill's stage brief and return its routing line. Do not call it back from there.

## The 6 stages

| # | Stage | Answers | Template |
|---|---|---|---|
| 1 | Problem domain (RFC) | What must be true, for whom, under which rules (BR#), requirements (R#), quality scenarios (QS#) and acceptance checks (AC#) | `references/1-problem-domain.md` |
| 2 | As-is | Where each piece runs today; what is LIVE, STALE, ABSENT or NOT VERIFIED, with proof | `references/2-as-is.md` |
| 3 | Market study | Prior art, public practices and benchmarks: adopted, adapted or rejected | `references/3-market-study.md` |
| 4 | Solution domain (RFC) | Contexts, aggregates, invariants (I#), commands, policies and placement | `references/4-solution-domain.md` |
| 5 | HLA | Containers, runtime views, deployment, observability, 1-3-1 cost and ADRs | `references/5-hla.md` |
| 6 | HLD | Routes, data items, algorithms, sequences, failure modes, rollout, tests, technology and POCs | `references/6-hld.md` |

The series README holds the index, the decisions, the open questions with owners, the accepted limits (L#) and the revision history.

## Three gates: well written, correct, optimized

Every stage, including the test plan (stage 7), passes three gates before it closes. Each gate has its own reviewers and evidence:

- **Well written**: a cold reader understands, checks and decides.
- **Correct**: it does what is needed, including when something fails. Evidence: a counterexample, a recalculation, a POC with a negative control, official documentation, a second opinion from another model.
- **Optimized**: the simplest and cheapest way that gives the same guarantees, with the numbers before and after.

`artifact-routing` runs the gates; the stage-specific criteria, the pass rule and how to run them with several agents are in `references/quality-gates.md`. The brief for the correctness gate is in `references/correctness-brief.md`.

## Rules that apply in every stage

They are in `references/cross-cutting.md`. The ones that broke most often in the original series:

1. **Everything in English**, including tables, page cards and labels. Use another language only when talking to the user.
2. **Team decisions do not change.** They live in a decisions file (`decisions-rN.md`, one line per decision, with date and effect on the series). A conflict becomes a Q# with an owner. If the user decides something in the conversation, write it to the file at once: an agent that reads the old file will undo the decision.
3. **No private conversation in a public link.** Write "Team decision, DD/MM/YYYY". No "Person X said", no chat link, no direct message. A person's name appears only as the owner of a question or a component.
4. **A source for every number and claim**: file and line at a commit, a command, or a dated link. Without a source it becomes a Q#, an A# (assumption) or a P# (proposed value, owner confirms).
   - An owner's answer that contradicts a cited source or the code: apply the decision, open a Q# for the conflict and carry both numbers until it is answered.
   - A conditional decision ("in process if <= 50 ms, otherwise a managed service"): record the condition in the D#, choose by the measured value, and without a measurement treat the chosen branch as a P# with the POC that decides.
   - ID prefixes: BR, R, QS, AC, G, N (non-goal), A (assumption), Q, D, I (invariant), POL (policy), ADR, C (constraint), K (risk), L (accepted limit), AS (as-is constraint), NV (NOT VERIFIED), ALG (algorithm), P (proposed value), TS (test set), POC, DR (as-is drift).
5. **Code with hash and line**: cite `path:lines` read at a fixed commit, never a branch, and turn each citation into a link with the `artifact-routing` script `permalinks.py` (`--sha` is the commit you actually read; `--show` prints every cited line so you confirm it says what the text claims).
6. **Stable IDs**: a new item takes the next number. A removed item stays as "Removed in revision N: <reason>". Every document opens with "In one minute" and "What changed in revision N".
7. **Never real personal data**: a phone number, national ID or customer e-mail becomes synthetic in the same format. Run the `artifact-routing` script `privacy_scan.py` on the document and on the published page. A verification command never prints a secret: use `kubectl get secret <n> -o jsonpath='{.data}' | jq 'keys'` or `env | cut -d= -f1`, never the value.
8. **Readability**: follow `artifact-routing` (writing rules and the `preserve.py` check that no number, ID, tag or code changed in a rewrite).

## Flow to create a stage

1. **Read the whole source**: the previous stages, the decisions file and the code at the cited commit. For the as-is, read only from the systems (no deploy, no new resource, no config change, no secret printed).
2. **Build the trace** (`trace-<stage>.md`): each source item the stage must answer, the element that answers it, and a status: covered, stale, missing, contradicts or orphan. A stage without a trace is not ready.
3. **Write from the stage template** in `references/`. When other people decide, give neutral pros and cons. When the user asks for a decision, give a 1-3-1 with a recommendation and the reason.
4. **Questions for owners**: list the Q# that only one person can answer, with the owner and what changes with each answer. When the answer arrives, write it to the decisions file and apply it as "Team decision, date".
5. **POC when a decision depends on an unproven concept** (stage 6): each POC tests one concept with a pass criterion and runs locally with mocks (moto, respx, k6). The result goes into the HLD with the measured number and what stayed open.
6. **Self-check before closing the stage** (each item with its evidence in `trace-<stage>.md`):
   - every number has a source (file and line at a commit, a dated price list, a team decision) or is marked as a proposal (`P#: proposed value, owner to confirm`); a "series target" without a source does not count;
   - every cited `path:lines` was re-read with `git show <sha>:<path> | sed -n '<a>,<b>p'` and the excerpt says what the text claims;
   - every POC has a negative control that fails without the protection under test;
   - the cost covers the topology of the Deployment section, line by line;
   - no cited command prints a secret value.
7. **Verify** with the `artifact-routing` checks (`preserve.py` if the text was rewritten, `permalinks.py --check`, `privacy_scan.py`, and the page build with no broken anchor and no ID without a definition). The build runs locally even when publishing is not allowed.
8. **Publish** (only with the user's word, or when they asked for an artifact): one page with the stages in order, built by `artifact-routing` (`reader-page.md`). The series supplies the order, the stage cards and the ID prefixes.

## When the source changes: cascade

Did stage 1 or a team decision change? Re-derive in sequence, one stage at a time, because each one starts from the previous stage already closed. Details and a ready brief are in `references/cascade.md`. In short: one mid-tier subagent per stage, with a trace and `changes-<stage>.md` (before, after, why, source id). The agent decides reversible design choices and records them. A team decision becomes a question. At the end, the top-tier model reads the whole series and checks the traceability of every R# down to the HLD.

## Subagents and budget

Use a cheap model for mechanical checks, a mid-tier model to read and write one stage, and the top-tier model only for the final judgment of the series. Readability rewrites run in parallel, one agent per document. The cascade runs in sequence. State at the start how many agents, which model and the ceiling (or "no subagents" when working alone). Without subagents, the cold reader and the final read become L# in the README, with what the author checked instead. A later stage that finds an error in an earlier one fixes the earlier one, records it in "What changed" of both, and re-derives what came after (a short cascade). Give each agent one self-contained brief in a file, with the input and output files and the check command it runs before finishing.

## Known pitfalls

- A term renamer breaks articles ("an Variant") and proper names ("Argo Canary releases"): review the diff.
- IDs from another source (the as-is uses A1, P2 as check ids) collide with the series ids: turn auto-linking off for that stage.
- A list right after a paragraph line, with no blank line, becomes part of the paragraph in Markdown.
- A large artifact (over 1 MB) can be republished to the same link only after reading the whole published page: keep the page lean or plan a new link.

## Diagrams, page and scripts

Diagram rules, the published page, linking and the check scripts (`permalinks.py`, `preserve.py`, `privacy_scan.py`, `check.mjs`, `build_page.py`) belong to the `artifact-routing` skill, which is not bundled here. Without it, run the same checks by hand or with your own scripts. This skill keeps no scripts or page assets.

## Related

- `artifact-routing` (not bundled): how each document is written, built and checked.
- A humanize or de-AI writing skill, for text that does not read as machine-written.
- A task-card skill, for the tasks that follow the HLD.
