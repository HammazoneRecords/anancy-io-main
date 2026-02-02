# Hacker CSI Research Agent v2.0

"""
Predictive Adversarial Analyst for CCF and MW-PL Pipeline Security.

This module simulates attacker strategies against governance pipelines,
generating comprehensive security analysis and risk assessments.
"""

from .csi_agent import HackerCSIResearchAgent
from .scenario_engine import ScenarioEngine, AttackScenario
from .risk_scorer import RiskScorer, SuitabilityRiskScore
from .governance_analyzer import GovernanceGapAnalyzer, GovernanceGap
from .research_register import ResearchGapsRegister, ResearchGap
from .exceptions import CSIError, ScenarioError, AnalysisError

__version__ = "2.0.0"
__all__ = [
    "HackerCSIResearchAgent",
    "ScenarioEngine",
    "AttackScenario",
    "RiskScorer",
    "SuitabilityRiskScore",
    "GovernanceGapAnalyzer",
    "GovernanceGap",
    "ResearchGapsRegister",
    "ResearchGap",
    "CSIError",
    "ScenarioError",
    "AnalysisError"
]
