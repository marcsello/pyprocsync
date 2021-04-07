class ProcSyncError(BaseException):
    """
    Base class for all exceptions in PyProcSync.
    """
    pass


class TooLateError(ProcSyncError):
    """
    This exception is raised when the announced continue time is already passed.
    That could be caused by high network latency or unsynchronized system clocks between nodes.
    """
    pass


class TimeOutError(ProcSyncError):
    """
    This exception is raised
    """
    pass
