"""Tests for scripts/preserve.py. Run: python -I tests/test_preserve.py"""
import contextlib
import io
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import preserve  # noqa: E402


def run(a, b, args=(), ext="md"):
    with tempfile.TemporaryDirectory() as d:
        pa, pb = os.path.join(d, "a." + ext), os.path.join(d, "b." + ext)
        for path, text in ((pa, a), (pb, b)):
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = preserve.main([pa, pb, *args])
        return code, out.getvalue()


class MarkdownTests(unittest.TestCase):
    def test_identical_ok(self):
        code, out = run("# H\n\nSee Q1 and 42 `x`.\n", "# H\n\nSee Q1 and 42 `x`.\n")
        self.assertEqual(code, 0, out)

    def test_lost_default_prefix_id(self):
        code, out = run("# H\n\nSee Q1 and Q2.\n", "# H\n\nSee Q1.\n")
        self.assertEqual(code, 1)
        self.assertIn("LOST id", out)

    def test_custom_prefixes(self):
        a, b = "# H\n\nSee CMD3 and ADR-12.\n", "# H\n\nSee CMD3.\n"
        self.assertEqual(run(a, b)[0], 0)  # not in the defaults, so not tracked
        code, out = run(a, b, ["--prefixes", "CMD", "ADR-"])
        self.assertEqual(code, 1)
        self.assertIn("ADR-12", out)

    def test_custom_tags(self):
        a, b = "# H\n\nText [UNTESTED] more [SAMPLE: x].\n", "# H\n\nText more.\n"
        self.assertEqual(run(a, b)[0], 0)
        code, out = run(a, b, ["--tags", "UNTESTED", "SAMPLE"])
        self.assertEqual(code, 1)
        self.assertIn("LOST tag", out)

    def test_added_number_fails(self):
        code, out = run("# H\n\nTen 10.\n", "# H\n\nTen 10 and 11.\n")
        self.assertEqual(code, 1)
        self.assertIn("ADDED number", out)

    def test_lost_url_and_code(self):
        code, out = run("# H\n\n[a](http://x.y/z)\n\n```\ncode\n```\n", "# H\n\ntext\n")
        self.assertEqual(code, 1)
        self.assertIn("LOST url", out)
        self.assertIn("LOST code", out)

    def test_legacy_flag_keeps_old_behavior(self):
        a, b = "# H\n\nSee BR12 and [LIVE: ok].\n", "# H\n\nSee nothing.\n"
        self.assertEqual(run(a, b)[0], 0)
        code, out = run(a, b, ["--legacy"])
        self.assertEqual(code, 1)
        self.assertIn("BR12", out)


HTML_A = """<html><body><script>var Q9 = 1;</script><h2 id="x">Setup</h2>
<p>Run <code>make all</code> with 3 workers. See <a href="https://e.com/a">docs</a> and S2.</p>
<pre>line one
line two</pre><p>Tag [UNTESTED].</p></body></html>"""


class HtmlTests(unittest.TestCase):
    def test_html_identical_ok(self):
        self.assertEqual(run(HTML_A, HTML_A, ["--prefixes", "S"], "html")[0], 0)

    def test_html_lost_heading_code_link_id_number(self):
        b = "<p>Run with workers.</p>"
        code, out = run(HTML_A, b, ["--prefixes", "S", "--tags", "UNTESTED"], "html")
        self.assertEqual(code, 1)
        for kind in ("heading", "code", "inline", "url", "id", "tag"):
            self.assertIn("LOST " + kind, out, out)

    def test_html_script_text_ignored_and_inpage_links_ignored(self):
        b = HTML_A.replace("S2", '<a class="ref" href="#def-S2">S2</a>').replace("var Q9 = 1;", "var Q9 = 2;")
        self.assertEqual(run(HTML_A, b, ["--prefixes", "S"], "html")[0], 0)

    def test_html_number_added(self):
        b = HTML_A.replace("3 workers", "3 workers and 5 more")
        code, out = run(HTML_A, b, ["--prefixes", "S"], "html")
        self.assertEqual(code, 1)
        self.assertIn("ADDED number", out)

    def test_html_entities_decoded(self):
        a = "<p>A &amp; B costs 5 &lt; 6</p>"
        self.assertEqual(run(a, "<p>A & B costs 5 < 6</p>", [], "html")[0], 0)


if __name__ == "__main__":
    unittest.main()
