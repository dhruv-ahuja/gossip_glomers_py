#!/usr/bin/env python3

import datetime
import random
import sys
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

    random_int = random.randint(0, sys.maxsize)
    timestamp = datetime.datetime.now(datetime.UTC).timestamp()

    id_ = f"{random_int}{int(timestamp)}"
    return {"type": "generate_ok", "id": id_, "in_reply_to": message_id}


node.run()
