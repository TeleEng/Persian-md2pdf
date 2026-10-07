"""
Core Markdown-to-HTML conversion engine for Persian and RTL documents.
Handles math equations (KaTeX), GitHub-style callouts, tables, code blocks,
and Persian digits formatting.
"""

import re
from typing import Optional, Dict, Tuple
import markdown

from .themes import get_theme_css

# SVG Icons for Callouts
CALLOUT_ICONS = {
    "note": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2.5a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"/></svg>',
    "tip": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.495H9.5c.085-.599.337-1.084.621-1.495.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.993-1.32.993-2.304 0-2.06-1.637-3.75-4-3.75ZM6 11.5a.5.5 0 0 1 .5-.5h3a.5.5 0 0 1 0 1h-3a.5.5 0 0 1-.5-.5Zm1 2a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 0 1h-1a.5.5 0 0 1-.5-.5Z"/></svg>',
    "important": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H9.06l-2.573 2.573A1.458 1.458 0 0 1 4 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h3.25a.75.75 0 0 1 .75.75v1.438L8.28 12.38a.75.75 0 0 1 .53-.22h5.44a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25ZM8 3.5a.75.75 0 0 1 .75.75v3a.75.75 0 0 1-1.5 0v-3A.75.75 0 0 1 8 3.5Zm0 6a.875.875 0 1 1 0-1.75.875.875 0 0 1 0 1.75Z"/></svg>',
    "warning": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM8 10.75a.875.875 0 1 1 0 1.75.875.875 0 0 1 0-1.75Z"/></svg>',
    "caution": '<svg viewBox="0 0 16 16" fill="currentColor"><path d="M4.47.047A.75.75 0 0 1 5 0h6a.75.75 0 0 1 .53.22l4.25 4.25c.141.14.22.331.22.53v6a.75.75 0 0 1-.22.53l-4.25 4.25A.75.75 0 0 1 11 16H5a.75.75 0 0 1-.53-.22L.22 11.53A.75.75 0 0 1 0 11V5c0-.199.079-.39.22-.53Zm.84 1.203L1.5 5.06v5.88l3.81 3.81h5.88l3.81-3.81V5.06L11.19 1.25ZM8 4a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 4Zm0 7a.875.875 0 1 1 0-1.75.875.875 0 0 1 0 1.75Z"/></svg>',
}

CALLOUT_TITLES_FA = {
    "note": "یادداشت",
    "tip": "نکته کاربردی",
    "important": "مهم",
    "warning": "هشدار",
    "caution": "احتیاط",
}

CALLOUT_ALIAS_MAP = {
    "note": "note",
    "نکته": "note",
    "یادداشت": "note",
    "tip": "tip",
    "ترفند": "tip",
    "پیشنهاد": "tip",
    "important": "important",
    "مهم": "important",
    "warning": "warning",
    "هشدار": "warning",
    "caution": "caution",
    "احتیاط": "caution",
    "توجه": "warning",
}

PERSIAN_DIGITS_TRANS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def to_persian_numbers(text: str) -> str:
    """
    Converts Latin digits 0-9 into Persian digits ۰-۹,
    carefully preserving HTML tags, URLs, math, and code blocks.
    """
    # Regex splitting text into protected parts (HTML tags, pre/code tags, math) vs normal text
    parts = re.split(r"(<[^>]+>|@@MATH[A-Z0-9_]+END@@|@@CALLOUT[A-Z0-9_]+END@@)", text)
    in_code_block = False

    result = []
    for part in parts:
        if not part:
            continue
        # Check tag boundaries
        if part.startswith("<"):
            tag_name = part.strip("<>").split()[0].lower() if part.strip("<>").split() else ""
            if tag_name in ("pre", "code", "script", "style"):
                in_code_block = True
            elif tag_name in ("/pre", "/code", "/script", "/style"):
                in_code_block = False
            result.append(part)
        elif part.startswith("@@MATH") or part.startswith("@@CALLOUT") or in_code_block:
            # Leave protected tokens and code blocks as-is
            result.append(part)
        else:
            # Regular Persian text node: convert digits
            result.append(part.translate(PERSIAN_DIGITS_TRANS))

    return "".join(result)


def extract_frontmatter(md_text: str) -> Tuple[Dict[str, str], str]:
    """
    Extracts simple YAML frontmatter (key: value) if present at top of markdown document.
    """
    meta: Dict[str, str] = {}
    pattern = r"^---\s*\n([\s\S]*?)\n---\s*\n"
    match = re.match(pattern, md_text)
    if match:
        yaml_content = match.group(1)
        md_text = md_text[match.end():]
        for line in yaml_content.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip().lower()] = v.strip().strip("\"'")
    return meta, md_text


def parse_callouts(md_text: str, callout_map: Dict[str, str]) -> str:
    """
    Preprocesses GitHub-style callouts:
    > [!NOTE]
    > text ...
    and replaces them with protected tokens before Markdown parsing.
    """
    pattern = re.compile(
        r"(?:^[ ]*>[ ]*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION|نکته|یادداشت|ترفند|پیشنهاد|مهم|هشدار|احتیاط|توجه)\][ ]*\n)"
        r"((?:^[ ]*>.*(?:\n|$))+)",
        re.MULTILINE | re.IGNORECASE
    )

    def replace_callout(match):
        raw_type = match.group(1).lower()
        callout_type = CALLOUT_ALIAS_MAP.get(raw_type, "note")
        raw_body = match.group(2)

        # Clean blockquote characters from body
        body_lines = []
        for line in raw_body.splitlines():
            cleaned = re.sub(r"^[ ]*>[ ]?", "", line)
            body_lines.append(cleaned)
        inner_markdown = "\n".join(body_lines).strip()

        # Convert inner markdown
        inner_html = markdown.markdown(inner_markdown, extensions=['tables', 'fenced_code', 'nl2br'])

        title = CALLOUT_TITLES_FA.get(callout_type, callout_type.capitalize())
        icon = CALLOUT_ICONS.get(callout_type, CALLOUT_ICONS["note"])

        token = f"@@CALLOUTTOKEN{len(callout_map)}END@@"
        callout_html = (
            f'<div class="callout callout-{callout_type}">\n'
            f'  <div class="callout-header">\n'
            f'    <span class="callout-icon">{icon}</span>\n'
            f'    <span>{title}</span>\n'
            f'  </div>\n'
            f'  <div class="callout-content">{inner_html}</div>\n'
            f'</div>\n'
        )
        callout_map[token] = callout_html
        return token + "\n\n"

    return pattern.sub(replace_callout, md_text)


def md_to_html(
    md_text: str,
    title: Optional[str] = None,
    theme: str = "modern",
    font: str = "Vazirmatn",
    page_size: str = "A4",
    margins: str = "20mm 15mm 20mm 15mm",
    persian_numbers: bool = False,
    katex: bool = True,
    custom_css: Optional[str] = None,
) -> str:
    """
    Transforms Persian/RTL Markdown into a complete, publication-ready HTML document.

    Args:
        md_text: Raw Markdown content.
        title: Document HTML title. Extracted automatically if None.
        theme: Theme name ('modern', 'academic', 'minimal', 'github').
        font: Font family name (default 'Vazirmatn').
        page_size: Page format (e.g. 'A4', 'Letter').
        margins: CSS margin string (e.g. '20mm 15mm 20mm 15mm').
        persian_numbers: If True, convert Latin digits to Persian digits.
        katex: If True, include KaTeX math rendering engine.
        custom_css: Optional custom CSS rules to inject.

    Returns:
        str: Valid HTML5 string with styles and assets.
    """
    # 1. Extract Frontmatter
    frontmatter, content = extract_frontmatter(md_text)

    # Determine document title
    if "title" in frontmatter:
        title = frontmatter["title"]
    elif not title:
        first_h1 = re.search(r"^#[ ]+(.+)$", content, re.MULTILINE)
        if first_h1:
            title = first_h1.group(1).strip()
        else:
            title = "سند فارسی"

    # 2. Protect LaTeX Math
    math_map: Dict[str, str] = {}

    if katex:
        def save_display_math(match):
            token = f"@@MATHDISPLAYTOKEN{len(math_map)}END@@"
            math_content = match.group(1).strip()
            math_map[token] = f'<div class="math-display">\\[{math_content}\\]</div>'
            return token

        def save_inline_math(match):
            token = f"@@MATHINLINETOKEN{len(math_map)}END@@"
            math_content = match.group(1).strip()
            math_map[token] = f'<span class="math-inline">\\({math_content}\\)</span>'
            return token

        # Extract display math $$ ... $$
        content = re.sub(r"\$\$([\s\S]+?)\$\$", save_display_math, content)
        # Extract inline math $ ... $
        content = re.sub(r"(?<!\\)\$(?!\$)([^\$\n]+?)(?<!\\)\$", save_inline_math, content)

    # 3. Parse Callouts / Admonitions
    callout_map: Dict[str, str] = {}
    content = parse_callouts(content, callout_map)

    # 4. Convert Markdown to HTML
    md_parser = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'nl2br',
        'toc',
        'attr_list',
        'def_list',
    ])
    html_body = md_parser.convert(content)

    # 5. Restore Math & Callout Tokens
    for token, math_html in math_map.items():
        html_body = html_body.replace(f"<p>{token}</p>", math_html)
        html_body = html_body.replace(token, math_html)

    for token, callout_html in callout_map.items():
        # Handle cases where markdown parser may wrap token in <p>...</p>
        html_body = html_body.replace(f"<p>{token}</p>", callout_html)
        html_body = html_body.replace(token, callout_html)

    # 6. Apply Persian Numbers if enabled
    if persian_numbers:
        html_body = to_persian_numbers(html_body)

    # 7. Generate Theme Stylesheet
    theme_css = get_theme_css(
        theme_name=theme,
        font_family=font,
        page_size=page_size,
        margins=margins,
        page_numbering=True,
        custom_css=custom_css,
    )

    # 8. KaTeX Scripts Injection
    katex_scripts = ""
    if katex:
        katex_scripts = """
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {
        delimiters: [
            {left: '\\\\[', right: '\\\\]', display: true},
            {left: '\\\\(', right: '\\\\)', display: false}
        ],
        throwOnError: false
    });">
</script>
"""

    # 9. Assemble HTML Document
    html_document = f"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
{katex_scripts}
<style>
{theme_css}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    return html_document
