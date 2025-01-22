#!/usr/bin/env python3

from typing import cast
from uuid import uuid4

from maelstrom import Body, Node, Request
from schema import RequestBody

node = Node()


@node.handler
async def generate(req: Request) -> Body:
    body = req.body
    body = cast(RequestBody, body)

    if body["type"] != "generate" or not body.get("msg_id"):
        return {}

    return {"type": "generate_ok", "id": str(uuid4()), "in_reply_to": body["msg_id"]}


node.run()
