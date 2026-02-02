"""MW-PS Usage Examples

Demonstrates how to create and use MW-PS compliant prompts.
"""

from .core import MWPSPrompt
from .templates import MWPSTemplate

def example_minimal():
    """Example: Minimal MW-PS prompt."""
    prompt = MWPSTemplate.minimal(
        intent="Analyze a dataset and generate a summary report",
        instructions=[
            "Load the dataset from the provided path",
            "Calculate basic statistics (mean, median, std dev)",
            "Generate a summary report in markdown format",
            "Save the report to the output directory"
        ]
    )

    print("=== Minimal MW-PS Prompt ===")
    print(prompt.to_text())
    print("
" + "="*50 + "
")

    return prompt

def example_standard():
    """Example: Standard MW-PS prompt with custom fields."""
    prompt = MWPSTemplate.standard(
        intent="Process user data and generate personalized recommendations",
        instructions=[
            "Load user profile data",
            "Analyze user preferences and history",
            "Generate top 5 recommendations",
            "Format recommendations as JSON",
            "Return results to caller"
        ],
        constraints={
            'data_privacy': 'Do not log or store personal data',
            'output_format': 'JSON only, no additional text'
        },
        forbidden=[
            'Accessing data outside user scope',
            'Making recommendations without data support'
        ],
        metadata={
            'version': '1.0',
            'author': 'AnancyIO',
            'created': '2026-01-31'
        }
    )

    print("=== Standard MW-PS Prompt ===")
    print(prompt.to_text())
    print("
" + "="*50 + "
")

    return prompt

def example_governance():
    """Example: Governance-focused MW-PS prompt."""
    prompt = MWPSTemplate.governance(
        intent="Execute system configuration changes",
        instructions=[
            "Review proposed configuration changes",
            "Validate changes against security policies",
            "Request user approval",
            "Apply changes if approved",
            "Log all actions to audit trail"
        ],
        risk_level="HIGH",
        approval_required=True,
        audit_trail=True
    )

    print("=== Governance MW-PS Prompt ===")
    print(prompt.to_text())
    print("
" + "="*50 + "
")

    return prompt

def example_custom():
    """Example: Fully custom MW-PS prompt."""
    prompt = MWPSPrompt(
        intent_declaration="Deploy a machine learning model to production",
        instruction_set=[
            "Validate model performance metrics",
            "Check deployment prerequisites",
            "Create deployment package",
            "Deploy to staging environment",
            "Run integration tests",
            "Deploy to production if tests pass",
            "Monitor deployment for 1 hour"
        ],
        intelligence_boundary={
            'constraints': {
                'environment': 'Production deployment only',
                'rollback': 'Automatic rollback on failure',
                'monitoring': 'Continuous monitoring required'
            },
            'forbidden': [
                'Deploying without validation',
                'Skipping integration tests',
                'Ignoring monitoring alerts'
            ]
        },
        termination_continuity={
            'exit_conditions': [
                'Deployment successful and stable',
                'Deployment failed - rollback completed',
                'User cancels deployment'
            ],
            'continuation_rules': [
                'Continue monitoring after deployment',
                'Report status every 15 minutes',
                'Escalate any anomalies immediately'
            ]
        },
        metadata={
            'deployment_type': 'ML Model',
            'environment': 'Production',
            'risk_level': 'CRITICAL',
            'approval_chain': ['Tech Lead', 'DevOps', 'Security']
        }
    )

    print("=== Custom MW-PS Prompt ===")
    print(prompt.to_text())
    print("
" + "="*50 + "
")

    return prompt

if __name__ == '__main__':
    print("
MW-PS Examples
" + "="*50 + "
")

    example_minimal()
    example_standard()
    example_governance()
    example_custom()

    print("
✅ All examples completed successfully!")
