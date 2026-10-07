"""
Themes and CSS generator for Persian RTL Markdown to PDF conversion.
Provides modern, academic, minimal, and github themes with full RTL & Paged Media support.
"""

from typing import Optional, Dict

AVAILABLE_THEMES = ["modern", "academic", "minimal", "github"]

THEME_PALETTES: Dict[str, Dict[str, str]] = {
    "modern": {
        "text_color": "#1e293b",
        "bg_color": "#ffffff",
        "primary": "#1d4ed8",
        "h1_color": "#1e3a8a",
        "h1_border": "#2563eb",
        "h2_color": "#1d4ed8",
        "h2_accent": "#3b82f6",
        "h3_color": "#2563eb",
        "code_bg": "#0f172a",
        "code_color": "#f8fafc",
        "inline_code_bg": "#f1f5f9",
        "inline_code_color": "#0f172a",
        "table_header_bg": "#f1f5f9",
        "table_header_color": "#0f172a",
        "table_stripe_bg": "#f8fafc",
        "table_border": "#cbd5e1",
        "quote_bg": "#eff6ff",
        "quote_border": "#3b82f6",
        "quote_color": "#1e3a8a",
        "hr_color": "#e2e8f0",
        "footer_color": "#64748b",
    },
    "academic": {
        "text_color": "#0f172a",
        "bg_color": "#ffffff",
        "primary": "#334155",
        "h1_color": "#0f172a",
        "h1_border": "#475569",
        "h2_color": "#1e293b",
        "h2_accent": "#64748b",
        "h3_color": "#334155",
        "code_bg": "#1e293b",
        "code_color": "#f1f5f9",
        "inline_code_bg": "#f1f5f9",
        "inline_code_color": "#0f172a",
        "table_header_bg": "#e2e8f0",
        "table_header_color": "#0f172a",
        "table_stripe_bg": "#f8fafc",
        "table_border": "#94a3b8",
        "quote_bg": "#f8fafc",
        "quote_border": "#64748b",
        "quote_color": "#334155",
        "hr_color": "#cbd5e1",
        "footer_color": "#475569",
    },
    "minimal": {
        "text_color": "#111827",
        "bg_color": "#ffffff",
        "primary": "#374151",
        "h1_color": "#111827",
        "h1_border": "#e5e7eb",
        "h2_color": "#1f2937",
        "h2_accent": "#9ca3af",
        "h3_color": "#374151",
        "code_bg": "#1f2937",
        "code_color": "#f9fafb",
        "inline_code_bg": "#f3f4f6",
        "inline_code_color": "#1f2937",
        "table_header_bg": "#f9fafb",
        "table_header_color": "#111827",
        "table_stripe_bg": "#ffffff",
        "table_border": "#e5e7eb",
        "quote_bg": "#f9fafb",
        "quote_border": "#d1d5db",
        "quote_color": "#374151",
        "hr_color": "#e5e7eb",
        "footer_color": "#9ca3af",
    },
    "github": {
        "text_color": "#24292f",
        "bg_color": "#ffffff",
        "primary": "#0969da",
        "h1_color": "#1f2328",
        "h1_border": "#d0d7de",
        "h2_color": "#1f2328",
        "h2_accent": "#d0d7de",
        "h3_color": "#1f2328",
        "code_bg": "#161b22",
        "code_color": "#e6edf3",
        "inline_code_bg": "#eff1f3",
        "inline_code_color": "#1f2328",
        "table_header_bg": "#f6f8fa",
        "table_header_color": "#1f2328",
        "table_stripe_bg": "#f6f8fa",
        "table_border": "#d0d7de",
        "quote_bg": "#f6f8fa",
        "quote_border": "#0969da",
        "quote_color": "#57606a",
        "hr_color": "#d0d7de",
        "footer_color": "#57606a",
    },
}


def get_theme_css(
    theme_name: str = "modern",
    font_family: str = "Vazirmatn",
    page_size: str = "A4",
    margins: str = "20mm 15mm 20mm 15mm",
    page_numbering: bool = True,
    custom_css: Optional[str] = None,
) -> str:
    """
    Constructs the complete CSS string for a chosen theme with RTL layout,
    typography, KaTeX, Callouts, and print styles.
    """
    palette = THEME_PALETTES.get(theme_name.lower(), THEME_PALETTES["modern"])

    # Fallback Persian font stack
    font_stack = f"'{font_family}', 'Shabnam', 'Sahel', 'B Nazanin', 'Segoe UI', Tahoma, Arial, sans-serif"
    code_font_stack = "'JetBrains Mono', 'Fira Code', 'Consolas', 'Courier New', monospace"

    page_counter_css = ""
    if page_numbering:
        page_counter_css = f"""
    @bottom-center {{
        content: "صفحه " counter(page);
        font-family: {font_stack};
        font-size: 8.5pt;
        color: {palette['footer_color']};
    }}
"""

    css = f"""
/* Google Fonts Import for Vazirmatn */
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap');

@page {{
    size: {page_size};
    margin: {margins};
{page_counter_css}
}}

* {{
    box-sizing: border-box;
}}

body {{
    font-family: {font_stack};
    font-size: 10.5pt;
    line-height: 1.85;
    color: {palette['text_color']};
    direction: rtl;
    text-align: justify;
    text-justify: inter-word;
    margin: 0;
    padding: 0;
    background-color: {palette['bg_color']};
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}}

/* Headings */
h1, h2, h3, h4, h5, h6 {{
    font-family: {font_stack};
    font-weight: 800;
    direction: rtl;
    text-align: right;
    margin-top: 1.8em;
    margin-bottom: 0.6em;
    page-break-after: avoid;
    break-after: avoid;
}}

h1 {{
    font-size: 17.5pt;
    color: {palette['h1_color']};
    border-bottom: 3px solid {palette['h1_border']};
    padding-bottom: 10px;
    margin-top: 0.5em;
}}

h2 {{
    font-size: 13.5pt;
    color: {palette['h2_color']};
    border-right: 4.5px solid {palette['h2_accent']};
    padding-right: 12px;
    margin-top: 1.6em;
}}

h3 {{
    font-size: 11.5pt;
    color: {palette['h3_color']};
    margin-top: 1.3em;
}}

h4 {{
    font-size: 10.5pt;
    color: {palette['text_color']};
}}

p {{
    margin-top: 0.3em;
    margin-bottom: 0.9em;
}}

/* Links */
a {{
    color: {palette['primary']};
    text-decoration: none;
    border-bottom: 1px dotted {palette['primary']};
}}

/* Lists */
ul, ol {{
    padding-right: 25px;
    padding-left: 0;
    margin-bottom: 1em;
}}

li {{
    margin-bottom: 0.45em;
}}

/* Tables */
table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1.6em 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
    break-inside: avoid;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}}

th, td {{
    border: 1px solid {palette['table_border']};
    padding: 8px 12px;
    text-align: right;
    vertical-align: middle;
}}

th {{
    background-color: {palette['table_header_bg']};
    color: {palette['table_header_color']};
    font-weight: 700;
}}

tr:nth-child(even) {{
    background-color: {palette['table_stripe_bg']};
}}

/* Code & Preformatted */
code {{
    font-family: {code_font_stack};
    background-color: {palette['inline_code_bg']};
    color: {palette['inline_code_color']};
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 9pt;
    direction: ltr !important;
    display: inline-block;
    unicode-bidi: isolate;
}}

pre {{
    background-color: {palette['code_bg']};
    color: {palette['code_color']};
    padding: 14px 18px;
    border-radius: 6px;
    direction: ltr !important;
    text-align: left !important;
    overflow-x: auto;
    font-size: 8.5pt;
    line-height: 1.55;
    page-break-inside: avoid;
    break-inside: avoid;
    margin: 1.2em 0;
}}

pre code {{
    background-color: transparent !important;
    color: inherit !important;
    padding: 0 !important;
    display: block;
    direction: ltr !important;
    text-align: left !important;
}}

/* Blockquotes */
blockquote {{
    margin: 1.3em 0;
    padding: 10px 18px;
    background-color: {palette['quote_bg']};
    border-right: 4px solid {palette['quote_border']};
    color: {palette['quote_color']};
    border-radius: 4px;
}}

hr {{
    border: none;
    border-top: 1.5px solid {palette['hr_color']};
    margin: 2em 0;
}}

/* Images */
img {{
    max-width: 100%;
    height: auto;
    display: block;
    margin: 1.5em auto;
    border-radius: 4px;
    page-break-inside: avoid;
    break-inside: avoid;
}}

/* Math formulas (KaTeX) */
.math-display {{
    direction: ltr !important;
    text-align: center;
    margin: 1.4em 0;
    display: block;
    page-break-inside: avoid;
    break-inside: avoid;
}}

.math-inline {{
    direction: ltr !important;
    display: inline-block;
    unicode-bidi: isolate;
}}

.katex {{
    direction: ltr !important;
    font-size: 1.08em;
    unicode-bidi: isolate;
}}

/* Callouts / Admonitions */
.callout {{
    margin: 1.3em 0;
    padding: 12px 18px;
    border-radius: 6px;
    page-break-inside: avoid;
    break-inside: avoid;
    border-right: 4.5px solid;
    direction: rtl;
    text-align: justify;
}}

.callout-header {{
    display: flex;
    align-items: center;
    font-weight: 700;
    font-size: 10pt;
    margin-bottom: 6px;
    gap: 8px;
}}

.callout-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 18px;
    height: 18px;
}}

.callout-icon svg {{
    width: 18px;
    height: 18px;
}}

.callout-content {{
    font-size: 10pt;
    line-height: 1.75;
}}

.callout-content p:last-child {{
    margin-bottom: 0;
}}

/* Callout Types */
.callout-note {{
    background-color: #eff6ff;
    border-color: #3b82f6;
    color: #1e3a8a;
}}
.callout-note .callout-header {{
    color: #1d4ed8;
}}

.callout-tip {{
    background-color: #ecfdf5;
    border-color: #10b981;
    color: #064e3b;
}}
.callout-tip .callout-header {{
    color: #047857;
}}

.callout-important {{
    background-color: #f5f3ff;
    border-color: #8b5cf6;
    color: #4c1d95;
}}
.callout-important .callout-header {{
    color: #6d28d9;
}}

.callout-warning {{
    background-color: #fffbeb;
    border-color: #f59e0b;
    color: #78350f;
}}
.callout-warning .callout-header {{
    color: #b45309;
}}

.callout-caution {{
    background-color: #fef2f2;
    border-color: #ef4444;
    color: #7f1d1d;
}}
.callout-caution .callout-header {{
    color: #b91c1c;
}}
"""

    if custom_css:
        css += f"\n\n/* Custom User Styles */\n{custom_css}\n"

    return css
