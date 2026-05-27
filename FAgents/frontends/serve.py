import asyncio


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .frontend import Frontend


async def ServeAsync(*frontends: Frontend) -> None:
    async with asyncio.TaskGroup() as tg:
        for frontend in frontends:
            tg.create_task(frontend.Serve())


def Serve(*frontends: Frontend) -> None:
    asyncio.run(ServeAsync(*frontends))
