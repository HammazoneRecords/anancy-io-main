# MW-SHA: System Health Agent v1.0

## Overview

MW-SHA (MindWave System Health Agent) is a pre-classification health check gate for AnancyIO governance. It provides comprehensive system monitoring and health assessment to ensure the AI system operates in a stable environment before processing user requests.

## Features

- **Pre-classification Gate**: Acts as the first line of defense in governance flows
- **Comprehensive Monitoring**: CPU, memory, disk, network, load, and process health
- **Multi-level Status**: Healthy, Warning, Critical, and Error classifications
- **Governance Integration**: Seamless integration with PromptSmith and risk classification
- **Continuous Monitoring**: Support for ongoing health surveillance
- **Export Capabilities**: JSON export for auditing and analysis
- **Exception Handling**: Robust error handling with meaningful diagnostics

## Architecture

```
MW-SHA
├── agent.py          # Main MWSystemHealthAgent class
├── checks.py         # Low-level system monitoring functions
├── exceptions.py     # Custom exception classes
├── examples.py       # Usage examples and demonstrations
└── __init__.py       # Package initialization
```

## Installation

MW-SHA requires the following dependencies:

```bash
pip install psutil
```

For development and testing:

```bash
pip install pytest pytest-cov
```

## Quick Start

### Basic Health Check

```python
from mwsha import MWSystemHealthAgent

# Create agent instance
agent = MWSystemHealthAgent()

# Perform full health check
result = agent.perform_full_check()

print(f"Overall Status: {result.overall_status}")
print(f"Summary: {result.summary}")
```

### Individual System Checks

```python
from mwsha.checks import SystemChecks

checks = SystemChecks()

# Check CPU usage
cpu_result = checks.check_cpu()
print(f"CPU Status: {cpu_result['status']}")
print(f"CPU Usage: {cpu_result['usage']} %")

# Check memory
mem_result = checks.check_memory()
print(f"Memory Status: {mem_result['status']}")
print(f"Available: {mem_result['available_gb']:.1f} GB")
```

## API Reference

### MWSystemHealthAgent

#### Methods

- `perform_full_check() -> HealthCheckResult`
  - Performs comprehensive health assessment
  - Returns: Complete health check result

- `perform_quick_check() -> HealthCheckResult`
  - Performs fast health assessment (subset of checks)
  - Returns: Quick health check result

- `get_health_status() -> HealthStatus`
  - Gets current overall health status
  - Returns: HealthStatus enum value

### HealthCheckResult

#### Attributes

- `overall_status: HealthStatus` - Overall system health
- `timestamp: datetime` - When check was performed
- `duration: float` - Time taken for check (seconds)
- `summary: str` - Human-readable summary
- `checks: dict` - Detailed results from each check

### HealthStatus Enum

- `HEALTHY` - System is operating normally
- `WARNING` - Issues detected, proceed with caution
- `CRITICAL` - Critical issues, block operations
- `ERROR` - Check failed, unable to determine status

### SystemChecks

#### Methods

- `check_cpu() -> dict` - CPU usage and load
- `check_memory() -> dict` - Memory utilization
- `check_disk() -> dict` - Disk space usage
- `check_load() -> dict` - System load average
- `check_network() -> dict` - Network connectivity and latency
- `check_processes() -> dict` - Process health and zombie detection
- `get_system_summary() -> dict` - Basic system information

## Governance Integration

MW-SHA integrates as the first step in the governance flow:

```python
from mwsha import MWSystemHealthAgent, HealthStatus

def governance_precheck():
    """Pre-classification health gate."""
    agent = MWSystemHealthAgent()
    result = agent.perform_full_check()

    if result.overall_status == HealthStatus.CRITICAL:
        raise Exception(f"System health critical: {result.summary}")

    if result.overall_status == HealthStatus.WARNING:
        print(f"Warning: {result.summary}")
        # Log warning but proceed

    return True  # Healthy or warning, proceed
```

## Configuration

MW-SHA uses sensible defaults but can be configured:

```python
# Custom thresholds (future enhancement)
agent = MWSystemHealthAgent(
    cpu_warning_threshold=75.0,
    memory_critical_threshold=95.0,
    # ... other thresholds
)
```

## Examples

### Continuous Monitoring

```python
from mwsha.examples import MWExamples

# Monitor system health for 60 seconds
MWExamples.continuous_monitoring_demo(60)
```

### Export Health Report

```python
from mwsha.examples import MWExamples

# Export comprehensive health report
report_file = MWExamples.export_health_report("system_health.json")
print(f"Report saved to: {report_file}")
```

### Run All Examples

```python
from mwsha.examples import demo

# Run complete demo suite
results = demo()
```

## Health Check Details

### CPU Check
- Monitors CPU usage percentage
- Checks load average normalized by CPU count
- Critical: >90% usage or >200% load
- Warning: >75% usage or >150% load

### Memory Check
- Monitors virtual memory usage
- Critical: >95% usage or <0.5GB available
- Warning: >85% usage or <1.0GB available

### Disk Check
- Monitors root filesystem usage
- Critical: >98% usage or <0.1GB free
- Warning: >95% usage or <0.5GB free

### Network Check
- Tests DNS resolution and HTTP connectivity
- Measures latency to external services
- Critical: DNS failure or >5000ms latency
- Warning: HTTP issues or >2000ms latency

### Process Check
- Monitors for zombie processes
- Critical: >10 zombies detected
- Warning: >5 zombies detected

## Error Handling

MW-SHA provides robust error handling:

```python
from mwsha.exceptions import MWHealthError, MWHealthWarning

try:
    result = agent.perform_full_check()
    if result.overall_status == HealthStatus.ERROR:
        print(f"Health check error: {result.summary}")
except MWHealthError as e:
    print(f"Critical health error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Testing

Run the test suite:

```bash
# Run examples
python -m mwsha.examples

# Run individual tests
python -c "from mwsha.examples import quick_health_check; quick_health_check()"
```

## Performance

- Full check: ~2-3 seconds (includes network tests)
- Quick check: ~0.5-1 second (CPU, memory, disk only)
- Individual checks: ~0.1-0.5 seconds each

## Security Considerations

- MW-SHA only reads system information, no write operations
- No network connections except for health testing
- All data stays local to the system
- No external dependencies for core functionality

## Troubleshooting

### Common Issues

1. **Import Error**: Ensure psutil is installed
   ```bash
   pip install psutil
   ```

2. **Permission Denied**: Some checks may require elevated permissions
   ```bash
   sudo python your_script.py
   ```

3. **Network Check Fails**: May be behind firewall or no internet
   - Network check is optional for basic operation

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Submit pull request

## License

MW-SHA is part of the AnancyIO framework and follows the same license terms.

## Version History

- **v1.0.0** - Initial release
  - Comprehensive system health monitoring
  - Governance integration
  - Full API and documentation

---

*MW-SHA ensures AnancyIO operates in a healthy environment, providing the foundation for reliable AI governance.*
