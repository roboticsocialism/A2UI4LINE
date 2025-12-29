from __future__ import annotations

import base64
import hashlib
import hmac

import httpx


def verify_line_signature(*, channel_secret: str, body: bytes, signature: str) -> bool:
    mac = hmac.new(channel_secret.encode("utf-8"), body, hashlib.sha256).digest()
    expected = base64.b64encode(mac).decode("ascii")

    try:
        return hmac.compare_digest(expected, signature)
    except Exception:
        return False


async def reply_to_line(*, channel_access_token: str, reply_token: str, messages: list[dict]) -> None:
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Authorization": f"Bearer {channel_access_token}",
        "Content-Type": "application/json",
    }
    payload = {"replyToken": reply_token, "messages": messages}

    async with httpx.AsyncClient(timeout=10.0) as client:
        r = await client.post(url, headers=headers, json=payload)

    if r.status_code >= 300:
        raise RuntimeError(f"LINE reply failed: {r.status_code} {r.text}")
