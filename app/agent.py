from __future__ import annotations

import re




async def decide_a2ui_response(*, user_text: str) -> list[dict]:
    t = (user_text or "").strip()

    if re.search(r"\b(hi|hello)\b", t, re.I) or re.search(r"你好|哈囉|嗨", t):
        return hello_card()

    if re.search(r"訂位|订位|book|reservation|餐廳|餐厅|restaurant", t, re.I):
        return booking_form_like()

    if re.search(r"carousel|list|列表|輪播|轮播", t, re.I):
        return carousel_card()

    if re.search(r"confirm|confirm.*|確認|确认", t, re.I):
        return confirm_card()

    if re.search(r"location|位置|where", t, re.I):
        return location_card()

    if re.search(r"audio|music|sound|音频|音乐", t, re.I):
        return audio_card()

    if re.search(r"video|movie|视频|电影", t, re.I):
        return video_card()

    if re.search(r"help|幫助|幫助|說明|说明", t, re.I):
        return help_card()

    return fallback_card(t)


def hello_card() -> list[dict]:
    return [
        {
            "surfaceUpdate": {
                "surfaceId": "main",
                "components": [
                    {"id": "root", "component": {"Column": {"children": {"explicitList": ["title", "desc", "btn"]}}}},
                    {"id": "title", "component": {"Text": {"text": {"literalString": "你好，我是 A2UI × LINE Demo"}, "usageHint": "h1"}}},
                    {"id": "desc", "component": {"Text": {"text": {"literalString": "你可以說：\n- 幫我訂位\n- 幫助"}}}},
                    {"id": "btn", "component": {"Button": {"child": "btnText", "action": {"name": "help"}}}},
                    {"id": "btnText", "component": {"Text": {"text": {"literalString": "看幫助"}}}},
                ],
            }
        },
        {"beginRendering": {"surfaceId": "main", "root": "root"}},
    ]


def help_card() -> list[dict]:
    return [
        {
            "surfaceUpdate": {
                "surfaceId": "main",
                "components": [
                    {"id": "root", "component": {"Column": {"children": {"explicitList": ["title", "body"]}}}},
                    {"id": "title", "component": {"Text": {"text": {"literalString": "使用說明"}, "usageHint": "h1"}}},
                    {
                        "id": "body",
                        "component": {
                            "Text": {
                                "text": {
                                    "literalString": "輸入關鍵字：訂位/餐廳，我會回一個 Flex UI。\n點擊按鈕會送出 @action 指令（demo 用）。"
                                }
                            }
                        },
                    },
                ],
            }
        },
        {"beginRendering": {"surfaceId": "main", "root": "root"}},
    ]


def booking_form_like() -> list[dict]:
    return [
        {
            "surfaceUpdate": {
                "surfaceId": "main",
                "components": [
                    {"id": "root", "component": {"Card": {"child": "content"}}},
                    {"id": "content", "component": {"Column": {"children": {"explicitList": ["title", "line1", "line2", "btn"]}}}},
                    {"id": "title", "component": {"Text": {"text": {"literalString": "訂位小幫手"}, "usageHint": "h1"}}},
                    {"id": "line1", "component": {"Text": {"text": {"literalString": "這裡示範：Agent 決定用「卡片 + 按鈕」來回覆。"}}}},
                    {"id": "line2", "component": {"Text": {"text": {"literalString": "你也可以回覆：@action book"}}}},
                    {"id": "btn", "component": {"Button": {"child": "btnText", "action": {"name": "book"}}}},
                    {"id": "btnText", "component": {"Text": {"text": {"literalString": "我要訂位"}}}},
                ],
            }
        },
        {"beginRendering": {"surfaceId": "main", "root": "root"}},
    ]


def carousel_card() -> list[dict]:
    return [
        {
            "surfaceUpdate": {
                "surfaceId": "main",
                "components": [
                    {"id": "root", "component": {"Carousel": {"children": {"explicitList": ["card1", "card2", "card3"]}}}},
                    
                    # Card 1
                    {"id": "card1", "component": {"Card": {"child": "col1"}}},
                    {"id": "col1", "component": {"Column": {"children": {"explicitList": ["title1", "desc1", "btn1"]}}}},
                    {"id": "title1", "component": {"Text": {"text": {"literalString": "Option A"}, "usageHint": "h1"}}},
                    {"id": "desc1", "component": {"Text": {"text": {"literalString": "Description for A"}}}},
                    {"id": "btn1", "component": {"Button": {"child": "btnText1", "action": {"name": "opt_a"}}}},
                    {"id": "btnText1", "component": {"Text": {"text": {"literalString": "Select A"}}}},

                    # Card 2
                    {"id": "card2", "component": {"Card": {"child": "col2"}}},
                    {"id": "col2", "component": {"Column": {"children": {"explicitList": ["title2", "desc2", "btn2"]}}}},
                    {"id": "title2", "component": {"Text": {"text": {"literalString": "Option B"}, "usageHint": "h1"}}},
                    {"id": "desc2", "component": {"Text": {"text": {"literalString": "Description for B"}}}},
                    {"id": "btn2", "component": {"Button": {"child": "btnText2", "action": {"name": "opt_b"}}}},
                    {"id": "btnText2", "component": {"Text": {"text": {"literalString": "Select B"}}}},

                    # Card 3
                    {"id": "card3", "component": {"Card": {"child": "col3"}}},
                    {"id": "col3", "component": {"Column": {"children": {"explicitList": ["title3", "desc3", "btn3"]}}}},
                    {"id": "title3", "component": {"Text": {"text": {"literalString": "Option C"}, "usageHint": "h1"}}},
                    {"id": "desc3", "component": {"Text": {"text": {"literalString": "Description for C"}}}},
                    {"id": "btn3", "component": {"Button": {"child": "btnText3", "action": {"name": "opt_c"}}}},
                    {"id": "btnText3", "component": {"Text": {"text": {"literalString": "Select C"}}}},
                ],
            }
        },
        {"beginRendering": {"surfaceId": "main", "root": "root"}},
    ]


def confirm_card() -> list[dict]:
    return [
        {
            "surfaceUpdate": {
                "surfaceId": "main",
                "components": [
                    {"id": "root", "component": {"Confirm": {
                        "text": {"literalString": "您確定要提交訂位嗎？"},
                        "leftButton": {"label": "取消", "action": {"name": "cancel"}},
                        "rightButton": {"label": "確認", "action": {"name": "submit"}}
                    }}},
                ],
            }
        },
        {"beginRendering": {"surfaceId": "main", "root": "root"}},
    ]


def location_card() -> list[dict]:
    return [
        {
            "surfaceUpdate": {
                "surfaceId": "main",
                "components": [
                    {
                        "id": "root",
                        "component": {
                            "Location": {
                                "title": {"literalString": "LINE Hub"},
                                "address": {"literalString": "1-3-3 Shibuya, Shibuya-ku, Tokyo, 150-0002"},
                                "latitude": 35.65910807942215,
                                "longitude": 139.70372892916203
                            }
                        }
                    }
                ],
            }
        },
        {"beginRendering": {"surfaceId": "main", "root": "root"}},
    ]


def audio_card() -> list[dict]:
    return [
        {
            "surfaceUpdate": {
                "surfaceId": "main",
                "components": [
                    {
                        "id": "root",
                        "component": {
                            "Audio": {
                                "url": {"literalString": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
                                "duration": 60000
                            }
                        }
                    }
                ],
            }
        },
        {"beginRendering": {"surfaceId": "main", "root": "root"}},
    ]


def video_card() -> list[dict]:
    return [
        {
            "surfaceUpdate": {
                "surfaceId": "main",
                "components": [
                    {
                        "id": "root",
                        "component": {
                            "Video": {
                                "url": {"literalString": "https://www.w3schools.com/html/mov_bbb.mp4"},
                                "previewUrl": {"literalString": "https://www.w3schools.com/html/pic_trulli.jpg"}
                            }
                        }
                    }
                ],
            }
        },
        {"beginRendering": {"surfaceId": "main", "root": "root"}},
    ]


def fallback_card(user_text: str) -> list[dict]:
    return [
        {
            "surfaceUpdate": {
                "surfaceId": "main",
                "components": [
                    {"id": "root", "component": {"Column": {"children": {"explicitList": ["title", "echo", "hint"]}}}},
                    {"id": "title", "component": {"Text": {"text": {"literalString": "收到你的訊息"}, "usageHint": "h1"}}},
                    {"id": "echo", "component": {"Text": {"text": {"literalString": user_text}}}},
                    {"id": "hint", "component": {"Text": {"text": {"literalString": "試試輸入：訂位 / 幫助 / 你好"}}}},
                ],
            }
        },
        {"beginRendering": {"surfaceId": "main", "root": "root"}},
    ]
