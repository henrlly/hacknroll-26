from typing import Literal


def get_manim_py_file_path(
    session_id: str, scene_number: int, version_number: int
) -> str:
    return f"static/{session_id}/scene_{scene_number}_{version_number}.py"


def get_manim_prompt_file_path(session_id: str, scene_number: int) -> str:
    return f"static/{session_id}/scene_{scene_number}.txt"


def get_manim_scene_version_video_file_path(
    session_id: str, scene_number: int, version_number: int
) -> str:
    return f"static/{session_id}/scene_{scene_number}_{version_number}.mp4"


def get_manim_scene_video_file_path(
    session_id: str, scene_number: int
) -> str:
    return f"static/{session_id}/scene_{scene_number}.mp4"


def get_manim_media_dir_path(
    session_id: str, scene_number: int, version_number: int
) -> str:
    return f"working/{session_id}/scene_{scene_number}_{version_number}"


def get_manim_scene_media_dir_output_file_path(
    session_id: str, scene_number: int, version_number: int
) -> str:
    return f"{get_manim_media_dir_path(session_id, scene_number, version_number)}/videos/scene_{scene_number}_{version_number}/480p15/Scene{scene_number}.mp4"


def get_final_video_file_path(session_id: str) -> str:
    return f"static/{session_id}/final_video.mp4"


def get_asset_dir_path(session_id: str, asset_id: str) -> str:
    return f"static/{session_id}/{asset_id}"


def get_selected_asset_file_path(
    session_id: str, asset_id: str, ext: Literal["mp3", "mp4"]
) -> str:
    return f"static/{session_id}/{asset_id}.{ext}"


def get_asset_file_path(
    session_id: str, asset_id: str, ext: Literal["mp3", "mp4"], id: str
) -> str:
    return f"static/{session_id}/{asset_id}/{id}.{ext}"


def get_narration_scene_file_path(session_id: str, scene_number: int) -> str:
    return f"static/{session_id}/narration_scene_{scene_number}.mp3"
