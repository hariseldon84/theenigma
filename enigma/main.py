"""CLI entrypoint — health check and quick tests."""
import sys

from enigma.config import configure_logging
from enigma.notion_client import get_recent_nuggets, _get_prop
from enigma.orchestrator import health_check, fetch_commitments, push_to_nexus, store_in_vault, read_from_vault
from enigma.sentinel import push_sample, run_loop
from enigma.brief import run_brief, run_and_deliver_brief


def main():
    configure_logging()
    if len(sys.argv) < 2:
        print("Usage: python -m enigma.main <command>")
        print("  health     — Check Notion + Supabase connectivity")
        print("  commitments — Fetch Open Commitments from Nexus")
        print("  push       — Push a test nugget (usage: push 'context' 'content')")
        print("  vault-set  — Store encrypted test value in Vault (usage: vault-set 'key_type' 'payload')")
        print("  vault-get  — List Vault rows (decrypted); optional: vault-get <key_type>")
        print("  sentinel   — Omni-Scribe: run loop (window + clipboard → Nexus every N min)")
        print("  sentinel-once — Push one sample to Nexus and exit")
        print("  nexus-recent — Show recent Nexus rows with Context and Last Updated (default 3)")
        print("  web        — Run Commitment Capture web app (http://127.0.0.1:<PORT>, default 5000)")
        print("  brief      — Generate and deliver Sovereign Brief (email + Telegram if configured)")
        print("  brief-only — Generate Brief and print to stdout (no delivery); use --show-context to print raw context then brief")
        print("  thought-stitch — Epic 5: LLM themes/suggestions from Thought Memory (run weekly)")
        sys.exit(1)

    cmd = sys.argv[1].lower()

    if cmd == "health":
        r = health_check()
        print("Notion:", "OK" if r["notion"] else "FAIL")
        print("Supabase:", "OK" if r["supabase"] else "FAIL")
        if r["errors"]:
            for e in r["errors"]:
                print("  Error:", e)
        sys.exit(0 if r["notion"] and r["supabase"] else 1)

    if cmd == "commitments":
        items = fetch_commitments()
        print(f"Open Commitments: {len(items)}")
        for i in items:
            props = i.get("properties", {})
            ctx = props.get("Context", {}).get("title", [{}])[0].get("plain_text", "?")
            print(f"  - {ctx}")
        sys.exit(0)

    if cmd == "push":
        if len(sys.argv) < 4:
            print("Usage: python -m enigma.main push 'context' 'content'")
            sys.exit(1)
        ctx, content = sys.argv[2], sys.argv[3]
        page = push_to_nexus(context=ctx, content=content)
        print("Created:", page.get("id", "?"))
        sys.exit(0)

    if cmd == "vault-set":
        if len(sys.argv) < 4:
            print("Usage: python -m enigma.main vault-set 'key_type' 'payload'")
            sys.exit(1)
        key_type, payload = sys.argv[2], sys.argv[3]
        row = store_in_vault("vault", {"key_type": key_type, "payload": payload, "metadata": {}})
        print("Stored (encrypted):", row.get("id", "?"))
        sys.exit(0)

    if cmd == "vault-get":
        # Optional arg = key_type value to filter by (e.g. vault-get qa_test)
        filters = {"key_type": sys.argv[2]} if len(sys.argv) > 2 else None
        rows = read_from_vault("vault", filters)
        print(f"Vault rows: {len(rows)}")
        for r in rows:
            print(f"  id={r.get('id')} key_type={r.get('key_type')} data={r.get('data')}")
        sys.exit(0)

    if cmd == "sentinel-once":
        ok = push_sample()
        print("Pushed to Nexus" if ok else "Push failed")
        sys.exit(0 if ok else 1)

    if cmd == "sentinel":
        interval = int(sys.argv[2]) if len(sys.argv) > 2 else None
        run_loop(interval_min=interval)
        sys.exit(0)

    if cmd == "nexus-recent":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        pages = get_recent_nuggets(limit=limit)
        print(f"Recent Nexus rows (up to {limit}):")
        for i, p in enumerate(pages, 1):
            ctx = _get_prop(p, "Context")
            last_updated = _get_prop(p, "Last Updated")
            print(f"  {i}. Context: {ctx or '(empty)'}")
            print(f"     Last Updated: {last_updated or '(not set)'}")
        sys.exit(0)

    if cmd == "web":
        import uvicorn
        from enigma.config import WEB_PORT
        uvicorn.run("enigma.web:app", host="127.0.0.1", port=WEB_PORT, reload=False)
        sys.exit(0)

    if cmd == "brief-only":
        show_context = "--show-context" in sys.argv or "--debug" in sys.argv
        if show_context:
            context_text, brief = run_brief(hours=24, return_context=True)
            print("--- Context (input to LLM) ---", file=sys.stderr)
            print(context_text, file=sys.stderr)
            print("--- Sovereign Brief ---", file=sys.stderr)
            print(brief)
        else:
            text = run_brief(hours=24)
            print(text)
        sys.exit(0)

    if cmd == "brief":
        result = run_and_deliver_brief(hours=24)
        print(result["brief"])
        if result.get("email_sent"):
            print("(Email sent)", file=sys.stderr)
        if result.get("telegram_sent"):
            print("(Telegram sent)", file=sys.stderr)
        sys.exit(0)

    if cmd == "thought-stitch":
        from enigma.thought_stitch import run_stitch
        summary = run_stitch()
        if summary:
            print(summary)
        else:
            print("No output from thought stitch.", file=sys.stderr)
        sys.exit(0)

    print("Unknown command:", cmd)
    sys.exit(1)


if __name__ == "__main__":
    main()
