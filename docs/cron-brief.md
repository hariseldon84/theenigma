# CRON setup for Sovereign Brief

**Purpose:** Run the Sovereign Brief daily at 09:00 so the digest is delivered automatically (FR-3.1).

---

## Quick setup

1. From the project root, run once manually to confirm env and delivery:
   ```bash
   cd /path/to/thenigma
   .venv/bin/python -m enigma.main brief
   ```

2. Open crontab:
   ```bash
   crontab -e
   ```

3. Add one line (replace `/path/to/thenigma` with your repo path):
   ```
   0 9 * * * cd /path/to/thenigma && .venv/bin/python -m enigma.main brief
   ```

4. Save and exit. Verify with `crontab -l`.

---

## Details

- **Time:** `0 9 * * *` = 09:00 every day in the **system time zone** of the machine. For UTC, set the server TZ to UTC or run in a container/env that uses UTC.
- **Path:** Use an absolute path. Cron runs with a minimal environment; `cd` into the repo so `.env` (in the project root) is loaded by the app.
- **Python:** Use the project venv (`.venv/bin/python`) so the same dependencies and interpreter as local runs are used.

---

## Optional: log output

To capture stdout/stderr for debugging:

```
0 9 * * * cd /path/to/thenigma && .venv/bin/python -m enigma.main brief >> /path/to/thenigma/logs/brief.log 2>&1
```

Create `logs` first: `mkdir -p /path/to/thenigma/logs`. Rotate or truncate the log periodically to avoid growth.

---

## Troubleshooting

| Issue | What to check |
|-------|----------------|
| Brief not received | Run the same command by hand from the repo directory. Check `.env` (NOTION_*, OPENAI_*, BRIEF_EMAIL_* or TELEGRAM_*). |
| Cron not running | `crontab -l` shows the job; ensure no typo in path. On macOS, grant Full Disk Access to cron if needed. |
| Wrong time zone | Cron uses system TZ. Run `date` and adjust the hour in the cron expression (e.g. `0 14 * * *` for 14:00 local). |

---

## Related

- [README — Sovereign Brief](../README.md#sovereign-brief-fr-31)
- [docs/brief-testing-and-delivery.md](brief-testing-and-delivery.md) — testing and Email/Telegram config
