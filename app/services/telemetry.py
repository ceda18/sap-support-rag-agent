from datetime import datetime, timezone

import httpx

from core.config import settings

# SUMMARY:
# Sends one telemetry record per answered question to the n8n webhook. Fire-and-forget:
# if n8n is down or slow, the user still gets their Slack answer, we just lose that one
# telemetry row.


async def send_telemetry(question: str, result: dict, user_id: str = "unknown") -> None:
    if not settings.N8N_WEBHOOK_URL:
        return

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_id": user_id,
        "query": question,
        "answer": result["answer"],
        "unanswered": result["unanswered"],
        "out_of_scope": result["out_of_scope"],
        "sources": result["sources"],
        "cost_usd": result.get("cost_usd", 0.0),
        **result.get("usage", {}),
    }

    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            await client.post(settings.N8N_WEBHOOK_URL, json=payload)
    except Exception:
        pass  # telemetry must never break the user-facing answer