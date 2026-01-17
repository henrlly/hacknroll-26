import json

from elevenlabs.types import CharacterAlignmentResponseModel

from app.core.config import app_config


def mock_word_alignment(full_text: str) -> str:
    words = []
    word_start_times = []
    word_end_times = []

    current_time = 0.0
    time_per_char = 0.05  # assume each character takes 50ms

    current_word = []
    current_start = None

    for char in full_text:
        if char.isspace():
            if current_word:
                words.append("".join(current_word))
                word_start_times.append(current_start)
                word_end_times.append(current_time)

                current_word = []
                current_start = None
        else:
            if not current_word:
                current_start = current_time
            current_word.append(char)
        current_time += time_per_char

    # finalize last word
    if current_word:
        words.append("".join(current_word))
        word_start_times.append(current_start)
        word_end_times.append(current_time)

    return json.dumps(
        {
            "words": words,
            "word_start_times_seconds": word_start_times,
            "word_end_times_seconds": word_end_times,
        },
        separators=(",", ":"),  # minify JSON
    )


def character_alignment_to_word_alignment(
    character_alignment: CharacterAlignmentResponseModel,
    keep_tags: bool = app_config.AUDIO_TRANSCRIPTION_KEEP_TAGS,
) -> str:
    words = []
    word_start_times = []
    word_end_times = []

    current_word = []
    current_start = None
    current_end = None

    # consider everything enclosed by square brackets as a single word
    in_brackets = False
    for (
        char,
        start_time,
        end_time,
    ) in zip(
        character_alignment.characters,
        character_alignment.character_start_times_seconds,
        character_alignment.character_end_times_seconds,
    ):
        if char == "[":
            in_brackets = True
            if current_word:
                words.append("".join(current_word))
                word_start_times.append(current_start)
                word_end_times.append(current_end)
                current_word = []
            current_word.append(char)
            current_start = start_time
        elif char == "]":
            in_brackets = False
            current_word.append(char)
            current_end = end_time
            if keep_tags:
                words.append("".join(current_word))
                word_start_times.append(current_start)
                word_end_times.append(current_end)
            current_word = []
            current_start = None
            current_end = None
        elif char.isspace() and not in_brackets:
            if current_word:
                words.append("".join(current_word))
                word_start_times.append(current_start)
                word_end_times.append(current_end)
                current_word = []
                current_start = None
                current_end = None
        else:
            if not current_word:
                current_start = start_time
            current_word.append(char)
            current_end = end_time

    return json.dumps(
        {
            "words": words,
            "word_start_times_seconds": word_start_times,
            "word_end_times_seconds": word_end_times,
        },
        separators=(",", ":"),  # minify JSON
    )
