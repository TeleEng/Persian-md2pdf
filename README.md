# Persian-md2pdf (تبدیل مارک‌داون فارسی به پی‌دی‌اف)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)](#)
[![RTL Supported](https://img.shields.io/badge/RTL-Persian%20%2F%20Farsi-brightgreen.svg)](#)

> **A professional, open-source tool and Python library to convert Persian and RTL Markdown files into publication-quality, beautiful PDF documents.**
> Complete with LaTeX math formulas (KaTeX), code syntax blocks, styled tables, GitHub callouts, and clean pagination.

[🇮🇷 مستندات فارسی (Persian Documentation)](README_FA.md)

---

## ✨ Features

- **Full Persian RTL Typography**: Native Right-to-Left text direction with balanced line spacing, text justification, and the beautiful Google **Vazirmatn** font (with Shabnam, Sahel, B Nazanin fallbacks).
- **Bidirectional Text Isolation**: English terms, acronyms, and technical phrases inside Persian sentences render without corrupted punctuation or flipped parenthesis.
- **LaTeX Math Rendering (KaTeX)**:
  - Inline formulas: `$E = mc^2$`
  - Display equations: `$$\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}$$`
  - All mathematical equations are automatically isolated into LTR so formulas and matrices never get mangled in RTL mode.
- **Code Block Formatting**: Monospace code blocks with clean LTR alignment, dark or academic styling, and terminal looks.
- **GitHub-style Callouts / Admonitions**: Beautiful styled alert boxes for `> [!NOTE]`, `> [!TIP]`, `> [!IMPORTANT]`, `> [!WARNING]`, and `> [!CAUTION]`, as well as Persian aliases (`> [!نکته]`, `> [!هشدار]`, `> [!مهم]`).
- **Multiple Built-in Themes**:
  - `modern`: Clean contemporary design with blue accents and crisp typography.
  - `academic`: Formal design optimized for theses, university reports, and scientific papers.
  - `minimal`: Sleek monochrome layout with high contrast.
  - `github`: Familiar GitHub documentation layout adapted for RTL.
- **Persian Digits Converter**: Optional conversion of Western digits (`0-9`) into Persian digits (`۰-۹`) via `--persian-numbers` while safely protecting code blocks, math, and HTML tags.
- **CSS Paged Media**: Automatic page numbering (`صفحه ۱`), headers, footers, and customizable page sizes (`A4`, `Letter`) and margins.
- **Zero Binary Setup**: Uses headless Chromium / Microsoft Edge / Google Chrome / Brave already installed on your machine. No bulky Cairo/Pango or wkhtmltopdf binaries required!
- **Live Watch Mode (`--watch`)**: Automatically detects file modifications and recompiles to PDF upon saving.
- **Batch Processing**: Convert single files, glob patterns, or entire directories with one command.

---

## 🚀 Installation

### From GitHub:
```bash
git clone https://github.com/TeleEng/Persian-md2pdf.git
cd Persian-md2pdf
pip install .
```

### For Development (Editable Mode):
```bash
pip install -e .
```

---

## 🛠️ Command-Line Interface (CLI)

Once installed, the `persian-md2pdf` command is available everywhere in your terminal:

```bash
# Basic conversion (creates document.pdf)
persian-md2pdf document.md

# Specify custom output path
persian-md2pdf document.md -o output.pdf

# Choose a theme (modern, academic, minimal, github)
persian-md2pdf thesis.md -o thesis.pdf --theme academic

# Convert numbers in Persian prose to Persian digits (۰-۹)
persian-md2pdf report.md --persian-numbers

# Watch mode for live editing (recompiles on save)
persian-md2pdf report.md --watch

# Convert an entire folder of markdown documents
persian-md2pdf ./docs/ -o ./dist/

# Export as HTML only
persian-md2pdf guide.md -o guide.html --html-only

# Apply custom CSS
persian-md2pdf report.md --css custom_style.css
```

### CLI Options Reference

| Option | Short | Description | Default |
| :--- | :---: | :--- | :--- |
| `input` | | Path to Markdown file(s) or directory | Required |
| `--output` | `-o` | Output PDF file or directory | Input name with `.pdf` |
| `--theme` | `-t` | Visual theme (`modern`, `academic`, `minimal`, `github`) | `modern` |
| `--font` | `-f` | Primary Persian font family | `Vazirmatn` |
| `--page-size` | | Page size (`A4`, `Letter`, etc.) | `A4` |
| `--margins` | | Page margins (`top right bottom left`) | `20mm 15mm 20mm 15mm` |
| `--persian-numbers` | | Convert digits 0-9 to Persian digits ۰-۹ | `False` |
| `--no-katex` | | Disable KaTeX math parsing | `False` |
| `--html-only` | | Generate only HTML output | `False` |
| `--keep-html` | | Keep intermediate HTML file next to PDF | `False` |
| `--css` | | Path to custom CSS file or stylesheet | `None` |
| `--browser` | | Custom path to Chrome/Edge executable | Auto-detected |
| `--watch` | `-w` | Watch for file modifications and recompile | `False` |
| `--version` | `-v` | Show installed version | |

---

## 🐍 Python API Usage

You can easily integrate `persian-md2pdf` into your Python scripts, web servers, or data pipelines:

```python
from persian_md2pdf import md2pdf, md2html

# Simple conversion
pdf_path = md2pdf("report.md", "report.pdf")

# Customized conversion
pdf_path = md2pdf(
    input_file="thesis.md",
    output_pdf="thesis.pdf",
    theme="academic",
    font="Vazirmatn",
    page_size="A4",
    persian_numbers=True,
    katex=True,
)

# Convert raw Markdown string to standalone HTML
html_content = md2html(
    input_source="# گزارش تست\nاین یک متن فارسی است.",
    theme="modern",
)
```

### Directory Batch Conversion

```python
from persian_md2pdf import compile_directory

# Compiles all .md files in docs/ into dist/
generated_files = compile_directory(
    input_dir="./docs",
    output_dir="./dist",
    theme="academic",
    recursive=True
)
print(f"Generated {len(generated_files)} PDF files.")
```

---

## 🎨 Themes Showcase

| Theme | Best For | Description |
| :--- | :--- | :--- |
| **`modern`** | Reports & Portfolios | Contemporary blue accents, subtle shadows, clean typography. |
| **`academic`** | Theses & Research Papers | Formal book styling, structured headers, traditional borders. |
| **`minimal`** | Documentation & Handouts | Distraction-free monochrome typography with high contrast. |
| **`github`** | Technical Guides | Authentic GitHub Markdown appearance adapted for RTL. |

---

## 📝 Markdown Syntax Examples

### Metadata (YAML Frontmatter)
```markdown
---
title: عنوان گزارش جامع
author: نام نویسنده
date: ۱۴۰۵/۰۱/۱۵
---
```

### LaTeX Math
```markdown
فرمول درون‌خطی انرژی: $E = mc^2$

فرمول بلوکی توزیع نرمال:
$$f(x) = \frac{1}{\sigma \sqrt{2\pi}} e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}$$
```

### GitHub Callouts / Admonitions
```markdown
> [!NOTE]
> این یک پیام یادداشت است.

> [!TIP]
> پیشنهاد می‌کنیم از سوئیچ watch استفاده کنید.

> [!WARNING]
> اطمینان حاصل کنید مرورگر کروم یا اج نصب باشد.
```

---

## 🌐 Supported Browsers

`persian-md2pdf` detects installed Chromium-based browsers automatically:
- **Windows**: Microsoft Edge, Google Chrome, Brave, Chromium
- **Linux**: Google Chrome, Chromium, Microsoft Edge, Brave
- **macOS**: Google Chrome, Microsoft Edge, Brave, Chromium

You can also specify a custom path using `--browser /path/to/browser` or by setting the `BROWSER_PATH` / `CHROME_BIN` environment variable.

---

## 🧪 Testing

Run the included test suite with:

```bash
python -m unittest discover tests -v
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE). Contributions, bug reports, and feature requests are welcome!
