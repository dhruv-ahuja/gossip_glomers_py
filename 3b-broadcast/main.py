#!/usr/bin/env python3

import asyncio
from typing import TypedDict, cast
from maelstrom import Body, Node, Request
from schema import RequestBody


class BroadcastMessage(TypedDict):
    type: str
    message: int


class TopologyMessage(TypedDict):
    type: str
    topology: dict[str, list[str]]


node = Node()
lock = asyncio.Lock()
broadcast_lock = asyncio.Lock()
values = []
neighbor_ids = []

# Track messages we've already seen to prevent cycles
# node adds value -> forwards to its neighbors -> neighbors do the same thing
# using a set prevents that as we just propagate values not seen before
seen_messages = set()


@node.handler
async def broadcast(req: Request) -> Body:
    body = cast(BroadcastMessage, req.body)
    if body["type"] != "broadcast":
        return {}

    message = int(body["message"])
    response = {"type": "broadcast_ok"}

    async with broadcast_lock:
        # Only process message if we haven't seen it before
        if message in seen_messages:
            return response

        seen_messages.add(message)
        values.append(message)

        # Propagate to neighbors
        for neighbor_id in neighbor_ids:
            # Don't send back to the sender
            if neighbor_id == req.src:
                continue

            # Create new request while preserving the original message
            new_body = {"type": "broadcast", "message": message}
            request = Request(node.node_id, neighbor_id, new_body)
            await node._send(request)

    return response


@node.handler
async def read(req: Request) -> Body:
    body = cast(RequestBody, req.body)
    if body["type"] != "read":
        return {}

    return {"type": "read_ok", "messages": values}


@node.handler
async def topology(req: Request) -> Body:
    body = cast(TopologyMessage, req.body)
    if body["type"] != "topology":
        return {}

    async with lock:
        neighbor_nodes = body["topology"][node.node_id]
        neighbor_ids.extend(neighbor_nodes)

    return {"type": "topology_ok"}


node.run()
