import asyncio
import shutil

from app.core.config import app_config
from app.utils.get_file_path import (
    get_manim_media_dir_path,
    get_manim_py_file_path,
    get_manim_scene_media_dir_output_file_path,
    get_manim_scene_version_video_file_path,
    get_manim_scene_video_file_path,
)
import ffmpeg

def get_video_duration(filename):
    try:
        info = ffmpeg.probe(filename)
        duration = float(info['format']['duration'])
        return duration
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e.stderr.decode('utf8')}")
        return None
    except KeyError:
        print("Could not find duration in video metadata.")
        return None

async def _render_manim_code(
    session_id: str,
    scene_number: int,
    version_number: int,
    mock: bool = app_config.MOCK_CODE_RENDER,
) -> tuple[str, str | None, number]:
    video_file_path = get_manim_scene_version_video_file_path(session_id, scene_number, version_number)
    if mock:
        shutil.copyfile(
            "mock/scene.mp4",
            video_file_path,
        )
        print("Mock render complete")
        return video_file_path, None, 0

    media_dir = get_manim_media_dir_path(session_id, scene_number, version_number)
    print(f"Rendering scene {scene_number}, task {version_number}...!")

    # TODO: cancel this if exception from outside
    process = await asyncio.create_subprocess_exec(
        "manim",
        get_manim_py_file_path(session_id, scene_number, version_number=version_number),
        f"Scene{scene_number}",
        "--disable_caching",
        "-ql",  # low quality for faster rendering
        "--media_dir",
        media_dir,
        "-v",
        "critical",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )

    stdout, stderr = await process.communicate()
    print(f"{stdout.decode()} {stderr.decode()}")

    if process.returncode != 0:
        print(f"Error rendering scene {scene_number}, task {version_number}")
        return video_file_path, stderr.decode(), 0

    print(f"Successfully rendered scene {scene_number}, task {version_number}")

    # copy the output from manim media dir to a standard location
    output_file_path = get_manim_scene_media_dir_output_file_path(
        session_id, scene_number, version_number
    )
    shutil.copyfile(output_file_path, video_file_path)
    print(f"Rendered scene {scene_number}, task {version_number} to {video_file_path}")

    duration = get_video_duration(video_file_path)
    # delete media dir to save space
    shutil.rmtree(media_dir, ignore_errors=True)
    return video_file_path, None, duration
