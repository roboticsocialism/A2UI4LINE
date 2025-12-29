from app.a2ui_state import A2UIState, apply_a2ui_messages
from app.a2ui_to_flex import a2ui_surface_to_line_flex


def test_convert_simple_column_text_button_to_line_flex():
    state = A2UIState()

    apply_a2ui_messages(
        state,
        [
            {
                "surfaceUpdate": {
                    "surfaceId": "main",
                    "components": [
                        {"id": "root", "component": {"Column": {"children": {"explicitList": ["t", "b"]}}}},
                        {"id": "t", "component": {"Text": {"text": {"literalString": "Hello"}}}},
                        {"id": "b", "component": {"Button": {"child": "bt", "action": {"name": "ok"}}}},
                        {"id": "bt", "component": {"Text": {"text": {"literalString": "OK"}}}},
                    ],
                }
            },
            {"beginRendering": {"surfaceId": "main", "root": "root"}},
        ],
    )

    surface = state.surfaces["main"]
    msg = a2ui_surface_to_line_flex(surface=surface, alt_text="demo")

    assert msg["type"] == "flex"
    assert msg["contents"]["type"] == "bubble"
    body = msg["contents"]["body"]
    assert body["type"] == "box"
    assert body["layout"] == "vertical"

    text, btn = body["contents"]
    assert text["type"] == "text"
    assert text["text"] == "Hello"
    assert btn["type"] == "button"
    assert btn["action"]["type"] == "message"


def test_convert_carousel_to_line_flex():
    state = A2UIState()

    apply_a2ui_messages(
        state,
        [
            {
                "surfaceUpdate": {
                    "surfaceId": "main",
                    "components": [
                        {"id": "root", "component": {"Carousel": {"children": {"explicitList": ["c1", "c2"]}}}},
                        {"id": "c1", "component": {"Card": {"child": "t1"}}},
                        {"id": "t1", "component": {"Text": {"text": {"literalString": "Card 1"}}}},
                        {"id": "c2", "component": {"Card": {"child": "t2"}}},
                        {"id": "t2", "component": {"Text": {"text": {"literalString": "Card 2"}}}},
                    ],
                }
            },
            {"beginRendering": {"surfaceId": "main", "root": "root"}},
        ],
    )

    surface = state.surfaces["main"]
    msg = a2ui_surface_to_line_flex(surface=surface, alt_text="carousel demo")

    assert msg["type"] == "flex"
    contents = msg["contents"]
    assert contents["type"] == "carousel"
    assert len(contents["contents"]) == 2
    
    b1 = contents["contents"][0]
    assert b1["type"] == "bubble"
    assert b1["body"]["type"] == "box"
    
    # Check content of first card
    # Note: Card component wraps its child in a box with padding/border
    # So b1["body"] is the outer box of the Card.
    # Inside it, we expect the child content.
    # Let's verify based on component_to_flex_element for Card:
    # It returns a box with vertical layout and one child (the content).
    # Wait, in a2ui_to_flex.py:
    # "contents": [component_to_flex_box(component_id=child_id, component=cc, surface=surface)]
    # So the Card's box contains another box (from component_to_flex_box) which contains the text.
    
    card_box = b1["body"]
    # Card implementation details:
    # return { "type": "box", ..., "contents": [ ... ] }
    assert len(card_box["contents"]) == 1
    inner_box = card_box["contents"][0]
    assert inner_box["type"] == "box"
    assert inner_box["contents"][0]["type"] == "text"
    assert inner_box["contents"][0]["text"] == "Card 1"


def test_convert_imagemap_to_line_message():
    state = A2UIState()
    
    apply_a2ui_messages(
        state,
        [
            {
                "surfaceUpdate": {
                    "surfaceId": "main",
                    "components": [
                        {"id": "root", "component": {"Imagemap": {
                            "baseUrl": {"literalString": "https://example.com/images"},
                            "altText": {"literalString": "Alt Text"},
                            "baseSize": {"width": 1040, "height": 1040},
                            "actions": [
                                {
                                    "type": "uri",
                                    "linkUri": "https://example.com",
                                    "area": {"x": 0, "y": 0, "width": 520, "height": 1040}
                                }
                            ]
                        }}}
                    ],
                }
            },
            {"beginRendering": {"surfaceId": "main", "root": "root"}},
        ],
    )

    surface = state.surfaces["main"]
    msg = a2ui_surface_to_line_flex(surface=surface, alt_text="imagemap demo")

    assert msg["type"] == "imagemap"
    assert msg["baseUrl"] == "https://example.com/images"
    assert msg["altText"] == "Alt Text"
    assert msg["baseSize"]["width"] == 1040
    assert msg["baseSize"]["height"] == 1040
    assert len(msg["actions"]) == 1
    assert msg["actions"][0]["type"] == "uri"
    assert msg["actions"][0]["linkUri"] == "https://example.com"
