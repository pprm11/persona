---
level: persona
metadata:
  level: persona
name: inline-widgets
description: Answers the user with inline visual widgets (show_widget) for status, plans, task queues, comparisons, results and numbers. Use whenever the reply has progress, a task or wave list, an option comparison, metrics or a plan. Skip for one-line answers.
---

# Inline widgets

The user wants replies that come with clean visual widgets, not only text and tables. The tool is `mcp__visualize__show_widget` (inline HTML/SVG in the chat).

## How

1. On the first widget of the session, call `mcp__visualize__read_me` (modules as needed: `mockup` for cards and dashboards, `chart` for charts, `diagram` for flows and dependencies). Do it silently, without narrating.
2. One widget per reply, two at most. Explanatory text stays OUTSIDE the widget, in the reply, short (simple wording, fractions, examples).
3. Formats that work:
   - **Execution status** (workflow, waves, PRs): a row of metric cards (done / running / failed / remaining + ETA) and, below, a list per stage with a state icon (`ti-check`, `ti-loader-2`, `ti-alert-triangle`, `ti-clock`) and a thin progress bar.
   - **Plan / waves / dependencies**: SVG diagram in columns per wave, foundations first, arrows for strong dependencies; color by category, at most 2-3 ramps.
   - **Option comparison**: side-by-side cards, the recommended one with a highlighted border and a badge.
   - **Results** (test battery, load test, audit): KPI row plus a simple bar or line chart; the detailed table stays in markdown in the reply.
   - **Environment** (hosting, connectors, CI): one card per service with its state (online, failed, missing config).
4. Buttons with `sendPrompt()` for the likely next step ("See the wave 1 PRs", "Run QA again").
5. Design rules: flat, no gradient or shadow, colors through CSS variables (dark mode required), sentence case, no emoji (Tabler outline icons), rounded numbers, no `position: fixed`.

## Do not

- Do not replace the text reply with the widget: the text states the essentials, the widget shows them.
- Do not put real personal data (phone numbers, IDs, names) in a widget.
- Do not invent numbers: everything shown must come from a tool in this session.
