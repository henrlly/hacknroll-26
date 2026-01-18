```sh
brew install manim ffmpeg
```

```sh
uv run fastapi dev --no-reload # static folder contains .py files
```

http://127.0.0.1:8000

Copy .env.example to .env, and add api key

# TODO

1. Change voice provider, remember to let it fail gracefully (with retries).
2. Use jupyter notebook to optimize plan prompt # add "use descriptive asset_ids"

Elevenlabs sfx generation *can't* fail surely, so that one don't need to fail gracefully

# IMPROVEMENTS

1. Semantic search for visual assets

# STYLE POLISH

1. remove extra deps from lockfile
2. organize `.gitignore`s in monorepo

# NOTES

- reasoning models (even small ones) are much more expensive (reasoning token costs) and not necessarily better
- 4.5 opus for code generation, opus can generate working code on the first try much more often than every other model, including sonnet
- sonnet can generate good code too much less of the time, and sonnet + reasoning = infinite loop

Static files are served from `/static`
`/static/{session_id}` contains

- `final_video.mp4`
- `scene_{i}_{version_number}.mp4` # rendered manim scene
- `scene_{i}.mp4` # rendered manim scene in final video
- `scene_{i}_{version_number}.py` # manim code
- `scene_{i}.txt` # prompt
- `narration_scene_{i}.mp3` # narration audio
- `{asset_id}.mp3,mp4` # chosen sfx or asset
- `{asset_id}/`
  - `{uuid}.mp3,mp4` # multiple variations of sfx or asset

`/working/{session_id}/scene_{scene_number}` is the media working directory for manim rendering
