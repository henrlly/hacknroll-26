import uuid
from typing import Any, Awaitable, Callable

import instructor
from openai import AsyncOpenAI
from openai.types.shared.reasoning_effort import ReasoningEffort
from pydantic import BaseModel

from app.api.types import AssetResponse
from app.core.config import app_config, settings
from app.core.models import VisualChoiceResponse
from app.utils.download_file import save_as_jpg, save_as_mp4
from app.utils.get_file_path import get_asset_file_path

oai_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1", api_key=settings.OPENROUTER_API_KEY
)

client = instructor.from_openai(oai_client)


async def generate_image(
    prompt: str,
    asset_id: str,
    session_id: str,
    callback: Callable[[BaseModel], Awaitable],
    enable_image_generation: bool = app_config.ENABLE_IMAGE_GENERATION,
) -> tuple[list[str], list[str]]:
    if not enable_image_generation:
        print("Image generation is disabled.")
        return [], []

    res = await oai_client.chat.completions.create(
        model="google/gemini-2.5-flash-image:nitro",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Generate an image with the description: {prompt}",
                    },
                ],
            }
        ],
        modalities=["text", "image"],  # pyright: ignore
    )

    res = res.model_dump()

    if res.get("choices"):
        message = res["choices"][0]["message"]
        if message.get("images"):
            for image in message["images"]:
                base64_url = image["image_url"]["url"]  # Base64 data URL
                candidate_id = uuid.uuid4().hex
                file_path = get_asset_file_path(
                    session_id=session_id,
                    asset_id=asset_id,
                    ext="mp4",
                    id=candidate_id,
                )
                await save_as_mp4(
                    url=base64_url,
                    file_name=file_path,
                )
                file_path_jpg = get_asset_file_path(
                    session_id=session_id,
                    asset_id=asset_id,
                    ext="jpg",
                    id=candidate_id,
                )
                await save_as_jpg(
                    url=base64_url,
                    file_name=file_path_jpg,
                )

                await callback(
                    AssetResponse(
                        event_type="generation_end",
                        asset_id=asset_id,
                        asset_type="visual",
                        candidate_id=candidate_id,
                    )
                )
                return [base64_url], [file_path]

    print("No images generated")
    return [], []


async def select_image(image_desc: str, image_urls: list[str]) -> list[int]:
    res: VisualChoiceResponse = await client.create(
        model="google/gemini-3-flash-preview:nitro",  # video url only supports yt video for gemini supported
        autodetect_images=True,
        messages=[
            {
                "role": "system",
                "content": "You are an expert image selector. Given a description and a set of images, you will select at least 3 images that best matches the description. Respond with only a list of the indexes (0-indexed) of the selected image.",
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"Image description: {image_desc}",
                    },
                    *[
                        {"type": "image_url", "image_url": {"url": url}}
                        for url in image_urls
                    ],
                ],
            },
        ],
        response_model=VisualChoiceResponse,
    )
    return res.selected_image_indexes


async def _generate_response_streamed(
    callback: Callable[[Any], Awaitable],
    input: str,
    instructions: str,
    model: str,
    temperature: float = 0,
    response_model: Any = None,
    reasoning_effort: ReasoningEffort | None = None,
) -> Any:
    kwargs = {"reasoning": {"effort": reasoning_effort}} if reasoning_effort else {}
    async with oai_client.responses.stream(
        model=f"{model}:nitro",  # nitro uses highest throughput provider
        instructions=instructions,
        input=input,
        text_format=response_model,
        temperature=temperature,
        extra_body={"provider": {"require_parameters": True}, **kwargs},
    ) as stream:
        async for event in stream:
            if event.type == "response.refusal.delta":
                await callback(event.delta)
            elif event.type == "response.output_text.delta":
                await callback(event.delta)
            elif event.type == "response.error":
                await callback(event.error)
            elif event.type == "response.completed":
                print("Completed")
                # print(event.response.output)

        final_response = await stream.get_final_response()

        return final_response.output_parsed


# TODO: loop this if return value is None
async def _generate_response_non_streamed(
    input: str,
    instructions: str,
    model: str,
    temperature: float = 0,
    response_model: Any = None,
    reasoning_effort: ReasoningEffort | None = None,
    retry_on_none: bool = app_config.RETRY_ON_NONE_RESPONSE,
) -> Any:
    kwarg = (
        {} if reasoning_effort is None else {"reasoning": {"effort": reasoning_effort}}
    )
    res = None
    while res is None or (retry_on_none and res.output_parsed is None):
        res = await oai_client.responses.parse(
            model=f"{model}:nitro",  # nitro uses highest throughput provider
            instructions=instructions.strip(),
            input=input,
            text_format=response_model,
            temperature=temperature,
            **kwarg,  # pyright: ignore
        )
        # TODO: add a delay between retries?

    # print(res)

    return res.output_parsed


async def generate_response(
    input: str,
    instructions: str,
    model: str,
    temperature: float = 0,
    response_model: Any = None,
    reasoning_effort: ReasoningEffort | None = None,
    callback: Callable[[Any], Awaitable] | None = None,
) -> Any:
    if callback:
        return await _generate_response_streamed(
            callback,
            input,
            instructions,
            model,
            temperature,
            response_model,
            reasoning_effort,
        )
    else:
        return await _generate_response_non_streamed(
            input,
            instructions,
            model,
            temperature,
            response_model,
            reasoning_effort,
        )
