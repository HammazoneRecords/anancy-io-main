"""
9-State Lifecycle Architecture

Provides structural proof of robust governance by separating epistemic stages.
Ensures explicit authority transitions and natural witness points.
"""

import enum
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict

class LifecycleState(enum.Enum):
    """The 9 states of the lifecycle architecture."""
    PREFLIGHT = "preflight"      # Initial validation and setup
    HEALTH = "health"            # System health verification
    CLASSIFICATION = "classification"  # Risk and intent classification
    APPROVAL = "approval"        # User confirmation and CSI invocation
    EXECUTION = "execution"      # Safe execution of approved actions
    WITNESS = "witness"          # Telemetry logging and audit
    CHECKPOINT = "checkpoint"    # TCP checkpoint creation
    RECOVERY = "recovery"        # Protocol of Return if needed
    FINAL = "final"              # Completion with loop-back capability

@dataclass
class LifecycleContext:
    """Context data passed through lifecycle states."""
    
    session_id: str
    user_query: str
    risk_classification: Optional[Dict[str, Any]] = None
    health_status: Optional[Dict[str, Any]] = None
    user_approval: Optional[Dict[str, Any]] = None
    execution_result: Optional[Dict[str, Any]] = None
    telemetry_events: List[Dict[str, Any]] = None
    checkpoint_data: Optional[Dict[str, Any]] = None
    recovery_needed: bool = False
    final_status: Optional[str] = None
    
    def __post_init__(self):
        if self.telemetry_events is None:
            self.telemetry_events = []
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

class LifecycleManager:
    """
    9-State Lifecycle Manager
    
    Orchestrates the complete governance lifecycle with explicit state transitions,
    ensuring structural proof of robust governance through separated epistemic stages.
    """
    
    def __init__(self):
        self.current_state = LifecycleState.PREFLIGHT
        self.context = None
        self.state_history: List[Dict[str, Any]] = []
        self.transition_handlers: Dict[LifecycleState, Callable] = {}
        self.loop_back_enabled = True
        
        # Register default transition handlers
        self._register_default_handlers()
    
    def _register_default_handlers(self):
        """Register default handlers for each state transition."""
        
        def preflight_handler(context: LifecycleContext) -> bool:
            """Validate initial setup and create session."""
            # Integration: Basic validation
            context.session_id = f"session_{hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]}"
            return True
        
        def health_handler(context: LifecycleContext) -> bool:
            """Verify system health via MW-SHA."""
            # Integration: MW-SHA health check
            # In real implementation, call MW-SHA
            context.health_status = {
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'checks_passed': True
            }
            return context.health_status['checks_passed']
        
        def classification_handler(context: LifecycleContext) -> bool:
            """Classify risk and intent."""
            # Integration: Risk Classifier
            # In real implementation, call risk classifier
            context.risk_classification = {
                'risk_level': 'LOW',
                'confidence': 0.95,
                'classification_type': 'SAFE_INFO',
                'timestamp': datetime.now().isoformat()
            }
            return True
        
        def approval_handler(context: LifecycleContext) -> bool:
            """Obtain user approval and invoke CSI if needed."""
            # Integration: User confirmation gates, CSI invocation
            risk_level = context.risk_classification.get('risk_level', 'UNKNOWN')
            if risk_level in ['HIGH', 'CRITICAL']:
                # Would invoke CSI analysis
                context.user_approval = {
                    'approved': False,
                    'requires_csi': True,
                    'timestamp': datetime.now().isoformat()
                }
                return False
            else:
                context.user_approval = {
                    'approved': True,
                    'requires_csi': False,
                    'timestamp': datetime.now().isoformat()
                }
                return True
        
        def execution_handler(context: LifecycleContext) -> bool:
            """Execute approved actions safely."""
            # Integration: Safe execution environment
            if not context.user_approval.get('approved', False):
                return False
            
            context.execution_result = {
                'success': True,
                'output': 'Action executed successfully',
                'timestamp': datetime.now().isoformat()
            }
            return True
        
        def witness_handler(context: LifecycleContext) -> bool:
            """Log telemetry and create audit trail."""
            # Integration: Witness Telemetry
            telemetry_event = {
                'event_type': 'lifecycle_witness',
                'metadata': {
                    'state': self.current_state.value,
                    'session_id': context.session_id,
                    'timestamp': datetime.now().isoformat()
                },
                'actor': 'lifecycle_manager'
            }
            context.telemetry_events.append(telemetry_event)
            return True
        
        def checkpoint_handler(context: LifecycleContext) -> bool:
            """Create TCP checkpoint."""
            # Integration: TCP/TCPC
            context.checkpoint_data = {
                'checkpoint_id': f"cp_{context.session_id}",
                'state_hash': hashlib.sha256(json.dumps(context.to_dict(), sort_keys=True).encode()).hexdigest(),
                'timestamp': datetime.now().isoformat()
            }
            return True
        
        def recovery_handler(context: LifecycleContext) -> bool:
            """Execute Protocol of Return if needed."""
            # Integration: TCPC Protocol of Return
            if context.recovery_needed:
                context.final_status = 'recovered'
                return True
            return False
        
        def final_handler(context: LifecycleContext) -> bool:
            """Complete lifecycle with loop-back capability."""
            context.final_status = 'completed'
            return True
        
        # Register all handlers
        self.transition_handlers = {
            LifecycleState.PREFLIGHT: preflight_handler,
            LifecycleState.HEALTH: health_handler,
            LifecycleState.CLASSIFICATION: classification_handler,
            LifecycleState.APPROVAL: approval_handler,
            LifecycleState.EXECUTION: execution_handler,
            LifecycleState.WITNESS: witness_handler,
            LifecycleState.CHECKPOINT: checkpoint_handler,
            LifecycleState.RECOVERY: recovery_handler,
            LifecycleState.FINAL: final_handler
        }
    
    def start_lifecycle(self, user_query: str) -> LifecycleContext:
        """Start a new lifecycle with the given user query."""
        self.context = LifecycleContext(
            session_id="",
            user_query=user_query
        )
        self.current_state = LifecycleState.PREFLIGHT
        self.state_history = []
        
        # Execute initial state
        self._execute_state(LifecycleState.PREFLIGHT)
        
        return self.context
    
    def advance_state(self) -> bool:
        """Advance to the next state in the lifecycle."""
        if not self.context:
            raise ValueError("No active lifecycle context")
        
        next_state = self._get_next_state()
        if next_state:
            return self._execute_state(next_state)
        return False
    
    def _get_next_state(self) -> Optional[LifecycleState]:
        """Determine the next state based on current state and context."""
        state_transitions = {
            LifecycleState.PREFLIGHT: LifecycleState.HEALTH,
            LifecycleState.HEALTH: LifecycleState.CLASSIFICATION,
            LifecycleState.CLASSIFICATION: LifecycleState.APPROVAL,
            LifecycleState.APPROVAL: LifecycleState.EXECUTION,
            LifecycleState.EXECUTION: LifecycleState.WITNESS,
            LifecycleState.WITNESS: LifecycleState.CHECKPOINT,
            LifecycleState.CHECKPOINT: LifecycleState.RECOVERY if self.context.recovery_needed else LifecycleState.FINAL,
            LifecycleState.RECOVERY: LifecycleState.FINAL,
            LifecycleState.FINAL: None  # End state, but loop-back possible
        }
        
        return state_transitions.get(self.current_state)
    
    def _execute_state(self, state: LifecycleState) -> bool:
        """Execute the specified state and update context."""
        if state not in self.transition_handlers:
            return False
        
        # Record state entry
        state_entry = {
            'state': state.value,
            'entry_time': datetime.now().isoformat(),
            'context_snapshot': self.context.to_dict() if self.context else None
        }
        
        # Execute state handler
        handler = self.transition_handlers[state]
        success = handler(self.context)
        
        # Record state exit
        state_entry['exit_time'] = datetime.now().isoformat()
        state_entry['success'] = success
        self.state_history.append(state_entry)
        
        if success:
            self.current_state = state
        
        return success
    
    def trigger_recovery(self, reason: str):
        """Trigger recovery mode with specified reason."""
        if self.context:
            self.context.recovery_needed = True
            self.context.final_status = f'recovery_triggered: {reason}'
    
    def get_state_history(self) -> List[Dict[str, Any]]:
        """Get the complete state transition history."""
        return self.state_history.copy()
    
    def get_current_context(self) -> Optional[LifecycleContext]:
        """Get the current lifecycle context."""
        return self.context
    
    def reset_lifecycle(self):
        """Reset the lifecycle for loop-back or restart."""
        if self.loop_back_enabled and self.context:
            # Preserve session but reset state progression
            self.current_state = LifecycleState.PREFLIGHT
            self.state_history = []
            # Could optionally preserve certain context data
    
    def is_complete(self) -> bool:
        """Check if the lifecycle has reached completion."""
        return self.current_state == LifecycleState.FINAL and self.context and self.context.final_status == 'completed'
