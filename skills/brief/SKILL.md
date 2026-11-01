---
level: persona
name: brief
description: "Request format (brief): required lines, defaults for each missing line, and how the agent applies them. Use when a new request arrives outside the format, when Goal, Done when or Mode is missing, or when the user asks for the brief, the request format or the template."
---

# Request format (brief)

Required: the first 3 lines.

```
Goal:            what changes when it is done (1 sentence)
Done when:       the signal you will check (command, link, number, "34 of 35")
Mode:            plan only | execute and tell me | execute until <milestone> and stop
---
Context:         pasted source or path (thread, PR, artifact, error), with the date if old
Where:           repo · branch · environment (dev / staging / prod)
Lens:            the angle of analysis (MECE, dev × safeguards)
Budget:          models, parallelism, ceiling on subagents or cost
Output:          format + audience (only me / team / client)
Allowed / Not:   what is released (commit, push to PR, draft PR, tracker) and what is not (publish, merge, scope X)
```

Defaults when a line is missing: Context and Where are the current ones, local (prod only if written); Lens is
the project's standard yardstick; Budget is an explicit model and a ceiling of 10 subagents; Output is a short
inline widget and short text ("team" or "client" turns on humanize and an artifact); Allowed / Not is editing
local files and running tests, everything else only with the user's word; Mode is "execute and tell me" if
the task is small, "plan only" if it is large, irreversible or touches an environment.

How the agent applies it: a new request outside the format opens with the brief filled in (only lines that
change something, `?` on guesses). A `?` in Goal, Done when, Where or Allowed / Not that would change the
action, or a large task: stop and ask for confirmation, otherwise show it and proceed. No brief for
continuations, one-line requests, conversation or requests already in the format. A line repeated with the
same value: propose making it the default.

This skill holds the full text of the "Request format (brief)" rule. The always-loaded rules keep only the
summary. The rule applies the same way in every harness.
