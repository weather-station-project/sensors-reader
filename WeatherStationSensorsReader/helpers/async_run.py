import asyncio


def run_async_from_sync(coroutine):
    """Async executions from sync methods"""
    return asyncio.get_event_loop().run_until_complete(future=coroutine)
