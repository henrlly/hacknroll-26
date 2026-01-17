import asyncio
import os
import uuid

from app.api.types import (
    FinalVideoResponse,
    PlanStreamedResponse,
    StartPipelineResponse,
)
from app.core.config import app_config
from app.core.generation.manim.generate_code import generate_manim_code_parallel
from app.core.generation.manim.render_loop import render_manim_loop_parallel
from app.core.generation.manim.stitch_scene import stitch_manim_scenes_together
from app.core.generation.plan import generate_plan
from app.core.generation.visuals import generate_visual_asset
from app.core.models import Asset, PipelineCallback, VideoPlan, VoiceType
from app.services.elevenlabs import generate_sound_effect, generate_speech
from app.utils.gather import gather_with_concurrency
from app.utils.get_file_path import (
    get_narration_scene_file_path,
    get_selected_asset_file_path,
)


# TODO: standardize where the callback is called
async def pipeline_scene(
    callback: PipelineCallback,
    session_id: str,
    scene_number: int,
    plan: VideoPlan,
    voice: VoiceType,
):
    scene = plan.scenes[scene_number]

    word_timing = await generate_speech(
        text=scene.narration_script,
        voice=voice,
        file_name=get_narration_scene_file_path(
            session_id=session_id, scene_number=scene_number
        ),
        callback=callback,
        scene_number=scene_number,
    )

    print(f"\nNarration_results:\n{word_timing}\n")

    # Step 3: Generate assets and manim code for each scene
    print("\nGenerating assets and manim code...\n")

    # split assets into sound effects and visual assets,
    # because sound effects have a concurrency limit of 5 on elevenlabs
    visual_assets: list[Asset] = [
        asset for asset in scene.assets_needed if asset.asset_type == "visual"
    ]
    sound_effects: list[Asset] = [
        asset for asset in scene.assets_needed if asset.asset_type == "sound_effect"
    ]

    # Max 5 concurrent requests for sound effects
    gather_sound_effects = gather_with_concurrency(
        5,
        *[
            generate_sound_effect(
                description=asset.asset_long_desc,
                file_name=get_selected_asset_file_path(
                    session_id=session_id, asset_id=asset.asset_id, ext="mp3"
                ),
                callback=callback,
                asset_id=asset.asset_id,
            )
            for asset in sound_effects
        ],
    )

    gather_visual_assets = asyncio.gather(
        *[
            generate_visual_asset(asset=asset, session_id=session_id, callback=callback)
            for asset in visual_assets
        ]
    )

    gather_manim_code = generate_manim_code_parallel(
        scene_number=scene_number,
        full_script=scene.narration_script,
        word_timings=word_timing,
        session_id=session_id,
        plan=plan,
        callback=callback,
        num_code_versions=app_config.NUM_CODE_VERSIONS_PER_SCENE,
    )

    await asyncio.gather(
        gather_sound_effects,
        gather_visual_assets,
        gather_manim_code,
    )

    print("\nGenerated assets and manim code!\n")

    # Step 4: Render manim scenes
    await render_manim_loop_parallel(
        session_id=session_id,
        scene_number=scene_number,
        callback=callback,
        num_code_version=app_config.NUM_CODE_VERSIONS_PER_SCENE,
    )

    return plan
