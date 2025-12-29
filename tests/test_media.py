import pytest
from app.agent import decide_a2ui_response
from app.a2ui_to_flex import a2ui_surface_to_line_flex
from app.a2ui_state import A2UIState, apply_a2ui_messages

@pytest.mark.asyncio
async def test_audio_response():
    # 1. Test decide_a2ui_response returns the correct A2UI message
    response = await decide_a2ui_response(user_text="audio")
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
    
    assert line_msg["type"] == "audio"
    assert "mp3" in line_msg["originalContentUrl"]
    assert line_msg["duration"] == 60000

@pytest.mark.asyncio
async def test_video_response():
    # 1. Test decide_a2ui_response returns the correct A2UI message
    response = await decide_a2ui_response(user_text="video")
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
    
    assert line_msg["type"] == "video"
    assert "mp4" in line_msg["originalContentUrl"]
    assert "jpg" in line_msg["previewImageUrl"]
