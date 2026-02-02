"""MW-PS Template System

Provides templates for creating MW-PS compliant prompts.
"""

from typing import Dict, List, Any, Optional
from .core import MWPSPrompt

class MWPSTemplate:
    """Template builder for MW-PS prompts."""

    @staticmethod
    def minimal(intent: str, instructions: List[str]) -> MWPSPrompt:
        """Create a minimal MW-PS compliant prompt.

        Args:
            intent: The intent declaration
            instructions: List of instructions

        Returns:
            MWPSPrompt with minimal required fields
        """
        return MWPSPrompt(
            intent_declaration=intent,
            instruction_set=instructions,
            intelligence_boundary={
                'constraints': {
                    'no_assumptions': 'Do not make assumptions beyond provided data',
                    'explicit_only': 'Only execute explicitly stated instructions'
                },
                'forbidden': [
                    'Implied intelligence or reasoning',
                    'Actions not explicitly instructed'
                ]
            },
            termination_continuity={
                'exit_conditions': [
                    'All instructions completed',
                    'Error encountered that prevents completion'
                ],
                'continuation_rules': [
                    'Await further instructions after completion'
                ]
            }
        )

    @staticmethod
    def standard(
        intent: str,
        instructions: List[str],
        constraints: Optional[Dict[str, str]] = None,
        forbidden: Optional[List[str]] = None,
        exit_conditions: Optional[List[str]] = None,
        continuation_rules: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> MWPSPrompt:
        """Create a standard MW-PS compliant prompt with custom fields.

        Args:
            intent: The intent declaration
            instructions: List of instructions
            constraints: Custom constraints (optional)
            forbidden: Custom forbidden items (optional)
            exit_conditions: Custom exit conditions (optional)
            continuation_rules: Custom continuation rules (optional)
            metadata: Custom metadata (optional)

        Returns:
            MWPSPrompt with specified fields
        """
        # Default constraints
        default_constraints = {
            'no_assumptions': 'Do not make assumptions beyond provided data',
            'explicit_only': 'Only execute explicitly stated instructions',
            'verify_before_action': 'Verify understanding before executing'
        }

        # Merge with custom constraints
        final_constraints = default_constraints.copy()
        if constraints:
            final_constraints.update(constraints)

        # Default forbidden items
        default_forbidden = [
            'Implied intelligence or reasoning',
            'Actions not explicitly instructed',
            'Assumptions about user intent'
        ]

        # Merge with custom forbidden
        final_forbidden = default_forbidden.copy()
        if forbidden:
            final_forbidden.extend(forbidden)

        # Default exit conditions
        default_exit = [
            'All instructions completed successfully',
            'Error encountered that prevents completion',
            'User requests termination'
        ]

        final_exit = exit_conditions if exit_conditions else default_exit

        # Default continuation rules
        default_continuation = [
            'Await further instructions after completion',
            'Report status and await confirmation'
        ]

        final_continuation = continuation_rules if continuation_rules else default_continuation

        return MWPSPrompt(
            intent_declaration=intent,
            instruction_set=instructions,
            intelligence_boundary={
                'constraints': final_constraints,
                'forbidden': final_forbidden
            },
            termination_continuity={
                'exit_conditions': final_exit,
                'continuation_rules': final_continuation
            },
            metadata=metadata or {}
        )

    @staticmethod
    def governance(
        intent: str,
        instructions: List[str],
        risk_level: str,
        approval_required: bool = True,
        audit_trail: bool = True
    ) -> MWPSPrompt:
        """Create a governance-focused MW-PS prompt.

        Args:
            intent: The intent declaration
            instructions: List of instructions
            risk_level: Risk level (LOW, MEDIUM, HIGH, CRITICAL)
            approval_required: Whether approval is required
            audit_trail: Whether to maintain audit trail

        Returns:
            MWPSPrompt with governance controls
        """
        constraints = {
            'no_assumptions': 'Do not make assumptions beyond provided data',
            'explicit_only': 'Only execute explicitly stated instructions',
            'verify_before_action': 'Verify understanding before executing',
            'risk_level': f'Risk level: {risk_level}',
            'approval_gate': 'User approval required' if approval_required else 'No approval required'
        }

        forbidden = [
            'Implied intelligence or reasoning',
            'Actions not explicitly instructed',
            'Bypassing approval gates',
            'Silent failures or errors'
        ]

        exit_conditions = [
            'All instructions completed successfully',
            'Error encountered that prevents completion',
            'User requests termination',
            'Risk threshold exceeded'
        ]

        continuation_rules = [
            'Await further instructions after completion',
            'Report status and await confirmation',
            'Escalate if risk level changes'
        ]

        metadata = {
            'risk_level': risk_level,
            'approval_required': approval_required,
            'audit_trail': audit_trail,
            'governance_version': '1.0'
        }

        return MWPSPrompt(
            intent_declaration=intent,
            instruction_set=instructions,
            intelligence_boundary={
                'constraints': constraints,
                'forbidden': forbidden
            },
            termination_continuity={
                'exit_conditions': exit_conditions,
                'continuation_rules': continuation_rules
            },
            metadata=metadata
        )
