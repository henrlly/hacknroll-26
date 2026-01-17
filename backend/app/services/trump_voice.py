from gradio_client import Client
import shutil
import os

client = Client("selfit-camera/Trump-Ai-Voice")

import shutil
import os

def generate_trump_voice(text: str, output_filename: str = "output.mp3"):
    result = client.predict(
        text=text,
        language_display="🇺🇸 English",
        api_name="/generate_trump_voice_with_realtime_updates"
    )

    status = result[0]
    temp_audio_path = result[1]

    if not isinstance(temp_audio_path, str) or not temp_audio_path.endswith(".mp3"):
        raise ValueError(f"Unexpected API output: {result}")

    output_path = os.path.join(os.getcwd(), output_filename)
    shutil.copy(temp_audio_path, output_path)

    return {
        "status": status,
        "path": output_path
    }
