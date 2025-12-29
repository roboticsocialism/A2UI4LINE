from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Surface:
    components: dict[str, dict] = field(default_factory=dict)
    data_model: dict = field(default_factory=dict)
    root: str | None = None


@dataclass
class A2UIState:
    surfaces: dict[str, Surface] = field(default_factory=dict)


def ensure_surface(state: A2UIState, surface_id: str) -> Surface:
    if surface_id not in state.surfaces:
        state.surfaces[surface_id] = Surface()
    return state.surfaces[surface_id]


def apply_a2ui_messages(state: A2UIState, messages: list[dict]) -> None:
    for msg in messages:
        if "surfaceUpdate" in msg:
            su = msg["surfaceUpdate"]
            surface = ensure_surface(state, su["surfaceId"])
            for c in su.get("components", []) or []:
                surface.components[c["id"]] = c["component"]

        elif "dataModelUpdate" in msg:
            dmu = msg["dataModelUpdate"]
            surface = ensure_surface(state, dmu["surfaceId"])
            apply_data_model_update(surface.data_model, dmu.get("path"), dmu.get("contents") or [])

        elif "beginRendering" in msg:
            br = msg["beginRendering"]
            surface = ensure_surface(state, br["surfaceId"])
            surface.root = br["root"]

        elif "deleteSurface" in msg:
            ds = msg["deleteSurface"]
            state.surfaces.pop(ds["surfaceId"], None)


def apply_data_model_update(data_model: dict, path: str | None, contents: list[dict]) -> None:
    if not path:
        data_model.clear()
        data_model.update(build_data_model_from_contents(contents))
        return

    target = ensure_object_at_pointer(data_model, path)
    if not isinstance(target, dict):
        return

    for entry in contents:
        target[entry["key"]] = decode_value(entry)


def build_data_model_from_contents(contents: list[dict]) -> dict:
    root: dict = {}
    for entry in contents:
        root[entry["key"]] = decode_value(entry)
    return root


def decode_value(entry: dict):
    if "valueString" in entry:
        return entry["valueString"]
    if "valueNumber" in entry:
        return entry["valueNumber"]
    if "valueBoolean" in entry:
        return entry["valueBoolean"]
    if "valueMap" in entry:
        obj: dict = {}
        for kv in entry.get("valueMap") or []:
            obj[kv["key"]] = decode_value(kv)
        return obj
    return None


def resolve_json_pointer(obj, pointer: str | None):
    if pointer is None or pointer == "" or pointer == "/":
        return obj
    if not pointer.startswith("/"):
        return None

    parts = [unescape_json_pointer(p) for p in pointer.split("/")[1:]]
    cur = obj
    for part in parts:
        if cur is None:
            return None
        if isinstance(cur, list):
            try:
                idx = int(part)
            except ValueError:
                return None
            if idx < 0 or idx >= len(cur):
                return None
            cur = cur[idx]
        elif isinstance(cur, dict):
            cur = cur.get(part)
        else:
            return None
    return cur


def unescape_json_pointer(s: str) -> str:
    return s.replace("~1", "/").replace("~0", "~")


def ensure_object_at_pointer(root: dict, pointer: str) -> dict:
    parts = [unescape_json_pointer(p) for p in pointer.split("/") if p]
    cur = root
    for p in parts:
        nxt = cur.get(p)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[p] = nxt
        cur = nxt
    return cur
