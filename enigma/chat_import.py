"""Epic 8: chat import (WhatsApp + Telegram) with re-import merge into canonical People Context."""
import json
import re
from collections import Counter
from typing import Dict, List, Optional, Tuple

from enigma.config import OPENAI_API_KEY
from enigma.notion_client import _get_prop, find_people_context_page, update_page_fields
from enigma.orchestrator import push_to_nexus

WHATSAPP_PATTERNS = (
    re.compile(r"^\[(?P<dt>[^\]]+)\]\s(?P<sender>[^:]+):\s(?P<msg>.+)$"),
    re.compile(r"^(?P<dt>\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2})\s-\s(?P<sender>[^:]+):\s(?P<msg>.+)$"),
)

TELEGRAM_TXT_PATTERNS = (
    re.compile(r"^(?P<dt>\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}):\s(?P<sender>[^:]+):\s(?P<msg>.+)$"),
    re.compile(r"^(?P<dt>\d{2}\.\d{2}\.\d{2},\s\d{2}:\d{2})\s-\s(?P<sender>[^:]+):\s(?P<msg>.+)$"),
)


def _normalize_lines(text: str) -> List[str]:
    return [ln.rstrip() for ln in (text or "").splitlines() if ln.strip()]


def _slug(s: str) -> str:
    s = re.sub(r"\s+", " ", (s or "").strip())
    s = re.sub(r"[^a-zA-Z0-9 ]+", "", s)
    return (s or "unknown").lower().replace(" ", "-")[:64]


def _contact_from_filename(filename: str) -> str:
    base = (filename or "chat").strip().rsplit("/", 1)[-1].rsplit("\\", 1)[-1]
    stem = re.sub(r"\.[A-Za-z0-9]+$", "", base)
    stem = re.sub(r"^(WhatsApp Chat with|Chat with|Telegram Chat with)\s+", "", stem, flags=re.I)
    stem = re.sub(r"\s+", " ", stem).strip(" -_")
    return stem or "Unknown Contact"


def _canonical_context(platform: str, contact: str) -> str:
    return f"People Context | {platform.capitalize()} | {contact}"[:180]


def _canonical_key(platform: str, contact: str) -> str:
    return f"pc:{platform}:{_slug(contact)}"


def _dedupe(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    out = []
    for m in messages:
        key = (
            (m.get("timestamp") or "").strip().lower(),
            (m.get("sender") or "").strip().lower(),
            (m.get("message") or "").strip().lower(),
        )
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "timestamp": (m.get("timestamp") or "").strip(),
            "sender": (m.get("sender") or "Unknown").strip(),
            "message": (m.get("message") or "").strip(),
        })
    return [x for x in out if x["message"]]


def parse_whatsapp_txt(text: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for ln in _normalize_lines(text):
        matched = None
        for p in WHATSAPP_PATTERNS:
            m = p.match(ln)
            if m:
                matched = {
                    "timestamp": (m.groupdict().get("dt") or "").strip(),
                    "sender": (m.groupdict().get("sender") or "").strip(),
                    "message": (m.groupdict().get("msg") or "").strip(),
                }
                break
        if matched:
            rows.append(matched)
        elif rows:
            rows[-1]["message"] = (rows[-1]["message"] + " " + ln.strip()).strip()
    return _dedupe(rows)


def parse_telegram_json(raw_bytes: bytes) -> List[Dict[str, str]]:
    data = json.loads(raw_bytes.decode("utf-8", errors="replace"))
    messages = data.get("messages") if isinstance(data, dict) else []
    out: List[Dict[str, str]] = []
    if not isinstance(messages, list):
        return out
    for m in messages:
        if not isinstance(m, dict):
            continue
        text = m.get("text")
        if isinstance(text, list):
            parts = []
            for t in text:
                if isinstance(t, str):
                    parts.append(t)
                elif isinstance(t, dict):
                    parts.append(str(t.get("text", "")))
            text = "".join(parts)
        out.append(
            {
                "timestamp": str(m.get("date", "")),
                "sender": str(m.get("from", "Unknown")),
                "message": str(text or "").strip(),
            }
        )
    return _dedupe(out)


def parse_telegram_txt(text: str) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for ln in _normalize_lines(text):
        matched = None
        for p in TELEGRAM_TXT_PATTERNS:
            m = p.match(ln)
            if m:
                matched = {
                    "timestamp": (m.groupdict().get("dt") or "").strip(),
                    "sender": (m.groupdict().get("sender") or "").strip(),
                    "message": (m.groupdict().get("msg") or "").strip(),
                }
                break
        if matched:
            rows.append(matched)
        elif rows:
            rows[-1]["message"] = (rows[-1]["message"] + " " + ln.strip()).strip()
    return _dedupe(rows)


def parse_telegram_html(text: str) -> List[Dict[str, str]]:
    """Best-effort parser for Telegram Desktop HTML exports."""
    blocks = re.findall(
        r'<div class="message[^"]*"[^>]*>(.*?)</div>\s*</div>',
        text,
        flags=re.S,
    )
    out = []
    for b in blocks:
        sender_m = re.search(r'<div class="from_name">(.*?)</div>', b, flags=re.S)
        text_m = re.search(r'<div class="text">(.*?)</div>', b, flags=re.S)
        date_m = re.search(r'<div class="date"[^>]*title="([^"]+)"', b, flags=re.S)
        sender = re.sub(r"<[^>]+>", "", sender_m.group(1)).strip() if sender_m else "Unknown"
        msg = re.sub(r"<[^>]+>", "", text_m.group(1)).strip() if text_m else ""
        ts = (date_m.group(1).strip() if date_m else "")
        if msg:
            out.append({"timestamp": ts, "sender": sender, "message": msg})
    return _dedupe(out)


def _openai_client():
    if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
        return None
    from openai import OpenAI
    return OpenAI(api_key=OPENAI_API_KEY.strip())


def summarize_messages(messages: List[Dict[str, str]], limit_preview: int = 16) -> Tuple[str, Dict[str, object]]:
    if not messages:
        return "No messages parsed from file.", {"count": 0, "top_senders": []}

    senders = Counter((m.get("sender") or "Unknown") for m in messages)
    top_senders = senders.most_common(8)
    preview = messages[-limit_preview:]
    lines = [
        f"Imported {len(messages)} messages.",
        "Top participants: " + ", ".join(f"{name} ({count})" for name, count in top_senders),
        "",
        "Recent excerpts:",
    ]
    for m in preview:
        sender = m.get("sender") or "Unknown"
        msg = (m.get("message") or "").replace("\n", " ").strip()
        if len(msg) > 200:
            msg = msg[:197] + "..."
        lines.append(f"- {sender}: {msg}")
    meta = {"count": len(messages), "top_senders": top_senders}
    return "\n".join(lines), meta


def _llm_refresh_summary(
    existing_summary: str,
    new_messages: List[Dict[str, str]],
    platform: str,
    contact: str,
) -> Optional[str]:
    client = _openai_client()
    if client is None:
        return None
    sample = "\n".join(
        f"- [{m.get('timestamp','')}] {m.get('sender','Unknown')}: {m.get('message','')[:240]}"
        for m in new_messages[-40:]
    )
    prompt = (
        f"Refresh a people-context summary for contact '{contact}' on {platform}. "
        "Keep one canonical summary with:\n"
        "1) Key topics\n2) Open commitments/actions\n3) Relationship/context cues\n4) Recent changes\n"
        "Be concise, factual, and grounded in the provided text."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": (
                    "Existing summary:\n"
                    + (existing_summary or "(none)")
                    + "\n\nNew messages:\n"
                    + (sample or "(none)")
                ),
            },
        ],
        max_tokens=800,
    )
    out = (response.choices[0].message.content or "").strip()
    return out or None


def _parse_telegram_by_extension(filename: str, file_bytes: bytes) -> List[Dict[str, str]]:
    lower = (filename or "").lower()
    text = file_bytes.decode("utf-8", errors="replace")
    if lower.endswith(".json"):
        return parse_telegram_json(file_bytes)
    if lower.endswith(".html") or lower.endswith(".htm"):
        parsed = parse_telegram_html(text)
        if parsed:
            return parsed
    return parse_telegram_txt(text)


def import_chat_to_nexus(platform: str, filename: str, file_bytes: bytes) -> Dict[str, object]:
    """Parse upload and upsert canonical people-context summary for contact."""
    platform_norm = (platform or "").strip().lower()
    if platform_norm not in ("whatsapp", "telegram"):
        raise ValueError("Unsupported platform. Use 'whatsapp' or 'telegram'.")

    contact = _contact_from_filename(filename)
    contact_key = _canonical_key(platform_norm, contact)
    canonical_context = _canonical_context(platform_norm, contact)

    if platform_norm == "whatsapp":
        messages = parse_whatsapp_txt(file_bytes.decode("utf-8", errors="replace"))
    else:
        messages = _parse_telegram_by_extension(filename, file_bytes)

    if not messages:
        raise ValueError("No messages parsed. Check that the file format matches selected platform.")

    deterministic_summary, meta = summarize_messages(messages)

    # FR-8.2: one canonical entry per contact (re-import refreshes existing summary)
    existing_page = find_people_context_page(canonical_context)
    existing_summary = _get_prop(existing_page, "Content") if existing_page else ""
    llm_summary = _llm_refresh_summary(
        existing_summary=existing_summary,
        new_messages=messages,
        platform=platform_norm,
        contact=contact,
    )
    summary_body = llm_summary or deterministic_summary
    summary = (
        f"Canonical Key: {contact_key}\n"
        f"Contact: {contact}\n"
        f"Platform: {platform_norm}\n\n"
        + summary_body
    )

    if existing_page:
        page = update_page_fields(
            existing_page.get("id"),
            context=canonical_context,
            content=summary,
            priority="low",
            sovereign_tag="people-context",
        )
        mode = "updated"
    else:
        page = push_to_nexus(
            context=canonical_context,
            content=summary,
            priority="low",
            tag="people-context",
        )
        mode = "created"

    return {
        "id": page.get("id"),
        "mode": mode,
        "context": canonical_context,
        "contact": contact,
        "contact_key": contact_key,
        "tag": "people-context",
        "summary_preview": summary_body[:320],
        "message_count": meta.get("count", 0),
        "top_senders": meta.get("top_senders", []),
        "llm_used": bool(llm_summary),
    }
