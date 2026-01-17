import asyncio

from app.core.config import app_config
from app.core.pipeline import pipeline
from app.utils.make_callback import make_callback


async def test():
    async def print_wrapper(message: str):
        print(message)

    print(app_config.model_dump_json(indent=2))

    topic = "Binary Trees"
    callback = make_callback(print_wrapper)
    await pipeline(callback=callback, topic=topic, voice="obama")


asyncio.run(test())
