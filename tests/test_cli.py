"""
Tests for CLI commands and argument parsing.
"""

import subprocess
import sys
import unittest

from persian_md2pdf import __version__


class TestCLI(unittest.TestCase):
    def test_cli_version(self):
        cmd = [sys.executable, "-m", "persian_md2pdf.cli", "--version"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0)
        self.assertIn(__version__, res.stdout + res.stderr)

    def test_cli_help(self):
        cmd = [sys.executable, "-m", "persian_md2pdf.cli", "--help"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0)
        self.assertIn("persian-md2pdf", res.stdout)
        self.assertIn("--theme", res.stdout)
        self.assertIn("--persian-numbers", res.stdout)


if __name__ == "__main__":
    unittest.main()
