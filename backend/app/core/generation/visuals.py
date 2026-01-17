import asyncio
import os
import shutil
import uuid
from typing import Awaitable, Callable

from pydantic import BaseModel

from app.api.types import AssetResponse, AssetSelectionResponse
from app.core.config import app_config
from app.core.models import Asset
from app.services.klipy import search_klipy
from app.services.openrouter import generate_image, select_image
from app.services.pixabay import search_pixabay_photo, search_pixabay_video
from app.utils.get_file_path import (
    get_asset_dir_path,
    get_asset_file_path,
    get_selected_asset_file_path,
)


async def generate_visual_asset(
    asset: Asset,
    session_id: str,
    callback: Callable[[BaseModel], Awaitable],
    mock: bool = app_config.MOCK_VISUAL_ASSET,
    enable_image_generation: bool = app_config.ENABLE_IMAGE_GENERATION,
    enable_image_selection: bool = app_config.ENABLE_IMAGE_SELECTION,
    num_stock_images: int = app_config.NUM_STOCK_IMAGES,
    num_stock_clips: int = app_config.NUM_STOCK_CLIPS,
    num_meme_clips: int = app_config.NUM_MEME_CLIPS,
):
    await callback(
        AssetResponse(
            event_type="generation_start",
            asset_id=asset.asset_id,
            asset_type="visual",
        )
    )

    selected_asset_path = get_selected_asset_file_path(
        session_id=session_id,
        asset_id=asset.asset_id,
        ext="mp4",
    )

    asset_dir_path = get_asset_dir_path(
        session_id=session_id,
        asset_id=asset.asset_id,
    )

    # make asset path directory if not exists
    os.makedirs(asset_dir_path, exist_ok=True)

    if mock:
        # copy a sample video to selected_asset_path
        mock_video_path = "mock/asset.mp4"
        uuids = [
            uuid.uuid4().hex
            for _ in range(num_stock_clips + num_stock_images + num_meme_clips)
        ]
        for i in range(num_stock_clips + num_stock_images + num_meme_clips):
            file_path = get_asset_file_path(
                session_id=session_id,
                asset_id=asset.asset_id,
                ext="mp4",
                id=uuids[i],
            )
            shutil.copyfile(mock_video_path, file_path)

            mock_image_path = "mock/asset.jpg"
            file_path_jpg = get_asset_file_path(
                session_id=session_id,
                asset_id=asset.asset_id,
                ext="jpg",
                id=uuids[i],
            )
            shutil.copyfile(mock_image_path, file_path_jpg)
            await callback(
                AssetResponse(
                    event_type="generation_end",
                    asset_id=asset.asset_id,
                    asset_type="visual",
                    candidate_id=uuids[i],
                )
            )

        base64_urls = [
            "" for _ in range(num_stock_clips + num_stock_images + num_meme_clips)
        ]

    else:
        [
            (stock_base64_urls, stock_uuids),
            (stock_base64_urls_vid, stock_uuids_vid),
            (meme_base64_urls, meme_uuids),
            (ai_base64_urls, ai_uuids),
        ] = await asyncio.gather(
            search_pixabay_photo(
                query=asset.asset_short_desc,
                asset_id=asset.asset_id,
                session_id=session_id,
                callback=callback,
                num_results=num_stock_images,
            ),
            search_pixabay_video(
                query=asset.asset_short_desc,
                asset_id=asset.asset_id,
                session_id=session_id,
                callback=callback,
                num_results=num_stock_clips,
            ),
            search_klipy(
                query=asset.asset_short_desc,
                asset_id=asset.asset_id,
                session_id=session_id,
                callback=callback,
                num_results=num_meme_clips,
            ),
            generate_image(
                prompt=asset.asset_long_desc,
                asset_id=asset.asset_id,
                session_id=session_id,
                callback=callback,
                enable_image_generation=enable_image_generation,
            ),
        )

        base64_urls = (
            stock_base64_urls
            + stock_base64_urls_vid
            + meme_base64_urls
            + ai_base64_urls
        )
        uuids = stock_uuids + stock_uuids_vid + meme_uuids + ai_uuids

    # print(f"stock_file_paths len: {len(stock_file_paths)}")
    # print(f"stock_file_paths_1 len: {len(stock_file_paths_1)}")
    # print(f"meme_file_paths len: {len(meme_file_paths)}")
    # print(f"ai_file_paths len: {len(ai_file_paths)}")

    # Assertion
    # print(f"Generated {len(base64_urls)} visual assets for asset_id {asset.asset_id}")

    await callback(
        AssetSelectionResponse(
            event_type="selection_start",
            asset_id=asset.asset_id,
            asset_type="visual",
        )
    )

    if enable_image_selection and not mock:
        idxs = await select_image(
            image_desc=asset.asset_long_desc,
            image_urls=base64_urls,
        )
    else:
        idxs = [0]

    if idxs is None:
        idxs = [0]

    idxs = [0 if i < 0 or i >= len(uuids) else i for i in idxs]

    await callback(
        AssetSelectionResponse(
            event_type="selection_end",
            asset_id=asset.asset_id,
            asset_type="visual",
            selected_candidate_ids=[uuids[i] for i in idxs],
            selected_candidate_id=uuids[idxs[0]],
        )
    )

    print(f"File paths: {uuids}\n")
    print(f"Selected asset indexes: {idxs}, selected index: {idxs[0]}\n")

    shutil.copyfile(
        get_asset_file_path(
            session_id=session_id,
            asset_id=asset.asset_id,
            ext="mp4",
            id=uuids[idxs[0]],
        ),
        selected_asset_path,
    )

    print(f"Selected asset saved to {selected_asset_path}\n")
