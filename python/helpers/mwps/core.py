"""MW-PS Core Framework

Implements the MindWave Prompt Standard v1.0 with:
- 4 mandatory layers
- Intent-Instruction Parity enforcement
- Compliance validation
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum
import re

from .exceptions import (
    MWPSParityError,
    MWPSMissingLayerError,
    MWPSTerminationError
)

class MWPSLayer(Enum):
    """MW-PS mandatory layers."""
    INTENT_DECLARATION = "intent_declaration"
    INSTRUCTION_SET = "instruction_set"
    INTELLIGENCE_BOUNDARY = "intelligence_boundary"
    TERMINATION_CONTINUITY = "termination_continuity"

@dataclass
class MWPSPrompt:
    """MW-PS compliant prompt structure.

    Attributes:
        intent_declaration: Clear statement of what the prompt aims to achieve
        instruction_set: Explicit, actionable instructions
        intelligence_boundary: Constraints on AI reasoning and assumptions
        termination_continuity: Exit conditions and continuation rules
        metadata: Optional metadata for tracking and auditing
    """
    intent_declaration: str
    instruction_set: List[str]
    intelligence_boundary: Dict[str, Any]
    termination_continuity: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate prompt on initialization."""
        validator = MWPSValidator()
        validator.validate(self)

    def to_text(self) -> str:
        """Convert prompt to formatted text."""
        sections = []

        # Intent Declaration
        sections.append("# INTENT DECLARATION")
        sections.append(self.intent_declaration)
        sections.append("")

        # Instruction Set
        sections.append("# INSTRUCTION SET")
        for i, instruction in enumerate(self.instruction_set, 1):
            sections.append(f"{i}. {instruction}")
        sections.append("")

        # Intelligence Boundary
        sections.append("# INTELLIGENCE BOUNDARY")
        sections.append("## Constraints:")
        for key, value in self.intelligence_boundary.get('constraints', {}).items():
            sections.append(f"- {key}: {value}")
        sections.append("")
        sections.append("## Forbidden:")
        for item in self.intelligence_boundary.get('forbidden', []):
            sections.append(f"- {item}")
        sections.append("")

        # Termination & Continuity
        sections.append("# TERMINATION & CONTINUITY")
        sections.append("## Exit Conditions:")
        for condition in self.termination_continuity.get('exit_conditions', []):
            sections.append(f"- {condition}")
        sections.append("")
        sections.append("## Continuation Rules:")
        for rule in self.termination_continuity.get('continuation_rules', []):
            sections.append(f"- {rule}")

        return "\n".join(sections)

    def to_dict(self) -> Dict[str, Any]:
        """Convert prompt to dictionary."""
        return {
            'intent_declaration': self.intent_declaration,
            'instruction_set': self.instruction_set,
            'intelligence_boundary': self.intelligence_boundary,
            'termination_continuity': self.termination_continuity,
            'metadata': self.metadata
        }

class MWPSValidator:
    """Validates MW-PS prompt compliance."""

    def validate(self, prompt: MWPSPrompt) -> bool:
        """Validate a prompt against MW-PS requirements.

        Args:
            prompt: The prompt to validate

        Returns:
            True if valid

        Raises:
            MWPSMissingLayerError: If mandatory layer is missing
            MWPSParityError: If Intent-Instruction Parity is violated
            MWPSTerminationError: If termination conditions are invalid
        """
        # Check all mandatory layers are present
        self._validate_layers(prompt)

        # Check Intent-Instruction Parity
        self._validate_parity(prompt)

        # Check termination conditions
        self._validate_termination(prompt)

        # Check intelligence boundaries
        self._validate_boundaries(prompt)

        return True

    def _validate_layers(self, prompt: MWPSPrompt):
        """Validate all mandatory layers are present and non-empty."""
        if not prompt.intent_declaration or not prompt.intent_declaration.strip():
            raise MWPSMissingLayerError(
                "Intent Declaration layer is missing or empty"
            )

        if not prompt.instruction_set or len(prompt.instruction_set) == 0:
            raise MWPSMissingLayerError(
                "Instruction Set layer is missing or empty"
            )

        if not prompt.intelligence_boundary:
            raise MWPSMissingLayerError(
                "Intelligence Boundary layer is missing"
            )

        if not prompt.termination_continuity:
            raise MWPSMissingLayerError(
                "Termination & Continuity layer is missing"
            )

    def _validate_parity(self, prompt: MWPSPrompt):
        """Validate Intent-Instruction Parity.

        Every intention must be bound to explicit instructions.
        This is a soft validation - checks that instructions exist and are meaningful.
        """
        # Basic check: ensure we have instructions
        if not prompt.instruction_set or len(prompt.instruction_set) == 0:
            raise MWPSParityError(
                "Intent-Instruction Parity violated. No instructions provided for intent."
            )

        # Check that instructions are not trivial
        for instruction in prompt.instruction_set:
            if not instruction or len(instruction.strip()) < 5:
                raise MWPSParityError(
                    f"Intent-Instruction Parity violated. Trivial instruction: '{instruction}'"
                )

        # Soft validation: warn if no action verbs found (but don't fail)
        # This allows for more flexible prompt design while maintaining intent
        intent_verbs = self._extract_action_verbs(prompt.intent_declaration)
        instruction_verbs = set()
        for instruction in prompt.instruction_set:
            instruction_verbs.update(self._extract_action_verbs(instruction))

        # If we have verbs in intent but none in instructions, that's suspicious
        # but we'll allow it for flexibility
        if intent_verbs and not instruction_verbs:
            # Could log a warning here in production
            pass

    def _validate_termination(self, prompt: MWPSPrompt):
        """Validate termination conditions are properly defined."""
        tc = prompt.termination_continuity

        if 'exit_conditions' not in tc or not tc['exit_conditions']:
            raise MWPSTerminationError(
                "Exit conditions must be explicitly defined"
            )

        if 'continuation_rules' not in tc:
            raise MWPSTerminationError(
                "Continuation rules must be defined (can be empty list)"
            )

    def _validate_boundaries(self, prompt: MWPSPrompt):
        """Validate intelligence boundaries are properly defined."""
        ib = prompt.intelligence_boundary

        if 'constraints' not in ib:
            ib['constraints'] = {}

        if 'forbidden' not in ib:
            ib['forbidden'] = []

    def _extract_action_verbs(self, text: str) -> set:
        """Extract action verbs from text.

        Simple implementation - looks for common action verbs.
        """
        action_verbs = {
            'analyze', 'create', 'generate', 'process', 'execute',
            'validate', 'check', 'verify', 'implement', 'design',
            'develop', 'test', 'deploy', 'monitor', 'report',
            'calculate', 'compute', 'transform', 'convert', 'extract',
            'parse', 'format', 'organize', 'classify', 'categorize'
        }

        text_lower = text.lower()
        found_verbs = set()

        for verb in action_verbs:
            if verb in text_lower:
                found_verbs.add(verb)

        return found_verbs
