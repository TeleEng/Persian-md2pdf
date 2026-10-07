"""
Tests for browser detection.
"""

import os
import unittest
from persian_md2pdf.browser import find_browser


class TestBrowser(unittest.TestCase):
    def test_find_browser(self):
        browser_path = find_browser()
        self.assertTrue(os.path.isfile(browser_path))
        base = os.path.basename(browser_path).lower()
        self.assertTrue(any(name in base for name in ("edge", "chrome", "brave", "chromium")))


if __name__ == "__main__":
    unittest.main()
