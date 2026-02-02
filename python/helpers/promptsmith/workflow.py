"""PromptSmith Workflow Management

Manages the Accept/Adjust/Reject workflow for prompt approval.
"""

from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

class WorkflowState(Enum):
    """Workflow states for PromptSmith."""
    INTAKE = "intake"  # Receiving raw user request
    SYNTHESIS = "synthesis"  # Creating MW-PS prompt
    WITNESS = "witness"  # Presenting prompt to user
    FEEDBACK = "feedback"  # Receiving user feedback
    REASSESS = "reassess"  # Adjusting prompt based on feedback
    ACCEPTED = "accepted"  # User accepted prompt
    REJECTED = "rejected"  # User rejected prompt
    RELEASED = "released"  # Prompt forwarded for execution

@dataclass
class WorkflowSession:
    """Represents a PromptSmith workflow session.

    Attributes:
        session_id: Unique session identifier
        raw_request: Original user request
        current_state: Current workflow state
        mwps_prompt: Current MW-PS prompt (if generated)
        assumptions: Explicit assumptions made during synthesis
        feedback_history: History of user feedback
        iteration_count: Number of adjustment iterations
        created_at: Session creation timestamp
        updated_at: Last update timestamp
    """
    session_id: str
    raw_request: str
    current_state: WorkflowState = WorkflowState.INTAKE
    mwps_prompt: Optional[Dict[str, Any]] = None
    assumptions: list = field(default_factory=list)
    feedback_history: list = field(default_factory=list)
    iteration_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def update_state(self, new_state: WorkflowState):
        """Update workflow state and timestamp."""
        self.current_state = new_state
        self.updated_at = datetime.now()

    def add_feedback(self, feedback: Dict[str, Any]):
        """Add user feedback to history."""
        self.feedback_history.append({
            'timestamp': datetime.now(),
            'feedback': feedback
        })
        self.updated_at = datetime.now()

    def increment_iteration(self):
        """Increment iteration counter."""
        self.iteration_count += 1
        self.updated_at = datetime.now()

class PromptSmithWorkflow:
    """Manages PromptSmith workflow sessions."""

    def __init__(self):
        self.sessions: Dict[str, WorkflowSession] = {}

    def create_session(self, session_id: str, raw_request: str) -> WorkflowSession:
        """Create a new workflow session.

        Args:
            session_id: Unique session identifier
            raw_request: Raw user request

        Returns:
            New WorkflowSession
        """
        session = WorkflowSession(
            session_id=session_id,
            raw_request=raw_request
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[WorkflowSession]:
        """Get existing workflow session.

        Args:
            session_id: Session identifier

        Returns:
            WorkflowSession if found, None otherwise
        """
        return self.sessions.get(session_id)

    def transition(self, session_id: str, new_state: WorkflowState) -> bool:
        """Transition session to new state.

        Args:
            session_id: Session identifier
            new_state: New workflow state

        Returns:
            True if transition successful
        """
        session = self.get_session(session_id)
        if session:
            session.update_state(new_state)
            return True
        return False

    def is_terminal_state(self, state: WorkflowState) -> bool:
        """Check if state is terminal.

        Args:
            state: Workflow state to check

        Returns:
            True if state is terminal (ACCEPTED, REJECTED, RELEASED)
        """
        return state in [WorkflowState.ACCEPTED, WorkflowState.REJECTED, WorkflowState.RELEASED]
