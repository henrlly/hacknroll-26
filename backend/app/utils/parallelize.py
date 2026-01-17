import asyncio
from types import CoroutineType


async def parallelize(
    coroutines: list[CoroutineType],
):
    tasks = [asyncio.create_task(coroutine) for coroutine in coroutines]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    winner = done.pop()

    for task in pending:
        task.cancel()

    return await winner
