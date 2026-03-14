"""Simple local JSON stores for Brief archive and Life Query history (Epic 7)."""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _brief_archive_path() -> Path:
    return _repo_root() / ".brief_archive.json"


def _query_history_path() -> Path:
    return _repo_root() / ".query_history.json"


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read_json_array(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(raw, list):
            return [x for x in raw if isinstance(x, dict)]
    except Exception:
        return []
    return []


def _write_json_array(path: Path, items: List[Dict[str, Any]]) -> None:
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")


def append_brief_archive(brief_text: str) -> Dict[str, Any]:
    """Append a generated Sovereign Brief to archive and return stored record."""
    record = {
        "id": f"brief-{int(datetime.now(timezone.utc).timestamp() * 1000)}",
        "created_at": _now_iso(),
        "text": (brief_text or "").strip(),
    }
    path = _brief_archive_path()
    items = _read_json_array(path)
    items.insert(0, record)
    _write_json_array(path, items[:200])
    return record


def get_brief_archive(limit: int = 50) -> List[Dict[str, Any]]:
    """Return recent brief archive records (newest first)."""
    return _read_json_array(_brief_archive_path())[: max(1, limit)]


def append_query_history(
    question: str,
    answer: str,
    brief_context_used: bool = False,
    source: str = "text",
) -> Dict[str, Any]:
    """Append a Life Query Q&A to local history and return stored record."""
    record = {
        "id": f"query-{int(datetime.now(timezone.utc).timestamp() * 1000)}",
        "created_at": _now_iso(),
        "question": (question or "").strip(),
        "answer": (answer or "").strip(),
        "brief_context_used": bool(brief_context_used),
        "source": source,
    }
    path = _query_history_path()
    items = _read_json_array(path)
    items.insert(0, record)
    _write_json_array(path, items[:500])
    return record


def get_query_history(limit: int = 100) -> List[Dict[str, Any]]:
    """Return recent Life Query history records (newest first)."""
    return _read_json_array(_query_history_path())[: max(1, limit)]

