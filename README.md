# persona

**Nine skills that make a coding agent work like a careful senior engineer.** Root cause before the fix, review
before the push, text that reads like a person wrote it, and a design series you can trace from problem to
detailed design.

[![skills.sh](https://img.shields.io/badge/skills.sh-pprm11%2Fpersona-000000)](https://www.skills.sh/pprm11/persona)
![skills](https://img.shields.io/badge/skills-9-blue)
![agents](https://img.shields.io/badge/works%20with-Claude%20Code%20%7C%20Codex%20%7C%20Cursor-555555)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)

```bash
npx skills add pprm11/persona
```

One command installs every skill into your agent through the [skills.sh](https://www.skills.sh/) CLI. Each skill
is a plain `skills/<name>/SKILL.md`, so you can read exactly what your agent will do before you install it.

## Skills

### Code

| Skill | What your agent does with it |
|---|---|
| [`root-cause`](skills/root-cause/SKILL.md) | Reproduces a bug or CI failure, draws an Ishikawa, asks why until the root is proven, then separates correction, containment and prevention |
| [`critical-code-review`](skills/critical-code-review/SKILL.md) | Reviews a branch before push through four lenses plus a scope audit, and fixes what it finds. Pairs with Uncle Bob's `ub-mode` (see [Credits](#credits)) |

### Design

| Skill | What your agent does with it |
|---|---|
| [`staged-engineering`](skills/staged-engineering/SKILL.md) | Drives a six-stage design series (problem, as-is, market study, solution domain, HLA with ADRs, HLD) and cascades a change in an early stage to the later ones. The page build and check scripts come from a separate `artifact-routing` skill, not bundled |
| [`brief`](skills/brief/SKILL.md) | Turns a loose request into a brief with goal, done-when, mode and scope, filling missing lines with stated defaults |

### Writing

| Skill | What your agent does with it |
|---|---|
| [`humanize`](skills/humanize/SKILL.md) | Rewrites a text in one pass so it reads well for a human, keeping the author's voice and meaning |
| [`humanize-heavy`](skills/humanize-heavy/SKILL.md) | Rewrites until the text passes a deterministic AI-tell scorer and three blind detection agents |

### Orchestration

| Skill | What your agent does with it |
|---|---|
| [`cross-harness-orchestration`](skills/cross-harness-orchestration/SKILL.md) | Splits work across Claude Code and Codex, with a model per task, self-contained briefs, one writer per file and a budget ceiling |
| [`claude-workflow-orchestration`](skills/claude-workflow-orchestration/SKILL.md) | Writes briefs and Workflow scripts for Sonnet and Haiku, long handoffs and recovery after a failed run. Claude Code only |
| [`inline-widgets`](skills/inline-widgets/SKILL.md) | Answers status, plans and comparisons with inline visual widgets. Needs the Claude app's visualize tool |

## Install

Everything:

```bash
npx skills add pprm11/persona
```

One skill:

```bash
npx skills add pprm11/persona --skill root-cause
```

Several skills, globally, for Claude Code:

```bash
npx skills add pprm11/persona --skill root-cause --skill critical-code-review -g -a claude-code
```

See the list before installing:

```bash
npx skills add pprm11/persona --list
```

Update later with `npx skills update`.

## Try it

After installing, ask your agent things like:

- "The login test fails only in CI. Find the root cause."
- "Review this branch before I push."
- "Humanize this README."
- "Start a design series for moving billing to events."

The agent picks the skill from its description; you do not have to name it.

## The practices file

[`global/practices.md`](global/practices.md) holds the rules these skills assume: status in three or four
bullets, decisions as a lettered menu, root cause before a fix, review before push, stop a review loop that does
not converge. The CLI installs skills only, so copy the lines you agree with into your `CLAUDE.md` or `AGENTS.md`.

## Use it as a layer

The repo is also the `persona` level of a layered agent context (named after Jung's persona, the public face a
person shows). It loads after `superego` and before `collective`, so a team, a company or the person can override
it. Precedence, strongest first: `id`, `ego`, `collective`, `persona`, `superego`. Nothing private lives here;
private history and settings belong to the `id` layer.

Add it to your `self` manifest between `superego` and `collective`:

```json
{"level": "persona", "name": "persona", "path": "persona", "repo": "https://github.com/pprm11/persona", "active": true, "mode": "readonly"}
```

## Credits

- **`ub-mode`** is Robert C. Martin's skill, and these skills assume it for every code change (make it work, make
  it right, follow practice, with CRAP, duplication and mutation checks). It is not bundled here. Install it from
  his repo:

  ```bash
  npx skills add unclebob/ub-mode
  ```

- **`humanize`** and **`humanize-heavy`** take part of their list of AI tells (words like "delve", "tapestry",
  "pivotal", stacked transitions and hedges) from Wikipedia's
  [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), kept by WikiProject AI
  Cleanup. The rewrite procedure and the scorer are written here.

## License

[MIT](LICENSE). The credited third-party work keeps its own terms.
