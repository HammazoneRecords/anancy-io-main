"""PromptSmith Exception Classes"""

class PromptSmithError(Exception):
    """Base exception for PromptSmith errors."""
    pass

class WorkflowError(PromptSmithError):
    """Raised when workflow encounters an error."""
    pass

class ValidationError(PromptSmithError):
    """Raised when prompt validation fails."""
    pass
