"""
SAFE_INFO Fast Path Exception Classes

Custom exceptions for Fast Path operations.
"""

class FastPathException(Exception):
    """Base exception for Fast Path errors."""
    pass

class FastPathEligibilityError(FastPathException):
    """Raised when a query is not eligible for fast path."""
    pass

class FastPathExecutionError(FastPathException):
    """Raised when fast path execution fails."""
    pass

class FastPathValidationError(FastPathException):
    """Raised when fast path validation fails."""
    pass

class FastPathIntegrityError(FastPathException):
    """Raised when fast path integrity check fails."""
    pass
