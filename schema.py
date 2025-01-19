from typing import Any, TypedDict


class RequestBody(TypedDict):
    msg_id: Any
    in_reply_to: Any | None
    type: str | None
    echo: Any | None


class ResponseBody(TypedDict):
    msg_id: Any
    in_reply_to: Any | None
    type: str
    id: Any
