
import shutil
from typing import Awaitable, Callable

from pydantic import BaseModel

from app.api.types import ManimCodeGenerationResponse
from app.core.config import app_config
from app.core.models import ManimCodeResponse
from app.core.prompts import (
    MANIM_FIX_PROMPT_INSTRUCTIONS,
    MANIM_FIX_PROMPT_TEMPLATE,
)
from app.services.openrouter import generate_response
from app.utils.get_file_path import (
    get_manim_prompt_file_path,
    get_manim_py_file_path,
)
from app.utils.template import render_prompt


async def _fix_manim_code(
    error_message: str,
    session_id: str,
    scene_number: int,
    version_number: int,
    callback: Callable[[BaseModel], Awaitable],
    attempt: int = 0,
    mock: bool = app_config.MOCK_CODE_FIX,
):
    await callback(
        ManimCodeGenerationResponse(
            event_type="code_generation_start",
            scene_number=scene_number,
            version_number=version_number,
            retry_number=attempt + 1,
        )
    )

    if mock:
        shutil.copyfile(
            "mock/scene_fixed.py",
            get_manim_py_file_path(session_id, scene_number, version_number),
        )
        with open("mock/scene.py", "r") as f:
            fix_response = ManimCodeResponse(code=f.read())
    else:
        manim_py_path = get_manim_py_file_path(session_id, scene_number, version_number)
        manim_prompt_path = get_manim_prompt_file_path(session_id, scene_number)

        with open(manim_py_path, "r") as f:
            code = f.read()
        with open(manim_prompt_path, "r") as f:
            original_prompt = f.read()

        fix_prompt = render_prompt(
            MANIM_FIX_PROMPT_TEMPLATE,
            code=code,
            error_messages=error_message,
            original_prompt=original_prompt,
        )
        fix_response: ManimCodeResponse = await generate_response(
            input=fix_prompt,
            instructions=MANIM_FIX_PROMPT_INSTRUCTIONS,
            model=app_config.CODE_FIX_MODEL,
            response_model=ManimCodeResponse,
            temperature=app_config.CODE_FIX_TEMPERATURE,
            reasoning_effort=app_config.CODE_FIX_REASONING_EFFORT,
        )
        with open(manim_py_path, "w") as f:
            f.write(fix_response.code)

    await callback(
        ManimCodeGenerationResponse(
            event_type="code_generation_end",
            scene_number=scene_number,
            version_number=version_number,
            retry_number=attempt + 1,
            success=fix_response is not None,
        )
    )
