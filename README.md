# persona

Reusable, independent skills for engineering, research, writing and collaboration. Each skill has a `SKILL.md` entrypoint and can be installed individually.

```bash
npx skills add pprm11/persona --list
npx skills add pprm11/persona --skill root-cause
```

To install every skill, run `npx skills add pprm11/persona`. For several named skills, repeat `--skill`; the CLI also supports global and agent selection flags. Review the CLI's current help before using those options. Update installed skills with `npx skills update`.

The CLI reads the published repository. A successful install and appearance in the skills.sh directory are separate observations. See [contribution and release](CONTRIBUTING.md).

## Catalog

| Skill | Owns |
|---|---|
| [artifact-routing](skills/artifact-routing/SKILL.md) | Route a document, HTML page or diagram to its Diataxis type (tutorial, how-to, reference, explanation), one type per tab when they share a page, then write, build and check it. Other media use the same routing plus a medium skill. Use when drafting or revising an artifact. |
| [brief](skills/brief/SKILL.md) | Request format (brief): required lines, defaults for each missing line, and how the agent applies them. Use when a new request arrives outside the format, when Goal, Done when or Mode is missing, or when the user asks for the brief, the request format or the template. |
| [claude-workflow-orchestration](skills/claude-workflow-orchestration/SKILL.md) | Prepare Claude Sonnet and Haiku briefs and Workflows, including long handoffs and failure recovery. Use when delegating to cheaper Claude models or authoring a Workflow script. Cross-harness coordination lives in cross-harness-orchestration. |
| [clean-architecture](skills/clean-architecture/SKILL.md) | Write or review domain boundaries, ports and adapters, dependency direction and typed domain models. |
| [context-ingest](skills/context-ingest/SKILL.md) | Save an explicitly authorized durable fact to the active memory system with deduplication and provenance. |
| [context-recall](skills/context-recall/SKILL.md) | Find and verify existing project memory, decisions, rules or skills before answering or acting. |
| [critical-code-review](skills/critical-code-review/SKILL.md) | Review a branch before push through four lenses, with scope audit and corrections. Use for a very critical code review or a review before pushing; reviewing an existing PR's comments is a separate skill. |
| [cross-harness-orchestration](skills/cross-harness-orchestration/SKILL.md) | Coordinate parallel work or second opinions across Claude Code and Codex, with model selection, self-contained briefs, isolated writers and a budget ceiling. Use for portable or cross-harness orchestration. |
| [decision-rfc](skills/decision-rfc/SKILL.md) | Write a decision RFC describing a sourced problem, options, tradeoffs and open questions. |
| [explained-by-cats](skills/explained-by-cats/SKILL.md) | Turn a document into a short vertical "explained by cats" reel (interactive 9:16 HTML page or narrated script), each scene a cat metaphor plus a plain translation. Use for a reels, stories or kittens version of a document. |
| [humanize](skills/humanize/SKILL.md) | Rewrite a text so it reads well for a human, in the author's voice, with the meaning intact. One pass, no scorer, no agents. Use on /humanize, "humanize this", "make this read better", or before delivering any written piece. When the user asks for the heavy, full or scored version ("with the scorer", "does this sound AI-written?"), use `humanize-heavy` instead. |
| [humanize-heavy](skills/humanize-heavy/SKILL.md) | Heavy mode of humanize. Iteratively rewrite a text until it passes a deterministic AI-tell scorer plus three context-free AI-detection agents; output stays in the input language. Use only when the user asks for the heavy, full or scored version ("heavy humanize", "with the scorer", "does this sound AI-written?") or a calling skill requires the scored pipeline. The default, unscored pass is the `humanize` skill. |
| [inline-widgets](skills/inline-widgets/SKILL.md) | Answers the user with inline visual widgets (show_widget) for status, plans, task queues, comparisons, results and numbers. Use whenever the reply has progress, a task or wave list, an option comparison, metrics or a plan. Skip for one-line answers. |
| [measured-correction](skills/measured-correction/SKILL.md) | Run a measured correction cycle for evaluation failures, including options and before/after comparison. |
| [publish-pull-request](skills/publish-pull-request/SKILL.md) | Publish an explicitly authorized author-side pull request or update and follow its checks. |
| [pull-request-description](skills/pull-request-description/SKILL.md) | Write or revise a pull request description that explains behavior, evidence and risk to reviewers. |
| [pull-request-review](skills/pull-request-review/SKILL.md) | Review an existing pull request as a reviewer and prepare actionable, evidence-backed findings. |
| [outcome-driven-development](skills/outcome-driven-development/SKILL.md) | Connects software outcomes, source authority, evidence and adoption. |
| [python-idioms](skills/python-idioms/SKILL.md) | Write or review idiomatic Python: types, errors, async, configuration, tests and I/O. |
| [root-cause](skills/root-cause/SKILL.md) | Diagnose an error, bug, CI failure or recurring rework: reproduce it, use an Ishikawa diagram and causal questions, prove the root cause, and separate correction, containment and prevention. Use for root cause analysis, Ishikawa or 5 whys. |
| [secret-backup](skills/secret-backup/SKILL.md) | Back up or restore secret files with an existing encrypted provider and locally configured manifest. |
| [session-closeout](skills/session-closeout/SKILL.md) | Close or archive a session when explicitly requested, preserving deliverables and unresolved work. |
| [staged-engineering](skills/staged-engineering/SKILL.md) | Drive a traceable six-stage engineering design series: problem domain and as-is, market study, solution domain, HLA with ADRs, then HLD. Use for RFC to HLA to HLD work, a design series with traceability, or cascading revisions when an earlier stage changes. |
| [task-cards](skills/task-cards/SKILL.md) | Turn a plan into actionable task cards with observable acceptance criteria and dependencies. |
| [tree-search](skills/tree-search/SKILL.md) | Research an internet topic in rounds, expanding from evidence, gaps and contradictions. |

## Workflow boundaries

- `root-cause` proves causes; `measured-correction` owns decisions and before/after evaluation.
- `critical-code-review` reviews the author’s local change; `pull-request-review` reviews an existing PR; `pull-request-description` writes its body; `publish-pull-request` handles authorized author publication.
- `outcome-driven-development` owns outcome, scope, evidence and adoption; `staged-engineering` owns an explicitly requested design series.
- `decision-rfc` handles one decision; `staged-engineering` handles a traceable design series; `artifact-routing` shapes artifacts and does not invoke the genre workflow back.
- `context-recall` reads memory; `context-ingest` writes authorized facts; `session-closeout` handles an explicitly requested closeout.
- `cross-harness-orchestration` owns cross-harness coordination; `claude-workflow-orchestration` supplies Claude-specific mechanics.

Optional sibling skills are referenced by name; when installed alone, use the fallback in the entrypoint. `ub-mode` and vendor tooling are external and retain their own terms.

## Credits

The `humanize` and `humanize-heavy` AI-tell lists draw in part on [Wikipedia's Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing); their rewrite procedure and scorer are maintained here. `ub-mode` is external work by Robert C. Martin and is not bundled; consult its own license before use. The artifact routing approach draws on [Diataxis](https://diataxis.fr/).

Some procedures adapt techniques, in our own words, from other skill collections:

- [mattpocock/skills](https://github.com/mattpocock/skills) (MIT): exact-symptom reproduction and falsifiable causes in `root-cause`, the spec check in `critical-code-review`, the ADR rule in `staged-engineering`, the deletion test in `clean-architecture`, expand-contract cards in `task-cards`.
- [obra/superpowers](https://github.com/obra/superpowers) (MIT): boundary logging and test-order bisection in `root-cause`, independent test oracles in `critical-code-review` and `python-idioms`, handling received review comments in `publish-pull-request`.
- [riekelt/technical-writer](https://github.com/riekelt/technical-writer) (MIT): goals, costs and fallback in `decision-rfc`, wrong turns in the postmortem skeleton of `artifact-routing`, three patterns in `humanize`.
- [ccheney/robust-skills](https://github.com/ccheney/robust-skills) (MIT): the outbox and idempotent consumer note in `clean-architecture`.
- [juliusbrussee/caveman](https://github.com/juliusbrussee/caveman) (Apache-2.0): the expand, migrate and contract sequence in `task-cards`.
- The removed-protection check in `pull-request-review` follows an idea from [trailofbits/skills](https://github.com/trailofbits/skills) (CC BY-SA 4.0); no wording is adapted.

## License

[MIT](LICENSE). The existing `humanize` scorer credits the external source in its skill.
