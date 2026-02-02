"""
9-State Lifecycle Architecture Usage Examples

Demonstrates the complete governance lifecycle with explicit state transitions.
"""

from lifecycle_manager import LifecycleManager, LifecycleState
from exceptions import LifecycleException
import time

def example_basic_lifecycle():
    """Basic lifecycle execution from start to finish."""
    print("=== Basic Lifecycle Example ===")
    
    manager = LifecycleManager()
    
    # Start lifecycle with user query
    context = manager.start_lifecycle("Show me the system status")
    print(f"Started lifecycle for session: {context.session_id}")
    print(f"Initial state: {manager.current_state.value}")
    
    # Advance through all states automatically
    states_executed = []
    while not manager.is_complete():
        success = manager.advance_state()
        current_state = manager.current_state.value
        states_executed.append(current_state)
        print(f"Executed {current_state}: {'SUCCESS' if success else 'FAILED'}")
        
        # Small delay for demonstration
        time.sleep(0.1)
    
    print(f"Lifecycle completed with status: {context.final_status}")
    print(f"States executed: {' → '.join(states_executed)}")
    
    # Show context summary
    print(f"Risk classification: {context.risk_classification}")
    print(f"User approval: {context.user_approval}")
    print(f"Telemetry events: {len(context.telemetry_events)}")
    
    return context

def example_manual_approval():
    """Lifecycle with manual approval step."""
    print("\n=== Manual Approval Example ===")
    
    manager = LifecycleManager()
    
    # Start with a potentially high-risk query
    context = manager.start_lifecycle("Execute system command: rm -rf /")
    print(f"High-risk query session: {context.session_id}")
    
    # Advance to approval state
    while manager.current_state != LifecycleState.APPROVAL:
        manager.advance_state()
        print(f"Advanced to: {manager.current_state.value}")
    
    # Check approval status
    if not context.user_approval.get('approved', False):
        print("Approval denied - would require CSI analysis")
        print(f"CSI required: {context.user_approval.get('requires_csi', False)}")
        
        # Simulate manual approval
        context.user_approval = {
            'approved': True,
            'manual_override': True,
            'timestamp': '2026-01-31T16:53:00Z',
            'approver': 'admin_user'
        }
        print("Manual approval granted")
    
    # Continue execution
    while not manager.is_complete():
        manager.advance_state()
        print(f"Advanced to: {manager.current_state.value}")
    
    print(f"Final status: {context.final_status}")
    
    return context

def example_recovery_scenario():
    """Lifecycle with recovery trigger and execution."""
    print("\n=== Recovery Scenario Example ===")
    
    manager = LifecycleManager()
    
    # Start normal lifecycle
    context = manager.start_lifecycle("Process user data")
    print(f"Normal processing session: {context.session_id}")
    
    # Advance to execution state
    while manager.current_state != LifecycleState.EXECUTION:
        manager.advance_state()
        print(f"Advanced to: {manager.current_state.value}")
    
    # Simulate execution failure
    print("Simulating execution anomaly...")
    context.execution_result = {
        'success': False,
        'error': 'Data corruption detected',
        'timestamp': '2026-01-31T16:53:00Z'
    }
    
    # Trigger recovery
    manager.trigger_recovery("Execution failure detected")
    print(f"Recovery triggered: {context.recovery_needed}")
    
    # Continue to recovery state
    while manager.current_state != LifecycleState.RECOVERY:
        manager.advance_state()
        print(f"Advanced to: {manager.current_state.value}")
    
    # Execute recovery
    manager.advance_state()  # To FINAL
    print(f"Recovery completed: {context.final_status}")
    
    return context

def example_state_history_analysis():
    """Analyze complete state transition history."""
    print("\n=== State History Analysis Example ===")
    
    manager = LifecycleManager()
    
    # Execute complete lifecycle
    context = manager.start_lifecycle("Analyze system logs")
    while not manager.is_complete():
        manager.advance_state()
    
    # Get state history
    history = manager.get_state_history()
    print(f"Total state transitions: {len(history)}")
    
    # Analyze each state
    for i, entry in enumerate(history, 1):
        state = entry['state']
        entry_time = entry['entry_time']
        exit_time = entry['exit_time']
        success = entry['success']
        
        print(f"{i}. {state.upper()}")
        print(f"   Entry: {entry_time}")
        print(f"   Exit: {exit_time}")
        print(f"   Success: {success}")
        
        # Show context changes
        if entry['context_snapshot']:
            ctx = entry['context_snapshot']
            if state == 'classification' and ctx.get('risk_classification'):
                risk = ctx['risk_classification']
                print(f"   Risk Level: {risk.get('risk_level')}")
            elif state == 'approval' and ctx.get('user_approval'):
                approval = ctx['user_approval']
                print(f"   Approved: {approval.get('approved')}")
            elif state == 'witness':
                events = ctx.get('telemetry_events', [])
                print(f"   Telemetry Events: {len(events)}")
    
    return history

def example_loop_back():
    """Demonstrate loop-back capability for continuous operation."""
    print("\n=== Loop-Back Example ===")
    
    manager = LifecycleManager()
    
    # First lifecycle
    print("Executing first lifecycle...")
    context1 = manager.start_lifecycle("Query 1")
    while not manager.is_complete():
        manager.advance_state()
    print(f"First lifecycle completed: {context1.final_status}")
    
    # Loop back - reset for new lifecycle
    print("Looping back for second lifecycle...")
    manager.reset_lifecycle()
    
    # Second lifecycle with same session
    context2 = manager.start_lifecycle("Query 2")
    print(f"Same session: {context1.session_id == context2.session_id}")
    
    while not manager.is_complete():
        manager.advance_state()
    print(f"Second lifecycle completed: {context2.final_status}")
    
    # Show both histories
    history1 = manager.get_state_history()
    print(f"Combined history length: {len(history1)}")
    
    return context1, context2

def example_error_handling():
    """Demonstrate error handling scenarios."""
    print("\n=== Error Handling Example ===")
    
    manager = LifecycleManager()
    
    # Try to advance without starting lifecycle
    try:
        manager.advance_state()
    except ValueError as e:
        print(f"Correctly caught error: {e}")
    
    # Start lifecycle and try invalid operations
    context = manager.start_lifecycle("Test query")
    
    # Try to trigger recovery without context
    try:
        manager.trigger_recovery("Test")
        print("Recovery trigger succeeded")
    except LifecycleException as e:
        print(f"Recovery error: {e}")
    
    # Test context access
    current_context = manager.get_current_context()
    if current_context:
        print(f"Context access successful: {current_context.session_id}")
    
    # Complete lifecycle
    while not manager.is_complete():
        manager.advance_state()
    
    print(f"Error handling test completed: {context.final_status}")

def run_all_examples():
    """Run all examples in sequence."""
    print("Running 9-State Lifecycle Architecture Examples...\n")
    
    try:
        example_basic_lifecycle()
        example_manual_approval()
        example_recovery_scenario()
        example_state_history_analysis()
        example_loop_back()
        example_error_handling()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        raise

if __name__ == "main__":
    run_all_examples()
