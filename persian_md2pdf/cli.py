"""
Command Line Interface (CLI) for persian-md2pdf.
"""

import os
import sys
import time
import argparse
from typing import List

from . import __version__
from .browser import find_browser
from .converter import md_to_html
from .core import compile_file, compile_directory, md2html
from .themes import AVAILABLE_THEMES

# Ensure Windows terminal handles UTF-8
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def print_banner():
    banner = f"""
╔═════════════════════════════════════════════════════════════════╗
║                   persian-md2pdf v{__version__:<30}║
║        تبدیل حرفه‌ای فایل‌های مارک‌داون فارسی به پی‌دی‌اف        ║
╚═════════════════════════════════════════════════════════════════╝
"""
    print(banner)


def run_watch_mode(input_path: str, args):
    """
    Watches a markdown file or directory for modifications and automatically recompiles.
    """
    print(f"[*] حالت تماشا (Watch Mode) فعال شد.")
    print(f"[*] در حال نظارت بر تغییرات: {input_path}")
    print("[*] برای خروج، کلید ترکیبی Ctrl+C را فشار دهید.\n")

    def get_mtimes():
        if os.path.isfile(input_path):
            return {input_path: os.path.getmtime(input_path)}
        mtimes = {}
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.endswith(".md"):
                    full_p = os.path.join(root, file)
                    try:
                        mtimes[full_p] = os.path.getmtime(full_p)
                    except OSError:
                        pass
        return mtimes

    last_mtimes = get_mtimes()

    try:
        while True:
            time.sleep(1.0)
            current_mtimes = get_mtimes()
            changed = False
            for p, mtime in current_mtimes.items():
                if p not in last_mtimes or mtime > last_mtimes[p]:
                    changed = True
                    break

            if changed:
                last_mtimes = current_mtimes
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] تغییرات شناسایی شد. در حال کامپایل مجدد...")
                try:
                    process_inputs([input_path], args, verbose=False)
                    print(f"[{timestamp}] کامپایل با موفقیت انجام شد.\n")
                except Exception as e:
                    print(f"[✗] خطا در کامپایل: {e}\n")
    except KeyboardInterrupt:
        print("\n[*] نظارت متوقف شد.")


def process_inputs(inputs: List[str], args, verbose: bool = True):
    for target in inputs:
        if os.path.isdir(target):
            # Compile whole directory
            if verbose:
                print(f"[*] در حال تبدیل پوشه: {target}")
            compile_directory(
                input_dir=target,
                output_dir=args.output,
                theme=args.theme,
                font=args.font,
                page_size=args.page_size,
                margins=args.margins,
                persian_numbers=args.persian_numbers,
                katex=not args.no_katex,
                custom_css=args.css,
                browser_path=args.browser,
                keep_html=args.keep_html,
            )
            if verbose:
                print(f"  [✓] تمام فایل‌های مارک‌داون پوشه با موفقیت تبدیل شدند.")
        elif os.path.isfile(target):
            filename = os.path.basename(target)
            if args.html_only:
                out_html = args.output
                if not out_html:
                    out_html = os.path.splitext(target)[0] + ".html"
                elif os.path.isdir(out_html):
                    out_html = os.path.join(out_html, os.path.splitext(filename)[0] + ".html")

                if verbose:
                    print(f"[*] ایجاد فایل HTML: {filename} -> {os.path.basename(out_html)} ...")
                md2html(
                    input_source=target,
                    output_html=out_html,
                    theme=args.theme,
                    font=args.font,
                    page_size=args.page_size,
                    margins=args.margins,
                    persian_numbers=args.persian_numbers,
                    katex=not args.no_katex,
                    custom_css=args.css,
                )
                if verbose:
                    print(f"  [✓] فایل HTML با موفقیت ذخیره شد: {out_html}")
            else:
                out_pdf = args.output
                if out_pdf and os.path.isdir(out_pdf):
                    out_pdf = os.path.join(out_pdf, os.path.splitext(filename)[0] + ".pdf")

                if verbose:
                    print(f"[*] در حال تبدیل: {filename} ...")
                pdf_path = compile_file(
                    input_file=target,
                    output_pdf=out_pdf,
                    theme=args.theme,
                    font=args.font,
                    page_size=args.page_size,
                    margins=args.margins,
                    persian_numbers=args.persian_numbers,
                    katex=not args.no_katex,
                    custom_css=args.css,
                    browser_path=args.browser,
                    keep_html=args.keep_html,
                )
                if verbose:
                    size_kb = os.path.getsize(pdf_path) / 1024.0
                    print(f"  [✓] فایل PDF ساخته شد: {pdf_path} ({size_kb:.1f} KB)")
        else:
            print(f"[✗] خطا: مسیر یافت نشد: {target}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        prog="persian-md2pdf",
        description="تبدیل فایل‌های مارک‌داون فارسی به اسناد پی‌دی‌اف زیبا، استاندارد و راست‌چین با پشتیبانی از فرمول‌های ریاضی و کدهای برنامه‌نویسی.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
نمونه‌های استفاده:
  persian-md2pdf report.md
  persian-md2pdf report.md -o output.pdf --theme academic
  persian-md2pdf ./docs/ -o ./dist/
  persian-md2pdf paper.md --persian-numbers --watch
  persian-md2pdf guide.md --theme github --html-only
""",
    )

    parser.add_argument(
        "input",
        nargs="+",
        help="مسیر فایل یا پوشه مارک‌داون (.md)",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="مسیر فایل پی‌دی‌اف یا پوشه خروجی",
    )
    parser.add_argument(
        "-t", "--theme",
        default="modern",
        choices=AVAILABLE_THEMES,
        help="قالب ظاهری سند (پیش‌فرض: modern)",
    )
    parser.add_argument(
        "-f", "--font",
        default="Vazirmatn",
        help="نام فونت فارسی متن (پیش‌فرض: Vazirmatn)",
    )
    parser.add_argument(
        "--page-size",
        default="A4",
        help="اندازه صفحه (A4, Letter و ...) (پیش‌فرض: A4)",
    )
    parser.add_argument(
        "--margins",
        default="20mm 15mm 20mm 15mm",
        help="فاصله‌های حاشیه صفحه (بالا راست پایین چپ) (پیش‌فرض: 20mm 15mm 20mm 15mm)",
    )
    parser.add_argument(
        "--persian-numbers",
        action="store_true",
        help="تبدیل اعداد انگلیسی به ارقام فارسی در متن گزارش",
    )
    parser.add_argument(
        "--no-katex",
        action="store_true",
        help="غیرفعال‌سازی پردازش فرمول‌های ریاضی LaTeX",
    )
    parser.add_argument(
        "--html-only",
        action="store_true",
        help="تنها تولید فایل HTML بدون تبدیل به PDF",
    )
    parser.add_argument(
        "--keep-html",
        action="store_true",
        help="نگه‌داشتن فایل موقت HTML در کنار فایل PDF خروجی",
    )
    parser.add_argument(
        "--css",
        default=None,
        help="مسیر فایل استایل سفارشی CSS برای تغییر ظاهر سند",
    )
    parser.add_argument(
        "--browser",
        default=None,
        help="مسیر دستی به فایل اجرایی مرورگر Chrome یا Edge",
    )
    parser.add_argument(
        "-w", "--watch",
        action="store_true",
        help="نظارت خودکار بر فایل و کامپایل مجدد با هر ذخیره‌سازی",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="نمایش نسخه برنامه",
    )

    args = parser.parse_args()

    # If --watch is requested, enter watch loop
    if args.watch:
        print_banner()
        if len(args.input) > 1:
            print("[!] در حالت watch تنها اولین مسیر نظارت می‌شود.")
        run_watch_mode(args.input[0], args)
        return

    # Normal conversion
    print_banner()
    try:
        browser_info = find_browser(args.browser)
        print(f"[*] مرورگر شناسایی‌شده: {os.path.basename(browser_info)}")
    except Exception as e:
        if not args.html_only:
            print(f"[!] هشدار مرورگر: {e}", file=sys.stderr)

    process_inputs(args.input, args, verbose=True)
    print("\n[✓] عملیات با موفقیت پایان یافت.")


if __name__ == "__main__":
    main()
