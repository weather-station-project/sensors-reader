import asyncio


def async_run_from_sync(method, parameter):
    """Method to execute async methods from sync"""
    loop = asyncio.get_event_loop()
    t = loop.create_task(method(parameter))

    return loop.run_until_complete(t)
