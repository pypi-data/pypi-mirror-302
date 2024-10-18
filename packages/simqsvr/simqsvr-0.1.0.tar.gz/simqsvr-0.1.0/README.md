# simqsvr

SIMQ服务器。基于redis的消息队列，通过web接口提供对外服务。

## 安装

```shell
pip install simqsvr
```

## 接口列表

接口地址 | 接口名称 |
-- | -- |
/simq/api/{channel}/rpush | 添加消息（高优先级） |
/simq/api/{channel}/lpush | 添加消息（低优先级） |
/simq/api/{channel}/dpush | 添加延迟消息 |
/simq/api/{channel}/pop | 获取消息执行 |
/simq/api/{channel}/ack | 确认消息执行完成 |
/simq/api/{channel}/ret | 退还消息 |
/simq/api/{channel}/query | 查询消息详情 |
/simq/api/{channel}/cancel | 取消消息（仅限待处理状态） |
/simq/api/{channel}/delete | 删除消息 |

## 简易使用方法

```shell
# 创建数据库
manage-simqsvr migrate
# 创建超级用户
manage-simqsvr createsuperuser

# 启动服务
manage-simqsvr runserver 0.0.0.0:80 --noreload
```

- 创建数据库&创建超级用户，只是用来登录swagger接口管理界面。
- 如果不需要使用swagger接口管理功能，可以忽略上述两个步骤。

## 注意事项

- simqsvr目前仅支持基于redis的消息队列。
- 必须要按django-redis标准来配置CACHES配置项。如：
    ```python
    # decode_responses=True是必须的
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://127.0.0.1:6379/0?decode_responses=True",
        }
    }
    ```

## 版本

### 0.1.0

- 版本首发。
