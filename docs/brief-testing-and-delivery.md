# Testing the Sovereign Brief and Configuring Email + Telegram

## 1. Testing: Last 24h Nexus + LLM synthesis

### See the synthesized output (no code change)

Run:

```bash
python -m enigma.main brief-only
```

This fetches Open Commitments + Nexus (last 24h via "Last Updated" filter), builds context, calls the LLM, and prints the brief to stdout. You should see headings and bullets for **priorities**, **open commitments**, and **suggested actions**.

### Verify which data was sent to the LLM

Run with `--show-context` (or `--debug`):

```bash
python -m enigma.main brief-only --show-context
```

- **Stderr:** Raw context (OPEN COMMITMENTS and NEXUS LAST 24H blocks) that was sent to the LLM.
- **Stdout:** The synthesized Sovereign Brief.

Use this to confirm exactly which commitments and Nexus entries (last 24h) were used and that the brief is derived from that context.

### Sanity check that Nexus is included

1. Add or update a few entries in your Notion Nexus (e.g. via the web capture or `push`).
2. Run `brief-only` again (with or without `--show-context`).
3. Confirm the brief mentions or reflects those items.

### If the brief is empty or generic

Likely causes: no Open Commitments and no Nexus rows with "Last Updated" in the last 24h. Add at least one commitment (Sovereign Tag containing "commitment") and some Nexus rows with "Last Updated" set, then re-run.

---

## 2. Configuring Email (SMTP) for sending the Brief

Set these in your `.env` (see [.env.example](../.env.example) in the project root).

| Variable | Meaning | Example |
|----------|---------|---------|
| `BRIEF_EMAIL_TO` | Where the brief is sent | `you@example.com` |
| `BRIEF_SMTP_HOST` | SMTP server | `smtp.gmail.com` or `smtp.sendgrid.net` |
| `BRIEF_SMTP_PORT` | Usually 587 (TLS) | `587` |
| `BRIEF_SMTP_USER` | Login / sender identity | Your email or `apikey` (SendGrid) |
| `BRIEF_SMTP_PASSWORD` | Password or app password | Gmail App Password or SendGrid API key |
| `BRIEF_SMTP_FROM` | From header (optional) | `Enigma <you@example.com>` |

### Gmail

1. Turn on 2FA for your Google account.
2. Create an **App Password**: Google Account → Security → 2-Step Verification → App passwords → generate for "Mail".
3. In `.env`:
   - `BRIEF_SMTP_HOST=smtp.gmail.com`
   - `BRIEF_SMTP_PORT=587`
   - `BRIEF_SMTP_USER=your@gmail.com`
   - `BRIEF_SMTP_PASSWORD=<the-16-char-app-password>`
   - `BRIEF_EMAIL_TO=your@gmail.com` (or another address)
   - `BRIEF_SMTP_FROM=Enigma <your@gmail.com>` (optional)

### SendGrid (or other SMTP relay)

1. Create an API key (or get SMTP credentials) in the provider dashboard.
2. In `.env` use the host/port they give (e.g. `smtp.sendgrid.net`, 587), and set `BRIEF_SMTP_USER` / `BRIEF_SMTP_PASSWORD` to the SMTP credentials (often `apikey` and the API key for SendGrid), plus `BRIEF_EMAIL_TO` and optionally `BRIEF_SMTP_FROM`.

### Test email

Run:

```bash
python -m enigma.main brief
```

(with `OPENAI_API_KEY` and Notion configured). If email is configured, the brief is sent to `BRIEF_EMAIL_TO`. Check inbox and spam.

---

## 3. Configuring Telegram for sending the Brief

Set these in your `.env`:

| Variable | Meaning | Example |
|----------|---------|---------|
| `TELEGRAM_BOT_TOKEN` | Token from BotFather | `123456789:AAH...` |
| `TELEGRAM_CHAT_ID` | Chat where the bot sends the message | `123456789` or `-100...` for groups |

### Get the token

1. In Telegram, open [@BotFather](https://t.me/BotFather).
2. Send `/newbot`, follow the prompts, copy the **token** (e.g. `123456789:AAH...`).
3. In `.env`: `TELEGRAM_BOT_TOKEN=123456789:AAH...`

### Get the chat ID

**Option A (simple):**

1. Start a chat with your bot (search by bot name, press "Start").
2. Send any message to the bot (e.g. "hi").
3. In a browser open (replace `YOUR_TOKEN` with your token):
   `https://api.telegram.org/botYOUR_TOKEN/getUpdates`
4. In the JSON, find `"chat":{"id": 123456789}`. That number is `TELEGRAM_CHAT_ID`.

**Option B:** Use a helper like [@userinfobot](https://t.me/userinfobot); or use getUpdates as above.

**Groups:** Add the bot to the group; the group chat id is usually negative (e.g. `-1001234567890`). Get it from `getUpdates` after sending a message in the group.

In `.env`: `TELEGRAM_CHAT_ID=123456789`

### Test Telegram

Run:

```bash
python -m enigma.main brief
```

With `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` set, the brief is sent to that chat. You can leave email vars unset and only test Telegram.

---

## 4. Summary

| Goal | Action |
|------|--------|
| Test last 24h Nexus + LLM synthesis | Run `python -m enigma.main brief-only` |
| See raw context sent to LLM | Run `python -m enigma.main brief-only --show-context` |
| Test email delivery | Set `BRIEF_EMAIL_TO` + `BRIEF_SMTP_*` in `.env`, run `python -m enigma.main brief` |
| Test Telegram delivery | Set `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`, run `python -m enigma.main brief` |
