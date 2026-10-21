"""
Tests for English LTR mode and Mermaid diagram support.
"""

import os
import sys
import tempfile
import unittest
import subprocess

from persian_md2pdf.converter import md_to_html
from persian_md2pdf.core import compile_file, md2html


class TestEnglishAndMermaid(unittest.TestCase):
    def test_english_md_to_html_attributes(self):
        md = """---
title: Test Document
---
# Welcome

This is an English paragraph with a callout:

> [!NOTE]
> This is a note callout.

> [!WARNING]
> This is a warning.
"""
        html = md_to_html(md, english=True)
        self.assertIn('lang="en"', html)
        self.assertIn('dir="ltr"', html)
        self.assertIn("Inter", html)
        self.assertIn("Note", html)
        self.assertIn("Warning", html)
        self.assertNotIn("یادداشت", html)
        self.assertNotIn("هشدار", html)
        self.assertIn("Page ", html)

    def test_mermaid_parsing(self):
        md = """# Diagram Test

Here is a flowchart:

```mermaid
graph TD
    A[Start] --> B[Finish]
```
"""
        html = md_to_html(md, english=True, mermaid=True)
        self.assertIn('<div class="mermaid">', html)
        self.assertIn("graph TD", html)
        self.assertIn("A[Start] --> B[Finish]", html)
        self.assertIn("mermaid.min.js", html)
        self.assertIn("mermaid.initialize", html)

    def test_mermaid_in_persian_mode(self):
        md = """# سند فارسی همراه با نمودار

```mermaid
graph LR
    A --> B
```
"""
        html = md_to_html(md, english=False, mermaid=True)
        self.assertIn('lang="fa"', html)
        self.assertIn('dir="rtl"', html)
        self.assertIn('<div class="mermaid">', html)
        self.assertIn("mermaid.min.js", html)

    def test_mermaid_font_size_customization(self):
        md = "```mermaid\ngraph LR\nA-->B\n```"
        html = md_to_html(md, english=True, mermaid_font_size="9px", mermaid_font="Fira Code", mermaid_theme="neutral")
        self.assertIn("--mermaid-font-size: 9px", html)
        self.assertIn("--mermaid-font-family: 'Fira Code', sans-serif", html)
        self.assertIn("fontSize: '9px'", html)
        self.assertIn("fontFamily: ''Fira Code', sans-serif'", html)
        self.assertIn("theme: 'neutral'", html)

    def test_mermaid_frontmatter_configuration(self):
        md = "---\nmermaid_font_size: 10px\nmermaid_font: JetBrains Mono\nmermaid_theme: forest\n---\n```mermaid\ngraph LR\nA-->B\n```"
        html = md_to_html(md, english=True)
        self.assertIn("--mermaid-font-size: 10px", html)
        self.assertIn("--mermaid-font-family: 'JetBrains Mono', sans-serif", html)
        self.assertIn("fontSize: '10px'", html)
        self.assertIn("fontFamily: ''JetBrains Mono', sans-serif'", html)
        self.assertIn("theme: 'forest'", html)

    def test_cli_english_flag(self):
        cmd = [sys.executable, "-m", "persian_md2pdf.cli", "--help"]
        res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(res.returncode, 0)
        self.assertIn("--english", res.stdout)
        self.assertIn("--no-mermaid", res.stdout)
        self.assertIn("--mermaid-font-size", res.stdout)
        self.assertIn("--mermaid-font", res.stdout)
        self.assertIn("--mermaid-theme", res.stdout)

    def test_end_to_end_english_compilation(self):
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
            f.write("""---
title: Architecture Test
---
# Architecture Overview

```mermaid
graph TD
    Client --> Server
```

Math: $E=mc^2$
""")
            md_path = f.name

        pdf_path = md_path.replace(".md", ".pdf")
        try:
            out = compile_file(md_path, pdf_path, english=True, mermaid=True)
            self.assertTrue(os.path.isfile(out))
            self.assertGreater(os.path.getsize(out), 5000)
        finally:
            if os.path.exists(md_path):
                os.remove(md_path)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)


if __name__ == "__main__":
    unittest.main()
