"""Manual Commitment Capture — transcribe, translate to default language, classify tag, push to Nexus."""
import tempfile
from typing import Optional

from enigma.config import OPENAI_API_KEY, NEXUS_DEFAULT_LANGUAGE
from enigma.orchestrator import push_to_nexus

# Sovereign tags for classification (can be extended via config later)
DEFAULT_SOVEREIGN_TAGS = (
    "commitment",
    "transient",
    "information",
    "decision",
    "tasks",
    "meetings",
)


def _openai_client():
    if not OPENAI_API_KEY or not OPENAI_API_KEY.strip():
        raise ValueError("OPENAI_API_KEY is required. Set it in .env")
    from openai import OpenAI
    return OpenAI(api_key=OPENAI_API_KEY.strip())


def transcribe_audio(audio_bytes: bytes, filename: Optional[str] = None) -> str:
    """Transcribe audio bytes using OpenAI Whisper API. Returns transcript text."""
    client = _openai_client()
    ext = ".webm"
    if filename:
        for e in (".m4a", ".mp4", ".mp3", ".mpeg", ".mpga", ".wav", ".ogg", ".flac"):
            if filename.lower().endswith(e):
                ext = e
                break
    with tempfile.NamedTemporaryFile(suffix=ext, delete=True) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        with open(tmp.name, "rb") as f:
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                file=f,
                response_format="text",
            )
    if isinstance(transcription, str):
        return transcription.strip()
    text = getattr(transcription, "text", None) or getattr(transcription, "content", None)
    return (text or "").strip()


def translate_to_default_language(text: str) -> str:
    """Translate text to NEXUS_DEFAULT_LANGUAGE (e.g. English). Returns translated text."""
    text = (text or "").strip()
    if not text:
        return text
    lang = (NEXUS_DEFAULT_LANGUAGE or "en").strip()
    if not lang or lang.lower() in ("en", "english"):
        lang = "English"
    client = _openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Translate the user's message to {lang}. "
                    "Preserve meaning and tone. Output only the translation, no explanation."
                ),
            },
            {"role": "user", "content": text},
        ],
        max_tokens=500,
    )
    out = (response.choices[0].message.content or "").strip()
    return out or text


def classify_sovereign_tag(text: str) -> str:
    """
    Classify the message into one sovereign tag using AI.
    Returns one of: commitment, transient, information, decision, tasks, meetings (or fallback commitment).
    """
    text = (text or "").strip()
    if not text:
        return "commitment"
    tags = ", ".join(DEFAULT_SOVEREIGN_TAGS)
    client = _openai_client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    f"Classify the user's message into exactly one of these tags: {tags}. "
                    "commitment = promise or obligation; transient = quick note/context; "
                    "information = fact or reference; decision = choice made; "
                    "tasks = to-do or action item; meetings = meeting note or summary. "
                    "Reply with only the single tag word, lowercase, nothing else."
                ),
            },
            {"role": "user", "content": text},
        ],
        max_tokens=20,
    )
    raw = (response.choices[0].message.content or "").strip().lower()
    for t in DEFAULT_SOVEREIGN_TAGS:
        if t in raw or raw == t:
            return t
    return "commitment"


def capture_commitment(audio_bytes: bytes, filename: Optional[str] = None) -> dict:
    """
    Transcribe audio, translate to default language, classify sovereign tag, push to Nexus.
    Returns { id, context, preview, tag }.
    """
    transcript = transcribe_audio(audio_bytes, filename=filename)
    transcript = (transcript or "").strip()
    if not transcript:
        raise ValueError("No speech detected in audio")

    # Translate to default language (e.g. English)
    content = translate_to_default_language(transcript)

    # Classify into sovereign tag
    tag = classify_sovereign_tag(content)
    context = tag.capitalize()

    page = push_to_nexus(
        context=context,
        content=content,
        priority="medium",
        tag=tag,
    )
    preview = content[:50] + ("..." if len(content) > 50 else "")
    return {
        "id": page.get("id"),
        "context": context,
        "preview": preview,
        "tag": tag,
    }


# Audio Summary Bridge (FR-2.3): People Context
SOVEREIGN_TAG_PEOPLE_CONTEXT = "people-context"
CONTEXT_PEOPLE_CONTEXT = "People Context"


def capture_people_context(audio_bytes: bytes, filename: Optional[str] = None) -> dict:
    """
    Transcribe audio, translate to default language, push to Nexus as People Context (chat/people summary).
    No classification — always tag people-context.
    Returns { id, context, preview, tag }.
    """
    transcript = transcribe_audio(audio_bytes, filename=filename)
    transcript = (transcript or "").strip()
    if not transcript:
        raise ValueError("No speech detected in audio")
    content = translate_to_default_language(transcript)
    page = push_to_nexus(
        context=CONTEXT_PEOPLE_CONTEXT,
        content=content,
        priority="medium",
        tag=SOVEREIGN_TAG_PEOPLE_CONTEXT,
    )
    preview = content[:50] + ("..." if len(content) > 50 else "")
    return {
        "id": page.get("id"),
        "context": CONTEXT_PEOPLE_CONTEXT,
        "preview": preview,
        "tag": SOVEREIGN_TAG_PEOPLE_CONTEXT,
    }


# Epic 5: Thought Memory (FR-5.1, FR-5.2)
SOVEREIGN_TAG_THOUGHT = "thought"
CONTEXT_THOUGHT = "Thought"


def capture_thought(audio_bytes: bytes, filename: Optional[str] = None) -> dict:
    """
    Transcribe audio, translate to default language, push to Nexus as Thought (no classification).
    Returns { id, context, preview, tag }.
    """
    transcript = transcribe_audio(audio_bytes, filename=filename)
    transcript = (transcript or "").strip()
    if not transcript:
        raise ValueError("No speech detected in audio")
    content = translate_to_default_language(transcript)
    page = push_to_nexus(
        context=CONTEXT_THOUGHT,
        content=content,
        priority="medium",
        tag=SOVEREIGN_TAG_THOUGHT,
    )
    preview = content[:50] + ("..." if len(content) > 50 else "")
    return {
        "id": page.get("id"),
        "context": CONTEXT_THOUGHT,
        "preview": preview,
        "tag": SOVEREIGN_TAG_THOUGHT,
    }
