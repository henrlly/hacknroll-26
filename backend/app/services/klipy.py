import asyncio
import uuid
from typing import Awaitable, Callable

from pydantic import BaseModel

from app.core.config import settings
from app.utils.api_client import ApiClient
from app.utils.download_file import save_video_and_get_image_b64

# https://support.google.com/tenor/answer/10455265#whatll-happen-to-the-tenor-api&zippy=%2Cwhatll-happen-to-the-tenor-api
# Tenor API is dead!

# Klipy has 100 requests per minute limit
# https://old.reddit.com/r/appdev/comments/1q81g0v/tenor_alternative_gif_api_migration_in_few/nyk47rl/
api_client = ApiClient(max_rate=1, time_period=1)  # 1 requests per 1 seconds


async def search_klipy(
    query: str,
    session_id: str,
    asset_id: str,
    callback: Callable[[BaseModel], Awaitable],
    sticker: bool = False,  # search stickers instead of gifs
    num_results: int = 3,
) -> tuple[list[str], list[str]]:
    url = f"https://api.klipy.com/v2/search?key={settings.KLIPY_API_KEY}&limit={num_results}&q={query}"

    if sticker:
        url += "&searchfilter=sticker"

    headers = {"Content-Type": "application/json"}
    # async with httpx.AsyncClient() as client:
    response = await api_client.get(url, headers=headers)

    if response.status_code != 200:
        print(
            f"Klipy search failed for query '{query}' with status code {response.status_code if response else 'N/A'}\n"
        )
        return [], []

    obj = response.json()
    # print("Klipy search response:", obj)
    items = obj.get("results", [])
    uuids = [uuid.uuid4().hex for _ in items]

    # only include if both mp4 and gifpreview are present
    zipped_urls = [
        (
            item.get("media_formats", {}).get("mp4", {}).get("url", ""),
            item.get("media_formats", {}).get("gifpreview", {}).get("url", ""),
        )
        for item in items
        if item.get("media_formats", {}).get("mp4", {}).get("url", "")
        and item.get("media_formats", {}).get("gifpreview", {}).get("url", "")
    ]
    base64_urls = await asyncio.gather(
        *[
            save_video_and_get_image_b64(
                video_url=video_url,
                image_url=image_url,
                session_id=session_id,
                asset_id=asset_id,
                uuid=uuids[i],
                callback=callback,
            )
            for i, (video_url, image_url) in enumerate(zipped_urls)
        ]
    )

    return base64_urls, uuids
