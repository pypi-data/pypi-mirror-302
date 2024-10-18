import uuid
import time
import json
import datetime

from django_redis import get_redis_connection
from django_apis.exceptions import Forbidden

from .settings import SIMQ_ACK_EVENT_EXPIRE
from .settings import SIMQ_DONE_ITEM_EXPIRE
from .settings import SIMQ_MQ_DEFAULT
from .settings import SIMQ_MQS
from .settings import SIMQ_PREFIX
from .settings import SIMQ_APIKEYS
from .settings import SIMQ_APIKEY_HEADER


def apikey_validate(request):
    if SIMQ_APIKEYS:
        if request.META.get(SIMQ_APIKEY_HEADER, None) in SIMQ_APIKEYS:
            return
        raise Forbidden()


def getdb(channel):
    name = SIMQ_MQS.get(channel, SIMQ_MQ_DEFAULT)
    return get_redis_connection(name)


def hset(db, key, data):
    mapping = {}
    for item, value in data.items():
        mapping[item] = json.dumps(value)
    db.hset(key, mapping=mapping)


def hgetall(db, key):
    data = {}
    mapping = db.hgetall(key)
    for item, value in mapping.items():
        data[item] = json.loads(value)
    return data


def get_mq_key(channel):
    return f"{SIMQ_PREFIX}:mq:{channel}"


def get_tmp_key(channel, tmpid):
    return f"{SIMQ_PREFIX}:tmp:{channel}:{tmpid}"


def get_done_key(id):
    if isinstance(id, bytes):
        id = id.decode("utf-8")
    return f"{SIMQ_PREFIX}:done:{id}"


def get_item_key(id):
    if isinstance(id, bytes):
        id = id.decode("utf-8")
    return f"{SIMQ_PREFIX}:item:{id}"


def _dumps(v):
    if isinstance(v, datetime.datetime):
        return v.isoformat()
    return v


def get_msgdata(msg):
    return json.dumps(msg, ensure_ascii=False, default=_dumps)


def rpush(channel, data, id=None):
    id = id or str(uuid.uuid4())
    db = getdb(channel)
    qkey = get_mq_key(channel)
    ikey = get_item_key(id=id)
    msg = {
        "id": id,
        "channel": channel,
        "add_time": time.time(),
        "mod_time": time.time(),
        "status": "ready",
        "data": data,
    }
    hset(db, ikey, msg)
    db.rpush(qkey, id)
    return id


def lpush(channel, data, id=None):
    id = id or str(uuid.uuid4())
    db = getdb(channel)
    qkey = get_mq_key(channel)
    ikey = get_item_key(id=id)
    msg = {
        "id": id,
        "channel": channel,
        "add_time": time.time(),
        "mod_time": time.time(),
        "status": "ready",
        "data": data,
    }
    hset(db, ikey, msg)
    db.lpush(qkey, id)
    return id


def pop(channel, worker, timeout=5):
    tmpid = str(uuid.uuid4())
    db = getdb(channel=channel)
    qkey = get_mq_key(channel=channel)
    tkey = get_tmp_key(channel=channel, tmpid=tmpid)
    id = db.brpoplpush(qkey, tkey, timeout=timeout)
    if id is None:
        return None
    ikey = get_item_key(id=id)
    msg = hgetall(db, ikey)
    if not msg:
        return None
    # 处理被取消的消息
    if msg.get("cancel_flag", False):
        hset(
            db,
            ikey,
            {
                "cancel_status": "canceled",
                "canceled_time": time.time(),
                "status": "canceled",
                "mod_time": time.time(),
                "done_time": time.time(),
                "result": None,
            },
        )
        tkey = get_tmp_key(channel=channel, tmpid=tmpid)
        db.delete(tkey)
        dkey = get_done_key(id=msg["id"])
        db.lpush(dkey, msg["id"])
        db.expire(dkey, SIMQ_ACK_EVENT_EXPIRE)
        db.expire(ikey, SIMQ_DONE_ITEM_EXPIRE)
        return None
    # 更新消息状态
    hset(
        db,
        ikey,
        {
            "running_id": tmpid,
            "start_time": time.time(),
            "mod_time": time.time(),
            "status": "running",
            "worker": worker,
        },
    )
    # 返回消息体
    msg = hgetall(db, ikey)
    return msg


def ack(channel, id, result=None):
    db = getdb(channel=channel)
    ikey = get_item_key(id=id)
    msg = hgetall(db, ikey)
    if not msg:
        return None
    hset(
        db,
        ikey,
        {
            "ack_time": time.time(),
            "mod_time": time.time(),
            "status": "done",
            "result": result,
        },
    )
    tkey = get_tmp_key(channel=channel, tmpid=msg["running_id"])
    db.delete(tkey)
    dkey = get_done_key(id=msg["id"])
    db.lpush(dkey, msg["id"])
    db.expire(dkey, SIMQ_ACK_EVENT_EXPIRE)
    db.expire(ikey, SIMQ_DONE_ITEM_EXPIRE)
    return True


def query(channel, id, timeout=0):
    db = getdb(channel=channel)
    ikey = get_item_key(id=id)
    if timeout == 0:
        msg = hgetall(db, ikey)
        if not msg:
            return None
        return msg
    else:
        dkey = get_done_key(id=id)
        db.brpop(dkey, timeout=timeout)
        msg = hgetall(db, ikey)
        if not msg:
            return None
        return msg


def cancel(channel, id):
    db = getdb(channel=channel)
    ikey = get_item_key(id=id)
    msg = hgetall(db, ikey)
    if not msg:
        return False
    if msg["status"] in ["running", "done", "canceled"]:
        return False
    hset(
        db,
        ikey,
        {
            "cancel_status": "canceling",
            "cancel_flag": True,
            "cancel_time": time.time(),
        },
    )
    return True


def ret(channel, id):
    db = getdb(channel=channel)
    ckey = get_mq_key(channel=channel)
    ikey = get_item_key(id=id)
    msg = hgetall(db, ikey)
    # 没有消息体，无法return
    if not msg:
        return False
    # 状态不为running，无法return
    if msg.get("status", "unknown") != "running":
        return False
    # 如果存在running状态变量，则删除
    if "running_id" in msg:
        tkey = get_tmp_key(channel=channel, tmpid=msg["running_id"])
        db.delete(tkey)
    # 更新消息状态
    hset(
        db,
        ikey,
        {
            "status": "ready",
            "return_flag": True,
            "return_time": time.time(),
            "mod_time": time.time(),
            "return_count": msg.get("return_count", 0) + 1,
            "worker": None,
        },
    )
    db.lpush(ckey, id)
    return True
