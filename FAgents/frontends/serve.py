import asyncio


async def ServeAsync(*frontends):
    async with asyncio.TaskGroup() as tg:
        for frontend in frontends:
            tg.create_task(frontend.Serve())


def Serve(*frontends):
    asyncio.run(ServeAsync(*frontends))
