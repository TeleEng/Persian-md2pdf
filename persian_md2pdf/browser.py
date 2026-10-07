"""
Browser detection and headless PDF rendering engine.
Supports Microsoft Edge, Google Chrome, Brave, and Chromium across Windows, macOS, and Linux.
"""

import os
import sys
import shutil
import subprocess
from typing import Optional, List


def find_browser(custom_path: Optional[str] = None) -> str:
    """
    Locates an available Chromium-based browser executable (Edge, Chrome, Brave, Chromium).
    Allows overriding via custom_path or BROWSER_PATH / CHROME_BIN environment variables.

    Raises:
        FileNotFoundError: If no suitable browser executable is found.
    """
    if custom_path:
        if os.path.isfile(custom_path):
            return os.path.abspath(custom_path)
        raise FileNotFoundError(f"Specified browser executable not found at: {custom_path}")

    # Check environment variables
    for env_var in ("BROWSER_PATH", "CHROME_BIN"):
        val = os.environ.get(env_var)
        if val and os.path.isfile(val):
            return os.path.abspath(val)

    candidates: List[str] = []

    if sys.platform.startswith("win"):
        # Windows search paths
        prog_files = os.environ.get("ProgramFiles", r"C:\Program Files")
        prog_files_x86 = os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")
        local_app_data = os.environ.get("LocalAppData", "")

        candidates.extend([
            os.path.join(prog_files, r"Microsoft\Edge\Application\msedge.exe"),
            os.path.join(prog_files_x86, r"Microsoft\Edge\Application\msedge.exe"),
            os.path.join(prog_files, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(prog_files_x86, r"Google\Chrome\Application\chrome.exe"),
            os.path.join(prog_files, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
            os.path.join(prog_files_x86, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
        ])
        if local_app_data:
            candidates.extend([
                os.path.join(local_app_data, r"Microsoft\Edge\Application\msedge.exe"),
                os.path.join(local_app_data, r"Google\Chrome\Application\chrome.exe"),
                os.path.join(local_app_data, r"BraveSoftware\Brave-Browser\Application\brave.exe"),
            ])
    elif sys.platform == "darwin":
        # macOS search paths
        candidates.extend([
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
            os.path.expanduser("~/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
        ])
    else:
        # Linux and Unix-like systems
        linux_binaries = [
            "google-chrome-stable",
            "google-chrome",
            "chromium-browser",
            "chromium",
            "microsoft-edge-stable",
            "microsoft-edge",
            "brave-browser",
        ]
        for binary in linux_binaries:
            found = shutil.which(binary)
            if found:
                return found

    # Verify candidates
    for path in candidates:
        if path and os.path.isfile(path):
            return os.path.abspath(path)

    # Final check via PATH for common names on Windows or Mac
    for binary in ("msedge", "chrome", "chromium", "brave"):
        found = shutil.which(binary)
        if found:
            return os.path.abspath(found)

    raise FileNotFoundError(
        "No Chromium-compatible browser (Microsoft Edge, Google Chrome, Brave, or Chromium) "
        "was detected on your system.\n"
        "Please install Microsoft Edge or Google Chrome, or specify the browser executable path "
        "via --browser or the BROWSER_PATH environment variable."
    )


def render_html_to_pdf(
    html_path: str,
    pdf_path: str,
    browser_path: Optional[str] = None,
    virtual_time_budget: int = 6000,
    timeout: int = 90
) -> bool:
    """
    Renders an HTML file to PDF using a headless Chromium browser.

    Args:
        html_path: Path to the HTML input file.
        pdf_path: Path where the output PDF should be written.
        browser_path: Optional custom browser executable path.
        virtual_time_budget: Milliseconds to wait for fonts and KaTeX scripts to render.
        timeout: Subprocess timeout in seconds.

    Returns:
        bool: True if PDF generation succeeded and file exists.
    """
    browser_exe = find_browser(browser_path)
    abs_html = os.path.abspath(html_path)
    abs_pdf = os.path.abspath(pdf_path)

    # Ensure output parent directory exists
    os.makedirs(os.path.dirname(abs_pdf) or ".", exist_ok=True)

    cmd = [
        browser_exe,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        "--run-all-compositor-stages-before-draw",
        f"--virtual-time-budget={virtual_time_budget}",
        f"--print-to-pdf={abs_pdf}",
        abs_html
    ]

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False
        )
    except subprocess.TimeoutExpired:
        raise TimeoutError(f"PDF rendering timed out after {timeout} seconds.")

    if os.path.exists(abs_pdf) and os.path.getsize(abs_pdf) > 0:
        return True

    # If modern --headless failed or returned 0 bytes, check stderr
    stderr_msg = result.stderr.decode("utf-8", errors="replace").strip()
    raise RuntimeError(
        f"Browser failed to generate PDF.\n"
        f"Exit code: {result.returncode}\n"
        f"Error details: {stderr_msg if stderr_msg else 'No output returned'}"
    )
