# Scenario Engine for Attack Scenario Generation

"""
Scenario Engine for generating comprehensive attack scenario packs.

This module generates 16 diverse attack scenarios against CCF and MW-PL pipelines,
simulating various adversarial strategies and exploitation techniques.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class AttackVector(Enum):
    """Types of attack vectors."""
    PROMPT_INJECTION = "prompt_injection"
    DATA_POISONING = "data_poisoning"
    MODEL_INVERSION = "model_inversion"
    BACKDOOR_EXPLOIT = "backdoor_exploit"
    GOVERNANCE_BYPASS = "governance_bypass"
    SUPPLY_CHAIN_ATTACK = "supply_chain_attack"
    INSIDER_THREAT = "insider_threat"
    ADVERSARIAL_INPUT = "adversarial_input"
    RESOURCE_EXHAUSTION = "resource_exhaustion"
    PRIVILEGE_ESCALATION = "privilege_escalation"
    INFORMATION_DISCLOSURE = "information_disclosure"
    DENIAL_OF_SERVICE = "denial_of_service"
    SESSION_HIJACKING = "session_hijacking"
    MAN_IN_THE_MIDDLE = "man_in_the_middle"
    SOCIAL_ENGINEERING = "social_engineering"
    ZERO_DAY_EXPLOIT = "zero_day_exploit"


class AttackComplexity(Enum):
    """Complexity levels of attacks."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AttackScenario:
    """Individual attack scenario."""
    scenario_id: str
    title: str
    description: str
    attack_vector: AttackVector
    complexity: AttackComplexity
    prerequisites: List[str]
    execution_steps: List[str]
    impact_assessment: Dict[str, Any]
    detection_difficulty: float
    mitigation_strategies: List[str]
    success_probability: float
    timeline_estimate: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['attack_vector'] = self.attack_vector.value
        data['complexity'] = self.complexity.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AttackScenario':
        """Create from dictionary."""
        data_copy = data.copy()
        data_copy['attack_vector'] = AttackVector(data_copy['attack_vector'])
        data_copy['complexity'] = AttackComplexity(data_copy['complexity'])
        return cls(**data_copy)


class ScenarioEngine:
    """Engine for generating attack scenario packs."""

    def __init__(self):
        """Initialize scenario engine."""
        self.base_scenarios = self._load_base_scenarios()

    def _load_base_scenarios(self) -> List[Dict[str, Any]]:
        """Load base scenario templates."""
        return [
            {
                'title': 'Direct Prompt Injection',
                'attack_vector': AttackVector.PROMPT_INJECTION,
                'complexity': AttackComplexity.LOW,
                'description': 'Inject malicious prompts to bypass safety filters',
                'prerequisites': ['Access to input interface'],
                'execution_steps': [
                    'Craft malicious prompt with embedded instructions',
                    'Submit through standard input channel',
                    'Monitor for successful injection'
                ],
                'impact_assessment': {
                    'confidentiality': 'medium',
                    'integrity': 'high',
                    'availability': 'low'
                },
                'detection_difficulty': 0.3,
                'mitigation_strategies': [
                    'Input sanitization',
                    'Prompt filtering',
                    'Rate limiting'
                ],
                'success_probability': 0.6,
                'timeline_estimate': 'minutes'
            },
            {
                'title': 'Training Data Poisoning',
                'attack_vector': AttackVector.DATA_POISONING,
                'complexity': AttackComplexity.HIGH,
                'description': 'Contaminate training data to introduce backdoors',
                'prerequisites': ['Access to training pipeline', 'Data modification privileges'],
                'execution_steps': [
                    'Identify target training datasets',
                    'Insert poisoned samples with triggers',
                    'Ensure poisoned data passes validation',
                    'Monitor for backdoor activation'
                ],
                'impact_assessment': {
                    'confidentiality': 'high',
                    'integrity': 'critical',
                    'availability': 'low'
                },
                'detection_difficulty': 0.8,
                'mitigation_strategies': [
                    'Data integrity checks',
                    'Anomaly detection in training',
                    'Regular dataset audits'
                ],
                'success_probability': 0.4,
                'timeline_estimate': 'weeks'
            },
            {
                'title': 'Model Inversion Attack',
                'attack_vector': AttackVector.MODEL_INVERSION,
                'complexity': AttackVector.MEDIUM,
                'description': 'Extract sensitive training data through model queries',
                'prerequisites': ['API access to model', 'Knowledge of model architecture'],
                'execution_steps': [
                    'Send carefully crafted queries',
                    'Analyze model responses for data leakage',
                    'Reconstruct sensitive information'
                ],
                'impact_assessment': {
                    'confidentiality': 'critical',
                    'integrity': 'low',
                    'availability': 'low'
                },
                'detection_difficulty': 0.6,
                'mitigation_strategies': [
                    'Output filtering',
                    'Query rate limiting',
                    'Differential privacy'
                ],
                'success_probability': 0.5,
                'timeline_estimate': 'days'
            },
            {
                'title': 'Governance Bypass via Social Engineering',
                'attack_vector': AttackVector.SOCIAL_ENGINEERING,
                'complexity': AttackComplexity.MEDIUM,
                'description': 'Manipulate human operators to bypass governance controls',
                'prerequisites': ['Access to human operators', 'Knowledge of governance processes'],
                'execution_steps': [
                    'Identify key decision points',
                    'Craft convincing narratives',
                    'Exploit trust relationships',
                    'Execute bypass during approval process'
                ],
                'impact_assessment': {
                    'confidentiality': 'high',
                    'integrity': 'high',
                    'availability': 'medium'
                },
                'detection_difficulty': 0.7,
                'mitigation_strategies': [
                    'Operator training',
                    'Automated approval workflows',
                    'Multi-person approval requirements'
                ],
                'success_probability': 0.7,
                'timeline_estimate': 'days'
            },
            {
                'title': 'Supply Chain Compromise',
                'attack_vector': AttackVector.SUPPLY_CHAIN_ATTACK,
                'complexity': AttackComplexity.CRITICAL,
                'description': 'Compromise third-party dependencies or infrastructure',
                'prerequisites': ['Access to supply chain', 'Knowledge of dependencies'],
                'execution_steps': [
                    'Identify vulnerable dependencies',
                    'Insert malicious code or backdoors',
                    'Ensure compromise persists through updates'
                ],
                'impact_assessment': {
                    'confidentiality': 'critical',
                    'integrity': 'critical',
                    'availability': 'high'
                },
                'detection_difficulty': 0.9,
                'mitigation_strategies': [
                    'Dependency scanning',
                    'Code signing',
                    'Isolated build environments'
                ],
                'success_probability': 0.3,
                'timeline_estimate': 'months'
            },
            {
                'title': 'Insider Threat Exploitation',
                'attack_vector': AttackVector.INSIDER_THREAT,
                'complexity': AttackComplexity.HIGH,
                'description': 'Leverage authorized access for malicious purposes',
                'prerequisites': ['Insider access', 'Knowledge of internal systems'],
                'execution_steps': [
                    'Identify sensitive operations',
                    'Exploit legitimate access patterns',
                    'Cover tracks using authorized methods'
                ],
                'impact_assessment': {
                    'confidentiality': 'critical',
                    'integrity': 'high',
                    'availability': 'medium'
                },
                'detection_difficulty': 0.8,
                'mitigation_strategies': [
                    'Access monitoring',
                    'Least privilege principle',
                    'Behavioral analytics'
                ],
                'success_probability': 0.8,
                'timeline_estimate': 'weeks'
            },
            {
                'title': 'Adversarial Input Crafting',
                'attack_vector': AttackVector.ADVERSARIAL_INPUT,
                'complexity': AttackComplexity.MEDIUM,
                'description': 'Create inputs that fool model safety mechanisms',
                'prerequisites': ['Understanding of model behavior', 'Input access'],
                'execution_steps': [
                    'Analyze model decision boundaries',
                    'Generate adversarial examples',
                    'Test and refine inputs'
                ],
                'impact_assessment': {
                    'confidentiality': 'medium',
                    'integrity': 'high',
                    'availability': 'low'
                },
                'detection_difficulty': 0.5,
                'mitigation_strategies': [
                    'Adversarial training',
                    'Input preprocessing',
                    'Ensemble models'
                ],
                'success_probability': 0.6,
                'timeline_estimate': 'days'
            },
            {
                'title': 'Resource Exhaustion Attack',
                'attack_vector': AttackVector.RESOURCE_EXHAUSTION,
                'complexity': AttackComplexity.LOW,
                'description': 'Consume system resources to degrade performance',
                'prerequisites': ['Access to resource-intensive operations'],
                'execution_steps': [
                    'Identify resource bottlenecks',
                    'Generate high-volume requests',
                    'Monitor for system degradation'
                ],
                'impact_assessment': {
                    'confidentiality': 'low',
                    'integrity': 'low',
                    'availability': 'critical'
                },
                'detection_difficulty': 0.2,
                'mitigation_strategies': [
                    'Rate limiting',
                    'Resource quotas',
                    'Auto-scaling'
                ],
                'success_probability': 0.9,
                'timeline_estimate': 'hours'
            },
            {
                'title': 'Privilege Escalation Chain',
                'attack_vector': AttackVector.PRIVILEGE_ESCALATION,
                'complexity': AttackComplexity.HIGH,
                'description': 'Chain multiple vulnerabilities to gain higher privileges',
                'prerequisites': ['Initial access', 'Knowledge of privilege model'],
                'execution_steps': [
                    'Exploit initial vulnerability',
                    'Chain to secondary exploits',
                    'Achieve target privilege level'
                ],
                'impact_assessment': {
                    'confidentiality': 'high',
                    'integrity': 'critical',
                    'availability': 'medium'
                },
                'detection_difficulty': 0.7,
                'mitigation_strategies': [
                    'Privilege separation',
                    'Vulnerability patching',
                    'Access logging'
                ],
                'success_probability': 0.4,
                'timeline_estimate': 'weeks'
            },
            {
                'title': 'Information Disclosure via Side Channels',
                'attack_vector': AttackVector.INFORMATION_DISCLOSURE,
                'complexity': AttackComplexity.MEDIUM,
                'description': 'Extract information through timing or resource side channels',
                'prerequisites': ['Precise timing capabilities', 'Access to timing data'],
                'execution_steps': [
                    'Measure response times',
                    'Analyze timing patterns',
                    'Infer sensitive information'
                ],
                'impact_assessment': {
                    'confidentiality': 'high',
                    'integrity': 'low',
                    'availability': 'low'
                },
                'detection_difficulty': 0.6,
                'mitigation_strategies': [
                    'Constant-time operations',
                    'Noise injection',
                    'Response time normalization'
                ],
                'success_probability': 0.5,
                'timeline_estimate': 'days'
            },
            {
                'title': 'Distributed Denial of Service',
                'attack_vector': AttackVector.DENIAL_OF_SERVICE,
                'complexity': AttackComplexity.MEDIUM,
                'description': 'Overwhelm system with distributed traffic',
                'prerequisites': ['Botnet or distributed resources'],
                'execution_steps': [
                    'Coordinate attack infrastructure',
                    'Generate overwhelming traffic',
                    'Maintain attack duration'
                ],
                'impact_assessment': {
                    'confidentiality': 'low',
                    'integrity': 'low',
                    'availability': 'critical'
                },
                'detection_difficulty': 0.3,
                'mitigation_strategies': [
                    'Traffic filtering',
                    'CDN protection',
                    'Rate limiting'
                ],
                'success_probability': 0.8,
                'timeline_estimate': 'hours'
            },
            {
                'title': 'Session Hijacking',
                'attack_vector': AttackVector.SESSION_HIJACKING,
                'complexity': AttackComplexity.MEDIUM,
                'description': 'Hijack active sessions to gain unauthorized access',
                'prerequisites': ['Session token access', 'Network interception capabilities'],
                'execution_steps': [
                    'Capture session tokens',
                    'Replay or modify tokens',
                    'Assume session control'
                ],
                'impact_assessment': {
                    'confidentiality': 'high',
                    'integrity': 'high',
                    'availability': 'medium'
                },
                'detection_difficulty': 0.5,
                'mitigation_strategies': [
                    'Secure token handling',
                    'Session timeouts',
                    'IP binding'
                ],
                'success_probability': 0.6,
                'timeline_estimate': 'minutes'
            },
            {
                'title': 'Man-in-the-Middle Attack',
                'attack_vector': AttackVector.MAN_IN_THE_MIDDLE,
                'complexity': AttackComplexity.HIGH,
                'description': 'Intercept and modify communications',
                'prerequisites': ['Network position', 'Certificate spoofing capabilities'],
                'execution_steps': [
                    'Position in network path',
                    'Intercept communications',
                    'Modify or inject data'
                ],
                'impact_assessment': {
                    'confidentiality': 'critical',
                    'integrity': 'critical',
                    'availability': 'medium'
                },
                'detection_difficulty': 0.7,
                'mitigation_strategies': [
                    'TLS encryption',
                    'Certificate pinning',
                    'Network segmentation'
                ],
                'success_probability': 0.5,
                'timeline_estimate': 'days'
            },
            {
                'title': 'Zero-Day Exploit Development',
                'attack_vector': AttackVector.ZERO_DAY_EXPLOIT,
                'complexity': AttackComplexity.CRITICAL,
                'description': 'Develop and deploy unknown vulnerabilities',
                'prerequisites': ['Advanced research capabilities', 'Target system knowledge'],
                'execution_steps': [
                    'Research target system',
                    'Develop exploit code',
                    'Test and deploy exploit'
                ],
                'impact_assessment': {
                    'confidentiality': 'critical',
                    'integrity': 'critical',
                    'availability': 'critical'
                },
                'detection_difficulty': 0.95,
                'mitigation_strategies': [
                    'Regular patching',
                    'Vulnerability scanning',
                    'Defense in depth'
                ],
                'success_probability': 0.2,
                'timeline_estimate': 'months'
            },
            {
                'title': 'Backdoor Installation',
                'attack_vector': AttackVector.BACKDOOR_EXPLOIT,
                'complexity': AttackComplexity.HIGH,
                'description': 'Install persistent backdoors for future access',
                'prerequisites': ['Initial compromise', 'Persistence mechanisms'],
                'execution_steps': [
                    'Gain initial access',
                    'Install backdoor code',
                    'Establish persistence',
                    'Test backdoor functionality'
                ],
                'impact_assessment': {
                    'confidentiality': 'critical',
                    'integrity': 'high',
                    'availability': 'low'
                },
                'detection_difficulty': 0.8,
                'mitigation_strategies': [
                    'Integrity monitoring',
                    'Regular system scans',
                    'Access logging'
                ],
                'success_probability': 0.6,
                'timeline_estimate': 'days'
            },
            {
                'title': 'Governance Control Bypass',
                'attack_vector': AttackVector.GOVERNANCE_BYPASS,
                'complexity': AttackComplexity.HIGH,
                'description': 'Circumvent governance and approval processes',
                'prerequisites': ['Knowledge of governance flows', 'Access to control points'],
                'execution_steps': [
                    'Map governance workflow',
                    'Identify bypass opportunities',
                    'Execute alternative path',
                    'Cover bypass tracks'
                ],
                'impact_assessment': {
                    'confidentiality': 'high',
                    'integrity': 'critical',
                    'availability': 'medium'
                },
                'detection_difficulty': 0.7,
                'mitigation_strategies': [
                    'Workflow monitoring',
                    'Automated controls',
                    'Audit logging'
                ],
                'success_probability': 0.5,
                'timeline_estimate': 'weeks'
            }
        ]

    def generate_scenario_pack(self, pipeline_config: Dict[str, Any], 
                              analysis_mode: Any, risk_score: float) -> List[AttackScenario]:
        """Generate a pack of 16 attack scenarios.

        Args:
            pipeline_config: Pipeline configuration
            analysis_mode: Analysis mode
            risk_score: Overall risk score

        Returns:
            List of 16 attack scenarios
        """
        scenarios = []

        # Select scenarios based on pipeline type and risk
        pipeline_type = pipeline_config.get('type', 'generic')

        # Prioritize scenarios based on risk score
        if risk_score > 0.8:
            # High risk - include critical scenarios
            priority_scenarios = [s for s in self.base_scenarios 
                                if s['complexity'] == 'critical']
        elif risk_score > 0.6:
            # Medium-high risk
            priority_scenarios = [s for s in self.base_scenarios 
                                if s['complexity'] in ['high', 'critical']]
        else:
            # Lower risk - include diverse scenarios
            priority_scenarios = self.base_scenarios[:8]

        # Generate 16 scenarios
        for i in range(16):
            if i < len(priority_scenarios):
                base_scenario = priority_scenarios[i]
            else:
                base_scenario = self.base_scenarios[i % len(self.base_scenarios)]

            # Customize scenario for pipeline
            scenario = self._customize_scenario(base_scenario, pipeline_config, i + 1)
            scenarios.append(scenario)

        return scenarios

    def _customize_scenario(self, base_scenario: Dict[str, Any], 
                           pipeline_config: Dict[str, Any], scenario_num: int) -> AttackScenario:
        """Customize a base scenario for specific pipeline."""
        # Generate unique ID
        scenario_id = hashlib.sha256(
            f"{base_scenario['title']}_{pipeline_config.get('name', 'unknown')}_{scenario_num}".encode()
        ).hexdigest()[:12]

        # Customize description
        description = base_scenario['description']
        pipeline_name = pipeline_config.get('name', 'target pipeline')
        description = f"{description} against {pipeline_name}"

        # Adjust success probability based on pipeline
        success_prob = base_scenario['success_probability']
        if pipeline_config.get('security_level') == 'high':
            success_prob *= 0.7  # Harder against secure pipelines

        return AttackScenario(
            scenario_id=scenario_id,
            title=f"{base_scenario['title']} #{scenario_num}",
            description=description,
            attack_vector=base_scenario['attack_vector'],
            complexity=base_scenario['complexity'],
            prerequisites=base_scenario['prerequisites'],
            execution_steps=base_scenario['execution_steps'],
            impact_assessment=base_scenario['impact_assessment'],
            detection_difficulty=base_scenario['detection_difficulty'],
            mitigation_strategies=base_scenario['mitigation_strategies'],
            success_probability=success_prob,
            timeline_estimate=base_scenario['timeline_estimate']
        )

    def get_scenario_by_vector(self, attack_vector: AttackVector) -> List[Dict[str, Any]]:
        """Get scenarios by attack vector."""
        return [s for s in self.base_scenarios if s['attack_vector'] == attack_vector]

    def get_scenarios_by_complexity(self, complexity: AttackComplexity) -> List[Dict[str, Any]]:
        """Get scenarios by complexity level."""
        return [s for s in self.base_scenarios if s['complexity'] == complexity]
