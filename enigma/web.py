"""Web app: Action Sphere + Epic 6/7 dashboard APIs."""
import logging
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from enigma.auth import get_current_user
from enigma.brief_store import get_last_brief
from enigma.chat_import import import_chat_to_nexus
from enigma.commitment_capture import capture_commitment, capture_people_context, capture_thought, transcribe_audio
from enigma.config import configure_logging, AUTH_REQUIRED, SUPABASE_ANON_KEY, SUPABASE_JWT_SECRET, SUPABASE_URL
from enigma.grandmas_closet import list_grandmas_closet, save_to_grandmas_closet, weekly_closet_digest
from enigma.history_store import get_brief_archive, get_query_history
from enigma.notion_client import _get_prop, get_recent_people_context, get_recent_thoughts
from enigma.orchestrator import fetch_commitments
from enigma.query import run_life_query

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Enigma Commitment Capture", version="0.1.0")

# Serve static files (commitment capture UI) from enigma/static
STATIC_DIR = Path(__file__).resolve().parent / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class QueryBody(BaseModel):
    question: str = ""
    brief_context: Optional[str] = None


class SaveClosetBody(BaseModel):
    content: str = ""
    context: Optional[str] = None


@app.get("/api/auth/config")
async def auth_config():
    """Public: whether auth is required and Supabase client config for login (url + anon key)."""
    try:
        return {
            "authRequired": bool(AUTH_REQUIRED),
            "supabaseUrl": (SUPABASE_URL or "").strip(),
            "supabaseAnonKey": (SUPABASE_ANON_KEY or "").strip(),
        }
    except Exception as e:
        logger.exception("auth_config failed")
        return {
            "authRequired": False,
            "supabaseUrl": "",
            "supabaseAnonKey": "",
            "error": str(e),
        }


@app.get("/api/auth/status")
async def auth_status():
    """Public: verify auth env vars are loaded (no secrets). Use to debug 401 after login."""
    return {
        "authRequired": bool(AUTH_REQUIRED),
        "hasSupabaseUrl": bool((SUPABASE_URL or "").strip()),
        "hasAnonKey": bool((SUPABASE_ANON_KEY or "").strip()),
        "hasJwtSecret": bool((SUPABASE_JWT_SECRET or "").strip()),
        "ready": bool(AUTH_REQUIRED and (SUPABASE_URL or "").strip() and (SUPABASE_ANON_KEY or "").strip() and (SUPABASE_JWT_SECRET or "").strip()),
    }


@app.get("/api/brief/context")
async def get_brief_context(user: dict = Depends(get_current_user)):
    """FR-3.4: Return last delivered Sovereign Brief for Life Query follow-up."""
    try:
        brief = get_last_brief()
        return {"brief": brief}
    except Exception as e:
        logger.exception("get_brief_context failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query")
async def post_query(body: QueryBody, user: dict = Depends(get_current_user)):
    """Life Query (FR-3.3): RAG over Nexus + Commitments, return LLM answer. FR-3.4: optional brief_context."""
    try:
        answer = run_life_query(
            question=(body.question or "").strip(),
            brief_context=body.brief_context,
        )
        return {"answer": answer}
    except Exception as e:
        logger.exception("post_query failed")
        raise HTTPException(status_code=500, detail=str(e))


def _audio_extension(content_type: str, filename: str) -> str:
    ext = ".webm"
    if content_type:
        ct = content_type.lower()
        if "mp4" in ct or "m4a" in ct:
            ext = ".m4a"
        elif "mp3" in ct or "mpeg" in ct:
            ext = ".mp3"
        elif "wav" in ct:
            ext = ".wav"
        elif "ogg" in ct:
            ext = ".ogg"
    if filename:
        for e in (".m4a", ".mp4", ".mp3", ".mpeg", ".mpga", ".wav", ".ogg", ".webm"):
            if filename.lower().endswith(e):
                return e
    return ext


@app.post("/api/query/voice")
async def post_query_voice(
    audio: UploadFile = File(...),
    brief_context: Optional[str] = Form(None),
    user: dict = Depends(get_current_user),
):
    """Life Query (FR-3.3): transcribe audio with Whisper, then RAG + LLM answer. FR-3.4: optional brief_context."""
    try:
        audio_bytes = await audio.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read audio: {e}")
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file")
    content_type = (audio.content_type or "").lower()
    filename = audio.filename or "audio.webm"
    ext = _audio_extension(content_type, filename)
    if not filename.lower().endswith((".webm", ".m4a", ".mp3", ".mp4", ".wav", ".ogg", ".mpeg", ".mpga")):
        filename = "audio" + ext
    try:
        question = transcribe_audio(audio_bytes, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Transcription failed: {e}")
    if not (question or "").strip():
        raise HTTPException(status_code=400, detail="No speech detected in audio")
    try:
        answer = run_life_query(question=question.strip(), brief_context=brief_context, source="voice")
        return {"question": question.strip(), "answer": answer}
    except Exception as e:
        logger.exception("post_query_voice failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/commitments")
async def get_commitments(user: dict = Depends(get_current_user)):
    """Return Open Commitments for Action Sphere feed (FR-3.2)."""
    try:
        pages = fetch_commitments()
        out = []
        for p in pages:
            out.append({
                "id": p.get("id"),
                "context": _get_prop(p, "Context"),
                "content": _get_prop(p, "Content"),
                "tag": _get_prop(p, "Sovereign Tag"),
            })
        return out
    except Exception as e:
        logger.exception("get_commitments failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/thoughts")
async def get_thoughts(user: dict = Depends(get_current_user)):
    """Epic 7: return recent Thought Memory entries."""
    try:
        pages = get_recent_thoughts(limit=120)
        out = []
        for p in pages:
            out.append(
                {
                    "id": p.get("id"),
                    "context": _get_prop(p, "Context"),
                    "content": _get_prop(p, "Content"),
                    "tag": _get_prop(p, "Sovereign Tag"),
                    "last_updated": _get_prop(p, "Last Updated"),
                }
            )
        return out
    except Exception as e:
        logger.exception("get_thoughts failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/conversations")
async def get_conversations(user: dict = Depends(get_current_user)):
    """Epic 7: return recent People Context / conversation summaries."""
    try:
        pages = get_recent_people_context(limit=120)
        out = []
        for p in pages:
            out.append(
                {
                    "id": p.get("id"),
                    "context": _get_prop(p, "Context"),
                    "content": _get_prop(p, "Content"),
                    "tag": _get_prop(p, "Sovereign Tag"),
                    "last_updated": _get_prop(p, "Last Updated"),
                }
            )
        return out
    except Exception as e:
        logger.exception("get_conversations failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/grandmas-closet")
async def get_grandmas_closet(user: dict = Depends(get_current_user)):
    """Epic 6: list deferred ideas."""
    try:
        return list_grandmas_closet(limit=200)
    except Exception as e:
        logger.exception("get_grandmas_closet failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/grandmas-closet/save")
async def post_grandmas_closet_save(body: SaveClosetBody, user: dict = Depends(get_current_user)):
    """Epic 6: save deferred idea into Grandma's Closet."""
    try:
        return save_to_grandmas_closet(content=body.content, context=body.context or "")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("post_grandmas_closet_save failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/grandmas-closet/digest")
async def get_grandmas_closet_digest(days: int = 7, user: dict = Depends(get_current_user)):
    """Epic 6: weekly digest payload for Grandma's Closet."""
    try:
        return weekly_closet_digest(days=days)
    except Exception as e:
        logger.exception("get_grandmas_closet_digest failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/brief/archive")
async def get_briefs_archive(user: dict = Depends(get_current_user)):
    """Epic 7.2: retrieve archived Sovereign Briefs."""
    try:
        return get_brief_archive(limit=120)
    except Exception as e:
        logger.exception("get_briefs_archive failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/query/history")
async def get_life_query_history(user: dict = Depends(get_current_user)):
    """Epic 7.2: retrieve Life Query history."""
    try:
        return get_query_history(limit=200)
    except Exception as e:
        logger.exception("get_life_query_history failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/import/chat")
async def post_import_chat(
    file: UploadFile = File(...),
    platform: str = Form(...),
    user: dict = Depends(get_current_user),
):
    """Epic 7.3: import WhatsApp TXT or Telegram JSON file and store summary to Nexus."""
    try:
        raw = await file.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")
    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    try:
        return import_chat_to_nexus(platform=platform, filename=file.filename or "", file_bytes=raw)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("post_import_chat failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    """Serve the Action Sphere UI (Epic 4)."""
    sphere = STATIC_DIR / "action-sphere.html"
    if sphere.exists():
        return FileResponse(sphere)
    index = STATIC_DIR / "index.html"
    if index.exists():
        return FileResponse(index)
    raise HTTPException(status_code=404, detail="Static files not found")


@app.get("/dashboard")
async def dashboard_page():
    """Serve Epic 7 dashboard UI."""
    page = STATIC_DIR / "dashboard.html"
    if not page.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    return FileResponse(page)


@app.get("/login")
async def login_page():
    """Serve the login page (Supabase Auth)."""
    login = STATIC_DIR / "login.html"
    if not login.exists():
        raise HTTPException(status_code=404, detail="Static files not found")
    return FileResponse(login)


@app.get("/capture")
async def capture_page():
    """Serve the commitment capture page (standalone)."""
    index = STATIC_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Static files not found")
    return FileResponse(index)


def _detail_msg(detail) -> str:
    """Turn FastAPI detail (str or list) into a single string for the UI."""
    if isinstance(detail, str):
        return detail
    if isinstance(detail, list) and detail:
        first = detail[0]
        if isinstance(first, dict) and "msg" in first:
            return first.get("msg", str(first))
        return str(first)
    return str(detail)


@app.post("/api/commitment")
async def post_commitment(
    audio: UploadFile = File(...),
    type: str = Form("commitment"),
    user: dict = Depends(get_current_user),
):
    """
    Accept audio file (multipart) and type (commitment | people_context | thought).
    Commitment: transcribe, translate, classify, push to Nexus.
    People context: transcribe, translate, push with tag people-context (Audio Summary Bridge).
    Thought (Epic 5): transcribe, translate, push with tag thought (Thought Memory).
    Returns { "id", "context", "preview", "tag" }.
    """
    try:
        audio_bytes = await audio.read()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read audio: {e}")
    if not audio_bytes:
        raise HTTPException(status_code=400, detail="Empty audio file")
    content_type = (audio.content_type or "").lower()
    ext = ".webm"
    if "mp4" in content_type or "m4a" in content_type:
        ext = ".m4a"
    elif "mp3" in content_type or "mpeg" in content_type:
        ext = ".mp3"
    elif "wav" in content_type:
        ext = ".wav"
    elif "ogg" in content_type:
        ext = ".ogg"
    filename = audio.filename or ("audio" + ext)
    if not filename.lower().endswith((".webm", ".m4a", ".mp3", ".mp4", ".wav", ".ogg", ".mpeg", ".mpga")):
        filename = "audio" + ext
    capture_type = (type or "commitment").strip().lower()
    if capture_type not in ("commitment", "people_context", "thought"):
        capture_type = "commitment"
    try:
        if capture_type == "people_context":
            result = capture_people_context(audio_bytes, filename=filename)
        elif capture_type == "thought":
            result = capture_thought(audio_bytes, filename=filename)
        else:
            result = capture_commitment(audio_bytes, filename=filename)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("post_commitment failed capture_type=%s", capture_type)
        raise HTTPException(status_code=500, detail=str(e))
