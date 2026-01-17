from typing import Literal, Optional

from pydantic import BaseModel

from app.core.models import VoiceType


class EditSceneRequest(BaseModel):
    type: Literal["edit_scene_request"] = "edit_scene_request"
    edit_prompt_type: Optional[Literal["funny", "detailed", "pictures"]]
    custom_edit_prompt: Optional[str]
    scene_number: int


class SelectImageRequest(BaseModel):
    type: Literal["select_image_request"] = "select_image_request"
    asset_id: str
    selected_candidate_id: str


class SelectImageResponse(BaseModel):
    type: Literal["select_image"] = "select_image"
    asset_id: str
    selected_candidate_id: str
    success: bool


class MakeSceneRequest(BaseModel):
    type: Literal["make_scene_request"] = "make_scene_request"
    scene_number: int


class RenderCodeRequest(BaseModel):
    type: Literal["render_code_request"] = "render_code_request"
    scene_number: int
    version_number: int


class StitchRequest(BaseModel):
    type: Literal["stitch_request"] = "stitch_request"


class UserRequest(BaseModel):
    prompt: str
    voice: VoiceType


class StartPipelineResponse(BaseModel):
    type: Literal["start"] = "start"
    session_id: str
    success: bool


class PlanStreamedResponse(BaseModel):
    type: Literal["plan"] = "plan"
    event_type: Literal["plan_start", "plan_stream", "plan_end"]
    # diff in content to append to plan json
    delta: Optional[str] = None  # only for plan_stream event


class SceneStreamedResponse(BaseModel):
    type: Literal["scene"] = "scene"
    event_type: Literal["scene_start", "scene_stream", "scene_end"]
    # diff in content to append to plan json
    delta: Optional[str] = None  # only for plan_stream event


class AssetResponse(BaseModel):
    type: Literal["asset"] = "asset"
    event_type: Literal[
        "selection_start", "selection_end", "generation_start", "generation_end"
    ]
    asset_id: str
    asset_type: Literal["visual", "sound_effect"]
    candidate_id: Optional[str] = None  # only for generation_end


class AssetSelectionResponse(BaseModel):
    type: Literal["asset_selection"] = "asset_selection"
    event_type: Literal["selection_start", "selection_end"]
    asset_id: str
    asset_type: Literal["visual"] = "visual"
    selected_candidate_ids: Optional[list[str]] = None  # only for selection_end event
    selected_candidate_id: Optional[str] = None  # only for selection_end event


class NarrationResponse(BaseModel):
    type: Literal["narration"] = "narration"
    event_type: Literal["narration_generation_start", "narration_generation_end"]
    scene_number: int


class ManimCodeGenerationResponse(BaseModel):
    type: Literal["code_generation"] = "code_generation"
    event_type: Literal["code_generation_start", "code_generation_end"]
    scene_number: int
    version_number: int
    # if failed during rendering,
    # retry_number indicates which attempt it is
    # initial generation will have retry_number = 0
    retry_number: int = 0
    # TODO: enforce not option when "code_generation_end"
    success: Optional[bool] = None  # only for code_generation_end event


class ManimCodeRendingResponse(BaseModel):
    type: Literal["code_rendering"] = "code_rendering"
    event_type: Literal["rendering_start", "rendering_end"]
    scene_number: int
    version_number: int
    # if failed during rendering,
    # retry_number indicates which attempt it is
    # initial generation will have retry_number = 0
    retry_number: int
    # TODO: enforce not option when "code_generation_end"
    success: bool
    error_message: Optional[Literal["cancelled"]] = None  # only for rendering_end event


class ManimCodeRenderingSelectionResponse(BaseModel):
    type: Literal["code_rendering_selection"] = "code_rendering_selection"
    scene_number: int
    version_number: int


class FinalVideoResponse(BaseModel):
    type: Literal["final_video"] = "final_video"
    event_type: Literal["stitching_start", "stitching_end"]
    # TODO: enforce not option when "stitching_end"
    success: Optional[bool] = None  # only for stitching_end event
    error_message: Optional[str] = None  # only for stitching_end event
