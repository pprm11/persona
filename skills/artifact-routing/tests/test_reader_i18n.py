"""Tests for the UI string dictionaries in assets/reader/reader.js. Run: python -I -X utf8 -m unittest discover -s tests"""
import os
import re
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
READER = os.path.join(HERE, "..", "assets", "reader", "reader.js")


def load():
    with open(READER, encoding="utf-8") as f:
        return f.read()


def dictionary(src, lang):
    """Return {key: raw JS string literal} for STRINGS.<lang>."""
    start = src.index("var STRINGS = {")
    end = src.index("var CAPTION_PREFIX", start)
    m = re.search(r"\n    %s: \{\n(.*?)\n    \}" % lang, src[start:end], re.S)
    assert m, lang
    out = {}
    for line in m.group(1).split("\n"):
        km = re.match(r'\s+(\w+): "((?:[^"\\]|\\.)*)",?\s*$', line)
        assert km, line
        out[km.group(1)] = km.group(2)
    return out


class ReaderI18nTests(unittest.TestCase):
    def setUp(self):
        self.src = load()
        self.en = dictionary(self.src, "en")
        self.pt = dictionary(self.src, "pt")

    def test_same_keys(self):
        self.assertEqual(set(self.en), set(self.pt))

    def test_no_empty_values(self):
        for name, d in (("en", self.en), ("pt", self.pt)):
            for k, v in d.items():
                self.assertTrue(v.strip(), "%s.%s is empty" % (name, k))

    def test_placeholders_match(self):
        for k in self.en:
            self.assertEqual(
                sorted(re.findall(r"\{\w+\}", self.en[k])),
                sorted(re.findall(r"\{\w+\}", self.pt[k])),
                k,
            )

    def test_every_looked_up_key_exists(self):
        used = set(re.findall(r'\bsay\("(\w+)"', self.src))
        for pair in re.findall(r'plural\([^"]*"(\w+)",\s*"(\w+)"\)', self.src):
            used |= set(pair)
        self.assertTrue(used)
        self.assertEqual(used - set(self.en), set())

    def test_caption_regex_accepts_figure_and_figura(self):
        m = re.search(r"var CAPTION_PREFIX = /(.*)/(\w*);", self.src)
        self.assertIsNotNone(m)
        rx = re.compile(m.group(1), re.I if "i" in m.group(2) else 0)
        for text, rest in (("Figure: Flow", "Flow"), ("Figura: Fluxo", "Fluxo"), ("figura: Fluxo", "Fluxo"), ("FIGURE:  X", "X")):
            self.assertEqual(rx.sub("", text), rest, text)
        self.assertEqual(rx.sub("", "Other: x"), "Other: x")

    def test_selection_and_override_present(self):
        self.assertIn("data-reader-strings", self.src)
        self.assertIn('indexOf("pt") === 0', self.src)


if __name__ == "__main__":
    unittest.main()
