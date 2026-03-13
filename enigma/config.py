"""Load configuration from environment."""
import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get(key: str, default: str = "") -> str:
    return os.getenv(key, default)


# Logging: env-based level (DEBUG, INFO, WARNING, ERROR). Default INFO.
LOG_LEVEL = (get("LOG_LEVEL") or "INFO").upper()
LOG_LEVEL = LOG_LEVEL if LOG_LEVEL in ("DEBUG", "INFO", "WARNING", "ERROR") else "INFO"


def configure_logging():
    """Configure root logger with env-based level and a simple format."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


# Notion (The Nexus)
NOTION_API_KEY = get("NOTION_API_KEY")
NOTION_NEXUS_DATABASE_ID = get("NOTION_NEXUS_DATABASE_ID")

# Supabase (The Vault)
SUPABASE_URL = get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = get("SUPABASE_SERVICE_KEY")
# Supabase Auth (optional): anon key for client-side login; JWT secret for backend verification.
# When AUTH_REQUIRED=1, /api/* routes require Authorization: Bearer <access_token>.
SUPABASE_ANON_KEY = (get("SUPABASE_ANON_KEY") or "").strip()
SUPABASE_JWT_SECRET = (get("SUPABASE_JWT_SECRET") or "").strip()
AUTH_REQUIRED = get("AUTH_REQUIRED", "").strip().lower() in ("1", "true", "yes")

# Web server port (default 5000; use e.g. 8000 if 5000 is taken by AirPlay on macOS)
WEB_PORT = int(get("PORT") or get("WEB_PORT") or "5000")

# Vault encryption (AES-256). Must be base64-encoded 32-byte key.
# Generate: python -c "import secrets, base64; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
VAULT_ENCRYPTION_KEY = get("VAULT_ENCRYPTION_KEY")

# Omni-Scribe (Desktop Sentinel): push interval in minutes
NEXUS_PUSH_INTERVAL_MIN = int(get("NEXUS_PUSH_INTERVAL_MIN") or "15")

# Manual Commitment Capture (FR-2.2): OpenAI Whisper + classification/translation
OPENAI_API_KEY = get("OPENAI_API_KEY")

# Default language for Nexus: all captured content is translated to this (e.g. "en", "English")
NEXUS_DEFAULT_LANGUAGE = get("NEXUS_DEFAULT_LANGUAGE") or "en"

# Sovereign Brief (FR-3.1): delivery time (HH:MM 24h, local or UTC depending on CRON)
BRIEF_DELIVERY_TIME = get("BRIEF_DELIVERY_TIME") or "09:00"
# Email
BRIEF_EMAIL_TO = get("BRIEF_EMAIL_TO")
BRIEF_SMTP_HOST = get("BRIEF_SMTP_HOST")
BRIEF_SMTP_PORT = get("BRIEF_SMTP_PORT") or "587"
BRIEF_SMTP_USER = get("BRIEF_SMTP_USER")
BRIEF_SMTP_PASSWORD = get("BRIEF_SMTP_PASSWORD")
BRIEF_SMTP_FROM = get("BRIEF_SMTP_FROM")
# Telegram
TELEGRAM_BOT_TOKEN = get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = get("TELEGRAM_CHAT_ID")

# FR-3.4 Brief-to-Query: base URL for "Ask follow-up" link in Brief (e.g. https://yourapp.com). If empty, link is path-only.
BRIEF_APP_BASE_URL = get("BRIEF_APP_BASE_URL") or ""
# Path to file storing last delivered brief (for Life Query follow-up). Default: project root .last_sovereign_brief
BRIEF_LAST_FILE_PATH = get("BRIEF_LAST_FILE_PATH") or ""
