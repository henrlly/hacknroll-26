import asyncio

from app.utils.get_file_path import (
    get_final_video_file_path,
    get_manim_scene_video_file_path,
)


async def stitch_manim_scenes_together(session_id: str, num_scenes: int):
    """returns (success: bool, error_message: str)"""
    # Use ffmpeg to stitch together the manim scenes
    input_files = ""
    for scene_number in range(num_scenes):
        scene_video_file_path = get_manim_scene_video_file_path(
            session_id, scene_number
        )
        input_files += f"-i {scene_video_file_path} "

    output_file = get_final_video_file_path(session_id)
    ffmpeg_command = f'ffmpeg {input_files}-filter_complex "[0:v:0][0:a:0]'
    for i in range(1, num_scenes):
        ffmpeg_command += f"[{i}:v:0][{i}:a:0]"
    ffmpeg_command += f'concat=n={num_scenes}:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" {output_file} -y'

    process = await asyncio.create_subprocess_shell(
        ffmpeg_command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    _, stderr = await process.communicate()
    return process.returncode == 0, stderr.decode()
