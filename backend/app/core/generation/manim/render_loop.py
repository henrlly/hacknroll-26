import asyncio
import shutil
from typing import Awaitable, Callable

from pydantic import BaseModel

from app.api.types import ManimCodeRenderingSelectionResponse, ManimCodeRendingResponse
from app.core.config import app_config
from app.utils.get_file_path import (
    get_manim_scene_version_video_file_path,
    get_manim_scene_video_file_path,
)
from app.utils.parallelize import parallelize

from .fix_code import _fix_manim_code
from .render_code import _render_manim_code


async def render_manim_loop_parallel(
    session_id: str,
    scene_number: int,
    callback: Callable[[BaseModel], Awaitable],
    num_code_version: int = app_config.NUM_CODE_VERSIONS_PER_SCENE,
):
    winner_version = await parallelize(
        [
            _render_manim_loop(
                session_id, scene_number, callback, version_number=version_number
            )
            for version_number in range(num_code_version)
        ]
    )
    winner_file_path = get_manim_scene_version_video_file_path(
        session_id, scene_number, winner_version
    )
    scene_video_file_path = get_manim_scene_video_file_path(session_id, scene_number)
    shutil.copyfile(winner_file_path, scene_video_file_path)
    await callback(
        ManimCodeRenderingSelectionResponse(
            scene_number=scene_number, version_number=winner_version
        )
    )
    return winner_version


async def _render_manim_loop(
    session_id: str,
    scene_number: int,
    callback: Callable[[BaseModel], Awaitable],
    version_number: int,
    max_retries: int = app_config.MANIM_SCENE_MAX_RETRIES,
):
    duration = 0
    retry_number = 0
    try:
        for attempt in range(max_retries):
            retry_number = attempt
            error_message = "Rendering timed out."
            try:
                await callback(
                    ManimCodeRendingResponse(
                        event_type="rendering_start",
                        scene_number=scene_number,
                        version_number=version_number,
                        retry_number=attempt,
                        success=True,
                    )
                )
                _video_file_path, error_message, duration = await asyncio.wait_for(
                    _render_manim_code(session_id, scene_number, version_number),
                    timeout=app_config.MANIM_RENDER_TIMEOUT_SECONDS,
                )  # wait_for has not been tested

            except asyncio.TimeoutError:
                error_message = "Rendering timed out."
                print("ERR")

            if error_message is None:
                await callback(
                    ManimCodeRendingResponse(
                        event_type="rendering_end",
                        scene_number=scene_number,
                        version_number=version_number,
                        retry_number=attempt,
                        duration=duration,
                        success=True,
                    )
                )
                return
            else:
                await callback(
                    ManimCodeRendingResponse(
                        event_type="rendering_end",
                        scene_number=scene_number,
                        version_number=version_number,
                        retry_number=attempt,
                        duration = duration,
                        success=False,
                    )
                )
                await _fix_manim_code(
                    error_message=error_message,
                    session_id=session_id,
                    scene_number=scene_number,
                    version_number=version_number,
                    callback=callback,
                    attempt=attempt,
                )
        print(f"Failed to render scene {scene_number} after {max_retries} attempts")
    except asyncio.CancelledError:
        await callback(
            ManimCodeRendingResponse(
                event_type="rendering_end",
                scene_number=scene_number,
                version_number=version_number,
                retry_number=retry_number,
                success=False,
                duration = duration,
                error_message="cancelled",
            )
        )
    finally:
        return version_number
