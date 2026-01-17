import base64
import shutil
from typing import Awaitable, Callable

from elevenlabs import AsyncElevenLabs
from pydantic import BaseModel

from app.api.types import AssetResponse, NarrationResponse
from app.core.config import app_config, settings
from app.core.models import VoiceType
from app.utils.alignment import (
    character_alignment_to_word_alignment,
    mock_word_alignment,
)
from app.utils.normalize_volume import normalize_volume

client = AsyncElevenLabs(
    api_key=settings.ELEVENLABS_API_KEY, base_url="https://api.elevenlabs.io"
)


async def generate_speech(
    text: str,
    voice: VoiceType,
    file_name: str,
    callback: Callable[[BaseModel], Awaitable],
    scene_number: int,
    mock: bool = True,
    use_flash: bool = app_config.MOCK_NARRATION,
) -> str:
    await callback(
        NarrationResponse(
            event_type="narration_generation_start", scene_number=scene_number
        )
    )

    if mock:
        shutil.copyfile(
            "mock/narration.mp3",
            file_name,
        )
        alignment = mock_word_alignment(text)
    else:
        res = await client.text_to_speech.convert_with_timestamps(
            model_id="eleven_flash_v2_5"
            if use_flash
            else "eleven_v3",  # eleven_flash_v2_5, eleven_v3
            voice_id="repzAAjoKlgcT2oOAIWt",  ## 6OzrBCQf8cjERkYgzSg8:black Ybqj6CIlqb6M85s9Bl4n:blacker repzAAjoKlgcT2oOAIWt:youtuber
            text=text,
        )
        base64_audio = res.audio_base_64
        audio_bytes = base64.b64decode(base64_audio)

        with open(file_name, "wb") as f:
            f.write(audio_bytes)

        if res.alignment is not None:
            alignment = character_alignment_to_word_alignment(res.alignment)
        else:
            return mock_word_alignment(text)

    await callback(
        NarrationResponse(
            event_type="narration_generation_end", scene_number=scene_number
        )
    )
    return alignment


async def generate_sound_effect(
    description: str,
    file_name: str,
    callback: Callable[[BaseModel], Awaitable],
    asset_id: str,
    mock: bool = app_config.MOCK_SFX,
):
    await callback(
        AssetResponse(
            event_type="generation_start",
            asset_id=asset_id,
            asset_type="sound_effect",
        )
    )

    if mock:
        shutil.copyfile(
            "mock/sfx.mp3",
            file_name,
        )
    else:
        res = client.text_to_sound_effects.convert(text=description)
        b = b""
        async for chunk in res:
            b += chunk
        with open(file_name, "wb") as f:
            f.write(b)
        print(f"Generated sound effect saved to {file_name}\n")

        await normalize_volume(file_name)
        print(f"Normalized volume for sound effect {file_name}\n")

    await callback(
        AssetResponse(
            type="asset",
            event_type="generation_end",
            asset_id=asset_id,
            asset_type="sound_effect",
        )
    )
