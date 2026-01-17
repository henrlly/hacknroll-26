import asyncio
import uuid
from typing import Awaitable, Callable

from pydantic import BaseModel

from app.core.config import settings
from app.utils.api_client import ApiClient
from app.utils.download_file import (
    save_image_and_get_b64,
    save_video_and_get_image_b64,
)

# Pixabay has a 100 requests per minute limit
# Pixabay remote URLs cannot be viewed by gemini servers

api_client = ApiClient(max_rate=90, time_period=60)  # 90 requests per 60 seconds


async def search_pixabay_photo(
    query: str,
    session_id: str,
    asset_id: str,
    callback: Callable[[BaseModel], Awaitable],
    num_results: int = 3,
) -> tuple[list[str], list[str]]:
    """Returns a tuple of (list of base64 URL of photo, list of file path of asset)"""

    query = query.replace(" ", "+")
    num_results = min(max(num_results, 3), 200)
    """Return list of photo URLs (ending with .jpeg) from Pexels API based on query."""
    url = f"https://pixabay.com/api/?key={settings.PIXABAY_API_KEY}&q={query}&per_page={num_results}"

    headers = {
        "Content-Type": "application/json",
    }

    response = await api_client.get(url, headers=headers)

    if response.status_code != 200:
        print(
            f"Pixabay photo search failed for query '{query}' with status code {response.status_code if response else 'N/A'}\n"
        )
        return [], []

    obj = response.json()
    items = obj.get("hits", [])
    uuids = [uuid.uuid4().hex for _ in items]

    base64_urls = await asyncio.gather(
        *[
            save_image_and_get_b64(
                remote_url=item["largeImageURL"],
                uuid=uuids[i],
                asset_id=asset_id,
                session_id=session_id,
                callback=callback,
            )
            for i, item in enumerate(items)
        ]
    )

    return base64_urls, uuids


async def search_pixabay_video(
    query: str,
    session_id: str,
    asset_id: str,
    callback: Callable[[BaseModel], Awaitable],
    num_results: int = 3,
) -> tuple[list[str], list[str]]:
    """Returns a tuple of (list of base64 URL of thumbnail, list of file path of asset)"""

    query = query.replace(" ", "+")
    num_results = min(max(num_results, 3), 200)
    """Returns list of video URLs (ending with .mp4) from Pexels matching the query."""
    url = f"https://pixabay.com/api/videos/?key={settings.PIXABAY_API_KEY}&q={query}&per_page={num_results}"

    headers = {
        "Content-Type": "application/json",
    }

    response = await api_client.get(url, headers=headers)

    if response.status_code != 200:
        print(
            f"Pixabay video search failed for query '{query}' with status code {response.status_code if response else 'N/A'}\n"
        )
        return [], []

    obj = response.json()
    items = obj.get("hits", [])
    uuids = [uuid.uuid4().hex for _ in items]

    base64_urls = await asyncio.gather(
        *[
            save_video_and_get_image_b64(
                video_url=item["videos"]["medium"]["url"],
                image_url=item["videos"]["medium"]["thumbnail"],
                session_id=session_id,
                asset_id=asset_id,
                uuid=uuids[i],
                callback=callback,
            )
            for i, item in enumerate(items)
        ]
    )

    return base64_urls, uuids
