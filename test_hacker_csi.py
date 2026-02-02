from python.helpers.hacker_csi_v2.csi_agent import HackerCSIResearchAgent, AnalysisMode
from python.helpers.hacker_csi_v2.scenario_engine import ScenarioEngine
from python.helpers.hacker_csi_v2.risk_scorer import RiskScorer
from python.helpers.hacker_csi_v2.governance_analyzer import GovernanceGapAnalyzer
from python.helpers.hacker_csi_v2.research_register import ResearchGapsRegister
from python.helpers.hacker_csi_v2.exceptions import CSIError
from python.helpers.hacker_csi_v2.examples import EXAMPLE_PIPELINES

print('=== Testing Hacker CSI v2.0 Implementation ===')

try:
    # Test basic imports
    print('✅ All imports successful')
    
    # Test CSI agent initialization
    csi_agent = HackerCSIResearchAgent()
    print('✅ CSI Agent initialized')
    
    # Test scenario engine
    scenario_engine = ScenarioEngine()
    print('✅ Scenario Engine initialized')
    
    # Test risk scorer
    risk_scorer = RiskScorer()
    print('✅ Risk Scorer initialized')
    
    # Test governance analyzer
    gov_analyzer = GovernanceGapAnalyzer()
    print('✅ Governance Analyzer initialized')
    
    # Test research register
    research_register = ResearchGapsRegister()
    print('✅ Research Register initialized')
    
    # Test basic analysis
    pipeline_config = EXAMPLE_PIPELINES['basic_ml_pipeline']
    report = csi_agent.analyze_pipeline(
        pipeline_config=pipeline_config,
        analysis_mode=AnalysisMode.CCF_PIPELINE
    )
    print('✅ Basic analysis completed')
    print(f'   Report ID: {report.report_id[:8]}...')
    print(f'   Risk Level: {report.suitability_risk_score.risk_level}')
    print(f'   Scenarios: {len(report.attack_scenarios)}')
    print(f'   Gaps: {len(report.governance_gaps)}')
    print(f'   Research Gaps: {len(report.research_gaps)}')
    
    # Test comprehensive analysis
    full_report = csi_agent.analyze_pipeline(
        pipeline_config=EXAMPLE_PIPELINES['secure_enterprise_pipeline'],
        analysis_mode=AnalysisMode.FULL_SYSTEM
    )
    print('✅ Full system analysis completed')
    print(f'   Risk Level: {full_report.suitability_risk_score.risk_level}')
    print(f'   Confidence: {full_report.confidence_level:.2f}')
    
    # Test scenario generation
    scenarios = scenario_engine.generate_scenario_pack(
        pipeline_config=pipeline_config,
        analysis_mode=AnalysisMode.FULL_SYSTEM,
        risk_score=0.7
    )
    print(f'✅ Generated {len(scenarios)} attack scenarios')
    
    # Test risk scoring
    score = risk_scorer.calculate_suitability_score(
        pipeline_config=pipeline_config,
        analysis_mode=AnalysisMode.FULL_SYSTEM,
        context={}
    )
    print(f'✅ Risk score calculated: {score.overall_score:.2f} ({score.risk_level})')
    
    # Test governance analysis
    gaps = gov_analyzer.analyze_gaps(pipeline_config, AnalysisMode.FULL_SYSTEM)
    print(f'✅ Identified {len(gaps)} governance gaps')
    
    # Test research gaps
    research_gaps = research_register.identify_gaps(pipeline_config, scenarios, gaps)
    print(f'✅ Identified {len(research_gaps)} research gaps')
    
    # Test history and export
    history = csi_agent.get_analysis_history()
    print(f'✅ Analysis history: {len(history)} reports')
    
    summary_file = csi_agent.export_analysis_summary()
    print(f'✅ Summary exported: {summary_file}')
    
    print('\n🎉 All tests passed! Hacker CSI v2.0 is fully functional.')
    
except Exception as e:
    print(f'❌ Test failed: {e}')
    import traceback
    traceback.print_exc()
