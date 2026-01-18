import asyncio
import logging
from typing import Awaitable, Callable

from pydantic import BaseModel

from app.core.config import app_config
from app.core.models import PipelineCallback


def make_callback(
    send_text: Callable[[str], Awaitable], delay: float = 0
) -> PipelineCallback:
    async def callback(model: BaseModel, delay: float = delay):
        await asyncio.sleep(delay)
        logging.info(f"Callback sending model data: {model.model_dump_json()}")
        await send_text(model.model_dump_json(indent=None))

    return callback
