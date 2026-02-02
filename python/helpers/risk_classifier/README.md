# Risk Classifier: Expanded Risk Assessment v1.0

## Overview

The Risk Classifier is an expanded risk assessment system for AnancyIO governance that classifies user queries into detailed risk levels. It provides granular risk categorization beyond simple LOW/MEDIUM/HIGH/CRITICAL levels, including specialized categories for safe information, system metadata, configuration changes, and security-related queries.

## Key Features

- **Expanded Risk Levels**: 11 distinct risk categories including new specialized classes
- **Pattern-Based Classification**: Uses regex patterns and keyword matching for accurate classification
- **Confidence Scoring**: Provides confidence levels for classification decisions
- **UNKNOWN as Error**: Treats unclassifiable queries as errors requiring fallback routing
- **Governance Integration**: Seamless integration with PromptSmith and MW-SHA
- **Structured Results**: Detailed classification results with reasoning and metadata
- **Exception Handling**: Robust error handling with specific exception types

## Risk Levels

### Original Levels
- **LOW**: Basic operations and greetings
- **MEDIUM**: System installations and modifications
- **HIGH**: Data destruction and sensitive operations
- **CRITICAL**: Privilege escalation and system compromise

### New Expanded Classes
- **SAFE_INFO**: Safe informational queries (what, how, why questions)
- **SYSTEM_META**: System metadata and diagnostics
- **CONFIG_CHANGE**: Configuration modifications and settings
- **DATA_ACCESS**: Data retrieval and viewing operations
- **DUAL_USE_SECURITY**: Security tools with potential dual use
- **PRESSURE_OVERRIDE_ATTEMPT**: Attempts to bypass safety measures
- **ILLEGAL_OR_HARMFUL**: Illegal or harmful activities

### Special States
- **UNKNOWN**: Cannot classify - treated as classification error

## Architecture

```
Risk Classifier
├── classifier.py       # Main RiskClassifier class and logic
├── exceptions.py       # Custom exception classes
├── examples.py         # Usage examples and demonstrations
└── __init__.py         # Package initialization
```

## Installation

The Risk Classifier is part of the AnancyIO helpers package. No additional dependencies required beyond the standard library.

```python
from risk_classifier import RiskClassifier, RiskLevel
from risk_classifier.exceptions import UnknownRiskError
```

## Quick Start

### Basic Classification

```python
from risk_classifier import RiskClassifier

classifier = RiskClassifier()

# Classify a query
result = classifier.classify("What is the current system status?")

print(f"Risk Level: {result.risk_level.value}")
print(f"Confidence: {result.confidence:.2f}")
print(f"Reasoning: {result.reasoning}")
```

### Safe Classification

```python
# Use safe classification to avoid exceptions
result = classifier.classify_safe("Unknown query type")
if result:
    print(f"Classified as: {result.risk_level.value}")
else:
    print("Could not classify - UNKNOWN")
```

## API Reference

### RiskClassifier

#### Methods

- `classify(query: str) -> ClassificationResult`
  - Classifies a query into a risk level
  - Raises: UnknownRiskError if query cannot be classified

- `classify_safe(query: str) -> Optional[ClassificationResult]`
  - Safe classification that returns None instead of raising exceptions

- `get_supported_levels() -> List[RiskLevel]`
  - Returns list of all supported risk levels

- `get_level_description(level: RiskLevel) -> str`
  - Returns human-readable description of a risk level

### ClassificationResult

#### Attributes

- `risk_level: RiskLevel` - The determined risk level
- `confidence: float` - Confidence score (0.0-1.0)
- `reasoning: List[str]` - List of reasons for classification
- `matched_patterns: List[str]` - Patterns that matched the query
- `timestamp: datetime` - When classification was performed
- `query_hash: str` - Hash of the input query
- `metadata: dict` - Additional classification metadata

#### Methods

- `to_dict() -> dict` - Convert to dictionary for serialization

### RiskLevel Enum

Enumeration of all supported risk levels with string values.

### Exceptions

- `RiskClassificationError` - Base exception for classification errors
- `UnknownRiskError` - Raised when query cannot be classified (UNKNOWN state)

## Classification Logic

### Pattern Matching

The classifier uses a combination of:

1. **Regex Patterns**: Compiled regular expressions for structural matching
2. **Keyword Matching**: Case-insensitive keyword presence detection
3. **Reason Templates**: Predefined reasoning strings for each pattern

### Confidence Calculation

- Based on number of pattern matches across all levels
- Normalized by total matches found
- Minimum confidence threshold (0.3) for valid classification
- Queries below threshold treated as UNKNOWN

### UNKNOWN Handling

- Queries that match no patterns are classified as UNKNOWN
- Low-confidence classifications (< 0.3) are also treated as UNKNOWN
- UNKNOWN state raises UnknownRiskError requiring fallback routing
- Governance systems should block or escalate UNKNOWN queries

## Governance Integration

### Basic Integration

```python
from risk_classifier import RiskClassifier, RiskLevel
from risk_classifier.exceptions import UnknownRiskError

def governance_gate(query):
    """Basic governance integration."""
    classifier = RiskClassifier()

    try:
        result = classifier.classify(query)

        # Apply governance rules
        if result.risk_level in [RiskLevel.SAFE_INFO, RiskLevel.SYSTEM_META]:
            return "ALLOW"
        elif result.risk_level in [RiskLevel.CONFIG_CHANGE, RiskLevel.DATA_ACCESS]:
            return "REVIEW"
        elif result.risk_level == RiskLevel.PRESSURE_OVERRIDE_ATTEMPT:
            return "BLOCK - Safety violation"
        else:
            return "RESTRICT"

    except UnknownRiskError:
        return "BLOCK - Cannot classify"
```

### Advanced Integration

```python
def advanced_governance(query, user_context):
    """Advanced governance with user context and confidence."""
    classifier = RiskClassifier()
    result = classifier.classify_safe(query)

    if not result:
        return {
            "decision": "BLOCK",
            "reason": "Cannot classify query",
            "escalate": True
        }

    # Adjust decision based on confidence and user context
    base_decision = get_decision_for_level(result.risk_level)

    if result.confidence < 0.5:
        return {
            "decision": "REVIEW",
            "reason": f"Low confidence classification ({result.confidence:.2f})",
            "escalate": False
        }

    return {
        "decision": base_decision,
        "confidence": result.confidence,
        "reasoning": result.reasoning
    }
```

## Examples

### Basic Demo

```python
from risk_classifier.examples import RiskExamples

# Run basic classification demo
results = RiskExamples.basic_classification_demo()
```

### Governance Demo

```python
from risk_classifier.examples import RiskExamples

# Show governance integration
results = RiskExamples.governance_integration_example()
```

### Export Report

```python
from risk_classifier.examples import RiskExamples

# Export comprehensive classification report
report_file = RiskExamples.export_classification_report()
print(f"Report saved to: {report_file}")
```

### Quick Classification

```python
from risk_classifier.examples import quick_classify

result = quick_classify("Check system health")
print(result)
# {'level': 'system_meta', 'confidence': 0.8, 'reasoning': [...]}
```

## Error Handling

### UNKNOWN Queries

```python
from risk_classifier import RiskClassifier
from risk_classifier.exceptions import UnknownRiskError

classifier = RiskClassifier()

try:
    result = classifier.classify("xyzabc123")
except UnknownRiskError as e:
    print(f"Classification failed: {e.reason}")
    # Implement fallback routing here
```

### General Errors

```python
from risk_classifier.exceptions import RiskClassificationError

try:
    result = classifier.classify(query)
except RiskClassificationError as e:
    print(f"Risk classification error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Performance

- **Classification Speed**: ~0.01-0.05 seconds per query
- **Memory Usage**: Minimal - precompiled patterns
- **Scalability**: Efficient for high-volume classification
- **Thread Safety**: Stateless design supports concurrent use

## Security Considerations

- **No External Calls**: Pure pattern matching, no network access
- **Input Validation**: Handles empty/whitespace queries safely
- **Error Isolation**: Exceptions prevent information leakage
- **Confidence Thresholds**: Prevents overconfident misclassifications

## Testing

### Run Examples

```bash
# Run all examples
python -m risk_classifier.examples

# Run specific demo
python -c "from risk_classifier.examples import demo; demo()"
```

### Unit Testing

```python
import pytest
from risk_classifier import RiskClassifier, RiskLevel

def test_safe_info_classification():
    classifier = RiskClassifier()
    result = classifier.classify("What is the weather?")
    assert result.risk_level == RiskLevel.SAFE_INFO
    assert result.confidence > 0.5

def test_unknown_handling():
    classifier = RiskClassifier()
    with pytest.raises(UnknownRiskError):
        classifier.classify("")
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure risk_classifier is in Python path
   - Check package installation

2. **UNKNOWN Classifications**
   - Review query for typos or unusual phrasing
   - Consider adding new patterns for common queries
   - Check confidence thresholds

3. **Low Confidence Scores**
   - Query matches multiple categories
   - Consider query rephrasing or manual review
   - Adjust confidence thresholds if needed

### Debug Mode

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Classifier will log pattern matches and decisions
result = classifier.classify("test query")
```

## Contributing

1. Add new risk levels to RiskLevel enum
2. Define patterns in _load_patterns() method
3. Add corresponding governance rules
4. Update tests and documentation
5. Submit pull request

## Version History

- **v1.0.0** - Initial release
  - Expanded risk classification system
  - UNKNOWN as error handling
  - Comprehensive API and documentation
  - Governance integration examples

---

*The Risk Classifier provides the foundation for intelligent, context-aware governance in AnancyIO systems.*
