#!/usr/bin/env python3

import secrets
import time
from typing import cast

from maelstrom import Body, Node, Request
from schema import RequestBody

node = Node()


@node.handler
async def generate(req: Request) -> Body:
    body = req.body
    body = cast(RequestBody, body)

    message_id = body.get("msg_id")
    if body["type"] != "generate" or not message_id:
        return {}

    random_int = secrets.randbits(64)
    timestamp = time.time()

    id_ = f"{random_int}{timestamp}"
    return {"type": "generate_ok", "id": id_, "in_reply_to": message_id}


node.run()
