import base64
from typing import Awaitable, Callable

import cv2
import httpx
import numpy as np
from pydantic import BaseModel

from app.api.types import AssetResponse
from app.utils.get_file_path import get_asset_file_path


async def save_video_and_get_image_b64(
    video_url: str,
    image_url: str,
    callback: Callable[[BaseModel], Awaitable],
    session_id: str,
    asset_id: str,
    uuid: str,
):
    async with httpx.AsyncClient() as client:
        video_response = await client.get(video_url)
        file_name = get_asset_file_path(
            session_id=session_id,
            asset_id=asset_id,
            ext="mp4",
            id=uuid,
        )
        with open(file_name, "wb") as f:
            f.write(video_response.content)

        await callback(
            AssetResponse(
                event_type="generation_end",
                asset_id=asset_id,
                asset_type="visual",
                candidate_id=uuid,
            )
        )

        image_response = await client.get(image_url)
        image_data = image_response.content
        file_name_jpg = get_asset_file_path(
            session_id=session_id,
            asset_id=asset_id,
            ext="jpg",
            id=uuid,
        )
        _save_raw_data_as_jpg(image_data, file_name_jpg)
        base64_data = base64.b64encode(image_data).decode("utf-8")
        content_type = image_response.headers.get("Content-Type", "image/jpeg")
        base64_url = f"data:{content_type};base64,{base64_data}"

        return base64_url


async def save_image_and_get_b64(
    remote_url: str,
    uuid: str,
    asset_id: str,
    session_id: str,
    callback: Callable[[BaseModel], Awaitable],
):
    async with httpx.AsyncClient() as client:
        response = await client.get(remote_url)
        file_name = get_asset_file_path(
            session_id=session_id,
            asset_id=asset_id,
            ext="mp4",
            id=uuid,
        )
        file_name_jpg = get_asset_file_path(
            session_id=session_id,
            asset_id=asset_id,
            ext="jpg",
            id=uuid,
        )
        _save_raw_data_as_mp4(response.content, file_name)
        _save_raw_data_as_jpg(response.content, file_name_jpg)
        await callback(
            AssetResponse(
                event_type="generation_end",
                asset_id=asset_id,
                asset_type="visual",
                candidate_id=uuid,
            )
        )

        image_data = response.content
        base64_data = base64.b64encode(image_data).decode("utf-8")
        content_type = response.headers.get("Content-Type", "image/jpeg")
        base64_url = f"data:{content_type};base64,{base64_data}"

        return base64_url


async def convert_image_url_to_base64_url(image_url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(image_url)
        image_data = response.content
        base64_data = base64.b64encode(image_data).decode("utf-8")
        content_type = response.headers.get("Content-Type", "image/jpeg")
        base64_url = f"data:{content_type};base64,{base64_data}"
        return base64_url


async def download_file(url: str, file_name: str):
    async with httpx.AsyncClient() as client:
        media_response = await client.get(url)
        with open(file_name, "wb") as f:
            f.write(media_response.content)


def _save_raw_data_as_jpg(data: bytes, file_name: str):
    image_array = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image from the provided data.")

    # Ensure filename ends with .jpg or .jpeg
    if not file_name.lower().endswith((".jpg", ".jpeg")):
        file_name += ".jpg"

    cv2.imwrite(file_name, img)


# if use webm/mp4/gif with transparency, need ffmpeg
def _save_raw_data_as_mp4(data: bytes, file_name: str):
    image_array = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image from the provided URL.")

    height, width, _layers = img.shape
    fourcc = cv2.VideoWriter.fourcc(
        *"avc1"
    )  # cannot use mp4v, web browser doesnt support
    video = cv2.VideoWriter(file_name, fourcc, 1, (width, height))

    video.write(img)  # write 1 frame
    video.release()


async def save_as_jpg(url: str, file_name: str):
    if url.startswith("data"):  # base64 data URL of an image
        data = base64.b64decode(url.split(",")[1])
        _save_raw_data_as_jpg(data, file_name)

async def save_as_mp4(url: str, file_name: str):
    if url.endswith(".mp4"):
        await download_file(url, file_name)

    elif url.startswith("data"):  # base64 data URL of an image
        data = base64.b64decode(url.split(",")[1])
        _save_raw_data_as_mp4(data, file_name)

    else:  # is png/jpeg, convert to a static mp4 with opencv
        async with httpx.AsyncClient() as client:
            media_response = await client.get(url)
            _save_raw_data_as_mp4(media_response.content, file_name)
