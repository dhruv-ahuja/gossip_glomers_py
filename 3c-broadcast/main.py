#!/usr/bin/env python3

import asyncio
from typing import TypedDict, cast
from maelstrom import Body, Node, Request
from schema import RequestBody


class BaseMessage(TypedDict):
    type: str


class BroadcastMessage(BaseMessage):
    message: int


class TopologyMessage(BaseMessage):
    topology: dict[str, list[str]]


class BroadcastAllMessage(BaseMessage):
    values: list


node = Node()
lock = asyncio.Lock()
broadcast_lock = asyncio.Lock()
values = []
neighbor_ids = []

# Track messages we've already seen to prevent cycles
# node adds value -> forwards to its neighbors -> neighbors do the same thing
# using a set prevents that as we just propagate values not seen before
seen_messages = set()


async def _broadcast_all_values():
    """Periodically broadcasts all seen/gathered values to all neighboring nodes.
    This ensures that all nodes receive the latest values and are eventually consistent."""

    node_id = node.node_id

    try:
        while True:
            for neighbor_id in neighbor_ids:
                # check for current node id just in case
                if neighbor_id == node_id:
                    continue

                body = {"type": "broadcast_all", "values": values}
                request = Request(node_id, neighbor_id, body)

                await node._send(request)
            await asyncio.sleep(1)
    except Exception as ex:
        await node.log(f"exception when broadcasting values from node {node.node_id}: {ex}")


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

    node.spawn(_broadcast_all_values())
    return {"type": "topology_ok"}


@node.handler
async def broadcast_all(req: Request) -> Body:
    body = cast(BroadcastAllMessage, req.body)
    if body["type"] != "broadcast_all":
        return {}

    # register all new values from the received value list
    # this ensures consistency across nodes after network partitions
    async with broadcast_lock:
        for value in body["values"]:
            if value not in seen_messages:
                seen_messages.add(value)
                values.append(value)

    return {"type": "broadcast_all_ok"}


node.run()
