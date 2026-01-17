import asyncio
import shutil
from typing import Awaitable, Callable

from pydantic import BaseModel

from app.api.types import ManimCodeGenerationResponse
from app.core.config import app_config
from app.core.models import ManimCodeResponse, VideoPlan
from app.core.prompts import (
    MANIM_PROMPT_INSTRUCTIONS,
    MANIM_PROMPT_TEMPLATE,
)
from app.services.openrouter import generate_response
from app.utils.assets import format_assets
from app.utils.get_file_path import (
    get_manim_prompt_file_path,
    get_manim_py_file_path,
)
from app.utils.template import render_prompt


async def _generate_manim_code(
    scene_number: int,
    full_script: str,
    word_timings: str,
    session_id: str,
    plan: VideoPlan,
    callback: Callable[[BaseModel], Awaitable],
    version_number: int = 0,
    mock: bool = app_config.MOCK_CODE_GEN,
    code_prompt_template: str = MANIM_PROMPT_TEMPLATE,
    code_prompt_instructions: str = MANIM_PROMPT_INSTRUCTIONS,
):
    try:
        await callback(
            ManimCodeGenerationResponse(
                event_type="code_generation_start",
                scene_number=scene_number,
                version_number=version_number,
            )
        )

        if mock:
            shutil.copyfile(
                "mock/manim_prompt.txt",
                get_manim_prompt_file_path(session_id, scene_number),
            )
            with open("mock/scene.py", "r") as f:
                manim_code = f.read()
                manim_code = manim_code.replace("Scene0", f"Scene{scene_number}")

            # Replace scene number in py file
            with open(
                get_manim_py_file_path(session_id, scene_number, version_number),
                "w",
            ) as f:
                f.write(manim_code)
            manim_code_response = ManimCodeResponse(code=manim_code)
        else:
            manim_prompt = render_prompt(
                raw_template=code_prompt_template,
                topic=plan.topic,
                scene_number=scene_number,
                full_script=full_script,
                word_timings=word_timings,
                session_id=session_id,
                scene_structure=plan.scenes[scene_number].scene_structure,
                scene_assets=format_assets(plan.scenes[scene_number].assets_needed),
                # scene_assets=json.dumps(plan.scenes[scene_number].assets_needed),
                # scene_plan=plan.scenes[scene_number].model_dump_json(),
                full_plan=plan.model_dump_json(),
            )
            manim_prompt_path = get_manim_prompt_file_path(session_id, scene_number)
            with open(manim_prompt_path, "w") as f:
                f.write(manim_prompt)

            manim_code_response: ManimCodeResponse = await generate_response(
                input=manim_prompt,
                instructions=code_prompt_instructions,
                model=app_config.CODE_GEN_MODEL,
                response_model=ManimCodeResponse,
                temperature=app_config.CODE_GEN_TEMPERATURE,
                reasoning_effort=app_config.CODE_GEN_REASONING_EFFORT,
            )

            manim_py_path = get_manim_py_file_path(
                session_id, scene_number, version_number
            )
            with open(manim_py_path, "w") as f:
                f.write(manim_code_response.code)

        await callback(
            ManimCodeGenerationResponse(
                event_type="code_generation_end",
                scene_number=scene_number,
                version_number=version_number,
                success=manim_code_response is not None,
            )
        )
        return manim_code_response

    except Exception as _:
        await callback(
            ManimCodeGenerationResponse(
                event_type="code_generation_end",
                scene_number=scene_number,
                version_number=version_number,
                success=False,
            )
        )


async def generate_manim_code_parallel(
    scene_number: int,
    full_script: str,
    word_timings: str,
    session_id: str,
    plan: VideoPlan,
    callback: Callable[[BaseModel], Awaitable],
    num_code_versions: int = app_config.NUM_CODE_VERSIONS_PER_SCENE,
    code_prompt_template: str = MANIM_PROMPT_TEMPLATE,
    code_prompt_instructions: str = MANIM_PROMPT_INSTRUCTIONS,
    mock: bool = app_config.MOCK_CODE_GEN,
):
    coroutines = [
        _generate_manim_code(
            scene_number,
            full_script,
            word_timings,
            session_id,
            plan,
            callback,
            version_number,
            code_prompt_template=code_prompt_template,
            code_prompt_instructions=code_prompt_instructions,
            mock=mock,
        )
        for version_number in range(num_code_versions)
    ]
    return await asyncio.gather(*coroutines)
