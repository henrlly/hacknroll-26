import asyncio
import os
import tempfile


async def normalize_volume(input_file: str) -> None:
    # use ffmpeg to normalize the volume of the input file, to that is is not too loud
    normalized_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=True).name
    command = [
        "ffmpeg",
        "-i",
        input_file,
        "-af",
        "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-y",
        normalized_file,
    ]
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    if process.returncode != 0:
        raise Exception(f"ffmpeg failed: {stderr.decode()}")

    os.replace(normalized_file, input_file)
    # os.remove(normalized_file)
