#!/usr/bin/env python3


from typing import cast

from maelstrom import Body, Node, Request
from schema import RequestBody

node = Node()


@node.handler
async def echo(req: Request) -> Body:
    body = req.body
    body = cast(RequestBody, body)
    return {
        "type": "echo_ok",
        "in_reply_to": body["msg_id"],
        "msg_id": body["msg_id"],
        "echo": body["echo"],
    }


node.run()
