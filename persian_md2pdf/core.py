"""
Core interface for compiling Persian Markdown files and directories into PDFs.
"""

import os
import glob
import tempfile
from typing import Optional, List, Union

from .converter import md_to_html
from .browser import render_html_to_pdf, find_browser


def compile_file(
    input_file: str,
    output_pdf: Optional[str] = None,
    title: Optional[str] = None,
    theme: str = "modern",
    font: str = "Vazirmatn",
    page_size: str = "A4",
    margins: str = "20mm 15mm 20mm 15mm",
    persian_numbers: bool = False,
    katex: bool = True,
    custom_css: Optional[str] = None,
    browser_path: Optional[str] = None,
    keep_html: bool = False,
    virtual_time_budget: int = 6000,
) -> str:
    """
    Compiles a single Markdown file into a PDF document.

    Args:
        input_file: Path to source .md file.
        output_pdf: Path to destination .pdf file. Defaults to same name as input.
        title: Document title (defaults to frontmatter or heading or filename).
        theme: Theme name ('modern', 'academic', 'minimal', 'github').
        font: Persian font family name (default 'Vazirmatn').
        page_size: 'A4' or 'Letter'.
        margins: CSS margin format, e.g. '20mm 15mm 20mm 15mm'.
        persian_numbers: Whether to translate 0-9 to ۰-۹.
        katex: Whether to render LaTeX math via KaTeX.
        custom_css: Additional CSS text or path to a .css file.
        browser_path: Custom path to browser executable.
        keep_html: If True, saves intermediate .html file next to the PDF.
        virtual_time_budget: Milliseconds for KaTeX and font rendering.

    Returns:
        str: Absolute path to the generated PDF.
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Markdown file not found: {input_file}")

    if not output_pdf:
        output_pdf = os.path.splitext(input_file)[0] + ".pdf"

    output_pdf = os.path.abspath(output_pdf)

    # Read markdown source
    with open(input_file, "r", encoding="utf-8") as f:
        md_text = f.read()

    # If custom_css points to an existing file, load its content
    if custom_css and os.path.isfile(custom_css):
        with open(custom_css, "r", encoding="utf-8") as f:
            custom_css = f.read()

    base_name = os.path.basename(input_file)
    default_title = os.path.splitext(base_name)[0].replace("_", " ")

    html_content = md_to_html(
        md_text=md_text,
        title=title or default_title,
        theme=theme,
        font=font,
        page_size=page_size,
        margins=margins,
        persian_numbers=persian_numbers,
        katex=katex,
        custom_css=custom_css,
    )

    if keep_html:
        html_path = os.path.splitext(output_pdf)[0] + ".html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        render_html_to_pdf(
            html_path=html_path,
            pdf_path=output_pdf,
            browser_path=browser_path,
            virtual_time_budget=virtual_time_budget,
        )
    else:
        # Use a temporary file
        temp_dir = os.path.dirname(output_pdf) or tempfile.gettempdir()
        temp_html = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".html",
            dir=temp_dir,
            delete=False,
            encoding="utf-8",
        )
        try:
            temp_html.write(html_content)
            temp_html.close()
            render_html_to_pdf(
                html_path=temp_html.name,
                pdf_path=output_pdf,
                browser_path=browser_path,
                virtual_time_budget=virtual_time_budget,
            )
        finally:
            if os.path.exists(temp_html.name):
                try:
                    os.remove(temp_html.name)
                except OSError:
                    pass

    return output_pdf


def md2pdf(input_file: str, output_pdf: Optional[str] = None, **kwargs) -> str:
    """Convenience alias for compile_file."""
    return compile_file(input_file, output_pdf=output_pdf, **kwargs)


def md2html(
    input_source: str,
    output_html: Optional[str] = None,
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
    Converts a Markdown file or raw string to a styled HTML document.

    If input_source is a file path that exists, reads the file.
    Otherwise, treats input_source as raw markdown string.
    If output_html is provided, writes to the file.
    Returns the HTML string.
    """
    if os.path.isfile(input_source):
        with open(input_source, "r", encoding="utf-8") as f:
            md_text = f.read()
        if not title:
            title = os.path.splitext(os.path.basename(input_source))[0].replace("_", " ")
    else:
        md_text = input_source
        title = None

    if custom_css and os.path.isfile(custom_css):
        with open(custom_css, "r", encoding="utf-8") as f:
            custom_css = f.read()

    html_str = md_to_html(
        md_text=md_text,
        title=title,
        theme=theme,
        font=font,
        page_size=page_size,
        margins=margins,
        persian_numbers=persian_numbers,
        katex=katex,
        custom_css=custom_css,
    )

    if output_html:
        os.makedirs(os.path.dirname(os.path.abspath(output_html)) or ".", exist_ok=True)
        with open(output_html, "w", encoding="utf-8") as f:
            f.write(html_str)

    return html_str


def compile_directory(
    input_dir: str,
    output_dir: Optional[str] = None,
    pattern: str = "*.md",
    recursive: bool = False,
    **kwargs
) -> List[str]:
    """
    Compiles all Markdown files matching pattern inside input_dir into PDFs.

    Returns:
        List[str]: List of paths to successfully generated PDFs.
    """
    if not os.path.isdir(input_dir):
        raise NotADirectoryError(f"Directory not found: {input_dir}")

    if not output_dir:
        output_dir = input_dir
    os.makedirs(output_dir, exist_ok=True)

    if recursive:
        search_path = os.path.join(input_dir, "**", pattern)
        md_files = glob.glob(search_path, recursive=True)
    else:
        search_path = os.path.join(input_dir, pattern)
        md_files = glob.glob(search_path, recursive=False)

    generated_pdfs: List[str] = []
    for md_file in md_files:
        rel_path = os.path.relpath(md_file, input_dir)
        pdf_rel = os.path.splitext(rel_path)[0] + ".pdf"
        out_pdf = os.path.join(output_dir, pdf_rel)
        pdf_path = compile_file(md_file, output_pdf=out_pdf, **kwargs)
        generated_pdfs.append(pdf_path)

    return generated_pdfs
