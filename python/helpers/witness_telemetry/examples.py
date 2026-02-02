"""
Witness Telemetry Usage Examples

Demonstrates key functionality of the Witness Telemetry Subsystem.
"""

from witness_telemetry import WitnessTelemetry
from exceptions import WitnessTelemetryException
import time

def example_basic_logging():
    """Basic event logging and retrieval."""
    print("=== Basic Logging Example ===")
    
    witness = WitnessTelemetry()
    
    # Log various governance events
    events = []
    
    # Risk classification event
    event1 = witness.log_event(
        event_type='risk_classification',
        metadata={
            'risk_level': 'LOW',
            'classifier_version': '1.0',
            'processing_time_ms': 145,
            'query_type': 'SAFE_INFO',
            'confidence_score': 0.92
        },
        actor='risk_classifier',
        context={'session_id': 'sess_123', 'user_type': 'anonymous'}
    )
    events.append(event1)
    
    # User approval event
    event2 = witness.log_event(
        event_type='user_approval',
        metadata={
            'decision': 'approved',
            'approval_type': 'manual',
            'review_time_ms': 2300,
            'risk_acknowledged': True
        },
        actor='user_interface',
        context={'session_id': 'sess_123', 'user_id': 'user_456'}
    )
    events.append(event2)
    
    # System health event
    event3 = witness.log_event(
        event_type='system_health',
        metadata={
            'component': 'mw_sha',
            'status': 'healthy',
            'cpu_usage': 45.2,
            'memory_usage': 67.8,
            'check_duration_ms': 50
        },
        actor='health_monitor',
        context={'system_version': '1.0.0'}
    )
    events.append(event3)
    
    print(f"Logged {len(events)} events")
    for i, event in enumerate(events, 1):
        print(f"  Event {i}: {event.event_id[:16]}... ({event.event_type})")
    
    # Retrieve specific event
    retrieved = witness.get_event(event1.event_id)
    if retrieved:
        print(f"Retrieved event matches: {retrieved.event_id == event1.event_id}")
        print(f"Event type: {retrieved.event_type}")
        print(f"Risk level: {retrieved.metadata.get('risk_level')}")
    
    return events

def example_event_querying():
    """Advanced event querying and filtering."""
    print("\n=== Event Querying Example ===")
    
    witness = WitnessTelemetry()
    
    # Create sample events for querying
    for i in range(10):
        risk_level = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL'][i % 4]
        witness.log_event(
            event_type='risk_classification',
            metadata={
                'risk_level': risk_level,
                'processing_time_ms': 100 + i * 10,
                'query_type': 'GENERAL' if i % 2 == 0 else 'SYSTEM_META'
            },
            actor='classifier',
            context={'batch_id': f'batch_{i//3}'}
        )
        time.sleep(0.01)  # Small delay for timestamp ordering
    
    # Query all risk classification events
    all_risk_events = witness.query_events(
        filters={'event_type': 'risk_classification'}
    )
    print(f"Total risk classification events: {len(all_risk_events)}")
    
    # Query high-risk events only
    high_risk_events = witness.query_events(
        filters={'event_type': 'risk_classification', 'risk_level': 'HIGH'}
    )
    print(f"High-risk events: {len(high_risk_events)}")
    
    # Query with time range (last 5 events)
    recent_events = witness.query_events(limit=5)
    print(f"Most recent 5 events:")
    for event in recent_events:
        print(f"  {event.timestamp[:19]}: {event.event_type} - {event.metadata.get('risk_level', 'N/A')}")
    
    # Count events by risk level
    risk_counts = {}
    for event in all_risk_events:
        level = event.metadata.get('risk_level')
        risk_counts[level] = risk_counts.get(level, 0) + 1
    
    print(f"Risk level distribution: {risk_counts}")
    
    return all_risk_events

def example_event_handlers():
    """Event handler registration and processing."""
    print("\n=== Event Handlers Example ===")
    
    witness = WitnessTelemetry()
    
    # Global event counter
    event_counts = {'total': 0}
    
    def audit_handler(event):
        """Global audit handler for all events."""
        event_counts['total'] += 1
        print(f"📝 Audit: {event.event_type} event logged")
    
    def alert_handler(event):
        """Alert handler for critical events."""
        if event.metadata.get('risk_level') == 'CRITICAL':
            print(f"🚨 CRITICAL ALERT: {event.event_id}")
            # In real implementation, this would send alerts
    
    def compliance_handler(event):
        """Compliance tracking for governance events."""
        if event.event_type in ['risk_classification', 'user_approval']:
            print(f"📋 Compliance: {event.event_type} recorded")
    
    # Register handlers
    witness.register_handler('*', audit_handler)  # All events
    witness.register_handler('risk_classification', alert_handler)
    witness.register_handler('user_approval', compliance_handler)
    witness.register_handler('risk_classification', compliance_handler)
    
    print("Registered event handlers")
    
    # Log events to trigger handlers
    witness.log_event('risk_classification', {'risk_level': 'LOW'}, 'test')
    witness.log_event('risk_classification', {'risk_level': 'CRITICAL'}, 'test')
    witness.log_event('user_approval', {'decision': 'approved'}, 'test')
    witness.log_event('system_health', {'status': 'ok'}, 'test')
    
    print(f"Total events processed by handlers: {event_counts['total']}")
    
    return event_counts['total']

def example_data_export():
    """Data export for compliance and analysis."""
    print("\n=== Data Export Example ===")
    
    witness = WitnessTelemetry()
    
    # Create sample events
    for i in range(5):
        witness.log_event(
            f'event_type_{i%3}',
            {'metric': i * 10, 'category': chr(65 + i%3)},
            f'actor_{i%2}'
        )
    
    # Export all events as JSON
    json_export = witness.export_events(format='json')
    print(f"JSON export length: {len(json_export)} characters")
    
    # Export filtered events
    filtered_export = witness.export_events(
        format='json',
        filters={'event_type': 'event_type_0'}
    )
    print(f"Filtered export length: {len(filtered_export)} characters")
    
    # In a real implementation, you would save to files:
    # with open('telemetry_export.json', 'w') as f:
    #     f.write(json_export)
    
    print("Data export completed (simulated file save)")
    
    return len(json_export)

def example_error_handling():
    """Error handling and edge cases."""
    print("\n=== Error Handling Example ===")
    
    witness = WitnessTelemetry()
    
    # Try to get non-existent event
    try:
        event = witness.get_event('non_existent_id')
        if event is None:
            print("Correctly handled missing event (returned None)")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Try invalid query
    try:
        events = witness.query_events(filters={'invalid_field': 'test'})
        print(f"Query with invalid filter returned {len(events)} events")
    except WitnessTelemetryException as e:
        print(f"Handled query error: {e}")
    
    # Test event verification
    event = witness.log_event('test_event', {'test': 'data'}, 'test_actor')
    is_valid = witness.verify_event(event)
    print(f"Event signature verification: {is_valid}")
    
    # Test handler error handling
    def failing_handler(event):
        raise ValueError("Handler failed intentionally")
    
    witness.register_handler('test_event', failing_handler)
    try:
        witness.log_event('test_event', {'test': 'data'}, 'test_actor')
        print("Handler error was caught and logged")
    except Exception as e:
        print(f"Handler error propagated: {e}")

def run_all_examples():
    """Run all examples in sequence."""
    print("Running Witness Telemetry Examples...\n")
    
    try:
        example_basic_logging()
        example_event_querying()
        example_event_handlers()
        example_data_export()
        example_error_handling()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        raise

if __name__ == "__main__":
    run_all_examples()
