"""MW-SHA Exception Classes"""

class MWHealthError(Exception):
    """Raised when system health check fails critically."""
    pass

class MWHealthWarning(Exception):
    """Raised when system health check detects warnings."""
    pass
