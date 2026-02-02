"""PromptSmith Usage Examples

Demonstrates the PromptSmith workflow for prompt synthesis and approval.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from python.helpers.promptsmith import PromptSmith

def example_simple_request():
    """Example: Simple user request."""
    print("="*70)
    print("Example 1: Simple Request")
    print("="*70)

    smith = PromptSmith()
    raw_request = "Analyze the sales data and create a report"

    print(f"
Raw Request: {raw_request}")
    print("
Synthesizing MW-PS prompt...
")

    result = smith.synthesize(raw_request)

    print(smith.format_for_user(result))
    print("
" + "="*70 + "
")

def example_complex_request():
    """Example: Complex multi-step request."""
    print("="*70)
    print("Example 2: Complex Request")
    print("="*70)

    smith = PromptSmith()
    raw_request = """Create a Python script that:
1. Reads CSV files from /data/input
2. Validates the data format
3. Generates summary statistics
4. Exports results to /data/output"""

    print(f"
Raw Request:
{raw_request}")
    print("
Synthesizing MW-PS prompt...
")

    result = smith.synthesize(raw_request)

    print(smith.format_for_user(result))
    print("
" + "="*70 + "
")

def example_high_risk_request():
    """Example: High-risk operation."""
    print("="*70)
    print("Example 3: High-Risk Request")
    print("="*70)

    smith = PromptSmith()
    raw_request = "Delete all temporary files and reset the configuration"

    print(f"
Raw Request: {raw_request}")
    print("
Synthesizing MW-PS prompt...
")

    result = smith.synthesize(raw_request)

    print(smith.format_for_user(result))
    print("
" + "="*70 + "
")

def example_ambiguous_request():
    """Example: Ambiguous request with assumptions."""
    print("="*70)
    print("Example 4: Ambiguous Request")
    print("="*70)

    smith = PromptSmith()
    raw_request = "Process it and send the results"

    print(f"
Raw Request: {raw_request}")
    print("
Synthesizing MW-PS prompt...
")

    result = smith.synthesize(raw_request)

    print(smith.format_for_user(result))
    print("
" + "="*70 + "
")

if __name__ == '__main__':
    print("
PromptSmith Examples
" + "="*70 + "
")

    example_simple_request()
    example_complex_request()
    example_high_risk_request()
    example_ambiguous_request()

    print("
✅ All examples completed successfully!")
    print("
PromptSmith demonstrates:")
    print("  ✓ Raw request intake")
    print("  ✓ Intent extraction")
    print("  ✓ Instruction synthesis")
    print("  ✓ Risk assessment")
    print("  ✓ Assumption identification")
    print("  ✓ MW-PS prompt generation")
    print("  ✓ User presentation format")
