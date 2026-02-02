"""MW-PS Unit Tests

Tests for MindWave Prompt Standard implementation.
"""

import pytest
from .core import MWPSPrompt, MWPSValidator
from .templates import MWPSTemplate
from .exceptions import (
    MWPSValidationError,
    MWPSParityError,
    MWPSMissingLayerError,
    MWPSTerminationError
)

class TestMWPSPrompt:
    """Test MWPSPrompt class."""

    def test_valid_prompt_creation(self):
        """Test creating a valid MW-PS prompt."""
        prompt = MWPSPrompt(
            intent_declaration="Test intent",
            instruction_set=["Do this", "Do that"],
            intelligence_boundary={
                'constraints': {'test': 'value'},
                'forbidden': ['something']
            },
            termination_continuity={
                'exit_conditions': ['done'],
                'continuation_rules': ['wait']
            }
        )

        assert prompt.intent_declaration == "Test intent"
        assert len(prompt.instruction_set) == 2

    def test_missing_intent_raises_error(self):
        """Test that missing intent raises error."""
        with pytest.raises(MWPSMissingLayerError):
            MWPSPrompt(
                intent_declaration="",
                instruction_set=["Do this"],
                intelligence_boundary={'constraints': {}, 'forbidden': []},
                termination_continuity={'exit_conditions': ['done'], 'continuation_rules': []}
            )

    def test_missing_instructions_raises_error(self):
        """Test that missing instructions raises error."""
        with pytest.raises(MWPSMissingLayerError):
            MWPSPrompt(
                intent_declaration="Test intent",
                instruction_set=[],
                intelligence_boundary={'constraints': {}, 'forbidden': []},
                termination_continuity={'exit_conditions': ['done'], 'continuation_rules': []}
            )

    def test_missing_termination_raises_error(self):
        """Test that missing termination raises error."""
        with pytest.raises(MWPSTerminationError):
            MWPSPrompt(
                intent_declaration="Test intent",
                instruction_set=["Do this"],
                intelligence_boundary={'constraints': {}, 'forbidden': []},
                termination_continuity={'continuation_rules': []}
            )

    def test_to_text_format(self):
        """Test text formatting."""
        prompt = MWPSTemplate.minimal(
            intent="Test intent",
            instructions=["Step 1", "Step 2"]
        )

        text = prompt.to_text()
        assert "# INTENT DECLARATION" in text
        assert "# INSTRUCTION SET" in text
        assert "# INTELLIGENCE BOUNDARY" in text
        assert "# TERMINATION & CONTINUITY" in text

    def test_to_dict(self):
        """Test dictionary conversion."""
        prompt = MWPSTemplate.minimal(
            intent="Test intent",
            instructions=["Step 1"]
        )

        data = prompt.to_dict()
        assert 'intent_declaration' in data
        assert 'instruction_set' in data
        assert 'intelligence_boundary' in data
        assert 'termination_continuity' in data

class TestMWPSTemplates:
    """Test MW-PS template system."""

    def test_minimal_template(self):
        """Test minimal template creation."""
        prompt = MWPSTemplate.minimal(
            intent="Test intent",
            instructions=["Do this"]
        )

        assert prompt.intent_declaration == "Test intent"
        assert len(prompt.instruction_set) == 1
        assert 'constraints' in prompt.intelligence_boundary
        assert 'exit_conditions' in prompt.termination_continuity

    def test_standard_template(self):
        """Test standard template creation."""
        prompt = MWPSTemplate.standard(
            intent="Test intent",
            instructions=["Do this"],
            constraints={'custom': 'value'},
            metadata={'version': '1.0'}
        )

        assert 'custom' in prompt.intelligence_boundary['constraints']
        assert prompt.metadata['version'] == '1.0'

    def test_governance_template(self):
        """Test governance template creation."""
        prompt = MWPSTemplate.governance(
            intent="Test intent",
            instructions=["Do this"],
            risk_level="HIGH",
            approval_required=True
        )

        assert prompt.metadata['risk_level'] == "HIGH"
        assert prompt.metadata['approval_required'] is True
        assert 'approval_gate' in prompt.intelligence_boundary['constraints']

class TestMWPSValidator:
    """Test MW-PS validator."""

    def test_valid_prompt_passes(self):
        """Test that valid prompt passes validation."""
        prompt = MWPSTemplate.minimal(
            intent="Analyze data",
            instructions=["Load data", "Analyze data"]
        )

        validator = MWPSValidator()
        assert validator.validate(prompt) is True

    def test_parity_validation(self):
        """Test intent-instruction parity validation."""
        # This should pass - 'analyze' is in both intent and instructions
        prompt = MWPSPrompt(
            intent_declaration="Analyze the dataset",
            instruction_set=["Analyze the data"],
            intelligence_boundary={'constraints': {}, 'forbidden': []},
            termination_continuity={'exit_conditions': ['done'], 'continuation_rules': []}
        )

        validator = MWPSValidator()
        assert validator.validate(prompt) is True

if __name__ == '__main__':
    print("Running MW-PS tests...")
    print("Note: Install pytest to run full test suite")
    print("Command: pip install pytest")
    print("Run: pytest test_mwps.py -v")
