# Hacker CSI Research Agent v2.0

"""
Main implementation of the Hacker CSI Research Agent.

This agent simulates adversarial strategies against CCF and MW-PL pipelines,
generating predictive security analysis and comprehensive risk assessments.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum


from .scenario_engine import ScenarioEngine, AttackScenario
from .risk_scorer import RiskScorer, SuitabilityRiskScore
from .governance_analyzer import GovernanceGapAnalyzer, GovernanceGap
from .research_register import ResearchGapsRegister, ResearchGap


class AnalysisMode(Enum):
    """Analysis modes for different pipeline types."""
    CCF_PIPELINE = "ccf_pipeline"
    MW_PL_PIPELINE = "mw_pl_pipeline"
    HYBRID_ANALYSIS = "hybrid_analysis"
    FULL_SYSTEM = "full_system"


@dataclass
class CSIReport:
    """Comprehensive CSI analysis report."""
    report_id: str
    timestamp: datetime
    analysis_mode: AnalysisMode
    target_pipeline: str
    suitability_risk_score: SuitabilityRiskScore
    governance_gaps: List[GovernanceGap]
    attack_scenarios: List[AttackScenario]
    research_gaps: List[ResearchGap]
    executive_summary: str
    recommendations: List[str]
    confidence_level: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['analysis_mode'] = self.analysis_mode.value
        data['timestamp'] = self.timestamp.isoformat()
        data['suitability_risk_score'] = self.suitability_risk_score.to_dict()
        data['governance_gaps'] = [gap.to_dict() for gap in self.governance_gaps]
        data['attack_scenarios'] = [scenario.to_dict() for scenario in self.attack_scenarios]
        data['research_gaps'] = [gap.to_dict() for gap in self.research_gaps]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CSIReport':
        """Create from dictionary."""
        data_copy = data.copy()
        data_copy['analysis_mode'] = AnalysisMode(data_copy['analysis_mode'])
        data_copy['timestamp'] = datetime.fromisoformat(data_copy['timestamp'])
        data_copy['suitability_risk_score'] = SuitabilityRiskScore.from_dict(data_copy['suitability_risk_score'])
        data_copy['governance_gaps'] = [GovernanceGap.from_dict(gap) for gap in data_copy['governance_gaps']]
        data_copy['attack_scenarios'] = [AttackScenario.from_dict(scenario) for scenario in data_copy['attack_scenarios']]
        data_copy['research_gaps'] = [ResearchGap.from_dict(gap) for gap in data_copy['research_gaps']]
        return cls(**data_copy)


class HackerCSIResearchAgent:
    """Main CSI Research Agent for predictive adversarial analysis."""

    def __init__(self, reports_dir: Optional[Path] = None):
        """Initialize CSI Research Agent.

        Args:
            reports_dir: Directory for storing analysis reports
        """
        self.reports_dir = reports_dir or Path('./csi_reports')
        self.reports_dir.mkdir(exist_ok=True)

        # Initialize components
        self.scenario_engine = ScenarioEngine()
        self.risk_scorer = RiskScorer()
        self.governance_analyzer = GovernanceGapAnalyzer()
        self.research_register = ResearchGapsRegister()

        # Analysis history
        self.analysis_history: List[CSIReport] = []

    def analyze_pipeline(self, pipeline_config: Dict[str, Any], 
                        analysis_mode: AnalysisMode = AnalysisMode.FULL_SYSTEM,
                        context: Optional[Dict[str, Any]] = None) -> CSIReport:
        """Perform comprehensive CSI analysis on a pipeline.

        Args:
            pipeline_config: Configuration of the pipeline to analyze
            analysis_mode: Type of analysis to perform
            context: Additional context for analysis

        Returns:
            Comprehensive CSI analysis report
        """
        try:
            # Generate report ID
            report_id = self._generate_report_id(pipeline_config)

            # Extract pipeline information
            pipeline_name = pipeline_config.get('name', 'unknown_pipeline')

            # Perform suitability risk scoring
            risk_score = self.risk_scorer.calculate_suitability_score(
                pipeline_config, analysis_mode, context or {}
            )

            # Analyze governance gaps
            governance_gaps = self.governance_analyzer.analyze_gaps(
                pipeline_config, analysis_mode
            )

            # Generate attack scenarios
            attack_scenarios = self.scenario_engine.generate_scenario_pack(
                pipeline_config, analysis_mode, risk_score.overall_score
            )

            # Identify research gaps
            research_gaps = self.research_register.identify_gaps(
                pipeline_config, attack_scenarios, governance_gaps
            )

            # Generate executive summary
            executive_summary = self._generate_executive_summary(
                risk_score, governance_gaps, attack_scenarios
            )

            # Generate recommendations
            recommendations = self._generate_recommendations(
                risk_score, governance_gaps, research_gaps
            )

            # Calculate confidence level
            confidence_level = self._calculate_confidence_level(
                risk_score, len(attack_scenarios), len(governance_gaps)
            )

            # Create report
            report = CSIReport(
                report_id=report_id,
                timestamp=datetime.now(),
                analysis_mode=analysis_mode,
                target_pipeline=pipeline_name,
                suitability_risk_score=risk_score,
                governance_gaps=governance_gaps,
                attack_scenarios=attack_scenarios,
                research_gaps=research_gaps,
                executive_summary=executive_summary,
                recommendations=recommendations,
                confidence_level=confidence_level
            )

            # Store in history
            self.analysis_history.append(report)

            # Save report
            self._save_report(report)

            return report

        except Exception as e:
            # Create error report
            error_report = CSIReport(
                report_id=self._generate_report_id({'error': str(e)}),
                timestamp=datetime.now(),
                analysis_mode=analysis_mode,
                target_pipeline=pipeline_config.get('name', 'error_pipeline'),
                suitability_risk_score=SuitabilityRiskScore(
                    overall_score=1.0,
                    breakdown={'error': 1.0},
                    risk_level='CRITICAL',
                    confidence=0.0
                ),
                governance_gaps=[],
                attack_scenarios=[],
                research_gaps=[],
                executive_summary=f"Analysis failed: {str(e)}",
                recommendations=["Investigate analysis failure", "Check pipeline configuration"],
                confidence_level=0.0
            )

            self.analysis_history.append(error_report)
            return error_report

    def _generate_report_id(self, config: Dict[str, Any]) -> str:
        """Generate unique report identifier."""
        content = json.dumps(config, sort_keys=True) + str(datetime.now().isoformat())
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _generate_executive_summary(self, risk_score: SuitabilityRiskScore, 
                                   gaps: List[GovernanceGap], 
                                   scenarios: List[AttackScenario]) -> str:
        """Generate executive summary of analysis."""
        risk_level = risk_score.risk_level
        gap_count = len(gaps)
        scenario_count = len(scenarios)

        summary = f"""CSI Analysis Summary:

Risk Level: {risk_level}
Suitability Score: {risk_score.overall_score:.2f}
Governance Gaps Identified: {gap_count}
Attack Scenarios Generated: {scenario_count}

Key Findings:
"""

        if risk_score.overall_score > 0.7:
            summary += "- High risk of adversarial exploitation"
"
        if gap_count > 5:
            summary += "- Significant governance gaps detected
"
        if scenario_count >= 16:
            summary += "- Comprehensive scenario coverage achieved
"

        return summary

    def _generate_recommendations(self, risk_score: SuitabilityRiskScore,
                                 gaps: List[GovernanceGap], 
                                 research_gaps: List[ResearchGap]) -> List[str]:
        """Generate security recommendations."""
        recommendations = []

        if risk_score.overall_score > 0.8:
            recommendations.append("Immediate security review required")

        if gaps:
            recommendations.append(f"Address {len(gaps)} identified governance gaps")

        if research_gaps:
            recommendations.append(f"Investigate {len(research_gaps)} research gaps")

        recommendations.extend([
            "Implement continuous monitoring",
            "Regular security assessments",
            "Update governance protocols"
        ])

        return recommendations

    def _calculate_confidence_level(self, risk_score: SuitabilityRiskScore, 
                                   scenario_count: int, gap_count: int) -> float:
        """Calculate analysis confidence level."""
        # Base confidence from risk score confidence
        confidence = risk_score.confidence

        # Adjust based on analysis completeness
        if scenario_count >= 16:
            confidence += 0.1
        if gap_count > 0:
            confidence += 0.05

        return min(confidence, 1.0)

    def _save_report(self, report: CSIReport):
        """Save report to file."""
        report_file = self.reports_dir / f'csi_report_{report.report_id}.json'

        with open(report_file, 'w') as f:
            json.dump(report.to_dict(), f, indent=2, default=str)

    def get_analysis_history(self) -> List[CSIReport]:
        """Get analysis history."""
        return self.analysis_history.copy()

    def get_report_by_id(self, report_id: str) -> Optional[CSIReport]:
        """Get specific report by ID."""
        for report in self.analysis_history:
            if report.report_id == report_id:
                return report
        return None

    def export_analysis_summary(self) -> str:
        """Export comprehensive analysis summary."""
        summary = {
            'timestamp': datetime.now().isoformat(),
            'total_analyses': len(self.analysis_history),
            'risk_distribution': {},
            'gaps_distribution': {},
            'scenarios_distribution': {},
            'reports': [report.to_dict() for report in self.analysis_history[-5:]]  # Last 5 reports
        }

        # Calculate distributions
        for report in self.analysis_history:
            risk_level = report.suitability_risk_score.risk_level
            gap_count = len(report.governance_gaps)
            scenario_count = len(report.attack_scenarios)

            summary['risk_distribution'][risk_level] = summary['risk_distribution'].get(risk_level, 0) + 1
            summary['gaps_distribution'][str(gap_count)] = summary['gaps_distribution'].get(str(gap_count), 0) + 1
            summary['scenarios_distribution'][str(scenario_count)] = summary['scenarios_distribution'].get(str(scenario_count), 0) + 1

        # Save summary
        summary_file = self.reports_dir / f'csi_analysis_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        return str(summary_file)
