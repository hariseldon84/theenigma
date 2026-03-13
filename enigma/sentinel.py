"""
Omni-Scribe (Desktop Sentinel) — samples active window title and clipboard,
pushes to The Nexus as Transient Memory every N minutes.
"""
import logging
import platform
import subprocess
import sys
import time
from typing import Optional

from enigma.config import NEXUS_PUSH_INTERVAL_MIN
from enigma.orchestrator import push_to_nexus

logger = logging.getLogger(__name__)

SOVEREIGN_TAG_TRANSIENT = "transient"
_CONTEXT_MAX = 500
_CONTENT_MAX = 2000


def get_active_window_title() -> str:
    """Return the title of the currently active window. Empty string on failure or unsupported platform."""
    system = platform.system()
    try:
        if system == "Darwin":
            return _get_active_window_macos()
        if system == "Windows":
            return _get_active_window_windows()
        if system == "Linux":
            return _get_active_window_linux()
    except Exception:
        pass
    return ""


def _get_active_window_macos() -> str:
    script = '''
    tell application "System Events" to set frontApp to name of first process whose frontmost is true
    tell application frontApp to set windowName to name of front window
    return windowName
    '''
    out = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        timeout=2,
    )
    if out.returncode == 0 and out.stdout:
        return out.stdout.strip() or ""
    return ""


def _get_active_window_windows() -> str:
    from ctypes import create_unicode_buffer, windll

    user32 = windll.user32
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return ""
    buf = create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buf, length + 1)
    return buf.value or ""


def _get_active_window_linux() -> str:
    # Requires xdotool: sudo apt install xdotool / yum install xdotool
    try:
        out = subprocess.run(
            ["xdotool", "getactivewindow", "getwindowname"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        if out.returncode == 0 and out.stdout:
            return out.stdout.strip() or ""
    except FileNotFoundError:
        pass
    return ""


def get_clipboard_content() -> str:
    """Return current clipboard text. Empty string on failure or if not text."""
    system = platform.system()
    try:
        if system == "Darwin":
            return _get_clipboard_macos()
        if system == "Windows":
            return _get_clipboard_windows()
        if system == "Linux":
            return _get_clipboard_linux()
    except Exception:
        pass
    return ""


def _get_clipboard_macos() -> str:
    out = subprocess.run(
        ["pbpaste"],
        capture_output=True,
        text=True,
        timeout=2,
    )
    if out.returncode == 0 and out.stdout is not None:
        return out.stdout
    return ""


def _get_clipboard_windows() -> str:
    from ctypes import create_unicode_buffer, windll

    user32 = windll.user32
    kernel32 = windll.kernel32
    CF_UNICODETEXT = 13
    if not user32.OpenClipboard(None):
        return ""
    try:
        h = user32.GetClipboardData(CF_UNICODETEXT)
        if not h:
            return ""
        ptr = kernel32.GlobalLock(h)
        if not ptr:
            return ""
        try:
            # Max reasonable clipboard size
            size = kernel32.GlobalSize(h)
            buf = create_unicode_buffer(size // 2)
            kernel32.RtlMoveMemory(buf, ptr, size)
            return buf.value or ""
        finally:
            kernel32.GlobalUnlock(h)
    finally:
        user32.CloseClipboard()


def _get_clipboard_linux() -> str:
    for cmd in [["xclip", "-selection", "clipboard", "-o"], ["xsel", "--clipboard", "--output"]]:
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
            if out.returncode == 0 and out.stdout is not None:
                return out.stdout
        except FileNotFoundError:
            continue
    return ""


def sample() -> tuple[str, str]:
    """Capture current window title and clipboard. Returns (context, content) for a single nugget."""
    window = get_active_window_title().strip() or "(no window)"
    clipboard = get_clipboard_content().strip() or "(empty)"
    context = f"Omni-Scribe: {window}"[:_CONTEXT_MAX]
    content = f"Window: {window}\nClipboard: {clipboard}"[:_CONTENT_MAX]
    return context, content


def push_sample() -> bool:
    """Capture one sample and push to Nexus with Sovereign Tag 'transient'. Returns True on success."""
    try:
        context, content = sample()
        push_to_nexus(context=context, content=content, priority="low", tag=SOVEREIGN_TAG_TRANSIENT)
        logger.debug("Omni-Scribe pushed sample context=%s", (context or "")[:80])
        return True
    except Exception as e:
        logger.warning("Omni-Scribe push failed: %s", e)
        return False


def run_loop(interval_min: Optional[int] = None) -> None:
    """Run the sentinel loop: sample and push every interval_min minutes. Ctrl+C to stop."""
    interval = interval_min if interval_min is not None else NEXUS_PUSH_INTERVAL_MIN
    if interval < 1:
        interval = NEXUS_PUSH_INTERVAL_MIN
    interval_sec = max(60, interval * 60)
    logger.info("Omni-Scribe running (push every %s min). Ctrl+C to stop.", interval)
    while True:
        if push_sample():
            logger.debug("Omni-Scribe push ok")
            print(".", end="", flush=True, file=sys.stderr)
        else:
            logger.debug("Omni-Scribe push failed")
            print("x", end="", flush=True, file=sys.stderr)
        time.sleep(interval_sec)
