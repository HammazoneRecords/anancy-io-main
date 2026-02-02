"""
TCP/TCPC Exception Classes

Custom exceptions for Trajectory Checkpoint Protocol and Controller operations.
"""

class TCPException(Exception):
    """Base exception for Trajectory Checkpoint Protocol errors."""
    pass

class TCPCException(Exception):
    """Base exception for Trajectory Checkpoint Controller errors."""
    pass

class CheckpointNotFoundError(TCPException):
    """Raised when a requested checkpoint cannot be found."""
    pass

class CheckpointVerificationError(TCPException):
    """Raised when checkpoint verification fails."""
    pass

class ProtocolOfReturnError(TCPCException):
    """Raised when Protocol of Return execution fails."""
    pass

class ComplianceHookError(TCPCException):
    """Raised when a compliance hook fails."""
    pass

class RecoveryHandlerError(TCPCException):
    """Raised when a recovery handler fails."""
    pass

class TrajectoryValidationError(TCPCException):
    """Raised when trajectory validation fails."""
    pass
