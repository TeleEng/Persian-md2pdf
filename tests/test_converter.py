"""
Unit tests for markdown-to-HTML conversion and RTL features.
"""

import unittest
from persian_md2pdf.converter import (
    md_to_html,
    to_persian_numbers,
    extract_frontmatter,
    parse_callouts,
    fix_persian_ezafe,
)


class TestConverter(unittest.TestCase):
    def test_extract_frontmatter(self):
        text = "---\ntitle: تست عنوان\nauthor: سهراب\n---\n# متن اصلی"
        meta, remaining = extract_frontmatter(text)
        self.assertEqual(meta.get("title"), "تست عنوان")
        self.assertEqual(meta.get("author"), "سهراب")
        self.assertIn("# متن اصلی", remaining)

    def test_to_persian_numbers(self):
        sample = "<p>سال 2026 میلادی و شماره 12345</p>"
        result = to_persian_numbers(sample)
        self.assertIn("۲۰۲۶", result)
        self.assertIn("۱۲۳۴۵", result)
        # Ensure HTML tags are not corrupted
        self.assertTrue(result.startswith("<p>") and result.endswith("</p>"))

    def test_callout_parsing(self):
        callout_map = {}
        sample = "> [!NOTE]\n> این یک پیام آزمایشی است.\n"
        replaced = parse_callouts(sample, callout_map)
        self.assertTrue(len(callout_map) == 1)
        token = list(callout_map.keys())[0]
        self.assertIn(token, replaced)
        self.assertIn("callout-note", callout_map[token])
        self.assertIn("یادداشت", callout_map[token])

    def test_katex_math_protection(self):
        md = "فرمول درون خطی $E = mc^2$ و فرمول بلوکی:\n\n$$\\int_0^1 x dx = 0.5$$\n"
        html = md_to_html(md, title="آزمون ریاضی")
        self.assertIn("math-inline", html)
        self.assertIn("math-display", html)
        self.assertIn("katex", html)
        self.assertIn("E = mc^2", html)
        self.assertIn("\\int_0^1 x dx = 0.5", html)

    def test_table_conversion(self):
        md = "| نام | امتیاز |\n| :--- | :---: |\n| علی | ۱۰۰ |\n"
        html = md_to_html(md)
        self.assertIn("<table>", html)
        self.assertIn("نام", html)
        self.assertIn("امتیاز", html)
        self.assertIn("علی", html)
        self.assertIn("۱۰۰", html)

    def test_fix_persian_ezafe(self):
        # Test heh + hamza above (\u0647\u0654) and single-char \u06C0
        sample = "<p>واژه‌نامهٔ زبان و خانهٔ قدیمی و دهٔ شصت</p>"
        result = fix_persian_ezafe(sample)
        self.assertIn('واژه‌نامه<span class="ezafe-hamza">ء</span> زبان', result)
        self.assertIn('خانه<span class="ezafe-hamza">ء</span> قدیمی', result)
        self.assertIn('ده<span class="ezafe-hamza">ء</span> شصت', result)

        # Ensure code blocks and tags are not affected
        code_sample = "<code>نامهٔ</code>"
        result_code = fix_persian_ezafe(code_sample)
        self.assertIn("<code>نامهٔ</code>", result_code)



if __name__ == "__main__":
    unittest.main()
