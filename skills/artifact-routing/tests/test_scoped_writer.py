import importlib.util
import json
import io
from unittest import mock
import pathlib
import os
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("scoped_writer", pathlib.Path(__file__).parents[1] / "scripts/scoped_writer.py")
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

class BundleTests(unittest.TestCase):
    def setUp(self):
        self.bundle = {"audience": "client", "use": "inform", "category": "Reference", "assignment": "Write", "sources": [{"id": "S1", "text": "Fact", "allowed_for": ["client", "on-call"]}]}

    def test_only_allowed_facts_reach_prompt(self):
        prompt = w.build_prompt(self.bundle)
        self.assertIn("Fact", prompt)
        self.assertNotIn("on-call", prompt)
        self.assertNotIn("allowed_for", prompt)

    def test_rejects_denied_and_duplicate_sources(self):
        self.bundle["sources"][0]["allowed_for"] = ["on-call"]
        with self.assertRaises(ValueError): w.build_prompt(self.bundle)
        self.bundle["sources"][0]["allowed_for"] = ["client"]
        self.bundle["sources"].append(dict(self.bundle["sources"][0]))
        with self.assertRaises(ValueError): w.build_prompt(self.bundle)

    def test_rejects_unknown_and_empty_evidence(self):
        for ids in ([], ["S2"]):
            with self.assertRaises(ValueError): w.validate_output({"artifact": "Fact", "handoff": "x", "claims": [{"claim": "Fact", "sources": ids}]}, {"S1"})

class EventTests(unittest.TestCase):
    def test_claude_metadata_and_reasoning_with_fenced_json(self):
        answer = {"artifact": "Fact", "handoff": "x", "claims": [{"claim": "Fact", "sources": ["S1"]}]}
        events = [
            {"type": "system", "subtype": "init", "tools": [], "mcp_servers": [], "session_id": "s"},
            {"type": "rate_limit_event", "rate_limit_info": {}},
            {"type": "assistant", "message": {"content": [{"type": "thinking", "thinking": "r"}]}},
            {"type": "result", "subtype": "success", "result": "```json\n" + json.dumps(answer) + "\n```"},
        ]
        _, _, parsed = w.parse_events("claude", "\n".join(map(json.dumps, events)))
        self.assertEqual(parsed, answer)
        events[2]["message"]["content"] = [{"type": "tool_use", "name": "Read"}]
        with self.assertRaises(ValueError):
            w.parse_events("claude", "\n".join(map(json.dumps, events)))

    def test_codex_only_accepts_exact_disabled_code_mode_notice(self):
        notice = "Code Mode is unavailable because code-mode host is disabled. Code mode will fail closed; enable `features.code_mode_host` and install `codex-code-mode-host`."
        answer = {"artifact": "Fact", "handoff": "x", "claims": [{"claim": "Fact", "sources": ["S1"]}]}
        events = [
            {"type": "thread.started", "thread_id": "s"},
            {"type": "turn.started"},
            {"type": "item.completed", "item": {"type": "error", "message": notice}},
            {"type": "item.completed", "item": {"type": "agent_message", "text": json.dumps(answer)}},
            {"type": "turn.completed"},
        ]
        self.assertEqual(w.parse_events("codex", "\n".join(map(json.dumps, events)))[2], answer)
        events[2]["item"]["message"] = "other error"
        with self.assertRaises(ValueError):
            w.parse_events("codex", "\n".join(map(json.dumps, events)))

    def test_category_is_restricted(self):
        bundle = {"audience": "c", "use": "x", "category": "other", "assignment": "x", "sources": [{"id": "S1", "text": "x", "allowed_for": ["c"]}]}
        with self.assertRaises(ValueError):
            w.build_prompt(bundle)

class IsolationTests(unittest.TestCase):
    def test_hardlink_lifecycle_and_exception_cleanup(self):
        with tempfile.TemporaryDirectory() as root:
            home = pathlib.Path(root)
            original = home / "auth.json"
            original.write_bytes(b"synthetic-test-only")
            (home / "AGENTS.md").write_text("canary", encoding="utf-8")
            env = {"CODEX_HOME": str(home)}
            before = dict(env)
            with self.assertRaisesRegex(RuntimeError, "test"):
                with w.isolated_codex_environment(env) as child:
                    isolated = pathlib.Path(child["CODEX_HOME"])
                    self.assertEqual({p.name for p in isolated.iterdir()}, {"auth.json"})
                    self.assertTrue(os.path.samefile(original, isolated / "auth.json"))
                    self.assertEqual(list(pathlib.Path(child["HOME"]).iterdir()), [])
                    raise RuntimeError("test")
            self.assertFalse(isolated.exists())
            self.assertEqual(original.read_bytes(), b"synthetic-test-only")
            self.assertEqual(env, before)

    def test_api_key_does_not_link_auth(self):
        with tempfile.TemporaryDirectory() as root:
            with w.isolated_codex_environment({"CODEX_HOME": root, "OPENAI_API_KEY": "synthetic"}) as child:
                self.assertEqual(list(pathlib.Path(child["CODEX_HOME"]).iterdir()), [])

    def test_missing_auth_fails_closed(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaisesRegex(ValueError, "configure OPENAI_API_KEY"):
                with w.isolated_codex_environment({"CODEX_HOME": root}):
                    self.fail("must not dispatch")

class ReceiptTests(unittest.TestCase):
    def test_utf8_input_and_private_original_handoff(self):
        bundle = {"audience": "client", "use": "understand status", "category": "Reference", "assignment": "Write", "sources": [{"id": "S1", "text": "Action done", "allowed_for": ["client"]}]}
        draft = {"artifact": "Action done", "handoff": "restrito: marcador incorreto", "claims": [{"claim": "Action done", "sources": ["S1"]}]}
        events = [{"type": "system", "subtype": "init", "tools": [], "mcp_servers": [], "session_id": "s"}, {"type": "result", "subtype": "success", "result": json.dumps(draft, ensure_ascii=False)}]
        result = mock.Mock(returncode=0, stdout="\n".join(map(json.dumps, events)).encode("utf-8"))
        stdin = mock.Mock(buffer=io.BytesIO(json.dumps(bundle, ensure_ascii=False).encode("utf-8")))
        stdout = io.StringIO()
        with mock.patch.object(w.sys, "argv", ["scoped_writer.py", "claude"]), mock.patch.object(w.sys, "stdin", stdin), mock.patch.object(w.sys, "stdout", stdout), mock.patch.object(w, "command", return_value=["fake"]), mock.patch.object(w.subprocess, "run", return_value=result) as run:
            w.main()
        wire = run.call_args.kwargs["input"]
        self.assertIn("Action done", wire.decode("utf-8"))
        receipt = json.loads(stdout.getvalue().encode("ascii"))
        self.assertEqual(receipt["model_draft"]["handoff"], "restrito: marcador incorreto")
        self.assertEqual(receipt["output"]["handoff"], "Audience: client \u00b7 Use: understand status \u00b7 Type: Reference")
        self.assertNotIn("restrito", receipt["output"]["handoff"])

if __name__ == "__main__": unittest.main()
