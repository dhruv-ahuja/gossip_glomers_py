#!/usr/bin/env python3

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
values = []
topology_ = {}


@node.handler
async def broadcast(req: Request) -> Body:
    body = cast(BroadcastMessage, req.body)
    if body["type"] != "broadcast":
        return {}

    values.append(body["message"])
    return {"type": "broadcast_ok"}


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

    global topology_
    topology_ = body["topology"]
    return {"type": "topology_ok"}


node.run()
