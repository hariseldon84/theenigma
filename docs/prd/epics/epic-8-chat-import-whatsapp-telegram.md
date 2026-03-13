# Epic 8: Chat Import (WhatsApp & Telegram)

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-8.1 | Parse WhatsApp .txt export (format: `[date] sender: message`) | P2 | Extract contact from filename; create Nexus entries with People Context |
| FR-8.2 | On re-import: do NOT auto-append — LLM updates latest context for that contact | P2 | One canonical entry per contact; existing summary + new messages → single refreshed summary |
| FR-8.3 | Parse Telegram export (JSON/HTML/TXT) | P2 | Same flow as WhatsApp; map to Nexus |
| FR-8.4 | Optional: Telegram AutoCapture via Takeout API | P3 | User auth once; periodic sync to Nexus |
| FR-8.5 | Optional: "Remind me to export WhatsApp" in Sovereign Brief weekly | P3 | Brief includes reminder; links to Import Chat |

## Chat Import workflow (WhatsApp)

- User exports chat in WhatsApp (Chat → Export Chat → Without Media) → `.txt`
- Format: `[DD/MM/YYYY, HH:MM:SS] Sender: Message`
- User uploads in Enigma Web → Import Chat → Parser extracts contact from filename, dedupes → LLM summarizes → Nexus with `people-context` tag
- **Re-import:** Do not append. LLM receives existing summary + new messages → single refreshed summary; overwrite Nexus entry for that contact

## Chat Import workflow (Telegram)

- Manual: Export via Telegram Desktop → upload JSON/HTML/TXT → same flow as WhatsApp
- AutoCapture (optional): User auth via Takeout API once → periodic sync to Nexus
