"""Tests for scripts/privacy_scan.py. Run: python -I tests/test_privacy_scan.py"""
import contextlib
import io
import os
import sys
import tempfile
import subprocess
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import privacy_scan  # noqa: E402


def scan(text, args=(), ext="md"):
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "f." + ext)
        with open(p, "w", encoding="utf-8") as f:
            f.write(text)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = privacy_scan.main([p, *args])
        return code, out.getvalue()


class DetectionTests(unittest.TestCase):
    def test_never_prints_matched_values(self):
        values = ["sk-" + "abcdefghijklmnop1234", "https://u:" + "examplepass" + "@example.org/x", "-----BEGIN RSA " + "PRIVATE KEY-----"]
        for value in values:
            code, out = scan(value)
            self.assertEqual(code, 1)
            self.assertNotIn(value, out)

    def test_cli_stdout_and_stderr_never_contain_secret(self):
        secret = "sk-" + "abcdefghijklmnopqrstuv"
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "input.md")
            with open(path, "w", encoding="utf-8") as f: f.write(secret)
            script = os.path.join(os.path.dirname(privacy_scan.__file__), "privacy_scan.py")
            result = subprocess.run([sys.executable, script, path], input="", capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertNotIn(secret, result.stdout + result.stderr)
            self.assertIn("token", result.stdout)

    def test_clean(self):
        code, out = scan("Plain text, version 1.2.3, on 2026-10-28 at 10:30, 3 steps.\n")
        self.assertEqual(code, 0, out)
        self.assertIn("RESULT: CLEAN", out)

    def assertFound(self, text, kind, args=(), ext="md"):
        code, out = scan(text, args, ext)
        self.assertEqual(code, 1, out)
        self.assertIn(f": {kind}:", out)

    def test_email(self):
        self.assertFound("mail jane.doe@corp.example.org now", "email")

    def test_phone_e164_and_national(self):
        # Fixtures are split so the repository's own privacy gate (tests/test_onboard.py) does not flag this file.
        self.assertFound("call +1415" + "5550123 now", "phone")
        self.assertFound("call +44 20 " + "7946 0958 now", "phone")
        self.assertFound("call (415) 555-0123 now", "phone")
        self.assertFound("call 415-555-0123 now", "phone")
        self.assertFound("ring 020 " + "7946 0958 now", "phone")

    def test_card_needs_luhn(self):
        self.assertFound("card 4111 1111 1111 1111 ok", "card")
        self.assertFound("card 4111-1111-1111-1111 ok", "card")
        code, out = scan("order 4111 1111 1111 1112 here\n")
        self.assertEqual(code, 0, out)

    def test_tokens_and_keys(self):
        self.assertFound("key " + "sk-" + "abcdefghijklmnop1234", "token")
        self.assertFound("key " + "ghp_" + "abcdefghijklmnopqrstu", "token")
        self.assertFound("key " + "AKIA" + "ABCDEFGHIJKLMNOP", "token")  # split so repo secret scanners skip the fixture
        self.assertFound("API_KEY" + ' = "abcd1234efgh5678ijkl"', "token")

    def test_private_key(self):
        self.assertFound("-----BEGIN RSA " + "PRIVATE KEY-----", "private_key")
        self.assertFound("-----BEGIN " + "PRIVATE KEY-----", "private_key")

    def test_url_with_credentials(self):
        self.assertFound("postgres://user:" + "secret" + "@" + "db.host/x", "url_credentials")
        self.assertFound("https://bob:" + "hunter2@example.com/a", "url_credentials")
        code, out = scan("see https://example.com/a:b and http://host:8080/x\n")
        self.assertEqual(code, 0, out)

    def test_html_entities_and_attributes(self):
        self.assertFound('<a href="mailto:jane&#46;doe@corp.example.org">x</a>', "email", ext="html")
        self.assertFound('<a href="https://bob:' + 'hunter2@example.com/a">x</a>', "url_credentials", ext="html")


class PackAndAllowTests(unittest.TestCase):
    def test_br_patterns_are_opt_in(self):
        text = "cpf 123.456." + "789-09 and 551198" + "7654321 and 12.345." + "678/0001-95\n"
        self.assertEqual(scan(text)[0], 0)
        code, out = scan(text, ["--pack", "br"])
        self.assertEqual(code, 1)
        for kind in ("cpf", "phone_br", "cnpj"):
            self.assertIn(f": {kind}:", out)

    def test_allow_prefix_skips_synthetic(self):
        text = "number 556299" + "0012345 here\n"
        self.assertEqual(scan(text, ["--pack", "br"])[0], 1)
        self.assertEqual(scan(text, ["--pack", "br", "--allow-prefix", "55629900"])[0], 0)

    def test_allow_prefix_repeatable_and_works_for_generic(self):
        text = "+1415" + "5550123 and test.user@example.org\n"
        self.assertEqual(scan(text, ["--allow-prefix", "+1415555", "--allow-prefix", "test.user@"])[0], 0)
        self.assertEqual(scan(text, ["--allow-prefix", "+1415555"])[0], 1)

    def test_unknown_pack_is_usage_error(self):
        with self.assertRaises(SystemExit):
            with contextlib.redirect_stderr(io.StringIO()):
                scan("x", ["--pack", "zz"])

    def test_result_line_states_limits(self):
        _, out = scan("nothing\n")
        self.assertIn("not checked", out.lower())


if __name__ == "__main__":
    unittest.main()
