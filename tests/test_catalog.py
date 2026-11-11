from pathlib import Path
import tempfile
import os
import unittest
from catalog_audit import audit_file, release, candidate_files

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / 'skills'
EXPECTED = set('brief root-cause critical-code-review staged-engineering humanize humanize-heavy cross-harness-orchestration claude-workflow-orchestration inline-widgets clean-architecture artifact-routing tree-search task-cards measured-correction context-ingest context-recall session-closeout python-idioms pull-request-description pull-request-review publish-pull-request decision-rfc secret-backup outcome-driven-development explained-by-cats'.split())

class CatalogTests(unittest.TestCase):
    def test_catalog(self):
        self.assertEqual(EXPECTED, {p.name for p in SKILLS.iterdir() if p.is_dir()})
        catalog = (ROOT/'README.md').read_text(encoding='utf-8')
        for name in EXPECTED:
            self.assertIn(f'](skills/{name}/SKILL.md)', catalog)
            self.assertTrue((SKILLS/name/'SKILL.md').is_file())

    def test_every_public_text_resource(self):
        for relative in candidate_files(ROOT):
            file = ROOT / relative
            if file.is_file():
                terms = os.environ.get('PERSONA_PRIVATE_TERMS', '').split('|')
                self.assertEqual([], audit_file(file, [x for x in terms if x]), str(file))

    def test_release_requires_private_patterns(self):
        self.assertEqual(2, release(ROOT, None))
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'patterns.json'
            p.write_text('[]', encoding='utf-8')
            self.assertEqual(2, release(ROOT, str(p)))
            p.write_text('["["]', encoding='utf-8')
            self.assertEqual(2, release(ROOT, str(p)))

    def test_fenced_links_and_privacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "document.md"
            cases = [
                ("```inline code```\n[after](missing.md)\n", ["broken link: missing.md"]),
                ("[before](missing.md)\n```md\n[hidden](...)\n", ["unclosed fence at line 2", "broken link: missing.md"]),
                ("~~~~\n~~~\n", ["unclosed fence at line 1"]),
                ("```lang\n[inside](missing.md)\n````\n[after](missing.md)\n", ["broken link: missing.md"]),
                ("```\nexample\n````\n[after](missing.md)\n````\nexample\n````\n", ["broken link: missing.md"]),
                ("~~~lang\n[inside](missing.md)\n~~~~~\n[after](...)\n", ["broken link: ..."]),
                ("````\n```\n[inside](missing.md)\n````\n[after](missing.md)\n", ["broken link: missing.md"]),
                ("~~~\n```\n[inside](missing.md)\n~~~~\n", []),
            ]
            for text, expected in cases:
                with self.subTest(text=text):
                    path.write_text(text, encoding="utf-8")
                    self.assertEqual(expected, audit_file(path))
            path.write_text("```\nPRIVATE_FIXTURE\n````\n", encoding="utf-8")
            self.assertIn("private marker", audit_file(path, ["PRIVATE_FIXTURE"]))
            path.write_text("```\n" + "sk-" + "abcdefghijklmnopqrstuv" + "\n````\n", encoding="utf-8")
            self.assertIn("secret token", audit_file(path))

    def test_negative_controls(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/'sample'; folder.mkdir(); path=folder/'SKILL.md'
            valid='---\nname: sample\ndescription: Example\n---\n\n# Sample\n'
            path.write_text(valid, encoding='utf-8'); self.assertEqual([], audit_file(path))
            path.write_text(valid+'[missing](no-file.md)', encoding='utf-8'); self.assertTrue(any('broken link' in x for x in audit_file(path)))
            path.write_text(valid+'[placeholder](...)', encoding='utf-8'); self.assertIn('broken link: ...', audit_file(path))
            path.write_text(valid+'[trailing](SKILL.md.)', encoding='utf-8'); self.assertIn('broken link: SKILL.md.', audit_file(path))
            path.write_text(valid+'```\n[example](...)\n```\n~~~\n[example](missing.md)\n~~~\n', encoding='utf-8'); self.assertEqual([], audit_file(path))
            path.write_text(valid+'```\n[example](...)\n```\n[after](missing.md)\n', encoding='utf-8'); self.assertIn('broken link: missing.md', audit_file(path))
            path.write_text(valid+'\n'+'sk-'+'abcdefghijklmnopqrstuv', encoding='utf-8'); self.assertIn('secret token', audit_file(path))
            path.write_text(valid+'\n'+'C:' + '\\' + 'Users' + '\\' + 'fixture', encoding='utf-8'); self.assertIn('user path', audit_file(path))
            path.write_text(valid+'\n'+'PRIVATE_FIXTURE', encoding='utf-8'); self.assertIn('private marker', audit_file(path, ['PRIVATE_FIXTURE']))
            path.write_text(valid.replace('name: sample','name: wrong'), encoding='utf-8'); self.assertIn('invalid name', audit_file(path))
            path.write_text(valid.replace('description: Example',''), encoding='utf-8'); self.assertIn('missing description', audit_file(path))
            path.write_text(valid.replace('description: Example','level: private\ndescription: Example'), encoding='utf-8'); self.assertIn('unsupported level', audit_file(path))

if __name__ == '__main__':
    unittest.main()
