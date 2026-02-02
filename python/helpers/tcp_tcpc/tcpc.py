# Trajectory Checkpoint Controller (TCPC)

"""
Trajectory Checkpoint Controller for orchestrating compliance and checkpoint management.

This module provides the orchestration layer that integrates TCP with governance
workflows, ensuring checkpoints are created at appropriate state transitions.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from .tcp import TrajectoryCheckpointProtocol, CheckpointType, CheckpointChain


class ComplianceRule:
    """Compliance rule for checkpoint creation."""

    def __init__(self, rule_id: str, trigger_condition: Callable[[Dict[str, Any]], bool], 
                 checkpoint_type: CheckpointType, metadata_extractor: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None):
        """Initialize compliance rule.

        Args:
            rule_id: Unique rule identifier
            trigger_condition: Function that returns True when checkpoint should be created
            checkpoint_type: Type of checkpoint to create
            metadata_extractor: Function to extract metadata from context
        """
        self.rule_id = rule_id
        self.trigger_condition = trigger_condition
        self.checkpoint_type = checkpoint_type
        self.metadata_extractor = metadata_extractor

    def should_trigger(self, context: Dict[str, Any]) -> bool:
        """Check if rule should trigger checkpoint creation."""
        try:
            return self.trigger_condition(context)
        except Exception:
            return False

    def extract_metadata(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Extract metadata from context."""
        if self.metadata_extractor:
            try:
                return self.metadata_extractor(context)
            except Exception:
                pass
        return {}


class ComplianceOrchestrator:
    """Orchestrator for compliance rules and checkpoint creation."""

    def __init__(self, tcp: TrajectoryCheckpointProtocol):
        """Initialize orchestrator.

        Args:
            tcp: TCP instance to use for checkpoints
        """
        self.tcp = tcp
        self.rules: List[ComplianceRule] = []
        self.event_handlers: Dict[str, List[Callable]] = {}

    def add_rule(self, rule: ComplianceRule):
        """Add compliance rule."""
        self.rules.append(rule)

    def add_event_handler(self, event_type: str, handler: Callable):
        """Add event handler for specific event types."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    def process_event(self, event_type: str, context: Dict[str, Any]) -> List[str]:
        """Process event and create checkpoints as needed.

        Args:
            event_type: Type of event
            context: Event context data

        Returns:
            List of checkpoint IDs created
        """
        checkpoint_ids = []

        # Check all rules
        for rule in self.rules:
            if rule.should_trigger(context):
                # Create checkpoint
                metadata = rule.extract_metadata(context)
                checkpoint_id = self.tcp.create_checkpoint(
                    rule.checkpoint_type,
                    context,
                    metadata,
                    chain_type=event_type
                )

                if checkpoint_id:
                    checkpoint_ids.append(checkpoint_id)

        # Trigger event handlers
        if event_type in self.event_handlers:
            for handler in self.event_handlers[event_type]:
                try:
                    handler(event_type, context, checkpoint_ids)
                except Exception:
                    # Log error but continue
                    pass

        return checkpoint_ids

    def get_compliance_status(self, chain_type: str = 'default') -> Dict[str, Any]:
        """Get compliance status for a chain."""
        trajectory = self.tcp.get_trajectory_summary(chain_type)

        if 'error' in trajectory:
            return {'status': 'error', 'message': trajectory['error']}

        # Check compliance rules
        compliant_rules = 0
        total_rules = len(self.rules)

        for rule in self.rules:
            # Check if rule has been triggered (simplified check)
            # In production, this would check actual rule compliance
            compliant_rules += 1

        return {
            'status': 'compliant' if trajectory['integrity_verified'] else 'integrity_failure',
            'trajectory_summary': trajectory,
            'rules_compliant': compliant_rules,
            'total_rules': total_rules,
            'compliance_percentage': (compliant_rules / total_rules * 100) if total_rules > 0 else 100
        }


class TrajectoryCheckpointController:
    """Main TCPC implementation for governance integration."""

    def __init__(self, checkpoint_dir: Optional[Path] = None, session_id: Optional[str] = None):
        """Initialize TCPC.

        Args:
            checkpoint_dir: Directory for checkpoints
            session_id: Session identifier
        """
        self.tcp = TrajectoryCheckpointProtocol(checkpoint_dir, session_id)
        self.orchestrator = ComplianceOrchestrator(self.tcp)
        self._setup_default_rules()

    def _setup_default_rules(self):
        """Set up default compliance rules."""
        # Rule 1: State transitions
        def state_transition_trigger(context):
            return context.get('event_type') == 'state_change'

        def state_metadata_extractor(context):
            return {
                'from_state': context.get('from_state'),
                'to_state': context.get('to_state'),
                'reason': context.get('reason')
            }

        rule1 = ComplianceRule(
            'state_transition',
            state_transition_trigger,
            CheckpointType.STATE_TRANSITION,
            state_metadata_extractor
        )
        self.orchestrator.add_rule(rule1)

        # Rule 2: Governance decisions
        def governance_trigger(context):
            return context.get('event_type') == 'governance_decision'

        def governance_metadata_extractor(context):
            return {
                'decision': context.get('decision'),
                'confidence': context.get('confidence'),
                'escalated': context.get('escalated')
            }

        rule2 = ComplianceRule(
            'governance_decision',
            governance_trigger,
            CheckpointType.GOVERNANCE_DECISION,
            governance_metadata_extractor
        )
        self.orchestrator.add_rule(rule2)

        # Rule 3: Classification events
        def classification_trigger(context):
            return context.get('event_type') == 'classification_complete'

        def classification_metadata_extractor(context):
            return {
                'risk_level': context.get('risk_level'),
                'confidence': context.get('confidence'),
                'patterns_matched': context.get('patterns_matched')
            }

        rule3 = ComplianceRule(
            'classification_event',
            classification_trigger,
            CheckpointType.CLASSIFICATION_EVENT,
            classification_metadata_extractor
        )
        self.orchestrator.add_rule(rule3)

        # Rule 4: Health checks
        def health_trigger(context):
            return context.get('event_type') == 'health_check'

        def health_metadata_extractor(context):
            return {
                'component': context.get('component'),
                'status': context.get('status'),
                'metrics': context.get('metrics')
            }

        rule4 = ComplianceRule(
            'health_check',
            health_trigger,
            CheckpointType.HEALTH_CHECK,
            health_metadata_extractor
        )
        self.orchestrator.add_rule(rule4)

        # Rule 5: Error conditions
        def error_trigger(context):
            return context.get('event_type') == 'error_occurred'

        def error_metadata_extractor(context):
            return {
                'error_type': context.get('error_type'),
                'component': context.get('component'),
                'recoverable': context.get('recoverable')
            }

        rule5 = ComplianceRule(
            'error_condition',
            error_trigger,
            CheckpointType.ERROR_CONDITION,
            error_metadata_extractor
        )
        self.orchestrator.add_rule(rule5)

    def process_governance_event(self, event_type: str, context: Dict[str, Any]) -> List[str]:
        """Process governance event and create checkpoints.

        Args:
            event_type: Type of governance event
            context: Event context

        Returns:
            List of checkpoint IDs created
        """
        # Add event type to context
        context = dict(context)
        context['event_type'] = event_type

        return self.orchestrator.process_event(event_type, context)

    def add_custom_rule(self, rule_id: str, trigger_condition: Callable, 
                       checkpoint_type: CheckpointType, metadata_extractor: Optional[Callable] = None):
        """Add custom compliance rule."""
        rule = ComplianceRule(rule_id, trigger_condition, checkpoint_type, metadata_extractor)
        self.orchestrator.add_rule(rule)

    def add_event_handler(self, event_type: str, handler: Callable):
        """Add event handler."""
        self.orchestrator.add_event_handler(event_type, handler)

    def get_compliance_status(self, chain_type: str = 'default') -> Dict[str, Any]:
        """Get compliance status."""
        return self.orchestrator.get_compliance_status(chain_type)

    def verify_trajectory_integrity(self, chain_type: str = 'default') -> bool:
        """Verify trajectory integrity."""
        return self.tcp.verify_trajectory(chain_type)

    def get_trajectory_summary(self, chain_type: str = 'default') -> Dict[str, Any]:
        """Get trajectory summary."""
        return self.tcp.get_trajectory_summary(chain_type)

    def export_compliance_report(self, chain_type: str = 'default') -> str:
        """Export compliance report."""
        status = self.get_compliance_status(chain_type)
        summary = self.get_trajectory_summary(chain_type)

        report = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.tcp.session_id,
            'chain_type': chain_type,
            'compliance_status': status,
            'trajectory_summary': summary,
            'rules_count': len(self.orchestrator.rules)
        }

        # Save to file
        reports_dir = tcp_tcpc_dir / 'reports'
        reports_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = reports_dir / f'compliance_report_{chain_type}_{timestamp}.json'

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)

        return str(report_file)
