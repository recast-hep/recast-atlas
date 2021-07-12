class FailedRunException(Exception):
    """
    raised when an a run has not succeeded
    """

class BackendNotAvailableException(Exception):
    """
    raise when a Backend is ill-configured
    """