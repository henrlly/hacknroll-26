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


async def pipeline(
    callback: PipelineCallback,
    topic: str,
    voice: VoiceType,
    input_plan: VideoPlan | None = None,
    mock_plan: bool = app_config.MOCK_PLAN,
    streaming_delay: float = app_config.STREAMING_DELAY,
    chars_per_stream_message: int = app_config.CHARS_PER_STREAM_MESSAGE,
):
    session_id = str(uuid.uuid4())

    os.makedirs(f"static/{session_id}", exist_ok=True)
    os.makedirs(f"working/{session_id}", exist_ok=True)

    # Step 1: Generate video plan
    await callback(StartPipelineResponse(session_id=session_id, success=True))

    plan = await generate_plan(
        input_plan=input_plan,
        topic=topic,
        streaming_delay=streaming_delay,
        callback=callback,
        mock_plan=mock_plan,
        chars_per_stream_message=chars_per_stream_message,
    )

    await callback(PlanStreamedResponse(event_type="plan_end"), delay=0)

    print(f"\nGenerated Plan:\n{plan.model_dump_json(indent=2)}\n")

    # Step 2: Generate narration for each scene
    print("\nGenerating narration...\n")

    scripts: list[str] = [scene.narration_script for scene in plan.scenes]

    # Generate narrations in parallel
    # Elevenlabs API has concurrency limits of 5
    # We're on creator tier, so 5 concurrent requests allowed for sound effects
    # 10 for narration cos flash/turbo model (using flash)
    # https://help.elevenlabs.io/hc/en-us/articles/14312733311761-How-many-requests-can-I-make-and-can-I-increase-it
    word_timings = await gather_with_concurrency(
        5,
        *[
            generate_speech(
                text=narration,
                voice=voice,
                file_name=get_narration_scene_file_path(
                    session_id=session_id, scene_number=i
                ),
                callback=callback,
                scene_number=i,
            )
            for i, narration in enumerate(scripts)
        ],
    )

    print(f"\nNarration_results:\n{word_timings}\n")

    # Step 3: Generate assets and manim code for each scene
    print("\nGenerating assets and manim code...\n")

    # split assets into sound effects and visual assets,
    # because sound effects have a concurrency limit of 5 on elevenlabs
    visual_assets: list[Asset] = [
        asset
        for scene in plan.scenes
        for asset in scene.assets_needed
        if asset.asset_type == "visual"
    ]
    sound_effects: list[Asset] = [
        asset
        for scene in plan.scenes
        for asset in scene.assets_needed
        if asset.asset_type == "sound_effect"
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

    gather_manim_code = asyncio.gather(
        *[
            generate_manim_code_parallel(
                scene_number=i,
                full_script=scripts[i],
                word_timings=word_timings[i],
                session_id=session_id,
                plan=plan,
                callback=callback,
                num_code_versions=app_config.NUM_CODE_VERSIONS_PER_SCENE,
            )
            for i in range(len(plan.scenes))
        ]
    )

    await asyncio.gather(
        gather_sound_effects,
        gather_visual_assets,
        gather_manim_code,
    )

    print("\nGenerated assets and manim code!\n")

    # Step 4: Render manim scenes
    await asyncio.gather(
        *[
            render_manim_loop_parallel(
                session_id=session_id,
                scene_number=i,
                callback=callback,
                num_code_version=app_config.NUM_CODE_VERSIONS_PER_SCENE,
            )
            for i in range(len(plan.scenes))
        ]
    )

    # Step 5: Stitch scenes together
    await callback(FinalVideoResponse(event_type="stitching_start"))
    success, error_message = await stitch_manim_scenes_together(
        session_id, len(plan.scenes)
    )
    await callback(
        FinalVideoResponse(
            event_type="stitching_end", success=success, error_message=error_message
        )
    )
    return session_id, plan
