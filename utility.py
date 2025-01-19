from asyncio import Lock

lock = Lock()
counter = 0


async def generate_unique_id(node_id: int):
    """Generates unique IDs by maintaining a thread-safe global counter value."""

    global counter
    async with lock:
        counter += 1
        return counter
