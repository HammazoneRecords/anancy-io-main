# API Reference - Hacker CSI Research Agent v2.0

## HackerCSIResearchAgent

### Methods

#### `analyze_pipeline(pipeline_config, analysis_mode, context=None)`

Perform comprehensive CSI analysis on a pipeline.

**Parameters:**
- `pipeline_config` (dict): Pipeline configuration to analyze
- `analysis_mode` (AnalysisMode): Type of analysis to perform
- `context` (dict, optional): Additional context for analysis

**Returns:** `CSIReport` object with complete analysis results

**Example:**
```python
report = csi_agent.analyze_pipeline(config, AnalysisMode.FULL_SYSTEM)
print(f"Risk: {report.suitability_risk_score.risk_level}")
```

#### `get_analysis_history()`

Get list of all previous analysis reports.

**Returns:** List of `CSIReport` objects

#### `get_report_by_id(report_id)`

Retrieve specific report by ID.

**Parameters:**
- `report_id` (str): Report identifier

**Returns:** `CSIReport` object or None

#### `export_analysis_summary()`

Export comprehensive analysis summary to file.

**Returns:** Path to exported summary file

## ScenarioEngine

### Methods

#### `generate_scenario_pack(pipeline_config, analysis_mode, risk_score)`

Generate 16 attack scenarios for a pipeline.

**Parameters:**
- `pipeline_config` (dict): Pipeline configuration
- `analysis_mode` (AnalysisMode): Analysis mode
- `risk_score` (float): Overall risk score

**Returns:** List of `AttackScenario` objects

#### `get_scenario_by_vector(attack_vector)`

Get base scenarios for specific attack vector.

**Parameters:**
- `attack_vector` (AttackVector): Attack vector type

**Returns:** List of scenario dictionaries

## RiskScorer

### Methods

#### `calculate_suitability_score(pipeline_config, analysis_mode, context)`

Calculate comprehensive risk score.

**Parameters:**
- `pipeline_config` (dict): Pipeline configuration
- `analysis_mode` (AnalysisMode): Analysis mode
- `context` (dict): Additional context

**Returns:** `SuitabilityRiskScore` object

#### `add_custom_risk_factor(factor_name, weight, factors)`

Add custom risk factor to evaluation.

**Parameters:**
- `factor_name` (str): Factor name
- `weight` (float): Factor weight (0-1)
- `factors` (dict): Factor configuration

#### `get_risk_trends(historical_scores)`

Analyze risk trends from historical data.

**Parameters:**
- `historical_scores` (list): List of `SuitabilityRiskScore` objects

**Returns:** Dictionary with trend analysis

## GovernanceGapAnalyzer

### Methods

#### `analyze_gaps(pipeline_config, analysis_mode)`

Identify governance gaps in pipeline.

**Parameters:**
- `pipeline_config` (dict): Pipeline configuration
- `analysis_mode` (AnalysisMode): Analysis mode

**Returns:** List of `GovernanceGap` objects

#### `add_custom_gap_pattern(gap_key, pattern)`

Add custom governance gap pattern.

**Parameters:**
- `gap_key` (str): Gap identifier
- `pattern` (dict): Gap pattern configuration

## ResearchGapsRegister

### Methods

#### `identify_gaps(pipeline_config, attack_scenarios, governance_gaps)`

Identify research gaps from analysis.

**Parameters:**
- `pipeline_config` (dict): Pipeline configuration
- `attack_scenarios` (list): Generated attack scenarios
- `governance_gaps` (list): Identified governance gaps

**Returns:** List of `ResearchGap` objects

#### `get_gaps_by_priority(priority)`

Get research gaps by priority level.

**Parameters:**
- `priority` (ResearchPriority): Priority level

**Returns:** List of `ResearchGap` objects

#### `export_gaps_register()`

Export complete research gaps register.

**Returns:** Path to exported register file

## Data Classes

### CSIReport

- `report_id`: Unique report identifier
- `timestamp`: Analysis timestamp
- `analysis_mode`: Analysis mode used
- `target_pipeline`: Pipeline name
- `suitability_risk_score`: Risk score object
- `governance_gaps`: List of governance gaps
- `attack_scenarios`: List of attack scenarios
- `research_gaps`: List of research gaps
- `executive_summary`: Analysis summary
- `recommendations`: List of recommendations
- `confidence_level`: Analysis confidence (0-1)

### SuitabilityRiskScore

- `overall_score`: Overall risk score (0-1)
- `breakdown`: Dictionary of factor scores
- `risk_level`: Risk level (LOW/MEDIUM/HIGH/CRITICAL)
- `confidence`: Scoring confidence (0-1)
- `assessment_factors`: Additional assessment data

### AttackScenario

- `scenario_id`: Unique scenario identifier
- `title`: Scenario title
- `description`: Detailed description
- `attack_vector`: Attack vector type
- `complexity`: Complexity level
- `prerequisites`: Required conditions
- `execution_steps`: Step-by-step execution
- `impact_assessment`: Impact evaluation
- `detection_difficulty`: Detection difficulty (0-1)
- `mitigation_strategies`: Mitigation approaches
- `success_probability`: Success probability (0-1)
- `timeline_estimate`: Estimated timeline

### GovernanceGap

- `gap_id`: Unique gap identifier
- `title`: Gap title
- `description`: Gap description
- `category`: Gap category
- `severity`: Gap severity
- `affected_components`: Affected components
- `root_cause`: Root cause analysis
- `impact_assessment`: Impact evaluation
- `remediation_steps`: Remediation steps
- `detection_method`: Detection method
- `compliance_implication`: Compliance impact

### ResearchGap

- `gap_id`: Unique gap identifier
- `title`: Research gap title
- `description`: Gap description
- `category`: Research category
- `priority`: Research priority
- `related_scenarios`: Related attack scenarios
- `knowledge_gap`: Knowledge gap description
- `potential_impact`: Potential impact
- `research_questions`: Research questions
- `proposed_methodology`: Proposed research method
- `estimated_effort`: Estimated effort
- `dependencies`: Research dependencies

## Enums

### AnalysisMode
- `CCF_PIPELINE`
- `MW_PL_PIPELINE`
- `HYBRID_ANALYSIS`
- `FULL_SYSTEM`

### AttackVector
- `PROMPT_INJECTION`
- `DATA_POISONING`
- `MODEL_INVERSION`
- `BACKDOOR_EXPLOIT`
- `GOVERNANCE_BYPASS`
- `SUPPLY_CHAIN_ATTACK`
- `INSIDER_THREAT`
- `ADVERSARIAL_INPUT`
- `RESOURCE_EXHAUSTION`
- `PRIVILEGE_ESCALATION`
- `INFORMATION_DISCLOSURE`
- `DENIAL_OF_SERVICE`
- `SESSION_HIJACKING`
- `MAN_IN_THE_MIDDLE`
- `SOCIAL_ENGINEERING`
- `ZERO_DAY_EXPLOIT`

### RiskLevel
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

### GapSeverity
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

### ResearchPriority
- `LOW`
- `MEDIUM`
- `HIGH`
- `CRITICAL`

### ResearchCategory
- `TECHNICAL_VULNERABILITIES`
- `ATTACK_VECTORS`
- `DEFENSE_MECHANISMS`
- `COMPLIANCE_FRAMEWORKS`
- `RISK_MODELS`
- `INCIDENT_ANALYSIS`
- `THREAT_INTELLIGENCE`
- `EMERGING_TECHNOLOGIES`
