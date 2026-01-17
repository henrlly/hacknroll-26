import os
import requests
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def transcribe_with_scribe_v2(
    audio_path: str
):
    if not ELEVENLABS_API_KEY:
        raise RuntimeError("ELEVENLABS_API_KEY not found in environment")

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"{audio_path} does not exist")

    url = "https://api.elevenlabs.io/v1/speech-to-text"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
    }

    files = {
        "file": (audio_path, open(audio_path, "rb"), "audio/mpeg"),
    }

    data = {
        "model_id": "scribe_v2",
        "timestamps": "true",   # IMPORTANT
        "diarization": "false"  # optional
    }

    response = requests.post(url, headers=headers, files=files, data=data)
    response.raise_for_status()

    result = response.json()

    # Debug print (full payload)
    print("=== Scribe v2 Raw Output ===")

    return extract_word_timestamps(result)


def extract_word_timestamps(transcription: dict):
    words = []
    word_start_times = []
    word_end_times = []

    for item in transcription.get("words", []):
        # Ignore pauses / spacing
        if item.get("type") != "word":
            continue

        words.append(item["text"])
        word_start_times.append(item["start"])
        word_end_times.append(item["end"])

    result =  {
        "words": words,
        "word_start_times_seconds": word_start_times,
        "word_end_times_seconds": word_end_times,
    }
    
    return result

