import asyncio


def async_run(coroutine):
    """Async executions for unit tests"""
    return asyncio.get_event_loop().run_until_complete(coroutine)
