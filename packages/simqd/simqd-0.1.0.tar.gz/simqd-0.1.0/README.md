# simqd

SIMQ服务提供者，同时也是SIMQ消息的消费者。

## 安装

```shell
pip install simqd
```

## 使用

### 命令帮忙信息

```shell
d:\simqd>simqd --help
Usage: simqd [OPTIONS]

Options:
  -p, --service-provider TEXT
  -s, --base-url TEXT
  -a, --api-key TEXT
  -w, --workers INTEGER
  --help                       Show this message and exit.

```

### 使用案例

```shell
simqd -p simqdsvr.debug.DebugPing -p simqdsvr.debug.DebugEcho
```

## 服务提供者开发

**simqdsvr/debug.py**

```python
from simqdsvr.service_providers import SimqServiceProvider

__all__ = [
    "DebugPing",
    "DebugEcho",
]


class DebugPing(SimqServiceProvider):
    channel = "debug.ping"

    def handler(self):
        return "pong"


class DebugEcho(SimqServiceProvider):
    channel = "debug.echo"

    def handler(self, msg):
        return msg
```

## 版本记录

### 0.1.0

- 版本首发。
