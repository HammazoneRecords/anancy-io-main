# PromptSmith - Prompt Suitability Agent v1.0

## Overview

PromptSmith is a governance layer that translates raw user requests into MW-PS compliant prompts, preserving user authority and preventing unintended execution.

## Core Principle

**User Authority First**: No execution without explicit user approval of the synthesized prompt.

## Workflow

```
Raw Request → Synthesis → Witness → Feedback → Accept/Adjust/Reject
```

### States

1. **INTAKE** - Receiving raw user request
2. **SYNTHESIS** - Creating MW-PS compliant prompt
3. **WITNESS** - Presenting prompt to user
4. **FEEDBACK** - Receiving user response
5. **REASSESS** - Adjusting based on feedback (if needed)
6. **ACCEPTED** - User approved prompt
7. **REJECTED** - User rejected prompt
8. **RELEASED** - Prompt forwarded for execution

## Features

- **Intent Extraction**: Identifies user's goal from raw request
- **Instruction Synthesis**: Generates actionable steps
- **Risk Assessment**: Classifies requests as LOW, MEDIUM, HIGH, or CRITICAL
- **Assumption Identification**: Makes explicit all assumptions
- **Alternative Generation**: Identifies other possible interpretations
- **Warning Detection**: Flags potential concerns
- **Confidence Scoring**: Rates synthesis quality (0.0-1.0)
- **MW-PS Integration**: Generates compliant prompts automatically

## Installation

```python
from python.helpers.promptsmith import PromptSmith
```

## Quick Start

```python
from python.helpers.promptsmith import PromptSmith

# Create PromptSmith instance
smith = PromptSmith()

# Synthesize prompt from raw request
raw_request = "Analyze the sales data and create a report"
result = smith.synthesize(raw_request)

# Present to user
print(smith.format_for_user(result))

# User responds: ACCEPT, ADJUST, or REJECT
```

## Usage Examples

### Simple Request

```python
smith = PromptSmith()
result = smith.synthesize("Search for Python tutorials")
print(smith.format_for_user(result))
```

### High-Risk Request

```python
smith = PromptSmith()
result = smith.synthesize("Delete all temporary files")
# Automatically flagged as CRITICAL risk
# Requires explicit approval
print(smith.format_for_user(result))
```

### Complex Request

```python
smith = PromptSmith()
raw_request = """Create a script that:
1. Reads data from database
2. Processes records
3. Generates report"""
result = smith.synthesize(raw_request)
print(smith.format_for_user(result))
```

## Synthesis Result

The `synthesize()` method returns a `SynthesisResult` with:

- `mwps_prompt`: MW-PS compliant prompt
- `assumptions`: List of explicit assumptions
- `confidence`: Confidence score (0.0-1.0)
- `alternatives`: Alternative interpretations
- `warnings`: Warnings or concerns

## Risk Levels

- **LOW**: Read-only operations, searches, analysis
- **MEDIUM**: Create, generate, build operations
- **HIGH**: Modify, update, configure, install operations
- **CRITICAL**: Delete, remove, destroy, reset operations

## User Options

After synthesis, users can:

- **ACCEPT** - Proceed with prompt as-is
- **ADJUST** - Provide feedback to refine
- **REJECT** - Cancel the request

## Integration with MW-PS

PromptSmith automatically generates MW-PS compliant prompts:

- LOW/MEDIUM risk → Standard template
- HIGH/CRITICAL risk → Governance template with approval gates

## Workflow Management

```python
from python.helpers.promptsmith import PromptSmithWorkflow, WorkflowState

workflow = PromptSmithWorkflow()
session = workflow.create_session("session-123", "raw request")

# Transition states
workflow.transition("session-123", WorkflowState.SYNTHESIS)
workflow.transition("session-123", WorkflowState.WITNESS)

# Check state
session = workflow.get_session("session-123")
print(session.current_state)
```

## Examples

Run examples:

```bash
python -m python.helpers.promptsmith.examples
```

## API Reference

### PromptSmith

**Methods:**
- `synthesize(raw_request, session_id=None)`: Synthesize MW-PS prompt
- `format_for_user(result)`: Format result for user presentation

### SynthesisResult

**Attributes:**
- `mwps_prompt`: MWPSPrompt
- `assumptions`: List[str]
- `confidence`: float
- `alternatives`: List[str]
- `warnings`: List[str]

### WorkflowSession

**Attributes:**
- `session_id`: str
- `raw_request`: str
- `current_state`: WorkflowState
- `mwps_prompt`: Optional[Dict]
- `assumptions`: List[str]
- `feedback_history`: List[Dict]
- `iteration_count`: int

## License

Part of AnancyIO project.

## Version

1.0.0
