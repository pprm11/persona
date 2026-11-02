"""Tests for scripts/build_page.py. Run from the skill folder: python -I tests/test_build_page.py"""
import pathlib
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(SKILL / "scripts"))
import build_page  # noqa: E402

LEAN = """<title>T</title>
<style>
body { color: red; }
/* reader.css */
/* /reader.css */
</style>
<div class="reader-root" lang="en"><main id="main" data-reader="all" data-id-prefixes="R,ADR-">
<h2>Defs</h2>
<ul><li><span class="defid" id="def-R1">R1</span>. Rule one. First rule.</li><li><span class="defid" id="def-ADR-1">ADR-1</span>. Decision. We decided.</li></ul>
<p>See R1 and ADR-1.</p>
<table data-glossary><tr><td>Widget</td><td>A thing.</td></tr></table>
<p>A Widget appears here.</p>
</main></div>
<script>
// reader.js
// /reader.js
</script>
"""


class InlineTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        (self.dir / "reader.css").write_text(".x { top: 0; }\n", encoding="utf-8")
        (self.dir / "reader.js").write_text("var a = 1;\n", encoding="utf-8")

    def test_inlines_between_markers(self):
        out = build_page.inline_reader(LEAN, self.dir)
        self.assertIn("/* reader.css */\n.x { top: 0; }\n/* /reader.css */", out)
        self.assertIn("// reader.js\nvar a = 1;\n// /reader.js", out)
        self.assertIn("body { color: red; }", out)

    def test_rebuild_is_idempotent(self):
        once = build_page.inline_reader(LEAN, self.dir)
        twice = build_page.inline_reader(once, self.dir)
        self.assertEqual(once, twice)

    def test_replaces_old_reader(self):
        old = LEAN.replace("// reader.js\n", "// reader.js\nvar stale = 0;\n")
        out = build_page.inline_reader(old, self.dir)
        self.assertNotIn("stale", out)

    def test_missing_marker_fails(self):
        with self.assertRaises(build_page.BuildError):
            build_page.inline_reader(LEAN.replace("// /reader.js", ""), self.dir)

    def test_duplicate_marker_fails(self):
        with self.assertRaises(build_page.BuildError):
            build_page.inline_reader(LEAN + "\n// reader.js\n// /reader.js\n", self.dir)

    def test_script_close_in_reader_fails(self):
        (self.dir / "reader.js").write_text("var s = '</script>';\n", encoding="utf-8")
        with self.assertRaises(build_page.BuildError):
            build_page.inline_reader(LEAN, self.dir)

    def test_page_prefixes(self):
        self.assertEqual(build_page.page_prefixes(LEAN), ["R", "ADR-"])
        self.assertEqual(build_page.page_prefixes("<main>"), [])


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = pathlib.Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        self.src = self.dir / "lean.html"
        self.src.write_text(LEAN, encoding="utf-8")

    def test_plain_build(self):
        out = self.dir / "sub" / "out.html"
        self.assertEqual(build_page.main([str(self.src), "-o", str(out)]), 0)
        text = out.read_text(encoding="utf-8")
        self.assertGreater(len(text), len(LEAN))
        self.assertNotIn('class="ref"', text)

    def test_autolink_build_links_ids_and_terms(self):
        out = self.dir / "out.html"
        self.assertEqual(build_page.main([str(self.src), "-o", str(out), "--autolink"]), 0)
        text = out.read_text(encoding="utf-8")
        self.assertIn('class="ref" href="#def-R1"', text)
        self.assertIn('class="term" href="#term-widget"', text)

    def test_missing_marker_exit_1(self):
        bad = self.dir / "bad.html"
        bad.write_text("<style></style>", encoding="utf-8")
        self.assertEqual(build_page.main([str(bad), "-o", str(self.dir / "o.html")]), 1)

    def test_undefined_id_makes_autolink_fail(self):
        bad = self.dir / "undef.html"
        bad.write_text(LEAN.replace("<p>See R1", "<p>See R9, R1"), encoding="utf-8")
        self.assertEqual(build_page.main([str(bad), "-o", str(self.dir / "o.html"), "--autolink"]), 1)


if __name__ == "__main__":
    unittest.main()
