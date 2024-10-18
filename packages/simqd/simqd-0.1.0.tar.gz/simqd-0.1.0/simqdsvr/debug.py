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
