"""
End-to-end tests for compilation.
"""

import os
import tempfile
import unittest
from persian_md2pdf.core import compile_file, md2html


class TestCore(unittest.TestCase):
    def test_md2html(self):
        sample_md = "# آزمایش تست\nاین یک متن تستی است."
        html = md2html(sample_md)
        self.assertIn("آزمایش تست", html)
        self.assertIn('dir="rtl"', html)

    def test_compile_file_e2e(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
            f.write("# گزارش تست ای‌تو‌دی\nمتن پاراگراف تستی.\n")
            md_path = f.name

        pdf_path = md_path.replace(".md", ".pdf")
        try:
            out = compile_file(md_path, pdf_path)
            self.assertTrue(os.path.isfile(out))
            self.assertGreater(os.path.getsize(out), 1000)
        finally:
            if os.path.exists(md_path):
                os.remove(md_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)


if __name__ == "__main__":
    unittest.main()
