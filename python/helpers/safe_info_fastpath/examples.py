"""
SAFE_INFO Fast Path Usage Examples

Demonstrates efficient processing of SAFE_INFO queries with minimal governance overhead.
"""

from fastpath_manager import FastPathManager
from exceptions import FastPathException
import time

def example_basic_fastpath():
    """Basic fast path execution for eligible queries."""
    print("=== Basic Fast Path Example ===")
    
    fastpath = FastPathManager()
    
    # Example SAFE_INFO queries
    safe_queries = [
        "What is the current date?",
        "Show system status",
        "List available commands",
        "What is 2 + 2?",
        "Display help information"
    ]
    
    for query in safe_queries:
        # Simulate classification (would come from risk classifier)
        classification = {
            'risk_level': 'LOW',
            'type': 'SAFE_INFO',
            'confidence': 0.95,
            'processing_time_ms': 45
        }
        
        # Check eligibility
        if fastpath.is_eligible(query, classification):
            print(f"✅ '{query}' eligible for fast path")
            
            # Execute via fast path
            start_time = time.time()
            result = fastpath.execute_fastpath(query, classification)
            execution_time = (time.time() - start_time) * 1000
            
            print(f"   Result: {result.result}")
            print(f"   Fast path time: {execution_time:.1f}ms")
            print(f"   Integrity verified: {fastpath.validate_result(result)}")
            print(f"   Witness logged: {result.witness_log_id is not None}")
        else:
            print(f"❌ '{query}' not eligible for fast path")
        print()
    
    return len(safe_queries)

def example_ineligible_queries():
    """Demonstrate queries that are not eligible for fast path."""
    print("=== Ineligible Queries Example ===")
    
    fastpath = FastPathManager()
    
    # Queries that should NOT use fast path
    ineligible_queries = [
        ("Delete all files", {'risk_level': 'CRITICAL', 'type': 'ILLEGAL_OR_HARMFUL'}),
        ("Execute system command", {'risk_level': 'HIGH', 'type': 'SYSTEM_MODIFICATION'}),
        ("Access user data", {'risk_level': 'MEDIUM', 'type': 'DATA_ACCESS'}),
        ("Low confidence query", {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.7})
    ]
    
    for query, classification in ineligible_queries:
        eligible = fastpath.is_eligible(query, classification)
        print(f"Query: '{query}'")
        print(f"Classification: {classification}")
        print(f"Eligible: {eligible} {'❌ (correctly rejected)' if not eligible else '✅ (should be rejected)'}")
        
        if not eligible:
            # Attempt fallback trigger
            try:
                fallback_success = fastpath.trigger_fallback(query, "Not eligible for fast path")
                print(f"Fallback triggered: {fallback_success}")
            except FastPathException as e:
                print(f"Fallback error: {e}")
        print()
    
    return len(ineligible_queries)

def example_fallback_scenarios():
    """Demonstrate fallback to full governance when fast path fails."""
    print("=== Fallback Scenarios Example ===")
    
    fastpath = FastPathManager()
    
    # Scenario 1: Fast path execution failure
    print("Scenario 1: Execution failure")
    query = "Complex calculation that might fail"
    classification = {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.95}
    
    try:
        result = fastpath.execute_fastpath(query, classification)
        if not result.success:
            print("Fast path execution failed, triggering fallback...")
            fallback_success = fastpath.trigger_fallback(query, "Execution failed")
            print(f"Fallback to full governance: {fallback_success}")
    except FastPathException as e:
        print(f"Exception caught, fallback triggered: {e}")
    
    # Scenario 2: Integrity validation failure
    print("\nScenario 2: Integrity validation failure")
    query = "Data integrity test"
    
    result = fastpath.execute_fastpath(query, classification)
    # Simulate integrity check failure
    result.integrity_hash = "tampered_hash"  # Would normally be validated
    
    is_valid = fastpath.validate_result(result)
    if not is_valid:
        print("Integrity check failed, triggering security response...")
        fallback_success = fastpath.trigger_fallback(query, "Integrity validation failed")
        print(f"Security fallback: {fallback_success}")
    
    return True

def example_performance_comparison():
    """Compare fast path vs full governance performance."""
    print("=== Performance Comparison Example ===")
    
    fastpath = FastPathManager()
    
    query = "What time is it?"
    classification = {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.95}
    
    # Measure fast path performance
    print("Measuring fast path performance...")
    fastpath_times = []
    for i in range(10):
        start_time = time.time()
        result = fastpath.execute_fastpath(query, classification)
        execution_time = (time.time() - start_time) * 1000
        fastpath_times.append(execution_time)
        time.sleep(0.01)  # Small delay between tests
    
    avg_fastpath = sum(fastpath_times) / len(fastpath_times)
    print(f"Fast path average: {avg_fastpath:.1f}ms")
    print(f"Fast path range: {min(fastpath_times):.1f}ms - {max(fastpath_times):.1f}ms")
    
    # Simulate full governance time (would be measured in real implementation)
    # Full governance typically takes 500-2000ms through 9 states
    simulated_full_governance = 750  # ms
    
    print(f"\nSimulated full governance: {simulated_full_governance}ms")
    print(f"Performance improvement: {((simulated_full_governance - avg_fastpath) / simulated_full_governance * 100):.1f}%")
    
    return avg_fastpath

def example_batch_processing():
    """Demonstrate batch processing of multiple SAFE_INFO queries."""
    print("=== Batch Processing Example ===")
    
    fastpath = FastPathManager()
    
    # Batch of SAFE_INFO queries
    batch_queries = [
        ("Date", {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.95}),
        ("Time", {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.94}),
        ("Status", {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.96}),
        ("Help", {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.93}),
        ("Info", {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.97})
    ]
    
    print("Processing batch of SAFE_INFO queries...")
    batch_results = []
    
    for query, classification in batch_queries:
        if fastpath.is_eligible(query, classification):
            result = fastpath.execute_fastpath(query, classification)
            batch_results.append(result)
            print(f"✅ {query}: {result.result} ({result.execution_time:.1f}ms)")
        else:
            print(f"❌ {query}: Not eligible")
    
    # Batch statistics
    successful = sum(1 for r in batch_results if r.success)
    total_time = sum(r.execution_time for r in batch_results)
    avg_time = total_time / len(batch_results) if batch_results else 0
    
    print(f"\nBatch Statistics:")
    print(f"Total queries: {len(batch_queries)}")
    print(f"Successful: {successful}")
    print(f"Total time: {total_time:.1f}ms")
    print(f"Average time: {avg_time:.1f}ms per query")
    
    return batch_results

def example_error_handling():
    """Demonstrate error handling in fast path operations."""
    print("=== Error Handling Example ===")
    
    fastpath = FastPathManager()
    
    # Test various error scenarios
    test_cases = [
        ("Valid query", {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.95}, "Should succeed"),
        ("Invalid classification", {'risk_level': 'UNKNOWN'}, "Should fail eligibility"),
        ("Empty query", {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.95}, "Should handle gracefully"),
        ("Low confidence", {'risk_level': 'LOW', 'type': 'SAFE_INFO', 'confidence': 0.5}, "Should fail eligibility")
    ]
    
    for query, classification, expected in test_cases:
        print(f"Testing: {query} - {expected}")
        
        try:
            if fastpath.is_eligible(query, classification):
                result = fastpath.execute_fastpath(query, classification)
                print(f"   Result: {'Success' if result.success else 'Failed'} - {result.result}")
            else:
                print("   Not eligible for fast path")
                fastpath.trigger_fallback(query, "Not eligible")
        except FastPathException as e:
            print(f"   Exception: {type(e).__name__}: {e}")
        except Exception as e:
            print(f"   Unexpected error: {e}")
        
        print()
    
    return len(test_cases)

def run_all_examples():
    """Run all examples in sequence."""
    print("Running SAFE_INFO Fast Path Examples...\n")
    
    try:
        example_basic_fastpath()
        example_ineligible_queries()
        example_fallback_scenarios()
        example_performance_comparison()
        example_batch_processing()
        example_error_handling()
        
        print("\n✅ All examples completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        raise

if __name__ == "__main__":
    run_all_examples()
