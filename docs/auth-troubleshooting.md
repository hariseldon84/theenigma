# Auth login — troubleshooting

## "Could not load auth config"

This means the login page could not reach `GET /api/auth/config`. After the latest update, the message will include the actual error (e.g. "Failed to fetch" or "Server returned 500"). Use that to narrow down the cause.

### 1. Open the app from the same origin as the API

The login page must be served by the same Enigma server that serves `/api/auth/config`.

- **Correct:** Open **http://127.0.0.1:5000** in the browser. You get redirected to **http://127.0.0.1:5000/login**. The page then calls `http://127.0.0.1:5000/api/auth/config`.
- **Wrong:** Opening the HTML file from disk (**file:///.../login.html**) or from another port (e.g. a Vite dev server on 5173). Then `fetch('/api/auth/config')` goes to the wrong place and you get "Failed to fetch" or CORS errors.

**Fix:** Always open **http://127.0.0.1:5000** (or **http://127.0.0.1:8000** if you set `PORT=8000`). Do not open the project folder in the browser via file://.

### 2. Server must be running

If the Enigma web server is not running, the fetch will fail (e.g. "Failed to fetch" or "net::ERR_CONNECTION_REFUSED").

**Fix:** In a terminal:

```bash
cd /Users/anandarora/thenigma
.venv/bin/python -m enigma.main web
```

Leave it running, then open http://127.0.0.1:5000 in the browser.

### 3. Check the browser console

Open DevTools (F12 or right‑click → Inspect) → **Console** tab. When you load the login page, look for:

- **Failed to fetch** → Network issue or wrong URL (see 1 and 2).
- **CORS** errors → You are on a different origin (e.g. frontend on another port). Use the same origin (open the app at 127.0.0.1:5000).
- **404** or **500** → Note the exact URL and response; the server may be misconfigured or the route missing.

### 4. Check .env (Supabase Auth)

For auth to be required and for the login form to work, you need:

- `AUTH_REQUIRED=1` (or `true` / `yes`)
- `SUPABASE_URL=` your project URL (e.g. `https://xxxx.supabase.co`)
- `SUPABASE_ANON_KEY=` the **anon public** key from Supabase (Settings → API)
- `SUPABASE_JWT_SECRET=` the JWT secret (Settings → API) for backend verification

If `SUPABASE_ANON_KEY` or `SUPABASE_URL` is missing or wrong, the auth config endpoint still returns 200; the login page then redirects to `/` when it sees `authRequired: false` or empty keys. So "Could not load auth config" usually means the **request never succeeded** (network / origin), not missing .env. To confirm the API response, open **http://127.0.0.1:5000/api/auth/config** in the browser; you should see JSON like:

```json
{"authRequired": true, "supabaseUrl": "https://....supabase.co", "supabaseAnonKey": "eyJ..."}
```

### 5. Quick test from the command line

With the server running:

```bash
curl -s http://127.0.0.1:5000/api/auth/config
```

You should get JSON. If you get "Connection refused", the server is not running or is on another port.

---

## Login: email + password

Login uses **email and password**: sign in with an existing account or use “Create an account” to sign up.

### Forgot password

Use **Forgot password?** on the login page. Enter your email and click **Send reset link**. Supabase sends a reset email; the link brings you back to `/login` to set a new password. The redirect URL (e.g. `http://127.0.0.1:5000/login`) must be allowlisted in Supabase: **Authentication → URL Configuration → Redirect URLs**.

### "Email rate limit exceeded"

Supabase limits how often password-reset (and other auth) emails can be sent, per email and per project. The limit is not just one minute—it can be longer (e.g. an hour). If you see this: wait at least an hour before requesting another reset link; if you still know your current password, sign in with it. To relax limits in development, check Supabase Dashboard → **Authentication** → **Rate Limits** if your plan exposes it. Enigma cannot change this limit; it is enforced by Supabase.

### Logged in but then 401 and redirected back to login (flash of Action Sphere then login again)

This means **login succeeds** (Supabase gives you a token and we store it), but when the app calls `/api/commitments` (or any protected API), the **backend rejects the token** and returns 401. The app then clears the token and sends you back to the login page.

**Cause:** The backend verifies the JWT using `SUPABASE_JWT_SECRET` in your `.env`. If that value does **not** exactly match the **JWT Secret** of the same Supabase project that issued the token (the one you use for `SUPABASE_URL` and `SUPABASE_ANON_KEY`), verification fails and the server returns 401.

**Fix:**

1. Open **Supabase Dashboard** → your project → **Project Settings** (gear) → **API** (or **JWT**).
2. Find the field labeled **JWT Secret** (or **JWT Signing Secret**). Copy it exactly—no extra spaces or newlines.
3. In your project root, set in `.env`:
   ```bash
   SUPABASE_JWT_SECRET=<paste the JWT Secret here>
   ```
4. Restart the Enigma web server so it picks up the new value.

**Do not** use the anon key or service role key as `SUPABASE_JWT_SECRET`. The JWT Secret is a separate value in the API/JWT settings. All three (`SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_JWT_SECRET`) must be from the **same** Supabase project.
