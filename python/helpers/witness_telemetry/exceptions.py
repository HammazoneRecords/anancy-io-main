"""
Witness Telemetry Exception Classes

Custom exceptions for Witness Telemetry Subsystem operations.
"""

class WitnessTelemetryException(Exception):
    """Base exception for Witness Telemetry errors."""
    pass

class EventNotFoundError(WitnessTelemetryException):
    """Raised when a requested telemetry event cannot be found."""
    pass

class SignatureVerificationError(WitnessTelemetryException):
    """Raised when event signature verification fails."""
    pass

class EventHandlerError(WitnessTelemetryException):
    """Raised when an event handler fails to execute."""
    pass

class ExportError(WitnessTelemetryException):
    """Raised when event export fails."""
    pass

class QueryError(WitnessTelemetryException):
    """Raised when a telemetry query fails."""
    pass
