import pytest
from app.agent import decide_a2ui_response
from app.a2ui_to_flex import a2ui_surface_to_line_flex
from app.a2ui_state import A2UIState, apply_a2ui_messages

@pytest.mark.asyncio
async def test_confirm_response():
    # 1. Test decide_a2ui_response returns the correct A2UI message
    response = await decide_a2ui_response(user_text="confirm")
    assert response is not None
    assert len(response) == 2
    
    # 2. Test applying to state
    state = A2UIState()
    apply_a2ui_messages(state, response)
    
    surface = state.surfaces.get("main")
    assert surface is not None
    assert surface.root == "root"
    
    # 3. Test conversion to LINE message
    line_msg = a2ui_surface_to_line_flex(surface=surface)
    
    assert line_msg["type"] == "template"
    assert line_msg["template"]["type"] == "confirm"
    assert line_msg["template"]["text"] == "您確定要提交訂位嗎？"
    
    actions = line_msg["template"]["actions"]
    assert len(actions) == 2
    
    left = actions[0]
    assert left["type"] == "message"
    assert left["label"] == "取消"
    assert left["text"] == "@action cancel"
    
    right = actions[1]
    assert right["type"] == "message"
    assert right["label"] == "確認"
    assert right["text"] == "@action submit"
