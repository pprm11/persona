"""Tests for scripts/mermaid/extract.py. Run: python -I tests/test_mermaid_extract.py"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "mermaid"))
import extract  # noqa: E402

MD = "# T\n\n```mermaid\nflowchart LR\n  A --> B\n```\n\ntext\n\n```mermaid\nsequenceDiagram\n  A->>B: hi\n```\n"
HTML = ('<main><figure><pre class="mermaid">flowchart LR\n  A --&gt; B\n</pre></figure>'
        "<pre class='mermaid x'>graph TD\n  C --&gt; D</pre><pre class=\"other\">not me</pre></main>")


class ExtractTests(unittest.TestCase):
    def test_default_output_is_current_directory(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "page.md")
            with open(p, "w", encoding="utf-8") as fh: fh.write(MD)
            old = os.getcwd()
            try:
                os.chdir(d)
                with contextlib.redirect_stdout(io.StringIO()): extract.main([p])
                self.assertTrue(os.path.isfile(os.path.join(d, "diagrams.json")))
            finally:
                os.chdir(old)

    def test_markdown_fences(self):
        b = extract.blocks_of("a.md", MD)
        self.assertEqual(len(b), 2)
        self.assertIn("A --> B", b[0])

    def test_html_pre_blocks_are_unescaped(self):
        b = extract.blocks_of("a.html", HTML)
        self.assertEqual(len(b), 2)
        self.assertIn("A --> B", b[0])
        self.assertIn("C --> D", b[1])
        self.assertNotIn("&gt;", b[0])

    def test_html_file_may_also_hold_fences_in_text(self):
        self.assertEqual(len(extract.blocks_of("a.htm", HTML)), 2)

    def test_zero_blocks_is_a_warning_not_ok(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.html")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write("<p>nothing</p>")
            err = io.StringIO()
            with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
                code = extract.main([p], out_dir=d)
            self.assertIn("warning", err.getvalue().lower())
            self.assertIn("no mermaid blocks", err.getvalue().lower())
            self.assertEqual(code, 0)

    def test_html_mentioning_mermaid_with_zero_blocks_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.html")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write('<div class="mermaid">flowchart LR\nA-->B</div>')
            with contextlib.redirect_stderr(io.StringIO()), contextlib.redirect_stdout(io.StringIO()):
                code = extract.main([p], out_dir=d)
            self.assertEqual(code, 1)

    def test_writes_json_with_basename_without_extension(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "page.html")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(HTML)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(extract.main([p], out_dir=d), 0)
            with open(os.path.join(d, "diagrams.json"), encoding="utf-8") as fh:
                data = json.load(fh)
            self.assertEqual([x["f"] for x in data], ["page", "page"])
            self.assertEqual([x["i"] for x in data], [1, 2])


if __name__ == "__main__":
    unittest.main()
