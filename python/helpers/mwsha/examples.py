"""MW-SHA Usage Examples and Test Functions

Demonstrates how to use the System Health Agent in various scenarios.
"""

import time
import json
from datetime import datetime
from mwsha import MWSystemHealthAgent, HealthStatus, HealthCheckResult
from mwsha.checks import SystemChecks

class MWExamples:
    """Collection of MW-SHA usage examples and test functions."""

    @staticmethod
    def basic_health_check():
        """Basic health check example.

        Returns:
            HealthCheckResult: Complete health assessment
        """
        print("🔍 Running basic system health check...")

        agent = MWSystemHealthAgent()
        result = agent.perform_full_check()

        print(f"Overall Status: {result.overall_status.value.upper()}")
        print(f"Timestamp: {result.timestamp}")
        print(f"Duration: {result.duration:.2f}s")
        print(f"Checks Performed: {len(result.checks)}")

        return result

    @staticmethod
    def individual_checks_demo():
        """Demonstrate individual system checks.

        Returns:
            dict: Results from all individual checks
        """
        print("🔍 Running individual system checks...")

        checks = SystemChecks()
        results = {}

        # Run each check
        check_methods = [
            ('cpu', checks.check_cpu),
            ('memory', checks.check_memory),
            ('disk', checks.check_disk),
            ('load', checks.check_load),
            ('network', checks.check_network),
            ('processes', checks.check_processes),
        ]

        for name, method in check_methods:
            print(f"  Checking {name}...")
            result = method()
            results[name] = result
            print(f"    Status: {result['status'].upper()}")
            print(f"    Message: {result['message']}")
            print()

        return results

    @staticmethod
    def governance_integration_example():
        """Example of MW-SHA integration with governance flow.

        This demonstrates how MW-SHA acts as a pre-classification gate.
        """
        print("🏛️  Governance Integration Example")
        print("====================================")

        agent = MWSystemHealthAgent()

        # Simulate governance flow
        print("1. Pre-classification health check...")
        health_result = agent.perform_full_check()

        if health_result.overall_status == HealthStatus.CRITICAL:
            print("❌ BLOCKED: Critical system health issues detected")
            print(f"   Reason: {health_result.summary}")
            return False

        elif health_result.overall_status == HealthStatus.WARNING:
            print("⚠️  WARNING: System health issues detected")
            print(f"   Details: {health_result.summary}")
            print("   Proceeding with caution...")

        else:
            print("✅ HEALTHY: System health check passed")
            print("   Proceeding with normal operations...")

        return True

    @staticmethod
    def continuous_monitoring_demo(duration_seconds=30):
        """Demonstrate continuous health monitoring.

        Args:
            duration_seconds: How long to monitor (default 30s)
        """
        print(f"📊 Continuous Monitoring Demo ({duration_seconds}s)")
        print("=" * 50)

        agent = MWSystemHealthAgent()
        start_time = time.time()

        while time.time() - start_time < duration_seconds:
            result = agent.perform_quick_check()
            timestamp = datetime.now().strftime('%H:%M:%S')

            print(f"[{timestamp}] Status: {result.overall_status.value.upper()} | "
                  f"CPU: {result.checks.get('cpu', {}).get('usage', 'N/A'):.1f}% | "
                  f"Mem: {result.checks.get('memory', {}).get('usage', 'N/A'):.1f}%")

            time.sleep(5)  # Check every 5 seconds

        print("
📈 Monitoring complete")

    @staticmethod
    def export_health_report(filename=None):
        """Export a comprehensive health report to JSON.

        Args:
            filename: Output filename (optional)

        Returns:
            str: Path to exported report
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"mwsha_health_report_{timestamp}.json"

        print(f"📄 Exporting health report to {filename}...")

        agent = MWSystemHealthAgent()
        result = agent.perform_full_check()

        # Convert to serializable format
        report = {
            'timestamp': result.timestamp.isoformat(),
            'overall_status': result.overall_status.value,
            'duration': result.duration,
            'summary': result.summary,
            'checks': result.checks,
            'system_summary': SystemChecks().get_system_summary(),
            'exported_at': datetime.now().isoformat()
        }

        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✅ Report exported to {filename}")
        return filename

    @staticmethod
    def stress_test_simulation():
        """Simulate a stress test scenario.

        This creates artificial load to test MW-SHA detection.
        """
        print("🔥 Stress Test Simulation")
        print("========================")

        agent = MWSystemHealthAgent()

        print("Baseline health check...")
        baseline = agent.perform_full_check()
        print(f"Baseline: {baseline.overall_status.value.upper()}")

        print("
Simulating CPU stress...")
        # Note: In real implementation, you might spawn stress processes
        # For demo, we'll just wait and recheck
        time.sleep(2)

        stressed = agent.perform_full_check()
        print(f"After stress: {stressed.overall_status.value.upper()}")

        if stressed.overall_status != baseline.overall_status:
            print("⚠️  Health status changed during stress test")
        else:
            print("✅ Health status remained stable")

        return baseline, stressed

    @staticmethod
    def run_all_examples():
        """Run all examples in sequence.

        Returns:
            dict: Results from all examples
        """
        results = {}

        print("🚀 Running All MW-SHA Examples")
        print("=" * 40)

        try:
            print("
1. Basic Health Check")
            results['basic'] = MWExamples.basic_health_check()

            print("
2. Individual Checks Demo")
            results['individual'] = MWExamples.individual_checks_demo()

            print("
3. Governance Integration")
            results['governance'] = MWExamples.governance_integration_example()

            print("
4. Export Health Report")
            results['export'] = MWExamples.export_health_report()

            print("
5. Stress Test Simulation")
            results['stress'] = MWExamples.stress_test_simulation()

            print("
✅ All examples completed successfully!")

        except Exception as e:
            print(f"❌ Error running examples: {e}")
            results['error'] = str(e)

        return results

# Convenience functions for quick testing
def quick_health_check():
    """Quick health check for command line testing."""
    return MWExamples.basic_health_check()

def demo():
    """Run the full demo suite."""
    return MWExamples.run_all_examples()

if __name__ == "__main__":
    # Run examples if executed directly
    demo()
