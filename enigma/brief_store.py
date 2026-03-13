"""Store last delivered Sovereign Brief for FR-3.4 Brief-to-Query handoff."""
from pathlib import Path
from typing import Optional

from enigma.config import BRIEF_LAST_FILE_PATH


def _path() -> Path:
    p = Path(BRIEF_LAST_FILE_PATH) if BRIEF_LAST_FILE_PATH else Path(__file__).resolve().parent.parent / ".last_sovereign_brief"
    return Path(p)


def save_last_brief(text: str) -> None:
    """Save the last delivered brief so Life Query can use it as follow-up context."""
    path = _path()
    path.write_text(text, encoding="utf-8")


def get_last_brief() -> Optional[str]:
    """Return the last delivered brief text, or None if none stored."""
    path = _path()
    if not path.exists():
        return None
    try:
        return path.read_text(encoding="utf-8").strip() or None
    except Exception:
        return None
