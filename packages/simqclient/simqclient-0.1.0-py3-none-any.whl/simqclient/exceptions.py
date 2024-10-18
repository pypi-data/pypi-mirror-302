class ServerError(RuntimeError):
    pass


class TaskStatusError(RuntimeError):
    pass


class TaskNotStartError(TaskStatusError):
    pass


class TaskRunningError(TaskStatusError):
    pass


class TaskCanceledError(TaskStatusError):
    pass
