"""Tests for the fix round: prefixes from the page, shared skip list, glossary aliases column."""
import contextlib
import io
import os
import re
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import autolink  # noqa: E402

PAGE = """<main data-id-prefixes="S,ADR-">
<ul><li>S1. Step one. Do it.</li><li>ADR-12. Decision. Chosen.</li></ul>
<p>See S1 and ADR-12 and D3.</p>
</main>"""


def run_cli(args):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        code = autolink.main(args)
    return code, buf.getvalue()


class PagePrefixTests(unittest.TestCase):
    def test_page_prefixes_read_from_main(self):
        self.assertEqual(autolink.page_prefixes('<div data-id-prefixes="X"></div><main id="m" data-id-prefixes="S, ADR-">'),
                         ["S", "ADR-"])
        self.assertEqual(autolink.page_prefixes("<main></main>"), [])

    def test_cli_without_flag_uses_page_prefixes(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "in.html")
            with open(src, "w", encoding="utf-8") as f:
                f.write(PAGE)
            code, out = run_cli([src, "--check"])
            self.assertEqual(code, 0, out)
            self.assertIn("IDs defined: 2", out)

    def test_explicit_flag_wins(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "in.html")
            with open(src, "w", encoding="utf-8") as f:
                f.write(PAGE)
            code, out = run_cli([src, "--check", "--prefixes", "D"])
            self.assertEqual(code, 1, out)
            self.assertIn("D3", out)

    def test_default_when_neither(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "in.html")
            with open(src, "w", encoding="utf-8") as f:
                f.write("<ul><li>Q1. Why. Because.</li></ul><p>Q1</p>")
            code, out = run_cli([src, "--check"])
            self.assertEqual(code, 0, out)
            self.assertIn("IDs defined: 1", out)


class SkipTests(unittest.TestCase):
    def _linked(self, wrapper_open, wrapper_close):
        body = ('<ul><li>Q1. Why. Because.</li></ul>' + wrapper_open + "Q1 and Widget" + wrapper_close +
                '<table data-glossary><tr><td>Widget</td><td>A thing.</td></tr></table>')
        out, _ = autolink.AutoLinker(body, ["Q"]).run(), None
        return out

    def test_skipped_containers(self):
        for o, c in (('<p><span class="tag">', "</span></p>"), ("<nav><p>", "</p></nav>"),
                     ('<p data-no-link>', "</p>"), ('<div class="figbar"><p>', "</p></div>"),
                     ('<p class="hlink">', "</p>"), ('<p class="copy">', "</p>"), ('<div class="pop"><p>', "</p></div>"),
                     ("<select><option>", "</option></select>")):
            with self.subTest(o=o):
                out = self._linked(o, c)
                inner = out[out.index(o):out.index(c, out.index(o)) + len(c)]
                self.assertNotIn("<a ", inner)

    def test_normal_paragraph_still_linked(self):
        out = self._linked("<p>", "</p>")
        self.assertIn('class="ref"', out)

    def test_docstring_lists_skip_set(self):
        for word in ("nav", "data-no-link", ".tag", ".figbar"):
            self.assertIn(word, autolink.__doc__)


class AliasColumnTests(unittest.TestCase):
    TABLE = ('<table data-glossary><thead><tr><th>Term</th><th>Definition</th><th>ALIASES</th></tr></thead>'
             '<tr><td>Widget</td><td>A thing.</td><td>gadget, gizmo</td></tr></table>')

    def test_aliases_column_links_synonyms(self):
        out = autolink.AutoLinker(self.TABLE + "<p>The gizmo works.</p>", ["Q"]).run()
        self.assertRegex(out, r'<a class="term" href="#term-widget"[^>]*>gizmo</a>')

    def test_no_aliases_column_unchanged(self):
        t = '<table data-glossary><tr><td>Widget</td><td>A thing.</td></tr></table><p>The gizmo works.</p>'
        out = autolink.AutoLinker(t, ["Q"]).run()
        self.assertNotIn(">gizmo</a>", out)

    def test_data_aliases_attribute_still_works(self):
        dl = '<dl><dt class="defterm" data-aliases="gizmo">Widget</dt><dd>A thing.</dd></dl><p>The gizmo works.</p>'
        out = autolink.AutoLinker(dl, ["Q"]).run()
        self.assertRegex(out, r'<a class="term" href="#term-widget"[^>]*>gizmo</a>')


class BuildPageAgreementTests(unittest.TestCase):
    def test_build_page_and_autolink_agree(self):
        import build_page
        for src in ('<div data-id-prefixes="X"></div><main id="m" data-id-prefixes="S, ADR-">',
                    "<main></main>", "<p data-id-prefixes='Z'>no main</p>", "<main data-id-prefixes='R,Q'>"):
            self.assertEqual(build_page.page_prefixes(src), autolink.page_prefixes(src), src)


if __name__ == "__main__":
    unittest.main()
