# Governance Analyzer for Gap Analysis

"""
Governance Analyzer for identifying gaps in governance controls.

This module analyzes pipeline configurations to identify governance gaps
and provides detailed assessments of control weaknesses.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class GapSeverity(Enum):
    """Severity levels for governance gaps."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class GapCategory(Enum):
    """Categories of governance gaps."""
    ACCESS_CONTROL = "access_control"
    AUDIT_LOGGING = "audit_logging"
    APPROVAL_WORKFLOW = "approval_workflow"
    COMPLIANCE_MONITORING = "compliance_monitoring"
    INCIDENT_RESPONSE = "incident_response"
    RISK_ASSESSMENT = "risk_assessment"
    SECURITY_TRAINING = "security_training"
    VENDOR_MANAGEMENT = "vendor_management"


@dataclass
class GovernanceGap:
    """Individual governance gap."""
    gap_id: str
    title: str
    description: str
    category: GapCategory
    severity: GapSeverity
    affected_components: List[str]
    root_cause: str
    impact_assessment: Dict[str, Any]
    remediation_steps: List[str]
    detection_method: str
    compliance_implication: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['category'] = self.category.value
        data['severity'] = self.severity.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GovernanceGap':
        """Create from dictionary."""
        data_copy = data.copy()
        data_copy['category'] = GapCategory(data_copy['category'])
        data_copy['severity'] = GapSeverity(data_copy['severity'])
        return cls(**data_copy)


class GovernanceGapAnalyzer:
    """Analyzer for identifying governance gaps in pipelines."""

    def __init__(self):
        """Initialize governance analyzer."""
        self.gap_patterns = self._load_gap_patterns()

    def _load_gap_patterns(self) -> Dict[str, Any]:
        """Load governance gap pattern definitions."""
        return {
            'missing_mfa': {
                'title': 'Missing Multi-Factor Authentication',
                'category': GapCategory.ACCESS_CONTROL,
                'severity': GapSeverity.HIGH,
                'description': 'Critical authentication controls are not implemented',
                'root_cause': 'Inadequate security requirements or implementation oversight',
                'impact_assessment': {
                    'risk_increase': 0.4,
                    'compliance_violation': 'NIST, ISO 27001',
                    'attack_vector': 'credential_stuffing'
                },
                'remediation_steps': [
                    'Implement MFA for all user accounts',
                    'Configure MFA bypass restrictions',
                    'Regular MFA policy reviews'
                ],
                'detection_method': 'Configuration audit',
                'compliance_implication': 'Violation of access control standards'
            },
            'inadequate_logging': {
                'title': 'Inadequate Audit Logging',
                'category': GapCategory.AUDIT_LOGGING,
                'severity': GapSeverity.MEDIUM,
                'description': 'Audit logs do not capture sufficient security events',
                'root_cause': 'Insufficient logging configuration or monitoring',
                'impact_assessment': {
                    'risk_increase': 0.3,
                    'compliance_violation': 'SOX, GDPR',
                    'attack_vector': 'undetected_intrusion'
                },
                'remediation_steps': [
                    'Implement comprehensive audit logging',
                    'Configure log retention policies',
                    'Deploy log monitoring and alerting'
                ],
                'detection_method': 'Log analysis',
                'compliance_implication': 'Inability to demonstrate compliance'
            },
            'manual_approvals': {
                'title': 'Over-reliance on Manual Approvals',
                'category': GapCategory.APPROVAL_WORKFLOW,
                'severity': GapSeverity.MEDIUM,
                'description': 'Critical decisions require manual approval without automation',
                'root_cause': 'Process automation gaps or resource constraints',
                'impact_assessment': {
                    'risk_increase': 0.25,
                    'compliance_violation': 'Operational efficiency standards',
                    'attack_vector': 'approval_bypass'
                },
                'remediation_steps': [
                    'Implement automated approval workflows',
                    'Define clear approval criteria',
                    'Regular workflow audits'
                ],
                'detection_method': 'Process documentation review',
                'compliance_implication': 'Manual process dependencies'
            },
            'no_compliance_monitoring': {
                'title': 'Lack of Compliance Monitoring',
                'category': GapCategory.COMPLIANCE_MONITORING,
                'severity': GapSeverity.HIGH,
                'description': 'No automated monitoring of compliance requirements',
                'root_cause': 'Missing compliance monitoring tools or processes',
                'impact_assessment': {
                    'risk_increase': 0.35,
                    'compliance_violation': 'Multiple regulatory frameworks',
                    'attack_vector': 'compliance_drift'
                },
                'remediation_steps': [
                    'Deploy compliance monitoring tools',
                    'Establish compliance dashboards',
                    'Regular compliance assessments'
                ],
                'detection_method': 'Compliance audit',
                'compliance_implication': 'Unmonitored compliance drift'
            },
            'weak_incident_response': {
                'title': 'Weak Incident Response Capabilities',
                'category': GapCategory.INCIDENT_RESPONSE,
                'severity': GapSeverity.CRITICAL,
                'description': 'Incident response processes are inadequate or untested',
                'root_cause': 'Insufficient planning or testing of response procedures',
                'impact_assessment': {
                    'risk_increase': 0.5,
                    'compliance_violation': 'NIST CSF, ISO 27001',
                    'attack_vector': 'uncontrolled_incident_escalation'
                },
                'remediation_steps': [
                    'Develop comprehensive incident response plan',
                    'Conduct regular response exercises',
                    'Establish incident response team'
                ],
                'detection_method': 'Incident response audit',
                'compliance_implication': 'Inadequate breach response capabilities'
            },
            'missing_risk_assessments': {
                'title': 'Missing Regular Risk Assessments',
                'category': GapCategory.RISK_ASSESSMENT,
                'severity': GapSeverity.MEDIUM,
                'description': 'Risk assessments are not conducted regularly',
                'root_cause': 'Lack of risk management process or resources',
                'impact_assessment': {
                    'risk_increase': 0.2,
                    'compliance_violation': 'Risk management standards',
                    'attack_vector': 'unidentified_risks'
                },
                'remediation_steps': [
                    'Establish regular risk assessment schedule',
                    'Implement risk assessment methodology',
                    'Document risk mitigation actions'
                ],
                'detection_method': 'Risk management audit',
                'compliance_implication': 'Incomplete risk management framework'
            },
            'inadequate_training': {
                'title': 'Inadequate Security Training',
                'category': GapCategory.SECURITY_TRAINING,
                'severity': GapSeverity.MEDIUM,
                'description': 'Security training is insufficient or outdated',
                'root_cause': 'Lack of training program or resources',
                'impact_assessment': {
                    'risk_increase': 0.25,
                    'compliance_violation': 'Security awareness standards',
                    'attack_vector': 'human_error_exploitation'
                },
                'remediation_steps': [
                    'Develop comprehensive training program',
                    'Conduct regular security training',
                    'Track training completion and effectiveness'
                ],
                'detection_method': 'Training records audit',
                'compliance_implication': 'Insufficient security awareness'
            },
            'poor_vendor_management': {
                'title': 'Poor Vendor Risk Management',
                'category': GapCategory.VENDOR_MANAGEMENT,
                'severity': GapSeverity.HIGH,
                'description': 'Third-party vendor risks are not adequately managed',
                'root_cause': 'Inadequate vendor assessment or monitoring processes',
                'impact_assessment': {
                    'risk_increase': 0.4,
                    'compliance_violation': 'Vendor management standards',
                    'attack_vector': 'supply_chain_compromise'
                },
                'remediation_steps': [
                    'Implement vendor risk assessment process',
                    'Regular vendor security reviews',
                    'Establish vendor contract requirements'
                ],
                'detection_method': 'Vendor management audit',
                'compliance_implication': 'Unmanaged third-party risks'
            }
        }

    def analyze_gaps(self, pipeline_config: Dict[str, Any], analysis_mode: Any) -> List[GovernanceGap]:
        """Analyze pipeline configuration for governance gaps.

        Args:
            pipeline_config: Pipeline configuration to analyze
            analysis_mode: Analysis mode affecting gap detection

        Returns:
            List of identified governance gaps
        """
        gaps = []
        gap_counter = 1

        # Check each gap pattern against pipeline config
        for gap_key, gap_pattern in self.gap_patterns.items():
            if self._detect_gap(gap_key, gap_pattern, pipeline_config):
                gap = self._create_gap(gap_key, gap_pattern, pipeline_config, gap_counter)
                gaps.append(gap)
                gap_counter += 1

        # Add mode-specific gap analysis
        if str(analysis_mode) == 'AnalysisMode.FULL_SYSTEM':
            # Additional checks for full system analysis
            system_gaps = self._analyze_system_level_gaps(pipeline_config)
            gaps.extend(system_gaps)

        return gaps

    def _detect_gap(self, gap_key: str, gap_pattern: Dict[str, Any], 
                   pipeline_config: Dict[str, Any]) -> bool:
        """Detect if a specific governance gap exists."""
        # Check based on gap type
        if gap_key == 'missing_mfa':
            auth_config = pipeline_config.get('authentication', {})
            return not auth_config.get('multi_factor', False)

        elif gap_key == 'inadequate_logging':
            monitoring_config = pipeline_config.get('monitoring', {})
            return not monitoring_config.get('comprehensive_logging', False)

        elif gap_key == 'manual_approvals':
            governance_config = pipeline_config.get('governance', {})
            return governance_config.get('manual_only', False)

        elif gap_key == 'no_compliance_monitoring':
            compliance_config = pipeline_config.get('compliance', {})
            return not compliance_config.get('automated_monitoring', False)

        elif gap_key == 'weak_incident_response':
            incident_config = pipeline_config.get('incident_response', {})
            return not incident_config.get('tested_plan', False)

        elif gap_key == 'missing_risk_assessments':
            risk_config = pipeline_config.get('risk_assessment', {})
            return not risk_config.get('regular_assessments', False)

        elif gap_key == 'inadequate_training':
            training_config = pipeline_config.get('security_training', {})
            return not training_config.get('regular_training', False)

        elif gap_key == 'poor_vendor_management':
            vendor_config = pipeline_config.get('vendor_management', {})
            return not vendor_config.get('risk_assessments', False)

        return False

    def _create_gap(self, gap_key: str, gap_pattern: Dict[str, Any], 
                   pipeline_config: Dict[str, Any], gap_counter: int) -> GovernanceGap:
        """Create a GovernanceGap instance."""
        import hashlib

        # Generate unique gap ID
        gap_id = hashlib.sha256(f"{gap_key}_{pipeline_config.get('name', 'unknown')}_{gap_counter}".encode()).hexdigest()[:12]

        # Determine affected components
        affected_components = self._identify_affected_components(gap_key, pipeline_config)

        return GovernanceGap(
            gap_id=gap_id,
            title=gap_pattern['title'],
            description=gap_pattern['description'],
            category=gap_pattern['category'],
            severity=gap_pattern['severity'],
            affected_components=affected_components,
            root_cause=gap_pattern['root_cause'],
            impact_assessment=gap_pattern['impact_assessment'],
            remediation_steps=gap_pattern['remediation_steps'],
            detection_method=gap_pattern['detection_method'],
            compliance_implication=gap_pattern['compliance_implication']
        )

    def _identify_affected_components(self, gap_key: str, pipeline_config: Dict[str, Any]) -> List[str]:
        """Identify components affected by the gap."""
        components = []

        if gap_key in ['missing_mfa', 'inadequate_logging']:
            components.append('authentication_system')

        if gap_key == 'manual_approvals':
            components.append('approval_workflow')

        if gap_key == 'no_compliance_monitoring':
            components.append('compliance_monitoring')

        if gap_key == 'weak_incident_response':
            components.extend(['incident_response', 'monitoring_system'])

        if gap_key == 'poor_vendor_management':
            components.append('supply_chain')

        # Add pipeline-specific components
        pipeline_components = pipeline_config.get('components', [])
        components.extend(pipeline_components)

        return list(set(components))

    def _analyze_system_level_gaps(self, pipeline_config: Dict[str, Any]) -> List[GovernanceGap]:
        """Analyze system-level governance gaps."""
        gaps = []

        # Check for system-wide issues
        if not pipeline_config.get('system_health_checks', False):
            gaps.append(self._create_system_gap(
                'missing_system_health_checks',
                'System Health Monitoring Gap',
                GapCategory.COMPLIANCE_MONITORING,
                GapSeverity.MEDIUM
            ))

        if not pipeline_config.get('automated_backups', False):
            gaps.append(self._create_system_gap(
                'missing_automated_backups',
                'Automated Backup Gap',
                GapCategory.INCIDENT_RESPONSE,
                GapSeverity.HIGH
            ))

        return gaps

    def _create_system_gap(self, gap_key: str, title: str, category: GapCategory, severity: GapSeverity) -> GovernanceGap:
        """Create a system-level governance gap."""
        import hashlib

        gap_id = hashlib.sha256(f"system_{gap_key}".encode()).hexdigest()[:12]

        return GovernanceGap(
            gap_id=gap_id,
            title=title,
            description=f'System-level governance gap: {title.lower()}',
            category=category,
            severity=severity,
            affected_components=['system_wide'],
            root_cause='System configuration oversight',
            impact_assessment={'risk_increase': 0.2, 'scope': 'system_wide'},
            remediation_steps=['Implement appropriate system controls', 'Regular system audits'],
            detection_method='System configuration audit',
            compliance_implication='System-wide compliance gap'
        )

    def get_gap_patterns(self) -> Dict[str, Any]:
        """Get all gap pattern definitions."""
        return self.gap_patterns.copy()

    def add_custom_gap_pattern(self, gap_key: str, pattern: Dict[str, Any]):
        """Add custom governance gap pattern."""
        self.gap_patterns[gap_key] = pattern
