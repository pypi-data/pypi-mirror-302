from django.conf import settings


SIMQ_MQ_DEFAULT = getattr(settings, "SIMQ_MQ_DEFAULT", "default")
SIMQ_MQS = getattr(settings, "SIMQ_MQS", {})
SIMQ_PREFIX = getattr(settings, "SIMQ_PREFIX", "simq")

# 已完成消息通知事件默认保留10分钟
SIMQ_ACK_EVENT_EXPIRE = getattr(settings, "SIMQ_ACK_EVENT_EXPIRE", 10 * 60)

# 已完成消息及结果默认保留7天
SIMQ_DONE_ITEM_EXPIRE = getattr(settings, "SIMQ_DONE_ITEM_EXPIRE", 60 * 60 * 7)

# 接口认证
SIMQ_APIKEYS = getattr(settings, "SIMQ_APIKEYS", [])
SIMQ_APIKEY_HEADER = getattr(settings, "SIMQ_APIKEY_HEADER", "HTTP_APIKEY")
