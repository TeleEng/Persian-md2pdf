"""
persian_md2pdf: Convert Persian & RTL Markdown documents to professional PDFs.
"""

__version__ = "1.0.0"
__author__ = "TeleEng"

from .browser import find_browser, render_html_to_pdf
from .converter import md_to_html, to_persian_numbers
from .core import md2pdf, md2html, compile_file, compile_directory
from .themes import get_theme_css, AVAILABLE_THEMES

__all__ = [
    "__version__",
    "md2pdf",
    "md2html",
    "compile_file",
    "compile_directory",
    "find_browser",
    "render_html_to_pdf",
    "to_persian_numbers",
    "get_theme_css",
    "AVAILABLE_THEMES",
]
