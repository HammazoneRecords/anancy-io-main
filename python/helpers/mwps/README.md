# MindWave Prompt Standard (MW-PS) v1.0

## Overview

The MindWave Prompt Standard (MW-PS) is a structured framework for issuing prompts to AI systems to prevent misalignment and errors through explicit governance.

## Core Principle

**Law of Intent–Instruction Parity**: Every intention must be explicitly bound to an instruction.

## Four Mandatory Layers

### 1. Intent Declaration
Clear statement of what the prompt aims to achieve.

### 2. Instruction Set
Explicit, actionable instructions that implement the intent.

### 3. Intelligence Boundary Declaration
Constraints on AI reasoning and assumptions.

### 4. Termination & Continuity
Exit conditions and continuation rules.

## Installation

```python
from python.helpers.mwps import MWPSPrompt, MWPSTemplate
```

## Quick Start

### Minimal Prompt

```python
from python.helpers.mwps import MWPSTemplate

prompt = MWPSTemplate.minimal(
    intent="Analyze a dataset and generate a summary report",
    instructions=[
        "Load the dataset from the provided path",
        "Calculate basic statistics (mean, median, std dev)",
        "Generate a summary report in markdown format",
        "Save the report to the output directory"
    ]
)

print(prompt.to_text())
```

### Standard Prompt

```python
prompt = MWPSTemplate.standard(
    intent="Process user data and generate recommendations",
    instructions=[
        "Load user profile data",
        "Analyze user preferences",
        "Generate top 5 recommendations",
        "Format as JSON"
    ],
    constraints={
        'data_privacy': 'Do not log personal data',
        'output_format': 'JSON only'
    },
    forbidden=[
        'Accessing data outside user scope'
    ]
)
```

### Governance Prompt

```python
prompt = MWPSTemplate.governance(
    intent="Execute system configuration changes",
    instructions=[
        "Review proposed changes",
        "Validate against policies",
        "Request user approval",
        "Apply changes if approved"
    ],
    risk_level="HIGH",
    approval_required=True,
    audit_trail=True
)
```

## Custom Prompts

```python
from python.helpers.mwps import MWPSPrompt

prompt = MWPSPrompt(
    intent_declaration="Your intent here",
    instruction_set=[
        "Step 1",
        "Step 2",
        "Step 3"
    ],
    intelligence_boundary={
        'constraints': {
            'key': 'value'
        },
        'forbidden': [
            'Forbidden action 1',
            'Forbidden action 2'
        ]
    },
    termination_continuity={
        'exit_conditions': [
            'Condition 1',
            'Condition 2'
        ],
        'continuation_rules': [
            'Rule 1',
            'Rule 2'
        ]
    },
    metadata={
        'version': '1.0',
        'author': 'Your Name'
    }
)
```

## Validation

All prompts are automatically validated on creation:

```python
try:
    prompt = MWPSPrompt(...)
except MWPSValidationError as e:
    print(f"Validation failed: {e}")
```

## Exceptions

- `MWPSValidationError`: Base validation error
- `MWPSParityError`: Intent-Instruction Parity violation
- `MWPSMissingLayerError`: Mandatory layer missing
- `MWPSTerminationError`: Invalid termination conditions

## Testing

```bash
pip install pytest
pytest test_mwps.py -v
```

## Examples

See `examples.py` for complete usage examples:

```bash
python -m python.helpers.mwps.examples
```

## API Reference

### MWPSPrompt

**Attributes:**
- `intent_declaration`: str
- `instruction_set`: List[str]
- `intelligence_boundary`: Dict[str, Any]
- `termination_continuity`: Dict[str, Any]
- `metadata`: Dict[str, Any]

**Methods:**
- `to_text()`: Convert to formatted text
- `to_dict()`: Convert to dictionary

### MWPSTemplate

**Static Methods:**
- `minimal(intent, instructions)`: Create minimal prompt
- `standard(intent, instructions, ...)`: Create standard prompt
- `governance(intent, instructions, risk_level, ...)`: Create governance prompt

### MWPSValidator

**Methods:**
- `validate(prompt)`: Validate prompt compliance

## License

Part of AnancyIO project.

## Version

1.0.0
