# Witness Telemetry Core Module

"""
Core telemetry logging functionality for metadata-only audit trails.

This module provides structured logging of governance events, state transitions,
and decision metadata without capturing sensitive user content or system data.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class EventType(Enum):
    """Types of telemetry events."""
    STATE_TRANSITION = "state_transition"
    QUERY_RECEIVED = "query_received"
    CLASSIFICATION_START = "classification_start"
    CLASSIFICATION_COMPLETE = "classification_complete"
    GOVERNANCE_DECISION = "governance_decision"
    HEALTH_CHECK = "health_check"
    ERROR_OCCURRED = "error_occurred"
    CHECKPOINT_CREATED = "checkpoint_created"
    POLICY_LOADED = "policy_loaded"


@dataclass
class TelemetryEvent:
    """Structured telemetry event data."""
    event_type: EventType
    timestamp: datetime
    event_id: str
    session_id: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data['event_type'] = self.event_type.value
        data['timestamp'] = self.timestamp.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TelemetryEvent':
        """Create from dictionary."""
        data_copy = data.copy()
        data_copy['event_type'] = EventType(data_copy['event_type'])
        data_copy['timestamp'] = datetime.fromisoformat(data_copy['timestamp'])
        return cls(**data_copy)


class WitnessTelemetry:
    """Core witness telemetry logging system."""

    def __init__(self, log_dir: Optional[Path] = None, session_id: Optional[str] = None):
        """Initialize telemetry logger.

        Args:
            log_dir: Directory for log files (default: ./telemetry_logs)
            session_id: Unique session identifier
        """
        self.log_dir = log_dir or Path('./telemetry_logs')
        self.log_dir.mkdir(exist_ok=True)
        self.session_id = session_id or self._generate_session_id()
        self.event_count = 0

    def _generate_session_id(self) -> str:
        """Generate unique session identifier."""
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(f"session_{timestamp}".encode()).hexdigest()[:16]

    def _generate_event_id(self) -> str:
        """Generate unique event identifier."""
        self.event_count += 1
        timestamp = datetime.now().isoformat()
        return hashlib.sha256(f"event_{self.session_id}_{self.event_count}_{timestamp}".encode()).hexdigest()[:16]

    def log_event(self, event_type: EventType, metadata: Dict[str, Any]) -> str:
        """Log a telemetry event.

        Args:
            event_type: Type of event
            metadata: Event metadata (no sensitive content)

        Returns:
            Event ID for tracking
        """
        event = TelemetryEvent(
            event_type=event_type,
            timestamp=datetime.now(),
            event_id=self._generate_event_id(),
            session_id=self.session_id,
            metadata=self._sanitize_metadata(metadata)
        )

        # Save to file
        self._save_event(event)

        return event.event_id

    def _sanitize_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitize metadata to ensure no sensitive content.

        This removes or hashes any potentially sensitive fields.
        """
        sanitized = {}

        for key, value in metadata.items():
            if isinstance(value, str):
                # Hash long strings that might contain content
                if len(value) > 50:
                    sanitized[key] = hashlib.sha256(value.encode()).hexdigest()[:16] + "..."
                else:
                    sanitized[key] = value
            elif isinstance(value, (int, float, bool)):
                sanitized[key] = value
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_metadata(value)
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_metadata({'item': item})['item'] if isinstance(item, dict) else item for item in value]
            else:
                # Convert other types to string representation
                sanitized[key] = str(type(value).__name__)

        return sanitized

    def _save_event(self, event: TelemetryEvent):
        """Save event to log file."""
        # Create daily log file
        date_str = event.timestamp.strftime('%Y-%m-%d')
        log_file = self.log_dir / f'telemetry_{date_str}.jsonl'

        # Append event as JSON line
        with open(log_file, 'a') as f:
            f.write(json.dumps(event.to_dict()) + "\n")
")
')

    def get_session_events(self, limit: int = 100) -> List[TelemetryEvent]:
        """Get recent events for current session.

        Args:
            limit: Maximum number of events to return

        Returns:
            List of telemetry events
        """
        events = []

        # Read from today's log file
        date_str = datetime.now().strftime('%Y-%m-%d')
        log_file = self.log_dir / f'telemetry_{date_str}.jsonl'

        if log_file.exists():
            with open(log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        event_data = json.loads(line)
                        event = TelemetryEvent.from_dict(event_data)
                        if event.session_id == self.session_id:
                            events.append(event)
                            if len(events) >= limit:
                                break

        return events

    def get_event_count(self) -> int:
        """Get total number of events logged in current session."""
        return len(self.get_session_events(limit=1000))


class TelemetryLogger:
    """Convenience logger for common telemetry events."""

    def __init__(self, telemetry: WitnessTelemetry):
        """Initialize with telemetry instance."""
        self.telemetry = telemetry

    def log_state_transition(self, from_state: str, to_state: str, reason: str):
        """Log state transition event."""
        return self.telemetry.log_event(
            EventType.STATE_TRANSITION,
            {
                'from_state': from_state,
                'to_state': to_state,
                'reason': reason
            }
        )

    def log_query_received(self, query_length: int, query_type: str):
        """Log query received event."""
        return self.telemetry.log_event(
            EventType.QUERY_RECEIVED,
            {
                'query_length': query_length,
                'query_type': query_type
            }
        )

    def log_classification(self, risk_level: str, confidence: float, patterns_matched: int):
        """Log classification completion."""
        return self.telemetry.log_event(
            EventType.CLASSIFICATION_COMPLETE,
            {
                'risk_level': risk_level,
                'confidence': confidence,
                'patterns_matched': patterns_matched
            }
        )

    def log_governance_decision(self, decision: str, confidence: float, escalated: bool):
        """Log governance decision."""
        return self.telemetry.log_event(
            EventType.GOVERNANCE_DECISION,
            {
                'decision': decision,
                'confidence': confidence,
                'escalated': escalated
            }
        )

    def log_health_check(self, component: str, status: str, metrics: Dict[str, Any]):
        """Log health check event."""
        return self.telemetry.log_event(
            EventType.HEALTH_CHECK,
            {
                'component': component,
                'status': status,
                'metrics': metrics
            }
        )

    def log_error(self, error_type: str, component: str, recoverable: bool):
        """Log error event."""
        return self.telemetry.log_event(
            EventType.ERROR_OCCURRED,
            {
                'error_type': error_type,
                'component': component,
                'recoverable': recoverable
            }
        )
