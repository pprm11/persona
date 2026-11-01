# Cascade: when the source changes

Use when the problem domain, a team decision or an as-is fact changes, or when the user says "rethink the following stages".

1. Back up the current revision and make a working copy (`rN/new/`, `rN/base/`). Record in the decisions file everything decided in the conversation since the last round.
2. Show the plan (inline widget) and ask how to treat decisions: A) the agent decides reversible design matters and lists each change with its reason, and a team decision becomes a question; B) a 1-3-1 menu at the end of each stage.
3. One stage at a time, in order (1 → 6), one Sonnet subagent per stage with the brief [cascade-brief](cascade-brief.md). Each delivers: the revised stage, `trace-<stage>.md` (covered, stale, missing, contradicts, orphan) and `changes-<stage>.md` (Id · Before · After · Why).
4. Between stages, check the report against the decisions file before launching the next one (an agent may "fix" a team decision from an old file). Send a status per stage.
5. End: Opus reads the whole series and checks traceability R# → solution element → ADR → HLD → test; README with "What changed in revision N"; permalinks; privacy scan; build; publication only with the user's word.
6. Report to the user: decisions that changed (one line each, with reason), new questions with owner, what was left out.
