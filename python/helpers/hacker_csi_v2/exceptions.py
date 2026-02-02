# Custom Exceptions for Hacker CSI Research Agent v2.0

"""
Custom exception classes for the Hacker CSI Research Agent.

These exceptions provide specific error handling for different failure modes
in the CSI analysis pipeline.
"""

from typing import Optional, Dict, Any


class CSIError(Exception):
    """Base exception for CSI-related errors."""

    def __init__(self, message: str, error_code: Optional[str] = None, 
                 context: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.error_code = error_code or 'CSI_ERROR'
        self.context = context or {}
        self.timestamp = None  # Will be set when raised

    def __str__(self):
        context_str = f" (Context: {self.context})" if self.context else ""
        return f"[{self.error_code}] {super().__str__()}{context_str}"


class ScenarioError(CSIError):
    """Exception raised for scenario generation errors."""

    def __init__(self, message: str, scenario_type: Optional[str] = None, 
                 pipeline_config: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            error_code='SCENARIO_ERROR',
            context={
                'scenario_type': scenario_type,
                'pipeline_info': pipeline_config
            }
        )


class AnalysisError(CSIError):
    """Exception raised for analysis processing errors."""

    def __init__(self, message: str, analysis_stage: Optional[str] = None, 
                 partial_results: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            error_code='ANALYSIS_ERROR',
            context={
                'analysis_stage': analysis_stage,
                'has_partial_results': partial_results is not None
            }
        )
        self.partial_results = partial_results


class RiskScoringError(CSIError):
    """Exception raised for risk scoring calculation errors."""

    def __init__(self, message: str, factor_name: Optional[str] = None, 
                 config_data: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            error_code='RISK_SCORING_ERROR',
            context={
                'factor_name': factor_name,
                'config_keys': list(config_data.keys()) if config_data else None
            }
        )


class GovernanceGapError(CSIError):
    """Exception raised for governance gap analysis errors."""

    def __init__(self, message: str, gap_category: Optional[str] = None, 
                 affected_components: Optional[list] = None):
        super().__init__(
            message,
            error_code='GOVERNANCE_GAP_ERROR',
            context={
                'gap_category': gap_category,
                'affected_components': affected_components
            }
        )


class ResearchGapError(CSIError):
    """Exception raised for research gap identification errors."""

    def __init__(self, message: str, gap_type: Optional[str] = None, 
                 research_context: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            error_code='RESEARCH_GAP_ERROR',
            context={
                'gap_type': gap_type,
                'research_context': research_context
            }
        )


class ConfigurationError(CSIError):
    """Exception raised for configuration-related errors."""

    def __init__(self, message: str, config_section: Optional[str] = None, 
                 missing_keys: Optional[list] = None):
        super().__init__(
            message,
            error_code='CONFIGURATION_ERROR',
            context={
                'config_section': config_section,
                'missing_keys': missing_keys
            }
        )


class ValidationError(CSIError):
    """Exception raised for data validation errors."""

    def __init__(self, message: str, field_name: Optional[str] = None, 
                 invalid_value: Optional[Any] = None):
        super().__init__(
            message,
            error_code='VALIDATION_ERROR',
            context={
                'field_name': field_name,
                'invalid_value_type': type(invalid_value).__name__ if invalid_value is not None else None
            }
        )


class IntegrationError(CSIError):
    """Exception raised for integration-related errors."""

    def __init__(self, message: str, integration_target: Optional[str] = None, 
                 connection_details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message,
            error_code='INTEGRATION_ERROR',
            context={
                'integration_target': integration_target,
                'connection_status': connection_details
            }
        )


# Exception hierarchy for easy catching
def get_exception_hierarchy():
    """Get the exception hierarchy for documentation."""
    return {
        'CSIError': {
            'ScenarioError': None,
            'AnalysisError': None,
            'RiskScoringError': None,
            'GovernanceGapError': None,
            'ResearchGapError': None,
            'ConfigurationError': None,
            'ValidationError': None,
            'IntegrationError': None
        }
    }


def create_error_report(exception: CSIError) -> Dict[str, Any]:
    """Create a detailed error report from a CSI exception."""
    import traceback
    import sys

    return {
        'error_type': type(exception).__name__,
        'error_code': exception.error_code,
        'message': str(exception),
        'context': exception.context,
        'traceback': traceback.format_exc(),
        'python_version': sys.version,
        'timestamp': None  # Would be set by calling code
    }
