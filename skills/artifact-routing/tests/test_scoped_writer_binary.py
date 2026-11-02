"""Tests for how scoped_writer.binary() finds the native executable. Run: python -I tests/test_scoped_writer_binary.py"""
import importlib.util
import os
import pathlib
import tempfile
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location("scoped_writer", pathlib.Path(__file__).parents[1] / "scripts/scoped_writer.py")
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)


class BinaryTests(unittest.TestCase):
    def test_env_var_wins(self):
        with tempfile.TemporaryDirectory() as d:
            exe = pathlib.Path(d) / "mycodex"
            exe.write_text("x")
            with mock.patch.dict(os.environ, {"SCOPED_WRITER_CODEX": str(exe)}):
                self.assertEqual(w.binary("codex"), str(exe))

    def test_env_var_must_be_a_file(self):
        with mock.patch.dict(os.environ, {"SCOPED_WRITER_CODEX": "/no/such/file"}):
            with self.assertRaises(ValueError):
                w.binary("codex")

    def test_missing_names_the_variable(self):
        with mock.patch.dict(os.environ, {"PATH": ""}, clear=False):
            os.environ.pop("SCOPED_WRITER_CODEX", None)
            with self.assertRaises(ValueError) as cm:
                w.binary("codex")
            self.assertIn("SCOPED_WRITER_CODEX", str(cm.exception))

    def test_no_machine_specific_path_in_source(self):
        src = (pathlib.Path(__file__).parents[1] / "scripts/scoped_writer.py").read_text(encoding="utf-8")
        self.assertNotIn("codex-win32-x64", src)
        self.assertNotIn("x86_64-pc-windows-msvc", src)


if __name__ == "__main__":
    unittest.main()
