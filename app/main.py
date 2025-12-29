from __future__ import annotations

import json

from fastapi import FastAPI, Header, Request, Response
from fastapi.responses import JSONResponse
from PIL import Image
import io
import os

from app.a2ui_state import A2UIState, apply_a2ui_messages
from app.a2ui_to_flex import a2ui_surface_to_line_flex, line_text
from app.agent import decide_a2ui_response
from app.config import settings
from app.line_api import reply_to_line, verify_line_signature

app = FastAPI()
state = A2UIState()


@app.get('/health')
async def health():
    return {"ok": True}


@app.post('/webhook')
async def webhook(
    request: Request,
    x_line_signature: str | None = Header(default=None),
):
    body = await request.body()

    if not (settings.env == 'test' or settings.allow_insecure_dev):
        if not settings.line_channel_secret:
            return JSONResponse(status_code=500, content={"ok": False, "error": "LINE_CHANNEL_SECRET not set"})
        if not x_line_signature:
            return JSONResponse(status_code=401, content={"ok": False, "error": "Missing X-Line-Signature"})

        ok = verify_line_signature(
            channel_secret=settings.line_channel_secret,
            body=body,
            signature=x_line_signature,
        )
        if not ok:
            return JSONResponse(status_code=401, content={"ok": False, "error": "Invalid signature"})

    payload = json.loads(body.decode('utf-8'))
    events = payload.get('events') or []

    for ev in events:
        await handle_event(ev)

    return {"ok": True}


async def handle_event(ev: dict) -> None:
    if ev.get('type') != 'message':
        return
    msg = ev.get('message') or {}
    if msg.get('type') != 'text':
        return

    reply_token = ev.get('replyToken')
    if not reply_token:
        return

    user_text = msg.get('text') or ''

    a2ui_messages = await decide_a2ui_response(user_text=user_text)
    apply_a2ui_messages(state, a2ui_messages)

    surface = state.surfaces.get('main')
    if surface is None:
        out = line_text('No surface')
    else:
        out = a2ui_surface_to_line_flex(surface=surface, alt_text='A2UI Demo')

    if not settings.line_channel_access_token:
        # 开发时如果你只是想看 webhook 收到什么，可以先不配 token。
        # 这里返回 200，避免 LINE 重试。
        return

    await reply_to_line(
        channel_access_token=settings.line_channel_access_token,
        reply_token=reply_token,
        messages=[out],
    )
