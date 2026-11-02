"""Dispatch one vetted audience bundle to an isolated native writer."""
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def build_prompt(bundle):
    if not isinstance(bundle, dict) or set(bundle) != {"audience", "use", "category", "assignment", "sources"}:
        raise ValueError("invalid bundle shape")
    if not all(nonempty(bundle[k]) for k in ("audience", "use", "category", "assignment")):
        raise ValueError("invalid audience or assignment")
    if bundle["category"] not in {"Tutorial", "How-to guide", "Reference", "Explanation"}:
        raise ValueError("invalid category")
    sources = bundle["sources"]
    if not isinstance(sources, list) or not sources:
        raise ValueError("sources required")
    ids = set()
    facts = []
    for source in sources:
        if not isinstance(source, dict) or set(source) != {"id", "text", "allowed_for"}:
            raise ValueError("invalid source shape")
        sid, allowed = source["id"], source["allowed_for"]
        if not nonempty(sid) or sid in ids or not nonempty(source["text"]):
            raise ValueError("invalid or duplicate source")
        if not isinstance(allowed, list) or not all(nonempty(a) for a in allowed) or bundle["audience"] not in allowed:
            raise ValueError("source not authorized")
        ids.add(sid)
        facts.append({"id": sid, "text": source["text"]})
    task = {k: bundle[k] for k in ("audience", "use", "category", "assignment")}
    task["sources"] = facts
    return ("Write in the language the task asks for; if none is given, use the language of the assignment. Use only the sources provided. "
            "Do not use tools. Do not add facts, causes, costs, impacts, status, promises or universal claims without support. "
            "Deliver one piece with only what the audience needs for the use, with no classification in the text. "
            "Omit next steps and unsupported editorial comments. Limit claims of absence to the evidence provided. "
            "Prefer literal passages from the sources where suitable. "
            "Return only JSON in this shape: {\"artifact\":\"text of the piece\",\"handoff\":\"Audience: ... \u00b7 Use: ... \u00b7 Type: ...\",\"claims\":[{\"claim\":\"sentence or imperative\",\"sources\":[\"ID\"]}]}. "
            "The handoff is a string separate from the piece. Map each substantive clause, including imperatives and limits, to the source IDs that support it.\n"
            + json.dumps(task, ensure_ascii=False))


def validate_output(output, ids):
    if not isinstance(output, dict) or set(output) != {"artifact", "handoff", "claims"}:
        raise ValueError("invalid response shape")
    if not nonempty(output["artifact"]) or not nonempty(output["handoff"]) or not isinstance(output["claims"], list) or not output["claims"]:
        raise ValueError("empty artifact, handoff or ledger")
    for claim in output["claims"]:
        if not isinstance(claim, dict) or set(claim) != {"claim", "sources"} or not nonempty(claim["claim"]):
            raise ValueError("invalid claim")
        refs = claim["sources"]
        if not isinstance(refs, list) or not refs or not all(isinstance(ref, str) and ref in ids for ref in refs):
            raise ValueError("missing or unknown source")
    return output


def binary(name):
    """Native executable for `claude` or `codex`.

    Order: the environment variable SCOPED_WRITER_<NAME> (for example SCOPED_WRITER_CODEX, a full path);
    then PATH (on Windows a real .exe, because a .cmd shim would start a shell); then, for codex on
    Windows only, the native binary inside the npm package that sits next to a codex.cmd found on PATH.
    """
    override = os.environ.get("SCOPED_WRITER_" + name.upper())
    if override:
        if not Path(override).is_file():
            raise ValueError(f"setup: SCOPED_WRITER_{name.upper()} is not a file: {override}")
        return override
    if os.name == "nt":
        for directory in os.get_exec_path():
            candidate = Path(directory) / (name + ".exe")
            if candidate.is_file():
                return str(candidate)
        if name == "codex":
            for directory in os.get_exec_path():
                base = Path(directory)
                if (base / "codex.cmd").is_file():
                    pattern = "node_modules/@openai/codex/node_modules/@openai/codex-*/vendor/*/bin/codex.exe"
                    for candidate in sorted(base.glob(pattern)):
                        if candidate.is_file():
                            return str(candidate)
        raise ValueError(f"setup: native executable not found: {name} (set SCOPED_WRITER_{name.upper()})")
    path = shutil.which(name)
    if not path:
        raise ValueError(f"executable not found: {name} (set SCOPED_WRITER_{name.upper()})")
    return path


def command(kind):
    if kind == "claude":
        return [binary(kind), "-p", "--safe-mode", "--restricted", "--tools", "", "--disable-slash-commands", "--strict-mcp-config", "--no-session-persistence", "--system-prompt", "Write only from the data received; do not use tools.", "--output-format", "stream-json", "--verbose"]
    args = [binary(kind), "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules", "--skip-git-repo-check", "--json", "--strict-config", "-c", "approval_policy=\"never\"", "-c", "project_doc_max_bytes=0", "-c", "web_search=\"disabled\"", "-c", "default_permissions=\"d115\"", "-c", 'permissions.d115.filesystem={":workspace_roots"="read"}', "-c", "permissions.d115.network.enabled=false"]
    for feature in ("shell_tool", "unified_exec", "multi_agent", "apps", "plugins", "memories", "code_mode_host", "view_image", "shell_snapshot"):
        args.extend(["--disable", feature])
    return args + ["-"]


def parse_events(kind, data):
    events = [json.loads(line) for line in data.splitlines() if line.strip()]
    types = [event.get("type") for event in events]
    session = None
    answer = None
    if kind == "claude":
        init = [e for e in events if e.get("type") == "system" and e.get("subtype") == "init"]
        if len(init) != 1 or init[0].get("tools") != [] or init[0].get("mcp_servers") != []:
            raise ValueError("no proof of empty Claude tools and MCP")
        session = init[0].get("session_id")
        for event in events:
            if event.get("type") == "assistant":
                blocks = event.get("message", {}).get("content", [])
                if any(b.get("type") not in {"text", "thinking"} or not isinstance(b.get("text" if b.get("type") == "text" else "thinking"), str) for b in blocks):
                    raise ValueError("non-text assistant event")
            if event.get("type") == "result":
                if event.get("is_error") or event.get("subtype") != "success":
                    raise ValueError("Claude failed")
                answer = event.get("result")
            if event.get("type") not in {"system", "assistant", "result", "rate_limit_event"}:
                raise ValueError("unexpected Claude event")
    else:
        for event in events:
            typ = event.get("type")
            if typ == "thread.started":
                session = event.get("thread_id")
            elif typ in {"item.started", "item.updated", "item.completed"}:
                item = event.get("item", {})
                notice = "Code Mode is unavailable because code-mode host is disabled. Code mode will fail closed; enable `features.code_mode_host` and install `codex-code-mode-host`."
                benign_notice = (typ == "item.completed" and item.get("type") == "error"
                                 and item.get("message") == notice)
                if item.get("type") not in {"agent_message", "reasoning"} and not benign_notice:
                    raise ValueError("event: tool or unknown item")
                if typ == "item.completed" and item.get("type") == "agent_message":
                    answer = item.get("text")
            elif typ not in {"turn.started", "turn.completed"}:
                raise ValueError("tool or unexpected event")
        if "turn.completed" not in types:
            raise ValueError("event: incomplete Codex turn")
    if not nonempty(session) or not nonempty(answer):
        raise ValueError("event: missing session or response")
    answer = answer.strip()
    if answer.startswith("```json\n") and answer.endswith("\n```"):
        answer = answer[8:-4]
    elif answer.startswith("```\n") and answer.endswith("\n```"):
        answer = answer[4:-4]
    try:
        parsed = json.loads(answer)
    except json.JSONDecodeError as exc:
        raise ValueError("event: invalid response JSON") from exc
    return session, types, parsed


@contextmanager
def isolated_codex_environment(original):
    """Provide empty customization roots and, if needed, a temporary auth hardlink."""
    parent = Path(original.get("CODEX_HOME") or (Path(original["USERPROFILE"] if os.name == "nt" else original["HOME"]) / ".codex"))
    if not parent.is_dir():
        raise ValueError("setup: original Codex home is unavailable")
    with tempfile.TemporaryDirectory(prefix="scoped-auth-", dir=parent) as root:
        root_path = Path(root)
        codex_home = root_path / "codex"
        user_home = root_path / "home"
        codex_home.mkdir()
        user_home.mkdir()
        link = codex_home / "auth.json"
        if not original.get("OPENAI_API_KEY"):
            source = parent / "auth.json"
            if source.is_symlink() or not source.is_file():
                raise ValueError("setup: configure OPENAI_API_KEY or a regular non-symlink Codex auth.json")
            try:
                os.link(source, link, follow_symlinks=False)
            except OSError as exc:
                raise ValueError("setup: cannot hardlink Codex auth.json; configure OPENAI_API_KEY") from exc
        env = original.copy()
        env.update({"CODEX_HOME": str(codex_home), "HOME": str(user_home), "USERPROFILE": str(user_home)})
        try:
            yield env
        finally:
            if link.exists():
                link.unlink()


def main():
    if len(sys.argv) != 2 or sys.argv[1] not in {"codex", "claude"}:
        raise ValueError("usage: scoped_writer.py codex|claude")
    kind = sys.argv[1]
    try:
        bundle = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("input: expected UTF-8 JSON bundle") from exc
    prompt = build_prompt(bundle)
    args = command(kind)
    env = os.environ.copy()
    env["CLAUDE_CODE_DISABLE_AUTO_MEMORY"] = "1"
    wire = prompt.encode("utf-8")
    with tempfile.TemporaryDirectory(prefix="scoped-writer-") as cwd:
        if kind == "codex":
            with isolated_codex_environment(env) as child_env:
                result = subprocess.run(args, input=wire, capture_output=True, cwd=cwd, env=child_env, timeout=180, check=False)
        else:
            result = subprocess.run(args, input=wire, capture_output=True, cwd=cwd, env=env, timeout=180, check=False)
    if result.returncode:
        raise ValueError(f"setup: native writer exited {result.returncode}; check CLI compatibility and authentication")
    try:
        session, types, answer = parse_events(kind, result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("event: invalid native event stream") from exc
    validate_output(answer, {source["id"] for source in bundle["sources"]})
    model_draft = dict(answer)
    answer = dict(answer)
    answer["handoff"] = f'Audience: {bundle["audience"]} \u00b7 Use: {bundle["use"]} \u00b7 Type: {bundle["category"]}'
    assertions = {"fresh_process_no_resume": True, "empty_working_directory_at_launch": True,
                  "isolated_codex_customization_roots": kind == "codex",
                  "claude_init_tools_and_mcp_empty": kind == "claude",
                  "no_tool_events_observed": True}
    record = {"model_draft": model_draft, "setup_assertions": assertions, "submitted_input": prompt, "input_sha256": hashlib.sha256(wire).hexdigest(), "command": args, "session_id": session, "event_types": types, "tool_check": "no tool events observed; semantic review required", "output": answer}
    print(json.dumps(record, ensure_ascii=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.SubprocessError) as exc:
        print("scoped writer setup failed: " + type(exc).__name__, file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print("scoped writer input rejected: invalid JSON", file=sys.stderr)
        sys.exit(1)
    except ValueError as exc:
        print("scoped writer rejected: " + str(exc), file=sys.stderr)
        sys.exit(1)
