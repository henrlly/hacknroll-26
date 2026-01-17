import base64
import json
import shutil
from typing import Awaitable, Callable

from elevenlabs import AsyncElevenLabs
from fishaudio import AsyncFishAudio
from fishaudio.utils import play, save
from pydantic import BaseModel

from app.api.types import AssetResponse, NarrationResponse
from app.core.config import app_config, settings
from app.core.models import VoiceType
from app.services.narration_timestamps import (
    extract_word_timestamps,
    transcribe_with_scribe_v2,
)
from app.services.trump_voice import generate_trump_voice
from app.utils.alignment import (
    character_alignment_to_word_alignment,
    mock_word_alignment,
    stt_response_to_character_alignment,
)
from app.utils.normalize_volume import normalize_volume

client = AsyncElevenLabs(
    api_key=settings.ELEVENLABS_API_KEY, base_url="https://api.elevenlabs.io"
)

fishClient = AsyncFishAudio(api_key=settings.FISH_API_KEY)

async def generate_speech(
    text: str,
    voice: VoiceType,
    file_name: str,
    callback: Callable[[BaseModel], Awaitable],
    scene_number: int,
    mock: bool = True,
    use_flash: bool = app_config.MOCK_NARRATION,
    use_local: bool = app_config.USE_LOCAL_TTS,
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
        if use_local:
            generate_trump_voice(text, file_name)
        else:
            voices: dict[VoiceType, str] = {
                "trump": "7ee05bf86c884881945ca034aeddbebb",
                "obama": "4ce7e917cedd4bc2bb2e6ff3a46acaa1",
                "peter": "a5c5987257a14018a90111ee52a4e71a"
            }
            audio = await fishClient.tts.convert(text="Saving this audio to a file!", reference_id=voices[voice])
            save(audio, file_name)
        with open(file_name, "rb") as f:
            transcription = await client.speech_to_text.convert(
                model_id="scribe_v1", file=f
            )
            print()
            print(transcription)
            print()
        return stt_response_to_character_alignment(transcription)

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
