#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script: generate_pdf_reports.py
Description: Backwards-compatible runner for converting Persian Markdown documents into PDFs.
             Powered by the modular 'persian_md2pdf' engine.
Usage:
    python generate_pdf_reports.py [file1.md file2.md ...]
"""

import os
import sys

# Ensure UTF-8 output on Windows terminal
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Add current directory to path if running directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from persian_md2pdf import compile_file, find_browser, __version__


def main():
    print("=" * 65)
    print(f"      PERSIAN MARKDOWN TO PDF CONVERTER (v{__version__})")
    print("=" * 65)

    try:
        browser_exe = find_browser()
        print(f"Browser Engine: {os.path.basename(browser_exe)}")
    except Exception as e:
        print(f"[-] Browser error: {e}", file=sys.stderr)
        return

    script_dir = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(script_dir, "Reports")
    examples_dir = os.path.join(script_dir, "examples")

    # If targets are passed via CLI arguments
    targets = sys.argv[1:]

    # Fallback to predefined reports if no arguments given
    if not targets:
        report_files = [
            "01_گزارش_جامع_مدیریتی.md",
            "02_گزارش_فنی_و_ریاضی.md",
            "03_گزارش_اثبات_و_آدیت_صحت‌سنجی.md",
            "04_گزارش_پیشنهادات_راهبردی_تز.md",
        ]
        if os.path.exists(reports_dir):
            for rf in report_files:
                p = os.path.join(reports_dir, rf)
                if os.path.exists(p):
                    targets.append(p)

        # Also check examples directory
        if not targets and os.path.exists(examples_dir):
            for f in os.listdir(examples_dir):
                if f.endswith(".md"):
                    targets.append(os.path.join(examples_dir, f))

        # Also check README_FA.md
        readme_fa = os.path.join(script_dir, "README_FA.md")
        if os.path.exists(readme_fa) and readme_fa not in targets:
            targets.append(readme_fa)

    if not targets:
        print("[-] No Markdown files found to convert.")
        print("[*] Tip: Use the new CLI command anywhere: persian-md2pdf your_document.md")
        return

    success_count = 0
    for file_path in targets:
        if not os.path.exists(file_path):
            print(f"[-] File not found: {file_path}")
            continue

        base_name = os.path.basename(file_path)
        pdf_path = os.path.splitext(file_path)[0] + ".pdf"
        print(f"[*] Converting: {base_name} -> {os.path.basename(pdf_path)} ...")

        try:
            out = compile_file(
                input_file=file_path,
                output_pdf=pdf_path,
                theme="academic" if "گزارش" in base_name else "modern",
            )
            size_kb = os.path.getsize(out) / 1024.0
            print(f"    [+] Successfully generated ({size_kb:.1f} KB)")
            success_count += 1
        except Exception as e:
            print(f"    [-] Failed to generate {pdf_path}: {e}")

    print("\n" + "=" * 65)
    print(f"  Finished: {success_count}/{len(targets)} documents successfully converted.")
    print("  TIP: You can also use the 'persian-md2pdf' CLI tool directly!")
    print("=" * 65)


if __name__ == "__main__":
    main()
