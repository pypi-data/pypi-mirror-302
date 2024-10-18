from typing import Optional
from typing import Any

import pydantic
from django_apis.views import apiview

from . import services


class PushPayload(pydantic.BaseModel):
    id: Optional[str] = None
    data: Any


@apiview(methods="post", tags="simq")
def rpush(request, channel: str, payload: PushPayload) -> str:
    """添加消息（高优先级）"""
    services.apikey_validate(request=request)
    return services.rpush(
        channel=channel,
        data=payload.data,
        id=payload.id,
    )


@apiview(methods="post", tags="simq")
def lpush(request, channel: str, payload: PushPayload) -> str:
    """添加消息（低优先级）"""
    services.apikey_validate(request=request)
    return services.lpush(
        channel=channel,
        data=payload.data,
        id=payload.id,
    )


class PopPayload(pydantic.BaseModel):
    worker: str
    timeout: int = 5


@apiview(methods="post", tags="simq")
def pop(request, channel: str, payload: PopPayload) -> Any:
    """获取消息执行"""
    services.apikey_validate(request=request)
    return services.pop(
        channel=channel,
        timeout=payload.timeout,
        worker=payload.worker,
    )


class AckPayload(pydantic.BaseModel):
    id: str
    result: Optional[Any] = None


@apiview(methods="post", tags="simq")
def ack(request, channel: str, payload: AckPayload) -> bool:
    """确认消息执行完成"""
    services.apikey_validate(request=request)
    return services.ack(
        channel=channel,
        id=payload.id,
        result=payload.result,
    )


class QueryPayload(pydantic.BaseModel):
    id: str
    timeout: int = 0


@apiview(methods="post", tags="simq")
def query(request, channel: str, payload: QueryPayload) -> bool:
    """查询消息详情。

    timeout: 为0时，表示及时返回当前任务详情。不为0时，等待消息确认或超时后返回最新任务详情。
    """
    services.apikey_validate(request=request)
    return services.query(
        channel=channel,
        id=payload.id,
        timeout=payload.timeout,
    )


class CancelPayload(pydantic.BaseModel):
    id: str


@apiview(methods="post", tags="simq")
def cancel(request, channel: str, payload: CancelPayload) -> bool:
    """取消消息（仅限待处理状态）。"""
    services.apikey_validate(request=request)
    return services.cancel(
        channel=channel,
        id=payload.id,
    )


class RetPayload(pydantic.BaseModel):
    id: str


@apiview(methods="post", tags="simq")
def ret(request, channel: str, payload: RetPayload) -> bool:
    """退还消息"""
    services.apikey_validate(request=request)
    return services.ret(
        channel=channel,
        id=payload.id,
    )
