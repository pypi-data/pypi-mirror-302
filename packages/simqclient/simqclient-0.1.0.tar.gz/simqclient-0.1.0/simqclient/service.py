from .client import SimqClient
from .exceptions import TaskNotStartError
from .exceptions import TaskRunningError
from .exceptions import TaskCanceledError

__all__ = [
    "SimqService",
]


class SimqService(SimqClient):

    default_channel_prefix = "default"

    def __init__(self, channel_prefix=None, execute_timeout=5, **kwargs):
        self.channel_prefix = channel_prefix or self.default_channel_prefix
        self.execute_timeout = execute_timeout
        super().__init__(**kwargs)

    def get_service_channel(self, service):
        return f"{self.channel_prefix}.{service}"

    def get_result(self, response_data):
        return response_data.get("result", None)

    def execute(self, service, priority=False, execute_timeout=None, **data):
        if execute_timeout is None:
            execute_timeout = self.execute_timeout
        channel, task_id = self.apply_async(service=service, priority=priority, **data)
        msg = self.query(channel=channel, id=task_id, timeout=execute_timeout)
        status = msg.get("status", None)
        if status == "ready":
            raise TaskNotStartError("task %s:%s not start yet...", channel, task_id)
        elif status == "running":
            raise TaskRunningError("task %s:%s still running...", channel, task_id)
        elif status == "canceled":
            raise TaskCanceledError("task %s:%s already canceled...", channel, task_id)
        elif status == "done":
            return self.get_result(msg)

    def apply_async(self, service, priority=False, **data):
        channel = self.get_service_channel(service)
        if priority:
            task_id = self.rpush(channel=channel, data=data)
        else:
            task_id = self.lpush(channel, data=data)
        return channel, task_id
