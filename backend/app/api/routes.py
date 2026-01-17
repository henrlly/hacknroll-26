from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from app.api.types import (
    EditSceneRequest,
    FinalVideoResponse,
    MakeSceneRequest,
    RenderCodeRequest,
    SelectImageRequest,
    SelectImageResponse,
    UserRequest,
)
from app.core.config import app_config
from app.core.editing.edit_prompt_request import edit_scene
from app.core.editing.select_image_request import select_image_request
from app.core.generation.manim.render_loop import _render_manim_loop
from app.core.generation.manim.stitch_scene import stitch_manim_scenes_together
from app.core.pipeline import pipeline
from app.core.scene_pipeline import pipeline_scene
from app.utils.make_callback import make_callback

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


@router.websocket("/ws")
async def websocket_input(websocket: WebSocket):
    await websocket.accept()
    try:
        initial_data = await websocket.receive_json()
        user_input = UserRequest.model_validate(initial_data)
        callback = make_callback(websocket.send_text)

        print(app_config.model_dump_json(indent=2))

        session_id, plan = await pipeline(
            callback=callback,
            topic=user_input.prompt,
            voice=user_input.voice,
        )

        while True:
            data = await websocket.receive_json()
            if data["type"] == "edit_scene_request":
                request = EditSceneRequest.model_validate(data)
                plan = await edit_scene(
                    topic=user_input.prompt,
                    plan=plan,
                    callback=callback,
                    scene_number=request.scene_number,
                    edit_prompt_type=request.edit_prompt_type,
                    custom_edit_prompt=request.custom_edit_prompt,
                )

            elif data["type"] == "select_image_request":
                request = SelectImageRequest.model_validate(data)
                select_image_request(
                    session_id=session_id, select_image_request=request
                )
                await callback(SelectImageResponse(success=True))

            elif data["type"] == "make_scene_request":
                request = MakeSceneRequest.model_validate(data)
                await pipeline_scene(
                    callback=callback,
                    session_id=session_id,
                    scene_number=request.scene_number,
                    plan=plan,
                    voice=user_input.voice,
                )

            elif data["type"] == "render_code_request":
                request = RenderCodeRequest.model_validate(data)
                await _render_manim_loop(
                    session_id=session_id,
                    scene_number=request.scene_number,
                    version_number=request.version_number,
                    callback=callback,
                )

            elif data["type"] == "stitch_request":
                await callback(FinalVideoResponse(event_type="stitching_start"))
                success, error_message = await stitch_manim_scenes_together(
                    session_id, len(plan.scenes)
                )
                await callback(
                    FinalVideoResponse(
                        event_type="stitching_end",
                        success=success,
                        error_message=error_message,
                    )
                )

    except WebSocketDisconnect:
        print("Client disconnected")
