"""MW-PS Exception Classes"""

class MWPSValidationError(Exception):
    """Base exception for MW-PS validation errors."""
    pass

class MWPSParityError(MWPSValidationError):
    """Raised when Intent-Instruction Parity is violated."""
    pass

class MWPSMissingLayerError(MWPSValidationError):
    """Raised when a mandatory layer is missing."""
    pass

class MWPSTerminationError(MWPSValidationError):
    """Raised when termination conditions are not properly defined."""
    pass
