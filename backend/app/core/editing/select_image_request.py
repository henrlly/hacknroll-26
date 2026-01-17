import shutil

from app.api.types import SelectImageRequest
from app.utils.get_file_path import get_asset_file_path, get_selected_asset_file_path


def select_image_request(session_id: str, select_image_request: SelectImageRequest):
    selected_asset_path = get_selected_asset_file_path(
        session_id=session_id,
        asset_id=select_image_request.asset_id,
        ext="mp4",
    )
    shutil.copyfile(
        get_asset_file_path(
            session_id=session_id,
            asset_id=select_image_request.asset_id,
            ext="mp4",
            id=select_image_request.selected_candidate_id,
        ),
        selected_asset_path,
    )
