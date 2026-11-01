# persona

Opinionated, opt-in working practices for coding agents: a set of skills and a short practices file, all in
English. It is the `persona` level of the layered agent context (named after Jung's persona, the public face a
person shows). It loads after `superego` and before `collective`, so a team, a company or the person can
override it. Precedence, strongest first: `id`, `ego`, `collective`, `persona`, `superego`.

Nothing private lives here. Private history and settings belong to the `id` layer.

## Skills

| Skill | Use it for |
|---|---|
| `ub-mode` | The cycle for any code change: make it work, make it right, follow practice |
| `root-cause` | Diagnosing an error or recurring rework down to a proven root cause |
| `critical-code-review` | A four-lens review of a branch before it is pushed |
| `brief` | The request format: goal, done-when, mode, scope |
| `cross-harness-orchestration` | Parallel work and second opinions across coding agents |
| `claude-workflow-orchestration` | Briefs and workflows for Claude models, long handoffs, failure recovery |
| `staged-engineering` | A traceable six-stage design series, from problem to detailed design |
| `humanize` | One pass that makes a text read well for a human, voice and meaning kept (the default) |
| `humanize-heavy` | The scored pipeline, script plus three agents, when the user asks for the heavy version |
| `inline-widgets` | Answering with inline visual widgets for status, plans and comparisons |

## Use it

Add the repo to your `self` manifest between `superego` and `collective`:

    {"level": "persona", "name": "persona", "path": "persona", "repo": "<this repo>", "active": true, "mode": "readonly"}

See `templates/persona` in `apparatus` for the layer skeleton and `docs/contract.md` for the rules a layer
follows.
