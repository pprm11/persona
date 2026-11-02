import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'permalinks.py'

class PermalinkTests(unittest.TestCase):
    def test_preserves_crlf_and_reports_invalid_line(self):
        with tempfile.TemporaryDirectory() as d:
            root = pathlib.Path(d)
            def git(*args):
                return subprocess.run(['git', '-C', d, *args], check=True, capture_output=True, text=True).stdout.strip()
            git('init', '-q'); git('config', 'user.name', 'Test'); git('config', 'user.email', 'test@example.invalid')
            (root/'a.py').write_text('one\ntwo\n', encoding='utf-8')
            git('add', 'a.py'); git('commit', '-qm', 'fixture'); sha=git('rev-parse', 'HEAD')
            doc=root/'doc.md'; doc.write_bytes(b'`a.py:1`\r\nmore\r\n')
            cmd=[sys.executable, str(SCRIPT), '--repo-dir', d, '--sha', sha, '--github', 'test/repo', str(doc)]
            result=subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertNotIn(b'\n', doc.read_bytes().replace(b'\r\n', b''))
            doc.write_bytes(b'`a.py:-5`\n')
            result=subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(1, result.returncode)
            self.assertNotIn('Traceback', result.stderr)
            self.assertIn('INVALID', result.stdout)

if __name__ == '__main__': unittest.main()
