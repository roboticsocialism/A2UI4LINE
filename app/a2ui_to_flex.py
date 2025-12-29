from __future__ import annotations

from app.a2ui_state import Surface, resolve_json_pointer


def a2ui_surface_to_line_flex(*, surface: Surface, alt_text: str = "A2UI") -> dict:
    if not surface.root:
        return line_text("Missing beginRendering/root")

    root_comp = surface.components.get(surface.root)
    if not root_comp:
        return line_text("Root component not found")

    ctype, props = unwrap_component(root_comp)
    if ctype == "Carousel":
        child_ids = resolve_children_ids(props.get("children"))
        bubbles = []
        for cid in child_ids:
            cc = surface.components.get(cid)
            if not cc:
                continue
            # Convert each child to a Box, then wrap in a Bubble
            box = component_to_flex_box(component_id=cid, component=cc, surface=surface)
            bubbles.append({"type": "bubble", "body": box})
        
        return {
            "type": "flex",
            "altText": alt_text,
            "contents": {
                "type": "carousel",
                "contents": bubbles
            }
        }

    if ctype == "Confirm":
        # Return a native LINE Confirm Template Message
        msg_text = resolve_a2ui_value(props.get("text"), surface.data_model) or "Are you sure?"
        
        def make_action(btn_prop_name: str, default_label: str):
            btn_props = props.get(btn_prop_name) or {}
            label = btn_props.get("label") or default_label
            action_name = (btn_props.get("action") or {}).get("name") or "action"
            return {
                "type": "message",
                "label": str(label),
                "text": f"@action {action_name}"
            }

        left_action = make_action("leftButton", "No")
        right_action = make_action("rightButton", "Yes")

        return {
            "type": "template",
            "altText": alt_text,
            "template": {
                "type": "confirm",
                "text": str(msg_text)[:240],  # LINE limit: 240 chars
                "actions": [left_action, right_action]
            }
        }

    if ctype == "Location":
        # Return a native LINE Location Message
        # Props: title, address, latitude, longitude
        title = resolve_a2ui_value(props.get("title"), surface.data_model) or "Location"
        address = resolve_a2ui_value(props.get("address"), surface.data_model) or ""
        latitude = props.get("latitude") or 0.0
        longitude = props.get("longitude") or 0.0
        
        return {
            "type": "location",
            "title": str(title),
            "address": str(address),
            "latitude": float(latitude),
            "longitude": float(longitude)
        }

    body = component_to_flex_box(component_id=surface.root, component=root_comp, surface=surface)

    return {
        "type": "flex",
        "altText": alt_text,
        "contents": {
            "type": "bubble",
            "body": body,
        },
    }


def line_text(text: str) -> dict:
    return {"type": "text", "text": str(text)}


def component_to_flex_box(*, component_id: str, component: dict, surface: Surface) -> dict:
    ctype, props = unwrap_component(component)

    if ctype in {"Column", "Row"}:
        layout = "horizontal" if ctype == "Row" else "vertical"
        child_ids = resolve_children_ids(props.get("children"))
        contents = []
        for cid in child_ids:
            cc = surface.components.get(cid)
            if not cc:
                continue
            contents.append(component_to_flex_element(component_id=cid, component=cc, surface=surface))
        return {"type": "box", "layout": layout, "contents": contents}

    fallback = component_to_flex_element(component_id=component_id, component=component, surface=surface)
    if fallback.get("type") == "box":
        return fallback
    return {"type": "box", "layout": "vertical", "contents": [fallback]}


def component_to_flex_element(*, component_id: str, component: dict, surface: Surface) -> dict:
    ctype, props = unwrap_component(component)

    if ctype in {"Column", "Row"}:
        return component_to_flex_box(component_id=component_id, component=component, surface=surface)

    if ctype == "Text":
        text = resolve_a2ui_value(props.get("text"), surface.data_model)
        return {"type": "text", "text": str(text or ""), "wrap": True}

    if ctype == "Button":
        label = resolve_button_label(props=props, surface=surface)
        action_name = (props.get("action") or {}).get("name") or "action"
        return {
            "type": "button",
            "style": "primary",
            "action": {"type": "message", "label": str(label or "OK"), "text": f"@action {action_name}"},
        }

    if ctype == "Card":
        child_id = props.get("child")
        if not child_id:
            return unsupported_component(ctype, component_id)
        cc = surface.components.get(child_id)
        if not cc:
            return unsupported_component(ctype, component_id)
        return {
            "type": "box",
            "layout": "vertical",
            "paddingAll": "12px",
            "borderWidth": "1px",
            "borderColor": "#DDDDDD",
            "cornerRadius": "8px",
            # "contents": [component_to_flex_element(component_id=child_id, component=cc, surface=surface)],
            "contents": [component_to_flex_box(component_id=child_id, component=cc, surface=surface)],
        }

    if ctype == "Confirm":
        # A simple Confirm mapping:
        # Props: text, leftButton, rightButton
        msg_text = resolve_a2ui_value(props.get("text"), surface.data_model) or "Are you sure?"
        
        # Helper to convert a button prop to flex button
        def make_btn(btn_prop_name: str):
            btn_props = props.get(btn_prop_name)
            if not btn_props:
                # Fallback button
                return {
                    "type": "button",
                    "style": "secondary",
                    "action": {"type": "message", "label": "OK", "text": "OK"}
                }
            # We assume the prop structure matches Button component props or similar
            # If it's just a button object directly:
            # We reuse component_to_flex_element logic if it were a component, but here it's embedded props.
            # Let's assume the A2UI "Confirm" passes full Button components as children or just inline props.
            # For simplicity, let's assume inline props: { "label": "Yes", "action": { "name": "yes" } }
            label = btn_props.get("label") or "OK"
            action_name = (btn_props.get("action") or {}).get("name") or "action"
            return {
                "type": "button",
                "style": "secondary" if btn_prop_name == "leftButton" else "primary",
                "action": {"type": "message", "label": str(label), "text": f"@action {action_name}"},
                "flex": 1,
            }

        left_btn = make_btn("leftButton")
        right_btn = make_btn("rightButton")

        return {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": str(msg_text),
                    "wrap": True,
                    "weight": "bold",
                    "align": "center",
                    "margin": "md"
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "margin": "md",
                    "spacing": "md",
                    "contents": [left_btn, right_btn]
                }
            ],
            "paddingAll": "20px",
            # "backgroundColor": "#FFFFFF",
            # "cornerRadius": "10px"
        }

    return unsupported_component(ctype, component_id)


def unsupported_component(component_type: str, component_id: str) -> dict:
    return {
        "type": "text",
        "text": f"[Unsupported component: {component_type} id={component_id}]",
        "wrap": True,
        "color": "#999999",
        "size": "sm",
    }


def resolve_button_label(*, props: dict, surface: Surface) -> str:
    child_id = props.get("child")
    if not child_id:
        return "Submit"

    child = surface.components.get(child_id)
    if not child:
        return "Submit"

    ctype, cprops = unwrap_component(child)
    if ctype != "Text":
        return "Submit"

    v = resolve_a2ui_value(cprops.get("text"), surface.data_model)
    return str(v or "Submit")


def resolve_a2ui_value(v: dict | None, data_model: dict):
    if not v:
        return None
    if "literalString" in v:
        return v["literalString"]
    if "path" in v:
        return resolve_json_pointer(data_model, v["path"])
    return None


def unwrap_component(component: dict) -> tuple[str, dict]:
    keys = list(component.keys())
    ctype = keys[0] if keys else "Unknown"
    return ctype, component.get(ctype) or {}


def resolve_children_ids(children: dict | None) -> list[str]:
    if not children:
        return []
    explicit = children.get("explicitList")
    if isinstance(explicit, list):
        return [str(x) for x in explicit]
    return []
