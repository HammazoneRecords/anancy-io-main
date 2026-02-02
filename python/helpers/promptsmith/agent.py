"""PromptSmith Agent - Core Synthesis Logic

Translates raw user requests into MW-PS compliant prompts with explicit governance.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import uuid
import re

from python.helpers.mwps import MWPSPrompt, MWPSTemplate
from .workflow import PromptSmithWorkflow, WorkflowSession, WorkflowState
from .exceptions import PromptSmithError, ValidationError

@dataclass
class SynthesisResult:
    """Result of prompt synthesis.

    Attributes:
        mwps_prompt: Generated MW-PS compliant prompt
        assumptions: Explicit assumptions made during synthesis
        confidence: Confidence score (0.0-1.0)
        alternatives: Alternative interpretations considered
        warnings: Any warnings or concerns
    """
    mwps_prompt: MWPSPrompt
    assumptions: List[str]
    confidence: float
    alternatives: List[str]
    warnings: List[str]

class PromptSmith:
    """Prompt Suitability Agent - Governance Layer for Prompt Creation.

    PromptSmith acts as a governance layer that:
    1. Receives raw user requests
    2. Synthesizes MW-PS compliant prompts
    3. Makes explicit assumptions
    4. Presents prompts for user approval
    5. Loops until acceptance
    6. Forwards only accepted prompts for execution
    """

    def __init__(self):
        self.workflow = PromptSmithWorkflow()
        self.action_verbs = {
            'analyze', 'create', 'generate', 'process', 'execute',
            'validate', 'check', 'verify', 'implement', 'design',
            'develop', 'test', 'deploy', 'monitor', 'report',
            'calculate', 'compute', 'transform', 'convert', 'extract',
            'parse', 'format', 'organize', 'classify', 'categorize',
            'search', 'find', 'locate', 'identify', 'detect',
            'build', 'construct', 'assemble', 'compile', 'install',
            'update', 'modify', 'change', 'edit', 'revise',
            'delete', 'remove', 'clean', 'purge', 'clear'
        }

    def synthesize(self, raw_request: str, session_id: Optional[str] = None) -> SynthesisResult:
        """Synthesize MW-PS compliant prompt from raw request.

        Args:
            raw_request: Raw user request
            session_id: Optional session ID (creates new if not provided)

        Returns:
            SynthesisResult with MW-PS prompt and metadata
        """
        # Create or get session
        if not session_id:
            session_id = str(uuid.uuid4())

        session = self.workflow.create_session(session_id, raw_request)
        session.update_state(WorkflowState.SYNTHESIS)

        # Extract intent
        intent = self._extract_intent(raw_request)

        # Extract instructions
        instructions = self._extract_instructions(raw_request)

        # Identify assumptions
        assumptions = self._identify_assumptions(raw_request, intent, instructions)

        # Determine risk level
        risk_level = self._assess_risk(raw_request, instructions)

        # Generate alternatives
        alternatives = self._generate_alternatives(raw_request, intent)

        # Identify warnings
        warnings = self._identify_warnings(raw_request, instructions, risk_level)

        # Calculate confidence
        confidence = self._calculate_confidence(raw_request, intent, instructions)

        # Create MW-PS prompt based on risk level
        if risk_level in ['HIGH', 'CRITICAL']:
            mwps_prompt = MWPSTemplate.governance(
                intent=intent,
                instructions=instructions,
                risk_level=risk_level,
                approval_required=True,
                audit_trail=True
            )
        else:
            mwps_prompt = MWPSTemplate.standard(
                intent=intent,
                instructions=instructions,
                metadata={
                    'risk_level': risk_level,
                    'session_id': session_id,
                    'synthesized_by': 'PromptSmith v1.0'
                }
            )

        # Store in session
        session.mwps_prompt = mwps_prompt.to_dict()
        session.assumptions = assumptions
        session.update_state(WorkflowState.WITNESS)

        return SynthesisResult(
            mwps_prompt=mwps_prompt,
            assumptions=assumptions,
            confidence=confidence,
            alternatives=alternatives,
            warnings=warnings
        )

    def _extract_intent(self, raw_request: str) -> str:
        """Extract intent from raw request.

        Args:
            raw_request: Raw user request

        Returns:
            Intent declaration
        """
        # Simple heuristic: look for action verbs and objects
        request_lower = raw_request.lower()

        # Find action verbs
        found_verbs = []
        for verb in self.action_verbs:
            if verb in request_lower:
                found_verbs.append(verb)

        if found_verbs:
            # Use first verb as primary action
            primary_verb = found_verbs[0].capitalize()
            # Extract object (simplified)
            words = raw_request.split()
            if len(words) > 2:
                return f"{primary_verb} {' '.join(words[1:])}"
            else:
                return raw_request
        else:
            # No clear verb, use request as-is
            return raw_request

    def _extract_instructions(self, raw_request: str) -> List[str]:
        """Extract actionable instructions from raw request.

        Args:
            raw_request: Raw user request

        Returns:
            List of instructions
        """
        instructions = []

        # Check if request contains explicit steps
        if any(marker in raw_request.lower() for marker in ['step', 'first', 'then', 'finally', '1.', '2.']):
            # Split by common step markers
            lines = raw_request.split('\n')
            for line in lines:
                line = line.strip()
                if line and any(line.startswith(str(i)) for i in range(1, 10)):
                    instructions.append(line)

        # If no explicit steps, create logical breakdown
        if not instructions:
            request_lower = raw_request.lower()

            # Common patterns
            if 'analyze' in request_lower or 'check' in request_lower:
                instructions.extend([
                    "Load and validate input data",
                    "Perform analysis according to requirements",
                    "Generate results and findings",
                    "Present results in requested format"
                ])
            elif 'create' in request_lower or 'generate' in request_lower or 'build' in request_lower:
                instructions.extend([
                    "Understand requirements and specifications",
                    "Design solution architecture",
                    "Implement solution components",
                    "Validate and test implementation",
                    "Deliver final output"
                ])
            elif 'search' in request_lower or 'find' in request_lower:
                instructions.extend([
                    "Define search criteria and scope",
                    "Execute search operation",
                    "Filter and rank results",
                    "Present findings"
                ])
            else:
                # Generic fallback
                instructions.extend([
                    "Parse and understand the request",
                    "Execute the requested operation",
                    "Verify results",
                    "Return output to user"
                ])

        return instructions

    def _identify_assumptions(self, raw_request: str, intent: str, instructions: List[str]) -> List[str]:
        """Identify explicit assumptions made during synthesis.

        Args:
            raw_request: Raw user request
            intent: Extracted intent
            instructions: Extracted instructions

        Returns:
            List of assumptions
        """
        assumptions = []

        # Check for ambiguities
        if len(raw_request.split()) < 5:
            assumptions.append("Request is brief - assuming standard interpretation")

        # Check for missing details
        if 'file' in raw_request.lower() and 'path' not in raw_request.lower():
            assumptions.append("File path not specified - will request or use default location")

        if 'format' not in raw_request.lower() and any(word in raw_request.lower() for word in ['generate', 'create', 'output']):
            assumptions.append("Output format not specified - will use appropriate default")

        # Check for scope
        if not any(word in raw_request.lower() for word in ['all', 'every', 'each', 'specific']):
            assumptions.append("Scope not explicitly defined - assuming reasonable default scope")

        return assumptions

    def _assess_risk(self, raw_request: str, instructions: List[str]) -> str:
        """Assess risk level of request.

        Args:
            raw_request: Raw user request
            instructions: Extracted instructions

        Returns:
            Risk level: LOW, MEDIUM, HIGH, or CRITICAL
        """
        request_lower = raw_request.lower()

        # CRITICAL risk indicators
        critical_keywords = ['delete', 'remove', 'drop', 'destroy', 'wipe', 'format', 'reset']
        if any(keyword in request_lower for keyword in critical_keywords):
            return 'CRITICAL'

        # HIGH risk indicators
        high_keywords = ['modify', 'change', 'update', 'configure', 'install', 'deploy', 'execute']
        if any(keyword in request_lower for keyword in high_keywords):
            return 'HIGH'

        # MEDIUM risk indicators
        medium_keywords = ['create', 'generate', 'build', 'compile', 'process']
        if any(keyword in request_lower for keyword in medium_keywords):
            return 'MEDIUM'

        # Default to LOW
        return 'LOW'

    def _generate_alternatives(self, raw_request: str, intent: str) -> List[str]:
        """Generate alternative interpretations.

        Args:
            raw_request: Raw user request
            intent: Extracted intent

        Returns:
            List of alternative interpretations
        """
        alternatives = []

        # Check for ambiguous terms
        if 'it' in raw_request.lower() or 'this' in raw_request.lower() or 'that' in raw_request.lower():
            alternatives.append("Request contains pronouns - may refer to previous context")

        # Check for multiple possible actions
        request_lower = raw_request.lower()
        action_count = sum(1 for verb in self.action_verbs if verb in request_lower)
        if action_count > 2:
            alternatives.append("Multiple actions detected - may need to prioritize or sequence")

        return alternatives

    def _identify_warnings(self, raw_request: str, instructions: List[str], risk_level: str) -> List[str]:
        """Identify warnings or concerns.

        Args:
            raw_request: Raw user request
            instructions: Extracted instructions
            risk_level: Assessed risk level

        Returns:
            List of warnings
        """
        warnings = []

        if risk_level in ['HIGH', 'CRITICAL']:
            warnings.append(f"⚠️ {risk_level} risk operation - requires explicit approval")

        if 'password' in raw_request.lower() or 'secret' in raw_request.lower():
            warnings.append("⚠️ Request involves sensitive data - ensure proper handling")

        if len(instructions) > 10:
            warnings.append("⚠️ Complex operation with many steps - consider breaking into subtasks")

        return warnings

    def _calculate_confidence(self, raw_request: str, intent: str, instructions: List[str]) -> float:
        """Calculate confidence score for synthesis.

        Args:
            raw_request: Raw user request
            intent: Extracted intent
            instructions: Extracted instructions

        Returns:
            Confidence score (0.0-1.0)
        """
        confidence = 1.0

        # Reduce confidence for ambiguities
        if len(raw_request.split()) < 5:
            confidence -= 0.2

        if 'it' in raw_request.lower() or 'this' in raw_request.lower():
            confidence -= 0.1

        if not any(verb in raw_request.lower() for verb in self.action_verbs):
            confidence -= 0.3

        return max(0.0, min(1.0, confidence))

    def format_for_user(self, result: SynthesisResult) -> str:
        """Format synthesis result for user presentation.

        Args:
            result: SynthesisResult to format

        Returns:
            Formatted string for user
        """
        output = []
        output.append("# PromptSmith - Prompt Synthesis Result")
        output.append("")
        output.append(f"**Confidence:** {result.confidence:.0%}")
        output.append("")

        # Warnings
        if result.warnings:
            output.append("## ⚠️ Warnings")
            for warning in result.warnings:
                output.append(f"- {warning}")
            output.append("")

        # MW-PS Prompt
        output.append("## Generated MW-PS Prompt")
        output.append("")
        output.append(result.mwps_prompt.to_text())
        output.append("")

        # Assumptions
        if result.assumptions:
            output.append("## Explicit Assumptions")
            for assumption in result.assumptions:
                output.append(f"- {assumption}")
            output.append("")

        # Alternatives
        if result.alternatives:
            output.append("## Alternative Interpretations")
            for alt in result.alternatives:
                output.append(f"- {alt}")
            output.append("")

        # User options
        output.append("## Your Options")
        output.append("")
        output.append("**ACCEPT** - Proceed with this prompt as-is")
        output.append("**ADJUST** - Provide feedback to refine the prompt")
        output.append("**REJECT** - Cancel this request")
        output.append("")
        output.append("Please respond with your choice and any feedback.")

        return "\n".join(output)
