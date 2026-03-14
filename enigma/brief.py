"""Sovereign Brief (FR-3.1): synthesize last 24h Nexus + Open Commitments, deliver via Email + Telegram."""
import logging
import smtplib
from datetime import datetime, timezone, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from enigma.config import (
    OPENAI_API_KEY,
    BRIEF_APP_BASE_URL,
    BRIEF_EMAIL_TO,
    BRIEF_SMTP_HOST,
    BRIEF_SMTP_PORT,
    BRIEF_SMTP_USER,
    BRIEF_SMTP_PASSWORD,
    BRIEF_SMTP_FROM,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
)
from enigma.brief_store import save_last_brief
from enigma.history_store import append_brief_archive
from enigma.notion_client import (
    get_nexus_since,
    get_open_commitments,
    get_recent_nuggets,
    get_recent_thoughts,
    get_recent_people_context,
    _get_prop,
)

logger = logging.getLogger(__name__)


def _openai_client():
    from openai import OpenAI
    if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
        raise ValueError("OPENAI_API_KEY is required for Sovereign Brief. Set it in .env")
    return OpenAI(api_key=OPENAI_API_KEY.strip())


def _since_iso(hours: int = 24) -> str:
    t = datetime.now(timezone.utc) - timedelta(hours=hours)
    return t.strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _build_context_text(commitments: list, nexus_pages: list, thoughts: list) -> str:
    """Build a single text blob for the LLM from commitments, Nexus entries, and thoughts (Epic 5)."""
    lines = []
    lines.append("=== OPEN COMMITMENTS ===")
    for p in commitments:
        ctx = _get_prop(p, "Context")
        content = _get_prop(p, "Content")
        tag = _get_prop(p, "Sovereign Tag")
        lines.append(f"- [{tag}] {ctx}: {content[:200]}")
    if not commitments:
        lines.append("(none)")
    lines.append("")
    lines.append("=== THOUGHTS (worth revisiting) ===")
    for p in thoughts[:30]:
        content = _get_prop(p, "Content")
        lines.append(f"- {content[:300]}")
    if not thoughts:
        lines.append("(none)")
    lines.append("")
    lines.append("=== NEXUS (LAST 24H) ===")
    for p in nexus_pages[:50]:
        ctx = _get_prop(p, "Context")
        content = _get_prop(p, "Content")
        tag = _get_prop(p, "Sovereign Tag")
        lines.append(f"- [{tag}] {ctx}: {content[:200]}")
    if not nexus_pages:
        lines.append("(none)")
    return "\n".join(lines)


def synthesize_brief(context_text: str) -> str:
    """Use LLM to produce the Sovereign Brief from context."""
    client = _openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are the Sovereign Brief: a concise daily digest for a busy professional. "
                    "Based on the Open Commitments, Thoughts, and Nexus activity below, write a brief (under 400 words) with: "
                    "1) Top priorities for today, 2) Open commitments to act on, 3) Thoughts worth revisiting (if any), 4) Suggested next actions. "
                    "Use clear headings. Be direct and actionable. No filler."
                ),
            },
            {"role": "user", "content": context_text},
        ],
        max_tokens=600,
    )
    return (response.choices[0].message.content or "").strip()


def _followup_link() -> str:
    """URL or hint for 'Ask follow-up' (FR-3.4)."""
    base = (BRIEF_APP_BASE_URL or "").strip().rstrip("/")
    if base:
        return base + "/?followup=1#life-query"
    return "Open Action Sphere and add ?followup=1#life-query to the URL, or long-press the orb for Life Query."


def _brief_body_with_followup(brief: str) -> str:
    """Append 'Ask follow-up' line to the brief for delivery."""
    return brief.rstrip() + "\n\n— Ask a follow-up: " + _followup_link() + _maybe_whatsapp_reminder()


def _maybe_whatsapp_reminder() -> str:
    """
    FR-8.5 (optional): weekly reminder to export/import chats.
    Show on Fridays when people-context has not been updated in the last 7 days.
    """
    now = datetime.now(timezone.utc)
    if now.weekday() != 4:  # Friday
        return ""
    try:
        recent_people = get_recent_people_context(limit=25)
    except Exception:
        recent_people = []
    threshold = now - timedelta(days=7)
    has_recent = False
    for p in recent_people:
        d = (_get_prop(p, "Last Updated") or "").strip()
        if not d:
            continue
        try:
            dt = datetime.fromisoformat(d.replace("Z", "+00:00"))
            if dt >= threshold:
                has_recent = True
                break
        except Exception:
            continue
    if has_recent:
        return ""
    return (
        "\n\n— Weekly reminder: Export and import your WhatsApp/Telegram chats via "
        "Dashboard -> Import Chat to refresh People Context."
    )


def send_brief_email(body: str) -> None:
    """Send the brief via SMTP. No-op if SMTP not configured."""
    if not BRIEF_EMAIL_TO or not BRIEF_SMTP_HOST:
        return
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Sovereign Brief — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}"
    msg["From"] = BRIEF_SMTP_FROM or BRIEF_SMTP_USER or "enigma@local"
    msg["To"] = BRIEF_EMAIL_TO
    msg.attach(MIMEText(_brief_body_with_followup(body), "plain"))
    port = int(BRIEF_SMTP_PORT or "587")
    with smtplib.SMTP(BRIEF_SMTP_HOST, port) as s:
        if BRIEF_SMTP_USER and BRIEF_SMTP_PASSWORD:
            s.starttls()
            s.login(BRIEF_SMTP_USER, BRIEF_SMTP_PASSWORD)
        s.sendmail(msg["From"], [BRIEF_EMAIL_TO], msg.as_string())


def send_brief_telegram(body: str) -> None:
    """Send the brief via Telegram bot. No-op if not configured."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    import urllib.request
    import urllib.parse
    import json
    text = _brief_body_with_followup(body)[:4000]
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({"chat_id": TELEGRAM_CHAT_ID, "text": text}).encode()
    req = urllib.request.Request(url, data=data, method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=10) as r:
        pass


def run_brief(hours: int = 24, return_context: bool = False):
    """
    Fetch last N hours from Nexus, open commitments, synthesize with LLM, return brief text.
    Does not send; caller can then call send_brief_email(brief) and send_brief_telegram(brief).
    If return_context is True, returns (context_text, brief); otherwise returns brief only.
    """
    since = _since_iso(hours=hours)
    commitments = get_open_commitments()
    try:
        nexus_pages = get_nexus_since(since)
    except Exception:
        nexus_pages = get_recent_nuggets(limit=100)
    try:
        thoughts = get_recent_thoughts(limit=50)
    except Exception:
        thoughts = []
    context_text = _build_context_text(commitments, nexus_pages, thoughts)
    brief = synthesize_brief(context_text)
    if return_context:
        return (context_text, brief)
    return brief


def run_and_deliver_brief(hours: int = 24) -> dict:
    """
    Run the full pipeline: fetch, synthesize, send email + Telegram.
    Returns { "brief": str, "email_sent": bool, "telegram_sent": bool }.
    Saves the brief for FR-3.4 follow-up (Life Query context).
    """
    brief = run_brief(hours=hours)
    save_last_brief(brief)
    append_brief_archive(brief)
    email_sent = False
    telegram_sent = False
    if BRIEF_EMAIL_TO and BRIEF_SMTP_HOST:
        try:
            send_brief_email(brief)
            email_sent = True
            logger.info("Sovereign Brief sent via email")
        except Exception as e:
            logger.warning("Sovereign Brief email delivery failed: %s", e)
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        try:
            send_brief_telegram(brief)
            telegram_sent = True
            logger.info("Sovereign Brief sent via Telegram")
        except Exception as e:
            logger.warning("Sovereign Brief Telegram delivery failed: %s", e)
    logger.info("Sovereign Brief generated and delivered email_sent=%s telegram_sent=%s", email_sent, telegram_sent)
    return {"brief": brief, "email_sent": email_sent, "telegram_sent": telegram_sent}
