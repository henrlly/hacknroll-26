from typing import Awaitable, Literal, Protocol

from pydantic import BaseModel


class PipelineCallback(Protocol):
    def __call__(self, model: BaseModel, delay: float = ...) -> Awaitable[None]: ...


VoiceType = Literal["trump", "peter", "obama"]


class Asset(BaseModel):
    asset_id: str
    asset_type: Literal[
        "visual",
        "sound_effect",
    ]
    asset_short_desc: str
    asset_long_desc: str


class Scene(BaseModel):
    scene_number: int
    duration_seconds: int
    visuals_description: str
    narration_script: str
    sound_description: str
    edit_notes: str
    assets_needed: list[Asset]
    scene_structure: str


class VideoPlan(BaseModel):
    topic: str
    main_font: str
    secondary_font: str
    scenes: list[Scene]


class ManimCodeResponse(BaseModel):
    code: str


class VisualChoiceResponse(BaseModel):
    selected_image_indexes: list[int]
