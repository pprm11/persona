---
name: humanize-heavy
description: Heavy mode of humanize. Iteratively rewrite a text until it passes a deterministic AI-tell scorer plus three context-free AI-detection agents; output stays in the input language. Use only when the user asks for the heavy, full or scored version ("heavy humanize", "with the scorer", "does this sound AI-written?") or a calling skill requires the scored pipeline. The default, unscored pass is the `humanize` skill.
---

# Humanize (heavy)

This is the scored pipeline. It runs only on request; the default pass is `humanize`, one rewrite with no scorer and no agents.

Take the explicitly supplied text, score it for AI tells, rewrite, and iterate until the bars below are met. Scoring is a fixed 100-point system so runs are reproducible:

- **60 points — deterministic script** (`scripts/ai_tells.py`): measurable stylometry. Same text always gets the same points.
- **40 points — agent rubric**: 8 binary pattern checks a script can't compute, answered by 3 context-free agents with majority voting. Not perfectly deterministic (LLM sampling never is — say so if the user asks), but binary evidence-backed votes are far more stable than gut percentages.

**Pass bar: combined score ≥ 80/100.**

## Input

The invocation takes one or two parts:

1. **The text** (required) — for direct invocation, the user supplies it in the skill argument or message, or explicitly points to the text or file; otherwise ask for it and stop. A named calling skill may pass a specific bounded draft or file and its immutable facts, numbers, links, IDs, paths, code and other constraints; use that scope without asking the user to paste it again. Never pull unrelated session history.
2. **Additional instructions** (optional) — per-run rules from the user. Two accepted forms:
   - Everything BEFORE a line containing only `---` is instructions; everything after is the text.
   - A first line starting with `instructions:` or `rules:` is instructions; the rest is the text.
   With neither marker, the entire input is the text (the original single-parameter behavior). When it is ambiguous whether a short opening line is an instruction or part of the text, ask instead of guessing — silently rewriting a line that was content, or applying content as a rule, both corrupt the run.

Instructions are the user speaking, so they override this skill's defaults for that run: they can relax constraints ("free rewrite allowed", "ok to drop the bullets"), tighten them ("also ban colons", "don't touch paragraph openers"), or set context ("this is a task brief, keep the imperative tone"). Two things they change only explicitly, never by vague implication: the meaning-preservation constraint, and the pass bars. Restate in the final report which instructions were applied.

After rewriting, re-audit factual integrity against the supplied original and the user-authorized scope. Preserve the intended meaning, including any explicit user-authorized change, and all items the user protects. In composed mode, preserve the caller-designated immutable items, including facts, numbers, links, IDs and citations, except where the user explicitly changes them. The caller still owns its genre-specific source audit. Composition does not relax the scoring bars.

Save the candidate to `<scratchpad>/humanize/candidate.md` so both the script and the agents read from disk — agents must receive only the text, never conversation context and never the instructions (detectors judge the text cold; instructions steer only the rewriting between rounds).

## Phase 1 — script loop (deterministic, no agents)

Run:

```bash
python <skill-dir>/scripts/ai_tells.py <scratchpad>/humanize/candidate.md
```

The scorer's lexical lists are English-only. For other languages, including Portuguese, the lexical score is incomplete and cannot establish the full pass bar; report this limitation and use a language-appropriate manual review. The JSON output gives `script_score` (0–60), per-check points, and rewrite `advice` for each failed check. Rewrite targeting exactly the failed checks (see "Rewriting rules"), save, re-run. Iterate until `script_score ≥ 50` or 5 iterations. This phase is free and instant — never spawn agents for it.

## Phase 2 — agent rubric (3 parallel agents, majority vote)

When three independent subagents are authorized and available, launch them together using the active harness interface. If fewer than three eligible independent evaluators are available or return valid votes, report the agent rubric and combined score as not measured; do not claim a pass. Identical prompts — determinism comes from binary questions plus majority voting, not from varied personas:

```
Read the file <path>. For each check below answer strictly true or false about
that text, quoting the exact excerpt that proves your answer (or "none found"
when answering that a pattern is absent). Do not give an overall opinion.

Reply with ONLY this JSON:
{"checks": {"A": {"present": bool, "evidence": "..."}, ... "H": {...}}}

A. thesis_openers: 70%+ of paragraphs open with a tidy topic/label sentence.
B. punchline_closers: half or more paragraphs end on an aphoristic takeaway.
C. moral_ending: the document's final sentence is a generalized lesson/moral
   rather than a concrete detail or open question.
D. performed_casualness: casual devices (splices, asides, slang) appear at
   metronomic intervals, reading applied rather than native.
E. self_answered_questions: a rhetorical question is immediately answered by
   its own next sentence.
F. exhaustive_symmetry: every enumeration is complete and syntactically
   parallel; nothing is truncated, hand-waved, or unevenly weighted.
G. uniform_density: every sentence carries maximal payload; no redundancy,
   digression, or loose end anywhere.
H. balanced_antithesis: polished two-part "not X but Y / either A or B"
   constructions recur as a rhetorical habit.
```

Scoring: for each of the 8 checks, take the **majority vote** (2 of 3 agents). Each check voted absent = **5 points**; present = 0. Combined score = `script_score` + rubric points.

- Combined ≥ 80 → done. If one or two checks are still voted present and the fix is small and localized (e.g., a moral-shaped final sentence), apply it and re-verify anyway — a clean 100 is usually one cheap edit away.
- Otherwise rewrite once, targeting only the majority-present checks (use the quoted evidence), re-run the script to confirm phase 1 hasn't regressed, and relaunch all three agents fresh. Max 5 rounds. If never met, stop and report the best round honestly.

**Never claim points without verification.** Any edit made after a vote invalidates that vote: re-run the script (free) and, if the edit could plausibly affect a rubric check, re-vote all three agents before reporting the score. Never estimate what an agent "would" score, and never fall back to asking agents for an overall confidence percentage — it is unstable on identical text.

## Rewriting rules

Non-negotiable constraints:

- **Preserve meaning strictly.** Change facts, claims, scores, examples, conclusions, or the substance of an argument only within the scope explicitly authorized by the user; preserve all other facts and protected material.
- **Keep the original language.** Output stays in the input language (a Portuguese text stays Portuguese, an English text stays English).
- **Keep technical terms intact.** Domain vocabulary, product names, code identifiers, rubric terms — never paraphrase these.
- **Match the user's voice**: direct, plain, slightly informal. No fake typos, no injected "honestly"-style filler, no slang the user wouldn't use.
- **No AI-tell punctuation** (user-validated list, enforced by the script's `banned_chars` check): em dash, en dash, spaced hyphen used as a dash (` - `), semicolon, **colon in prose**, ellipsis character, curly quotes/apostrophes, bullet characters, parentheses used as asides, **hyphenated compound words** (`in-memory`, `read-then-write`, `long-running`), invisible unicode (non-breaking/zero-width spaces). Convert parenthetical asides to commas or their own sentence. Rewrite a prose colon as two sentences, a comma, or "like"/"such as"; rewrite hyphenated compounds to their open form ("in memory") or rephrase the sentence. Exemptions the script honors: inline code in backticks, bare call parens like `run()`, colons between digits (times, ratios) and inside URLs, flag tokens starting with `-` (`-r`), and hyphenated tokens containing a dot or slash (file names like `repository-test-suite.ts`, paths). A hyphenated technical identifier with none of those markers (`mongodb-memory-server`) must be wrapped in backticks to be exempt — or the sentence rephrased around it; never respell the identifier itself.

Practical guidance per rubric check: vary paragraph openers (A) — start some mid-thought or on a detail; end paragraphs on data, not lessons (B); end the document on a concrete open item (C); if casualness reads applied, remove devices rather than adding more (D); turn Q&A into statements or leave the question hanging (E); weight one enumeration item and fold the rest into prose with varied syntax (F); allow one redundancy or aside, let a thread trail (G); break symmetric clause pairs (H).

**Never manufacture paragraph variance with a stub paragraph** — a standalone one-liner ("My two trajectories split exactly there.") or a clipped two-sentence verdict stub ("touch() throws loudly in both trees. What differs favors A."). The script caps `paragraph_variance_cv` when a paragraph has ≤1 sentence at ≤15 words, or ≤2 sentences at ≤18 words. A short closing paragraph must still be a real paragraph (roughly 25+ words of substance); otherwise fold the verdict into the preceding paragraph and accept a lower variance score — the combined pass bar is 80, not 100, and a stub is a worse tell than a 3-point variance check.

Known ceiling, tell the user when it applies: content that must exhaustively enumerate (file lists, backend-by-backend coverage) caps checks F and G — perfect coverage inherently reads "compiled". Don't drop facts to chase points.

Make each rewrite a targeted revision of flagged passages, not a global re-generation — regenerating tends to reintroduce the same tells.

## Final report

For a composed invocation, return the revised bounded text or file and the score breakdown and limitations to the calling skill for integration; the caller owns the final presentation and source audit. For standalone invocation, end with, in this order:

1. **The final text**, in a fenced block, ready to copy.
2. The score breakdown: script score with failed checks, rubric votes per check, combined total per round.
3. One or two sentences on what changed. If the bar wasn't reached within the caps, say so plainly and name the checks that wouldn't move.

## Credits

Part of the AI-tell lexicon in `scripts/ai_tells.py` comes from Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), kept by WikiProject AI Cleanup.
