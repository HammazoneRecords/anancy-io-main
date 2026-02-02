"""
TCP/TCPC Usage Examples

Demonstrates key functionality of Trajectory Checkpoint Protocol and Controller.
"""

from tcp import TrajectoryCheckpointProtocol
from tcpc import TrajectoryCheckpointController
from exceptions import TCPException, TCPCException

def example_basic_checkpoint():
    """Basic checkpoint creation and management."""
    print("=== Basic Checkpoint Example ===")
    
    tcp = TrajectoryCheckpointProtocol()
    
    # Create a checkpoint
    checkpoint = tcp.create_checkpoint(
        drayl_id='user_session_123',
        state_data={
            'user': 'alice',
            'action': 'login',
            'risk_score': 0.2,
            'timestamp': '2026-01-31T16:50:00Z'
        },
        alignment_score=0.95,
        metadata={'phase': 'authentication', 'version': '1.0'}
    )
    
    print(f"Created checkpoint: {checkpoint.checkpoint_id}")
    print(f"Alignment score: {checkpoint.alignment_score}")
    print(f"State hash: {checkpoint.state_hash[:16]}...")
    
    # Retrieve checkpoint
    retrieved = tcp.get_checkpoint(checkpoint.checkpoint_id)
    if retrieved:
        print(f"Retrieved checkpoint matches: {retrieved.checkpoint_id == checkpoint.checkpoint_id}")
    
    # List checkpoints for Drayl
    checkpoints = tcp.list_checkpoints('user_session_123')
    print(f"Total checkpoints for Drayl: {len(checkpoints)}")
    
    return checkpoint

def example_compliance_orchestration():
    """Compliance hook registration and trajectory validation."""
    print("\n=== Compliance Orchestration Example ===")
    
    tcpc = TrajectoryCheckpointController()
    
    # Register compliance hooks
    def risk_threshold_check(state_data):
        """Check if risk score is below threshold."""
        return state_data.get('risk_score', 1.0) < 0.8
    
    def alignment_minimum_check(checkpoint):
        """Check if alignment score meets minimum."""
        return checkpoint.alignment_score > 0.7
    
    tcpc.register_compliance_hook('risk_check', risk_threshold_check)
    tcpc.register_compliance_hook('alignment_check', alignment_minimum_check)
    
    print("Registered compliance hooks: risk_check, alignment_check")
    
    # Sample trajectory
    trajectory = [
        {'action': 'user_input', 'risk_score': 0.3, 'data': 'login request'},
        {'action': 'validation', 'risk_score': 0.1, 'data': 'credentials ok'},
        {'action': 'processing', 'risk_score': 0.5, 'data': 'session created'},
        {'action': 'output', 'risk_score': 0.2, 'data': 'login successful'}
    ]
    
    # Validate trajectory
    is_compliant = tcpc.validate_trajectory(trajectory)
    print(f"Trajectory compliance: {is_compliant}")
    
    if not is_compliant:
        print("Non-compliant trajectory detected - would trigger Protocol of Return")
    
    return is_compliant

def example_forensic_analysis():
    """Query and analyze checkpoint history."""
    print("\n=== Forensic Analysis Example ===")
    
    tcp = TrajectoryCheckpointProtocol()
    tcpc = TrajectoryCheckpointController()
    
    # Create multiple checkpoints for demonstration
    for i in range(3):
        tcp.create_checkpoint(
            drayl_id='analysis_session_456',
            state_data={'step': i, 'action': f'phase_{i}', 'risk': 0.1 * i},
            alignment_score=0.9 - 0.05 * i,
            metadata={'iteration': i}
        )
    
    # Query trajectory
    history = tcpc.query_trajectory('analysis_session_456')
    print(f"Found {len(history)} checkpoints in history")
    
    # Get alignment history
    alignment_history = tcp.get_alignment_history('analysis_session_456')
    print("Alignment score history:")
    for entry in alignment_history:
        print(f"  {entry['timestamp'][:19]}: {entry['alignment_score']:.2f}")
    
    return history

def example_protocol_of_return():
    """Demonstrate Protocol of Return execution."""
    print("\n=== Protocol of Return Example ===")
    
    tcpc = TrajectoryCheckpointController()
    tcp = TrajectoryCheckpointProtocol()
    
    # Create a checkpoint
    checkpoint = tcp.create_checkpoint(
        drayl_id='recovery_test_789',
        state_data={'status': 'stable', 'integrity': 'verified'},
        alignment_score=0.98,
        metadata={'recovery_point': True}
    )
    
    print(f"Created recovery checkpoint: {checkpoint.checkpoint_id}")
    
    # Simulate system state change (would normally be detected)
    current_state = {'status': 'compromised', 'integrity': 'failed'}
    
    # Execute Protocol of Return
    try:
        result = tcpc.execute_protocol_of_return('recovery_test_789')
        print(f"Protocol of Return executed: {result['success']}")
        print(f"Recovered to checkpoint: {result['checkpoint_id']}")
    except TCPCException as e:
        print(f"Protocol of Return failed: {e}")
    
    return result if 'result' in locals() else None

def example_error_handling():
    """Demonstrate error handling scenarios."""
    print("\n=== Error Handling Example ===")
    
    tcp = TrajectoryCheckpointProtocol()
    
    # Try to get non-existent checkpoint
    try:
        checkpoint = tcp.get_checkpoint('non_existent_id')
        if checkpoint is None:
            print("Correctly handled missing checkpoint (returned None)")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    # Try to verify against wrong state
    checkpoint = tcp.create_checkpoint(
        drayl_id='verification_test',
        state_data={'test': 'original'},
        alignment_score=0.9
    )
    
    wrong_state = {'test': 'modified'}
    is_valid = tcp.verify_checkpoint(checkpoint, wrong_state)
    print(f"Verification against wrong state: {is_valid} (should be False)")
    
    correct_state = {'test': 'original'}
    is_valid = tcp.verify_checkpoint(checkpoint, correct_state)
    print(f"Verification against correct state: {is_valid} (should be True)")

def run_all_examples():
    """Run all examples in sequence."""
    print("Running TCP/TCPC Examples...\n")
    
    try:
        example_basic_checkpoint()
        example_compliance_orchestration()
        example_forensic_analysis()
        example_protocol_of_return()
        example_error_handling()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        raise

if __name__ == "__main__":
    run_all_examples()
