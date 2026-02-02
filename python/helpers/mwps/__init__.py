"""MindWave Prompt Standard (MW-PS) v1.0

A structured framework for issuing prompts to AI systems to prevent
misalignment and errors through explicit governance.
"""

from .core import MWPSPrompt, MWPSValidator, MWPSLayer
from .exceptions import (
    MWPSValidationError,
    MWPSParityError,
    MWPSMissingLayerError,
    MWPSTerminationError
)
from .templates import MWPSTemplate

__version__ = '1.0.0'
__all__ = [
    'MWPSPrompt',
    'MWPSValidator',
    'MWPSLayer',
    'MWPSTemplate',
    'MWPSValidationError',
    'MWPSParityError',
    'MWPSMissingLayerError',
    'MWPSTerminationError',
]
