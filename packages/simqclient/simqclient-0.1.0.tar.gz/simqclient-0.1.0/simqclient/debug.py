from .service import SimqService

__all__ = [
    "DebugService",
]


class DebugService(SimqService):

    default_channel_prefix = "debug"

    def ping(self):
        return self.execute("ping")

    def async_ping(self):
        return self.apply_async("ping")

    def echo(self, msg):
        return self.execute("echo", msg=msg)

    def async_echo(self, msg):
        return self.apply_async("echo", msg=msg)
