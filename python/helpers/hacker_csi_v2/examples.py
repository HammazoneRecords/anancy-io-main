# Usage Examples for Hacker CSI Research Agent v2.0

"""
Practical examples demonstrating the usage of the Hacker CSI Research Agent.

These examples show how to perform comprehensive adversarial analysis on
CCF and MW-PL pipelines using the CSI framework.
"""

from pathlib import Path
from typing import Dict, Any
from ..csi_agent import HackerCSIResearchAgent, AnalysisMode
from ..scenario_engine import AttackVector
from ..risk_scorer import RiskScorer
from ..governance_analyzer import GovernanceGapAnalyzer
from ..research_register import ResearchGapsRegister


# Example pipeline configurations
EXAMPLE_PIPELINES = {
    'basic_ml_pipeline': {
        'name': 'Basic ML Pipeline',
        'type': 'machine_learning',
        'authentication': {
            'multi_factor': False,
            'weak_passwords': True
        },
        'monitoring': {
            'comprehensive_logging': False
        },
        'governance': {
            'automated_controls': False,
            'manual_only': True
        },
        'uses_ml': True,
        'adversarial_training': False,
        'components': ['model_training', 'inference_api']
    },
    'secure_enterprise_pipeline': {
        'name': 'Secure Enterprise Pipeline',
        'type': 'enterprise_ai',
        'authentication': {
            'multi_factor': True,
            'role_based': True
        },
        'monitoring': {
            'comprehensive_logging': True
        },
        'governance': {
            'automated_controls': True,
            'manual_only': False
        },
        'data_protection': {
            'encryption_at_rest': True,
            'encryption_in_transit': True
        },
        'compliance': {
            'automated_monitoring': True
        },
        'uses_ml': True,
        'adversarial_training': True,
        'components': ['secure_training', 'audited_inference', 'compliance_monitor']
    },
    'edge_ai_system': {
        'name': 'Edge AI System',
        'type': 'edge_ai',
        'authentication': {
            'multi_factor': False
        },
        'infrastructure': {
            'isolated_networks': False,
            'public_exposure': True
        },
        'supply_chain': {
            'verified_dependencies': False,
            'untrusted_sources': True
        },
        'user_interface': True,
        'third_party_dependencies': True,
        'components': ['edge_devices', 'local_inference', 'cloud_sync']
    }
}


def basic_csi_analysis():
    """Basic example of performing CSI analysis on a pipeline."""
    print('=== Basic CSI Analysis Example ===')

    # Initialize CSI agent
    csi_agent = HackerCSIResearchAgent()

    # Get example pipeline
    pipeline_config = EXAMPLE_PIPELINES['basic_ml_pipeline']

    # Perform analysis
    report = csi_agent.analyze_pipeline(
        pipeline_config=pipeline_config,
        analysis_mode=AnalysisMode.CCF_PIPELINE
    )

    # Display results
    print(f'Pipeline: {report.target_pipeline}')
    print(f'Risk Level: {report.suitability_risk_score.risk_level}')
    print(f'Overall Score: {report.suitability_risk_score.overall_score:.2f}')
    print(f'Governance Gaps: {len(report.governance_gaps)}')
    print(f'Attack Scenarios: {len(report.attack_scenarios)}')
    print(f'Research Gaps: {len(report.research_gaps)}')
    print(f'Confidence: {report.confidence_level:.2f}')

    print('
Executive Summary:')
    print(report.executive_summary)

    print('
Recommendations:')
    for rec in report.recommendations:
        print(f'- {rec}')

    return report


def comprehensive_system_analysis():
    """Example of comprehensive system-wide analysis."""
    print('
=== Comprehensive System Analysis Example ===')

    # Initialize CSI agent with custom reports directory
    reports_dir = Path('./example_reports')
    csi_agent = HackerCSIResearchAgent(reports_dir=reports_dir)

    # Analyze multiple pipelines
    results = {}
    for pipeline_name, config in EXAMPLE_PIPELINES.items():
        print(f'
Analyzing {pipeline_name}...')

        report = csi_agent.analyze_pipeline(
            pipeline_config=config,
            analysis_mode=AnalysisMode.FULL_SYSTEM,
            context={'analysis_priority': 'comprehensive'}
        )

        results[pipeline_name] = {
            'risk_level': report.suitability_risk_score.risk_level,
            'score': report.suitability_risk_score.overall_score,
            'gaps': len(report.governance_gaps),
            'scenarios': len(report.attack_scenarios),
            'confidence': report.confidence_level
        }

        print(f'  Risk: {results[pipeline_name]["risk_level"]} ({results[pipeline_name]["score"]:.2f})')
        print(f'  Gaps: {results[pipeline_name]["gaps"]}, Scenarios: {results[pipeline_name]["scenarios"]}')

    # Generate summary report
    summary_file = csi_agent.export_analysis_summary()
    print(f'
Summary report saved: {summary_file}')

    return results


def scenario_engine_demo():
    """Demonstrate scenario engine capabilities."""
    print('
=== Scenario Engine Demo ===')

    from ..scenario_engine import ScenarioEngine, AttackVector

    engine = ScenarioEngine()

    # Generate scenarios for edge AI system
    pipeline_config = EXAMPLE_PIPELINES['edge_ai_system']
    scenarios = engine.generate_scenario_pack(
        pipeline_config=pipeline_config,
        analysis_mode=AnalysisMode.FULL_SYSTEM,
        risk_score=0.7
    )

    print(f'Generated {len(scenarios)} attack scenarios')

    # Display first few scenarios
    for i, scenario in enumerate(scenarios[:5]):
        print(f'
{i+1}. {scenario.title}')
        print(f'   Vector: {scenario.attack_vector.value}')
        print(f'   Complexity: {scenario.complexity.value}')
        print(f'   Success Probability: {scenario.success_probability:.2f}')
        print(f'   Detection Difficulty: {scenario.detection_difficulty:.2f}')

    # Show scenarios by vector
    injection_scenarios = engine.get_scenario_by_vector(AttackVector.PROMPT_INJECTION)
    print(f'
Prompt injection scenarios available: {len(injection_scenarios)}')

    return scenarios


def risk_scorer_demo():
    """Demonstrate risk scoring capabilities."""
    print('
=== Risk Scorer Demo ===')

    from ..risk_scorer import RiskScorer

    scorer = RiskScorer()

    # Score different pipeline configurations
    for pipeline_name, config in EXAMPLE_PIPELINES.items():
        score = scorer.calculate_suitability_score(
            pipeline_config=config,
            analysis_mode=AnalysisMode.FULL_SYSTEM,
            context={}
        )

        print(f'
{pipeline_name}:')
        print(f'  Overall Score: {score.overall_score:.2f}')
        print(f'  Risk Level: {score.risk_level}')
        print(f'  Confidence: {score.confidence:.2f}')
        print(f'  Breakdown:')
        for factor, value in score.breakdown.items():
            print(f'    {factor}: {value:.2f}')

    # Add custom risk factor
    scorer.add_custom_risk_factor(
        'custom_security',
        0.1,
        {'advanced_monitoring': -0.3, 'legacy_systems': 0.4}
    )

    print('
Added custom risk factor: custom_security')

    return scorer


def governance_analysis_demo():
    """Demonstrate governance gap analysis."""
    print('
=== Governance Analysis Demo ===')

    from ..governance_analyzer import GovernanceGapAnalyzer

    analyzer = GovernanceGapAnalyzer()

    # Analyze governance gaps
    pipeline_config = EXAMPLE_PIPELINES['basic_ml_pipeline']
    gaps = analyzer.analyze_gaps(pipeline_config, AnalysisMode.CCF_PIPELINE)

    print(f'Identified {len(gaps)} governance gaps')

    # Display gaps by severity
    severity_count = {}
    for gap in gaps:
        severity = gap.severity.value
        severity_count[severity] = severity_count.get(severity, 0) + 1

        if severity == 'HIGH':
            print(f'
High Severity Gap: {gap.title}')
            print(f'  Category: {gap.category.value}')
            print(f'  Affected: {gap.affected_components}')
            print(f'  Root Cause: {gap.root_cause}')

    print(f'
Gap severity distribution: {severity_count}')

    return gaps


def research_gaps_demo():
    """Demonstrate research gap identification."""
    print('
=== Research Gaps Demo ===')

    from ..research_register import ResearchGapsRegister

    register = ResearchGapsRegister()

    # Simulate analysis inputs
    pipeline_config = EXAMPLE_PIPELINES['edge_ai_system']
    attack_scenarios = []  # Would be generated by scenario engine
    governance_gaps = []   # Would be identified by governance analyzer

    # Identify research gaps
    gaps = register.identify_gaps(pipeline_config, attack_scenarios, governance_gaps)

    print(f'Identified {len(gaps)} research gaps')

    # Display gaps by priority
    for gap in gaps:
        print(f'
{gap.title}')
        print(f'  Priority: {gap.priority.value}')
        print(f'  Category: {gap.category.value}')
        print(f'  Effort: {gap.estimated_effort}')
        print(f'  Questions: {len(gap.research_questions)}')

    # Export register
    if gaps:
        export_file = register.export_gaps_register()
        print(f'
Research gaps register exported: {export_file}')

    return gaps


def integration_with_agent0_demo():
    """Demonstrate integration with Agent0 for full reports."""
    print('
=== Integration with Agent0 Demo ===')

    # This would typically be called from within Agent0
    # Here we simulate the integration

    csi_agent = HackerCSIResearchAgent()

    # Perform analysis
    pipeline_config = EXAMPLE_PIPELINES['secure_enterprise_pipeline']
    report = csi_agent.analyze_pipeline(
        pipeline_config=pipeline_config,
        analysis_mode=AnalysisMode.FULL_SYSTEM
    )

    # Simulate report delivery to Agent0
    print('CSI Analysis Report for Agent0:')
    print(f'Report ID: {report.report_id}')
    print(f'Analysis Mode: {report.analysis_mode.value}')
    print(f'Risk Assessment: {report.suitability_risk_score.risk_level}')
    print(f'Actionable Insights: {len(report.recommendations)} recommendations')

    # In real integration, this would be sent to Agent0's response system
    print('
Report would be delivered to Agent0 for user presentation')

    return report


def run_all_examples():
    """Run all examples in sequence."""
    print('Running all Hacker CSI v2.0 Examples...
')

    try:
        # Run examples
        basic_report = basic_csi_analysis()
        comprehensive_results = comprehensive_system_analysis()
        scenarios = scenario_engine_demo()
        scorer = risk_scorer_demo()
        gaps = governance_analysis_demo()
        research_gaps = research_gaps_demo()
        integration_report = integration_with_agent0_demo()

        print('
=== All Examples Completed Successfully ===')
        print(f'Basic analysis: {basic_report.target_pipeline}')
        print(f'Comprehensive analysis: {len(comprehensive_results)} pipelines')
        print(f'Scenario generation: {len(scenarios)} scenarios')
        print(f'Risk scoring: {len(scorer.get_risk_factors())} factors')
        print(f'Governance analysis: {len(gaps)} gaps')
        print(f'Research gaps: {len(research_gaps)} gaps')
        print(f'Agent0 integration: {integration_report.report_id[:8]}...')

        return {
            'basic_report': basic_report,
            'comprehensive_results': comprehensive_results,
            'scenarios': scenarios,
            'scorer': scorer,
            'gaps': gaps,
            'research_gaps': research_gaps,
            'integration_report': integration_report
        }

    except Exception as e:
        print(f'❌ Error running examples: {e}')
        import traceback
        traceback.print_exc()
        return None


if __name__ == '__main__':
    # Run all examples when executed directly
    run_all_examples()
