"""PromptSmith - Prompt Suitability Agent

A governance layer that translates raw user requests into MW-PS compliant prompts,
preserving user authority and preventing unintended execution.
"""

from .agent import PromptSmith
from .workflow import PromptSmithWorkflow, WorkflowState
from .exceptions import PromptSmithError, WorkflowError

__version__ = '1.0.0'
__all__ = [
    'PromptSmith',
    'PromptSmithWorkflow',
    'WorkflowState',
    'PromptSmithError',
    'WorkflowError',
]
