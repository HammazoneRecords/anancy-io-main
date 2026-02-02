"""MW-SHA - System Health Agent

Pre-classification health check gate for AnancyIO governance.
"""

from .agent import MWSystemHealthAgent, HealthStatus, HealthCheckResult
from .exceptions import MWHealthError, MWHealthWarning
from .checks import SystemChecks

__version__ = '1.0.0'
__all__ = [
    'MWSystemHealthAgent',
    'HealthStatus',
    'HealthCheckResult',
    'MWHealthError',
    'MWHealthWarning',
    'SystemChecks',
]
