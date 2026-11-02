import importlib.util
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location("svg_gate", Path(__file__).resolve().parent.parent / "scripts" / "svg_gate.py")
svg_gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(svg_gate)


def page(label: str, x: int = 20, anchor: str = "start") -> str:
    return ('<svg viewBox="0 0 300 100"><rect x="10" y="10" width="200" height="40"/>'
            f'<text x="{x}" y="30" font-size="11" text-anchor="{anchor}">{label}</text></svg>')


class SvgGateTest(unittest.TestCase):
    def test_label_inside_its_box_passes(self):
        self.assertEqual(svg_gate.check(page("short label")), [])

    def test_label_wider_than_its_box_fails(self):
        problems = svg_gate.check(page("a label that is clearly far too long for a two hundred pixel box"))
        self.assertEqual(len(problems), 1)
        self.assertIn("box allows", problems[0])

    def test_label_outside_any_box_is_held_to_the_viewbox(self):
        html = '<svg viewBox="0 0 120 60"><text x="10" y="50" font-size="11">this caption runs past the edge</text></svg>'
        self.assertIn("viewBox allows", svg_gate.check(html)[0])

    def test_middle_anchor_is_measured_from_the_centre(self):
        self.assertEqual(svg_gate.check(page("centred", x=110, anchor="middle")), [])


if __name__ == "__main__":
    unittest.main()
