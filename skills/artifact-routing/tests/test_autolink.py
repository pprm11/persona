import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import autolink  # noqa: E402


def run(body, prefixes=None, internal_only=False):
    linker = autolink.AutoLinker(body, prefixes, internal_only)
    return linker.run(), linker


QS = """<h2>Questions</h2>
<ul>
<li>Q1. Which region do we use? Decide before launch.</li>
<li>Q13b. Narrow follow-up for the region.</li>
</ul>
"""


class IdTests(unittest.TestCase):
    def test_mention_becomes_ref_with_tip(self):
        out, _ = run(QS + "<p>See Q1 for the region.</p>")
        m = re.search(r'<a class="ref" href="#def-Q1" data-tip="([^"]*)">Q1</a>', out)
        self.assertIsNotNone(m)
        self.assertTrue(m.group(1).startswith("Q1 \u00b7 Which region do we use?"))

    def test_anchor_on_definition_line(self):
        out, _ = run(QS)
        self.assertIn('<li><span class="defid" id="def-Q1">Q1</span>. Which region', out)

    def test_letter_suffix_links_and_anchors(self):
        out, lk = run(QS + "<p>Also Q13b.</p>")
        self.assertIn('id="def-Q13b"', out)
        self.assertIn('href="#def-Q13b"', out)
        self.assertNotIn("Q13b", lk.undefined)

    def test_table_cell_that_only_mentions_does_not_get_the_anchor(self):
        html = ("<table><tr><th>Assumption</th><th>Replaces</th></tr>"
                "<tr><td>A1</td><td>Q1</td></tr></table>" + QS)
        out, lk = run(html)
        self.assertEqual(out.count('id="def-Q1"'), 1)
        self.assertIn('<li><span class="defid" id="def-Q1">Q1</span>.', out)
        self.assertIn('<td><a class="ref" href="#def-Q1"', out)
        self.assertEqual(autolink.check_anchors(out), [])

    def test_table_row_definition_when_first_cell_is_id(self):
        html = "<table><tr><td>D1</td><td>Use one database. Cheaper.</td></tr></table><p>Per D1 we agreed.</p>"
        out, _ = run(html)
        self.assertIn('<td><span class="defid" id="def-D1">D1</span></td>', out)
        self.assertIn('href="#def-D1"', out)

    def test_list_definition_beats_table_row(self):
        html = "<table><tr><td>Q1</td><td>Mention row</td></tr></table>" + QS
        out, lk = run(html)
        self.assertIn('<li><span class="defid" id="def-Q1">Q1</span>.', out)
        self.assertNotIn('<td><span class="defid"', out)
        self.assertIn("Q1", lk.dups)

    def test_explicit_defid(self):
        html = '<p><span class="defid">L7</span> Latency budget is 200 ms.</p><p>Check L7.</p>'
        out, _ = run(html)
        self.assertIn('<span id="def-L7" class="defid">L7</span>', out)
        self.assertIn('data-tip="L7 \u00b7 Latency budget is 200 ms."', out)

    def test_undefined_id_is_reported(self):
        out, lk = run("<p>We rely on Q99 here.</p>")
        self.assertIn('<span class="ref missing"', out)
        self.assertEqual(lk.undefined, {"Q99"})

    def test_custom_prefixes(self):
        html = "<ul><li>R1. First risk.</li></ul><p>R1 and Q1.</p>"
        out, lk = run(html, prefixes=["R"])
        self.assertIn('href="#def-R1"', out)
        self.assertNotIn("Q1</a>", out)
        self.assertEqual(lk.undefined, set())

    def test_guards_keep_lookalikes_as_text(self):
        out, lk = run("<p>The A1 context and XQ1 and Q1-2 stay text.</p>")
        self.assertNotIn("<a ", out)
        self.assertEqual(lk.undefined, set())


class SkipTests(unittest.TestCase):
    def test_never_inside_code_pre_heading_link_diagram(self):
        html = (QS + "<p><code>Q1</code></p><pre>Q1</pre><h3>About Q1</h3>"
                '<p><a href="#x">Q1</a></p><div class="diagram">Q1 here</div>'
                '<p id="x">ok</p>')
        out, _ = run(html)
        self.assertIn("<code>Q1</code>", out)
        self.assertIn("<pre>Q1</pre>", out)
        self.assertIn("<h3>About Q1</h3>", out)
        self.assertIn('<a href="#x">Q1</a>', out)
        self.assertIn('<div class="diagram">Q1 here</div>', out)

    def test_script_and_style_untouched(self):
        html = QS + "<script>var s = 'Q1' < 3;</script><style>.Q1{}</style>"
        out, _ = run(html)
        self.assertIn("<script>var s = 'Q1' < 3;</script>", out)

    def test_first_occurrence_per_block(self):
        out, _ = run(QS + "<p>Q1 then Q1 again.</p><p>Q1 in the next paragraph.</p>")
        para1 = re.search(r"<p><a[^>]*>Q1</a> then.*?</p>", out).group(0)
        self.assertEqual(para1.count("<a "), 1)
        self.assertEqual(out.count('<a class="ref" href="#def-Q1"'), 2)

    def test_first_occurrence_per_list_item_and_cell(self):
        html = QS + "<ul><li>Q1 Q1</li><li>Q1</li></ul><table><tr><td>Q1 Q1</td><td>Q1</td></tr></table>"
        out, _ = run(html)
        self.assertEqual(out.count('<a class="ref" href="#def-Q1"'), 4)

    def test_idempotent(self):
        once, _ = run(QS + "<p>See Q1 and Q99.</p>")
        twice, lk = run(once)
        self.assertEqual(once, twice)
        self.assertEqual(lk.undefined, {"Q99"})


GLOSS = ('<table data-glossary><thead><tr><th>Term</th><th>Definition</th></tr></thead><tbody>'
         '<tr><td>Variant</td><td>One arm of an experiment. It receives a share of traffic.</td></tr>'
         '<tr><td>Variant group</td><td>A set of variants tested together.</td></tr>'
         '<tr><td>Box</td><td>A container.</td></tr></tbody></table>')


class TermTests(unittest.TestCase):
    def test_term_cells_get_anchor_and_mentions_link(self):
        out, _ = run(GLOSS + "<p>Each Variant gets traffic.</p>")
        self.assertIn('<td><span class="defterm" id="term-variant">Variant</span></td>', out)
        self.assertIn('<a class="term" href="#term-variant" data-tip="Variant \u00b7 One arm of an experiment. '
                      'It receives a share of traffic.">Variant</a>', out)
        self.assertEqual(autolink.check_anchors(out), [])

    def test_plural_suffix(self):
        out, _ = run(GLOSS + "<p>Two Variants and three Boxes.</p>")
        self.assertIn(">Variants</a>", out)
        self.assertIn(">Boxes</a>", out)

    def test_longest_term_first(self):
        out, _ = run(GLOSS + "<p>A Variant group runs.</p>")
        self.assertIn('href="#term-variant-group"', out)
        self.assertNotIn('href="#term-variant">Variant</a> group', out)

    def test_case_sensitive_and_first_per_block(self):
        out, _ = run(GLOSS + "<p>variant is lower. Box and Box.</p>")
        self.assertNotIn(">variant</a>", out)
        self.assertEqual(out.count('<a class="term" href="#term-box"'), 1)

    def test_terms_skip_headings_and_code(self):
        out, _ = run(GLOSS + "<h2>Variant</h2><p><code>Box</code></p>")
        self.assertIn("<h2>Variant</h2>", out)
        self.assertIn("<code>Box</code>", out)

    def test_glossary_term_cell_itself_not_linked(self):
        out, _ = run(GLOSS)
        self.assertEqual(out.count('id="term-variant"'), 1)
        self.assertNotIn('<a class="term" href="#term-variant">', out)
        self.assertNotIn('<span class="defterm" id="term-variant"><a', out)


ABBR = ('<table data-abbr><tr><th>Abbreviation</th><th>Expansion</th></tr>'
        '<tr><td>TTL</td><td>Time to live</td></tr></table>')


class AbbrTests(unittest.TestCase):
    def test_first_use_only(self):
        out, _ = run(ABBR + "<p>Set the TTL. Then the TTL expires.</p><p>TTL again.</p>")
        self.assertEqual(out.count('<abbr title="Time to live">TTL</abbr>'), 1)
        self.assertIn("<td>TTL</td>", out)

    def test_not_inside_code_or_heading(self):
        out, _ = run(ABBR + "<h2>TTL</h2><p><code>TTL</code></p>")
        self.assertNotIn("<abbr", out)


class ExternalTests(unittest.TestCase):
    def test_external_gets_target_and_rel(self):
        out, _ = run('<p><a href="https://example.org/x">site</a> <a href="#a">in</a><span id="a"></span></p>')
        self.assertIn('<a href="https://example.org/x" target="_blank" rel="noopener">', out)
        self.assertIn('<a href="#a">', out)

    def test_existing_rel_is_extended(self):
        out, _ = run('<a href="https://example.org" rel="nofollow">x</a>')
        self.assertIn('rel="nofollow noopener"', out)
        self.assertIn('target="_blank"', out)

    def test_internal_only_reports_and_does_not_decorate(self):
        out, lk = run('<a href="https://example.org/x">site</a>', internal_only=True)
        self.assertEqual(lk.external, ["https://example.org/x"])
        self.assertNotIn("target=", out)


class CliTests(unittest.TestCase):
    def _cli(self, html, *extra):
        with tempfile.TemporaryDirectory() as d:
            src, dst = os.path.join(d, "in.html"), os.path.join(d, "out.html")
            with open(src, "w", encoding="utf-8") as f:
                f.write(html)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = autolink.main([src, "-o", dst, *extra])
            with open(dst, encoding="utf-8") as f:
                return code, buf.getvalue(), f.read()

    def test_clean_page_exits_zero(self):
        code, out, _ = self._cli(QS + "<p>See Q1.</p>")
        self.assertEqual(code, 0)
        self.assertIn("undefined IDs: []", out)
        self.assertIn("broken anchors: []", out)

    def test_undefined_exits_nonzero(self):
        code, out, _ = self._cli("<p>See Q5.</p>")
        self.assertEqual(code, 1)
        self.assertIn("['Q5']", out)

    def test_broken_anchor_exits_nonzero(self):
        code, out, _ = self._cli('<p><a href="#nowhere">go</a></p>')
        self.assertEqual(code, 1)
        self.assertIn("['nowhere']", out)

    def test_internal_only_exit(self):
        code, out, _ = self._cli('<p><a href="https://example.org">x</a></p>', "--internal-only")
        self.assertEqual(code, 1)
        self.assertIn("example.org", out)

    def test_check_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "in.html")
            with open(src, "w", encoding="utf-8") as f:
                f.write(QS)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(autolink.main([src, "--check"]), 0)
            self.assertEqual(os.listdir(d), ["in.html"])


DL = ('<dl><dt class="defterm" id="term-archive">Archive</dt>'
      '<dd>A sealed copy kept for audit. It never changes.</dd>'
      '<dt class="defterm" id="term-run-log" data-aliases="log file, journal">Run log</dt>'
      '<dd>The record of one run.</dd></dl>')


class DefinitionListTests(unittest.TestCase):
    def test_dl_terms_are_collected_and_linked(self):
        out, lk = run(DL + "<p>Each Archive is signed.</p>")
        self.assertEqual(set(lk.terms), {"Archive", "Run log"})
        self.assertIn('<a class="term" href="#term-archive" data-tip="Archive \u00b7 A sealed copy kept for audit. '
                      'It never changes.">Archive</a>', out)
        self.assertEqual(autolink.check_anchors(out), [])

    def test_dl_term_itself_is_not_linked_and_dd_is_linked(self):
        out, _ = run(DL + "<dl><dt>Other</dt><dd>See Archive here.</dd></dl>")
        self.assertIn('<dt class="defterm" id="term-archive">Archive</dt>', out)
        self.assertIn('<dd>See <a class="term" href="#term-archive"', out)

    def test_dl_alias_links_to_the_term(self):
        out, _ = run(DL + "<p>Read the journal first.</p>")
        self.assertIn('<a class="term" href="#term-run-log"', out)
        self.assertIn(">journal</a>", out)

    def test_dl_term_without_id_gets_the_reader_slug(self):
        out, lk = run('<dl><dt class="defterm">Caf\u00e9 menu</dt><dd>What is on offer.</dd></dl><p>The Caf\u00e9 menu.</p>')
        self.assertIn('<dt id="term-caf-menu" class="defterm">', out)
        self.assertIn('href="#term-caf-menu"', out)
        self.assertEqual(autolink.check_anchors(out), [])

    def test_check_summary_counts_dl_terms(self):
        with tempfile.TemporaryDirectory() as d:
            src = os.path.join(d, "in.html")
            with open(src, "w", encoding="utf-8") as f:
                f.write(DL + GLOSS)
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                autolink.main([src, "--check"])
        self.assertIn("glossary terms: 5", buf.getvalue())

    def test_dl_run_twice_is_stable(self):
        once, _ = run(DL + "<p>The Archive and the Archives.</p>")
        twice, _ = run(once)
        self.assertEqual(once, twice)


class IdempotenceTests(unittest.TestCase):
    def test_plural_after_existing_link_stays_plain(self):
        once, _ = run(DL + "<p>The Archive holds Archives.</p>")
        self.assertEqual(once.count('<a class="term" href="#term-archive"'), 1)
        twice, _ = run(once)
        self.assertEqual(once, twice)

    def test_hand_written_link_counts_as_first_mention(self):
        html = DL + '<p>Plain Archives, then <a href="#term-archive">the archive</a>, then Archive.</p>'
        out, _ = run(html)
        self.assertEqual(out.count("<a "), 1)

    def test_link_to_alias_counts_for_the_term(self):
        html = DL + '<p><a href="#term-run-log">the journal</a> and the Run log.</p>'
        out, _ = run(html)
        self.assertEqual(out.count("<a "), 1)

    def test_other_block_still_gets_its_link(self):
        html = DL + '<p><a href="#term-archive">archive</a> Archive</p><p>Archive</p>'
        out, _ = run(html)
        self.assertEqual(out.count("<a "), 2)

    def test_repeated_id_after_existing_ref_stays_plain(self):
        once, _ = run(QS + "<p>Q1 then Q1 again.</p>")
        twice, _ = run(once)
        self.assertEqual(once, twice)
        html = QS + '<p><a href="#def-Q1">Q1</a> and Q1.</p>'
        out, _ = run(html)
        self.assertEqual(out.count("<a "), 1)

    def test_whole_page_second_run_changes_nothing(self):
        page = (QS + GLOSS + DL + ABBR + "<table><tr><td>D1</td><td>One database.</td></tr></table>"
                "<p>Q1, D1, Variant, Variants, Archive, Archives, journal, TTL and TTL.</p>"
                "<ul><li>Box then Boxes. Archive.</li></ul>")
        once, _ = run(page)
        twice, _ = run(once)
        self.assertEqual(once, twice)


MEANING = ('<table><thead><tr><th>ID</th><th>Name</th><th>{hdr}</th></tr></thead><tbody>'
           '<tr><td>D1</td><td>One database</td><td>{body}</td></tr></tbody></table><p>Per D1.</p>')


class PopoverTextTests(unittest.TestCase):
    def tip(self, out, href="#def-D1"):
        return re.search(r'<a class="ref" href="' + href + r'" data-tip="([^"]*)"', out).group(1)

    def test_name_and_meaning(self):
        out, _ = run(MEANING.format(hdr="Meaning", body="Cheaper to run."))
        self.assertEqual(self.tip(out), "D1 \u00b7 One database \u00b7 Cheaper to run.")

    def test_header_match_is_case_insensitive_and_covers_three_names(self):
        for hdr in ("DESCRIPTION", "definition", " Meaning "):
            out, _ = run(MEANING.format(hdr=hdr, body="Cheaper."))
            self.assertEqual(self.tip(out), "D1 \u00b7 One database \u00b7 Cheaper.", hdr)

    def test_other_header_adds_nothing(self):
        out, _ = run(MEANING.format(hdr="Owner", body="Platform team"))
        self.assertEqual(self.tip(out), "D1 \u00b7 One database")

    def test_long_meaning_is_trimmed_to_about_160(self):
        out, _ = run(MEANING.format(hdr="Meaning", body="word " * 80))
        body = self.tip(out)[len("D1 \u00b7 "):]
        self.assertLessEqual(len(body), 161)
        self.assertTrue(body.endswith("\u2026"))
        self.assertTrue(body.startswith("One database \u00b7 word"))

    def test_meaning_in_second_column_is_not_repeated(self):
        html = ('<table><thead><tr><th>ID</th><th>Meaning</th></tr></thead><tbody>'
                '<tr><td>D1</td><td>Use one database.</td></tr></tbody></table><p>Per D1.</p>')
        out, _ = run(html)
        self.assertEqual(self.tip(out), "D1 \u00b7 Use one database.")

    def test_reader_split_keeps_id_as_header(self):
        out, _ = run(MEANING.format(hdr="Meaning", body="Cheaper."))
        tip = self.tip(out)
        self.assertEqual(tip[:tip.index(" \u00b7 ")], "D1")

    def test_explicit_defid_cell_uses_the_meaning_column_too(self):
        html = ('<table><thead><tr><th>ID</th><th>Name</th><th>Meaning</th></tr></thead><tbody>'
                '<tr><td><span class="defid">D1</span></td><td>One database</td><td>Cheaper.</td></tr>'
                '</tbody></table><p>Per D1.</p>')
        out, _ = run(html)
        self.assertEqual(self.tip(out), "D1 \u00b7 One database \u00b7 Cheaper.")


class SlugTests(unittest.TestCase):
    CASES = {
        "Variant": "term-variant",
        "Variant group": "term-variant-group",
        "Caf\u00e9": "term-caf",
        "Na\u00efve Bayes": "term-na-ve-bayes",
        "Stra\u00dfe": "term-stra-e",
        "A/B test": "term-a-b-test",
        "C++": "term-c",
        "  Spaced   out  ": "term-spaced-out",
        "\u00dcn\u00ef\u2013c\u00f6d\u00e9": "term-n-c-d",
        "???": "term-section",
    }

    def test_known_terms(self):
        for term, want in self.CASES.items():
            self.assertEqual(autolink.slug(term), want, term)

    def test_page_anchor_matches_slug(self):
        html = ('<table data-glossary><tr><td>Caf\u00e9 au lait</td><td>Coffee with milk.</td></tr></table>'
                '<p>Order a Caf\u00e9 au lait.</p>')
        out, _ = run(html)
        self.assertIn('id="term-caf-au-lait"', out)
        self.assertEqual(autolink.check_anchors(out), [])

    def test_slug_collision_is_warned(self):
        html = ('<table data-glossary><tr><td>Caf\u00e9</td><td>One.</td></tr><tr><td>Caf</td><td>Two.</td></tr></table>')
        _, lk = run(html)
        self.assertTrue(any("term-caf" in w for w in lk.warnings))

    @unittest.skipUnless(shutil.which("node"), "node not installed")
    def test_matches_reader_js(self):
        reader = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "reader", "reader.js")
        with open(reader, encoding="utf-8") as f:
            m = re.search(r"function slug\(s\) \{.*?\n  \}", f.read(), re.S)
        self.assertIsNotNone(m)
        terms = list(self.CASES) + ["\u00c5ngstr\u00f6m unit", "\u03a9mega 2", "na\u00efve \u2014 caf\u00e9", "a_b", "x.y.z", "\u65e5\u672c\u8a9e term", "\u0130stanbul"]
        script = m.group(0) + "\nconsole.log(JSON.stringify(%s.map(function (t) { return 'term-' + slug(t); })));" % json.dumps(terms)
        res = subprocess.run(["node", "-e", script], capture_output=True, text=True, encoding="utf-8", check=True)
        self.assertEqual(json.loads(res.stdout), [autolink.slug(t) for t in terms])


class PrefixTests(unittest.TestCase):
    PAGE = ("<ul><li>ADR-3. Use queues. Because they decouple.</li><li>CMD2. Start the job.</li>"
            "<li>A1. Single letter.</li></ul>")

    def test_default_prefixes_unchanged(self):
        self.assertEqual(autolink.DEFAULT_PREFIXES, ["G", "A", "Q", "D", "L", "P"])

    def test_multi_letter_and_dash_prefixes(self):
        out, lk = run(self.PAGE + "<p>See ADR-3, CMD2 and ERR-9.</p>", prefixes=["ADR-", "CMD", "ERR-"])
        self.assertIn('<a class="ref" href="#def-ADR-3" data-tip="ADR-3 \u00b7 Use queues.', out)
        self.assertIn('href="#def-CMD2"', out)
        self.assertEqual(lk.undefined, {"ERR-9"})
        self.assertEqual(autolink.check_anchors(out), [])

    def test_longest_prefix_wins_over_shorter_one(self):
        out, lk = run(self.PAGE + "<p>ADR-3 and A1.</p>", prefixes=["A", "ADR-"])
        self.assertIn('href="#def-ADR-3"', out)
        self.assertIn('href="#def-A1"', out)
        self.assertEqual(lk.undefined, set())

    def test_dash_prefix_with_suffix_letter_and_guards(self):
        html = "<ul><li>ADR-12b. Narrow.</li></ul><p>ADR-12b, xADR-12 and ADR-12-2 and ADR-12c.</p>"
        out, lk = run(html, prefixes=["ADR-"])
        self.assertIn('href="#def-ADR-12b"', out)
        self.assertEqual(lk.undefined, {"ADR-12c"})

    def test_parse_prefixes_accepts_and_rejects(self):
        self.assertEqual(autolink.parse_prefixes(["ADR-", "CMD", "OPT"]), ["ADR-", "CMD", "OPT"])
        self.assertEqual(autolink.parse_prefixes(["ADR-,CMD"]), ["ADR-", "CMD"])
        for bad in (["bad prefix"], ["A.B"], [""], ["-A"], ["A--"], ["1A"]):
            with self.assertRaises(ValueError, msg=bad):
                autolink.parse_prefixes(bad)

    def test_cli_accepts_prefixes(self):
        with tempfile.TemporaryDirectory() as d:
            src, dst = os.path.join(d, "in.html"), os.path.join(d, "out.html")
            with open(src, "w", encoding="utf-8") as f:
                f.write(self.PAGE + "<p>ADR-3 and CMD2.</p>")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = autolink.main([src, "-o", dst, "--prefixes", "ADR-", "CMD"])
            self.assertEqual(code, 0)
            self.assertIn("IDs defined: 2", buf.getvalue())


if __name__ == "__main__":
    unittest.main()
