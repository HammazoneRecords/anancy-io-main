"""
9-State Lifecycle Exception Classes

Custom exceptions for Lifecycle Architecture operations.
"""

class LifecycleException(Exception):
    """Base exception for Lifecycle Architecture errors."""
    pass

class InvalidStateTransitionError(LifecycleException):
    """Raised when attempting an invalid state transition."""
    pass

class StateHandlerError(LifecycleException):
    """Raised when a state handler fails to execute."""
    pass

class ContextNotFoundError(LifecycleException):
    """Raised when lifecycle context is not available."""
    pass

class RecoveryTriggerError(LifecycleException):
    """Raised when recovery cannot be triggered."""
    pass

class LifecycleResetError(LifecycleException):
    """Raised when lifecycle reset fails."""
    pass
