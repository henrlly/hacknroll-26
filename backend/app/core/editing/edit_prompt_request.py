from typing_extensions import Literal, Optional

from app.api.types import PlanStreamedResponse, SceneStreamedResponse
from app.core.config import app_config
from app.core.models import PipelineCallback, Scene, VideoPlan
from app.core.prompts import SCENE_EDIT_PROMPT_INSTRUCTIONS, SCENE_EDIT_PROMPT_TEMPLATE
from app.services.openrouter import generate_response
from app.utils.template import render_prompt


async def edit_scene(
    topic: str,
    plan: VideoPlan,
    scene_number: int,
    callback: PipelineCallback,
    edit_prompt_type: Optional[Literal["funny", "detailed", "pictures"]] = None,
    custom_edit_prompt: Optional[str] = None,
    mock: bool = app_config.MOCK_EDIT_SCENE,
    streaming_delay: float = app_config.STREAMING_DELAY,
    chars_per_stream_message: int = app_config.CHARS_PER_STREAM_MESSAGE,
    scene_edit_prompt_template: str = SCENE_EDIT_PROMPT_TEMPLATE,
    scene_edit_prompt_instructions: str = SCENE_EDIT_PROMPT_INSTRUCTIONS,
) -> VideoPlan:
    print("editing")
    await callback(
        SceneStreamedResponse(event_type="scene_start"),
        delay=streaming_delay,
    )

    async def scene_stream_callback(message: str):
        await callback(
            SceneStreamedResponse(event_type="scene_stream", delta=message),
            delay=streaming_delay,
        )

    if mock:
        plan.scenes[scene_number].narration_script += "."
        scene = plan.scenes[scene_number]
        scene_json = scene.model_dump_json()

        for i in range(0, len(scene_json), chars_per_stream_message):
            chunk = scene_json[i : min(i + chars_per_stream_message, len(scene_json))]
            await scene_stream_callback(chunk)

        print(scene_json)

        await callback(
            SceneStreamedResponse(event_type="scene_end"),
        )
        print("end!")
        return plan

    else:
        plan_prompt = render_prompt(
            scene_edit_prompt_template,
            topic=topic,
            plan=plan.model_dump_json(),
            scene_number=scene_number,
            edit_prompt=(edit_prompt_type if edit_prompt_type else custom_edit_prompt),
        )
        plan = await generate_response(
            input=plan_prompt,
            instructions=scene_edit_prompt_instructions,
            model=app_config.PLAN_GEN_MODEL,
            response_model=Scene,
            temperature=app_config.PLAN_GEN_TEMPERATURE,
            reasoning_effort=app_config.PLAN_GEN_REASONING_EFFORT,
            callback=scene_stream_callback,
        )
        await callback(
            SceneStreamedResponse(event_type="scene_end"),
        )
        return plan
