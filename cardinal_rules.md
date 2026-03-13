# Enigma OS — Cardinal Rules for Development

**Purpose:** Technical architecture first, product-ready for SaaS in future.

---

## 1. Architecture & Structure

### 1.1 Layered Architecture

- **Data layer:** Notion (Nexus), Supabase (Vault, Auth). No business logic in DB.
- **Service layer:** `enigma/` — orchestration, clients, domain logic. No UI code.
- **API layer:** REST or Edge Functions. Stateless; auth on every request.
- **Presentation layer:** Flutter/FlutterFlow (mobile), Web (dashboard). Consume API only.

**Rule:** Dependencies flow inward. UI → API → Service → Data. Never the reverse.

### 1.2 Multi-Tenancy Readiness

- **User/tenant ID:** Every Nexus query, Vault insert, and Brief must be scoped by `user_id` or `tenant_id`.
- **Schema:** Add `user_id` (or `tenant_id`) to all tables and Notion filters as soon as multi-user is planned.
- **Isolation:** No cross-tenant data access. Enforce in service layer, not just UI.

**Rule:** Assume multi-user from day one. Single-user MVP = `user_id` constant; schema supports switch.

### 1.3 Configuration Over Code

- All secrets, URLs, feature flags → environment variables or config service.
- No hardcoded API keys, DB IDs, or deployment-specific values.
- Use `.env.example` as the single source of truth for required vars.

**Rule:** `if os.getenv("X")` is fine; `X = "hardcoded"` is not.

---

## 2. Security

### 2.1 Secrets & Credentials

- Never commit `.env`, API keys, or service role keys.
- Use Supabase Service Role only server-side; never in client bundles.
- Rotate keys on compromise; support key rotation without code change.

### 2.2 Encryption

- **Vault:** AES-256 at app layer before insert. Key from env or KMS.
- **In transit:** HTTPS only. No plain HTTP for APIs.
- **At rest:** Supabase/Notion handle DB encryption; we encrypt sensitive payloads in Vault.

### 2.3 Auth & Authorization

- Supabase Auth for user identity. JWT or session-based.
- Every API endpoint validates auth before processing.
- Row-level security (RLS) on Supabase tables when multi-user.

**Rule:** No "trust the client." Validate identity and permissions server-side.

---

## 3. Data & Storage

### 3.1 Nexus (Notion)

- Sovereign Tags: `commitment`, `thought`, `transient`, `people-context`, `grandmas-closet`.
- Query by tag + time window. Paginate large result sets.
- Notion API 2025: Use `data_sources.query` when `databases.query` is deprecated.

### 3.2 Vault (Supabase)

- Encrypt before insert. Store `key_type`, `encrypted_data`, `metadata`.
- No PII in logs. No raw sensitive data in error messages.

### 3.3 Idempotency & Deduplication

- Chat import: one canonical entry per contact. Re-import = merge, not append.
- Use idempotency keys for critical writes (e.g., Brief delivery) when scaling.

---

## 4. API Design (SaaS-Ready)

### 4.1 REST Conventions

- `GET` for reads, `POST` for creates, `PATCH` for updates, `DELETE` for deletes.
- Version API: `/v1/` prefix or `Accept` header. No breaking changes without version bump.
- Return JSON. Use consistent error shape: `{ "error": "...", "code": "..." }`.

### 4.2 Rate Limiting & Quotas

- Plan for rate limits (per user, per endpoint) when moving to SaaS.
- Document limits in API docs. Return `429` with `Retry-After` when exceeded.

### 4.3 Observability

- Structured logging (JSON). Include `request_id`, `user_id`, `action`.
- Log levels: DEBUG (dev), INFO (prod), WARN/ERROR for failures.
- No PII in logs. Redact emails, names, content in production.

---

## 5. Frontend & UI

### 5.1 Milan Minimalism

- **Colors:** Obsidian Black `#050505`, Titanium White, Electric Cerulean accent.
- **Style:** Liquid Glass (~80% backdrop blur), Zero-UI, minimal chrome.
- **Typography:** San Francisco or Inter; bold, high-contrast.

**Rule:** Every new screen must pass a "Milan Minimalism" review.

### 5.2 Accessibility

- Semantic HTML / accessible widgets. Keyboard navigation.
- Sufficient contrast. Support reduced motion where possible.

### 5.3 Responsive

- Mobile-first for Action Sphere (orb). Web dashboard responsive.
- No fixed widths that break on small screens.

---

## 6. LLM & AI

### 6.1 Human-in-the-Loop

- No auto-send for drafts, replies, or external actions. User approves.
- Brief is read-only synthesis. Life Query is read-only. No side effects without confirmation.

### 6.2 Cost & Latency

- Cache RAG results where possible. Limit context window size.
- Use cheaper models for classification; reserve premium for synthesis.
- Timeout LLM calls (e.g., 30s). Fail gracefully.

### 6.3 Privacy

- User data stays in our stack. No training on user content without explicit consent.
- Log prompts/responses only for debugging; redact in production.

---

## 7. Deployment & Ops

### 7.1 Environment Parity

- Dev, staging, prod use same code paths. Differences only in config.
- No "if production" branches for business logic. Use feature flags instead.

### 7.2 Failures

- Services fail gracefully. Health checks for Notion, Supabase, LLM.
- Retry with backoff for transient failures. Circuit breaker for repeated failures.

### 7.3 Migrations

- Schema changes via migrations (Supabase). Version migrations. No manual ALTER in prod.

---

## 8. Code Quality

### 8.1 Naming

- `user_id` not `uid`. `created_at` not `timestamp`. Clear, consistent.
- Functions: verb + noun. `fetch_commitments`, `push_to_nexus`.

### 8.2 Testing

- Unit tests for orchestration and business logic.
- Integration tests for Notion/Supabase (use test DB).
- No tests that hit production APIs with real data.

### 8.3 Dependencies

- Pin versions in `requirements.txt`. Audit for CVEs.
- Prefer standard library; add deps only when justified.

---

## 9. SaaS Checklist (Future)

When moving to multi-tenant SaaS, ensure:

- [ ] `user_id` / `tenant_id` on all data
- [ ] Supabase RLS enabled
- [ ] Billing / usage tracking hooks
- [ ] Rate limits per tenant
- [ ] Audit log for sensitive actions
- [ ] Data export / deletion (GDPR)
- [ ] Feature flags for gradual rollout

---

## 10. Anti-Patterns (Never Do)

- **No** direct Notion/Supabase access from client (use API layer).
- **No** storing secrets in code or config files in repo.
- **No** logging PII or raw user content.
- **No** breaking changes without versioning.
- **No** skipping auth on "internal" endpoints.
- **No** hardcoding tenant or user IDs in business logic.
