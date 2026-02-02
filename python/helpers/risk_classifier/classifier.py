"""Risk Classification Engine for AnancyIO Governance

Provides expanded risk classification with detailed categories.
"""

import re
from enum import Enum
from typing import Dict, Any, Optional, List
from datetime import datetime

from .exceptions import RiskClassificationError, UnknownRiskError

class RiskLevel(Enum):
    """Expanded risk classification levels."""

    # Original levels
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"

    # New expanded classes
    SAFE_INFO = "safe_info"                    # Safe informational queries
    SYSTEM_META = "system_meta"                # System metadata/diagnostics
    CONFIG_CHANGE = "config_change"            # Configuration modifications
    DATA_ACCESS = "data_access"                # Data retrieval/access
    DUAL_USE_SECURITY = "dual_use_security"    # Security tools with dual use
    PRESSURE_OVERRIDE_ATTEMPT = "pressure_override_attempt"  # Attempts to override safety
    ILLEGAL_OR_HARMFUL = "illegal_or_harmful"  # Illegal or harmful activities

    # Special states
    UNKNOWN = "unknown"                        # Cannot classify - treated as error

class ClassificationResult:
    """Structured result from risk classification.

    Attributes:
        risk_level: The determined risk level
        confidence: Confidence score (0.0-1.0)
        reasoning: List of reasons for classification
        matched_patterns: Patterns that matched the query
        timestamp: When classification was performed
        query_hash: Hash of the input query for tracking
        metadata: Additional classification metadata
    """

    def __init__(self, risk_level: RiskLevel, confidence: float, 
                 reasoning: List[str], matched_patterns: List[str],
                 query_hash: str, metadata: Optional[Dict[str, Any]] = None):
        self.risk_level = risk_level
        self.confidence = confidence
        self.reasoning = reasoning
        self.matched_patterns = matched_patterns
        self.timestamp = datetime.now()
        self.query_hash = query_hash
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'risk_level': self.risk_level.value,
            'confidence': self.confidence,
            'reasoning': self.reasoning,
            'matched_patterns': self.matched_patterns,
            'timestamp': self.timestamp.isoformat(),
            'query_hash': self.query_hash,
            'metadata': self.metadata
        }

    def __str__(self) -> str:
        return f"ClassificationResult(level={self.risk_level.value}, confidence={self.confidence:.2f})"

class RiskClassifier:
    """Main risk classification engine.

    Classifies queries into expanded risk levels using pattern matching
    and keyword analysis. Treats UNKNOWN as a classification error.
    """

    def __init__(self):
        """Initialize classifier with pattern definitions."""
        self.patterns = self._load_patterns()
        self._compiled_patterns = self._compile_patterns()

    def _load_patterns(self) -> Dict[RiskLevel, List[Dict[str, Any]]]:
        """Load classification patterns for each risk level.

        Returns:
            Dictionary mapping risk levels to pattern lists
        """
        return {
            RiskLevel.SAFE_INFO: [
                {
                    'pattern': r'(what|who|when|where|how|why).*\?', 
                    'keywords': ['information', 'about', 'tell me', 'explain'],
                    'reason': 'Informational question'
                },
                {
                    'pattern': r'(help|guide|tutorial|documentation)',
                    'keywords': ['how to', 'learn', 'understand'],
                    'reason': 'Help and learning request'
                }
            ],

            RiskLevel.SYSTEM_META: [
                {
                    'pattern': r'(status|health|diagnostic|system|version|log)',
                    'keywords': ['check', 'monitor', 'inspect', 'view'],
                    'reason': 'System metadata or diagnostics'
                },
                {
                    'pattern': r'(memory|cpu|disk|network|process).*(usage|load|info)',
                    'keywords': ['performance', 'metrics', 'statistics'],
                    'reason': 'System performance monitoring'
                }
            ],

            RiskLevel.CONFIG_CHANGE: [
                {
                    'pattern': r'(change|modify|update|set|configure).*(config|setting|parameter)',
                    'keywords': ['alter', 'adjust', 'customize'],
                    'reason': 'Configuration modification'
                },
                {
                    'pattern': r'(enable|disable|turn on|turn off).*(feature|option|mode)',
                    'keywords': ['switch', 'toggle', 'activate'],
                    'reason': 'Feature toggling'
                }
            ],

            RiskLevel.DATA_ACCESS: [
                {
                    'pattern': r'(access|retrieve|get|fetch|read).*(data|file|database|record)',
                    'keywords': ['download', 'export', 'query', 'search'],
                    'reason': 'Data access request'
                },
                {
                    'pattern': r'(show|display|list|view).*(history|log|record|entry)',
                    'keywords': ['browse', 'examine', 'review'],
                    'reason': 'Data viewing request'
                }
            ],

            RiskLevel.DUAL_USE_SECURITY: [
                {
                    'pattern': r'(hack|penetration|exploit|vulnerability).*(test|tool|scan)',
                    'keywords': ['security', 'ethical', 'research', 'assessment'],
                    'reason': 'Security testing tools'
                },
                {
                    'pattern': r'(encryption|cryptography|password).*(break|crack|recover)',
                    'keywords': ['forensic', 'recovery', 'analysis'],
                    'reason': 'Cryptographic analysis'
                }
            ],

            RiskLevel.PRESSURE_OVERRIDE_ATTEMPT: [
                {
                    'pattern': r'(ignore|override|bypass|force|emergency).*(safety|security|rule|restriction)',
                    'keywords': ['urgent', 'critical', 'must', 'immediately', 'now'],
                    'reason': 'Attempt to override safety measures'
                },
                {
                    'pattern': r'(just do it|trust me|i know what|let me|allow me)',
                    'keywords': ['please', 'begging', 'insisting', 'demanding'],
                    'reason': 'Pressure tactics to bypass controls'
                }
            ],

            RiskLevel.ILLEGAL_OR_HARMFUL: [
                {
                    'pattern': r'(hack|crack|steal|damage|destroy|exploit).*(system|network|data)',
                    'keywords': ['illegal', 'malicious', 'harmful', 'dangerous'],
                    'reason': 'Potentially illegal or harmful activity'
                },
                {
                    'pattern': r'(weapon|nuclear|chemical|biological|bomb|virus)',
                    'keywords': ['create', 'build', 'make', 'develop'],
                    'reason': 'Dangerous or prohibited technology'
                }
            ],

            # Original risk levels with expanded patterns
            RiskLevel.LOW: [
                {
                    'pattern': r'(hello|hi|goodbye|bye|thanks|thank you)',
                    'keywords': ['greeting', 'polite', 'courtesy'],
                    'reason': 'Basic social interaction'
                }
            ],

            RiskLevel.MEDIUM: [
                {
                    'pattern': r'(install|setup|configure|deploy).*(software|tool|application)',
                    'keywords': ['installation', 'deployment', 'setup'],
                    'reason': 'Software installation and setup'
                }
            ],

            RiskLevel.HIGH: [
                {
                    'pattern': r'(delete|remove|erase|destroy).*(file|data|system)',
                    'keywords': ['permanent', 'irreversible', 'dangerous'],
                    'reason': 'High-risk data destruction'
                }
            ],

            RiskLevel.CRITICAL: [
                {
                    'pattern': r'(root|admin|sudo|superuser).*(access|privilege|elevation)',
                    'keywords': ['escalation', 'rootkit', 'backdoor'],
                    'reason': 'Critical system privilege escalation'
                }
            ]
        }

    def _compile_patterns(self) -> Dict[RiskLevel, List[Dict[str, Any]]]:
        """Compile regex patterns for efficiency.

        Returns:
            Dictionary with compiled patterns
        """
        compiled = {}
        for level, patterns in self.patterns.items():
            compiled[level] = []
            for pattern_dict in patterns:
                compiled_pattern = {
                    'pattern': re.compile(pattern_dict['pattern'], re.IGNORECASE),
                    'keywords': pattern_dict['keywords'],
                    'reason': pattern_dict['reason']
                }
                compiled[level].append(compiled_pattern)
        return compiled

    def classify(self, query: str) -> ClassificationResult:
        """Classify a query into a risk level.

        Args:
            query: The query text to classify

        Returns:
            ClassificationResult with risk assessment

        Raises:
            UnknownRiskError: If query cannot be classified
        """
        if not query or not query.strip():
            raise UnknownRiskError(query, "Empty or whitespace-only query")

        query_lower = query.lower()
        query_hash = str(hash(query))  # Simple hash for tracking

        # Track matches for each level
        level_matches = {}
        matched_patterns = []
        reasoning = []

        # Check each risk level
        for level, patterns in self._compiled_patterns.items():
            matches = 0
            level_patterns = []
            level_reasons = []

            for pattern_dict in patterns:
                pattern_match = pattern_dict['pattern'].search(query)
                keyword_match = any(kw in query_lower for kw in pattern_dict['keywords'])

                if pattern_match or keyword_match:
                    matches += 1
                    level_patterns.append(pattern_dict['reason'])
                    level_reasons.append(pattern_dict['reason'])

            if matches > 0:
                level_matches[level] = {
                    'count': matches,
                    'patterns': level_patterns,
                    'reasons': level_reasons
                }

        # Determine best classification
        if not level_matches:
            # No matches found - UNKNOWN state
            raise UnknownRiskError(
                query, 
                "No patterns matched - query cannot be classified into known risk levels"
            )

        # Find level with most matches
        best_level = max(level_matches.keys(), key=lambda l: level_matches[l]['count'])
        best_matches = level_matches[best_level]

        # Calculate confidence based on match strength
        total_matches = sum(m['count'] for m in level_matches.values())
        confidence = min(best_matches['count'] / total_matches, 1.0)

        # If confidence is too low, treat as unknown
        if confidence < 0.3:
            raise UnknownRiskError(
                query,
                f"Low confidence classification ({confidence:.2f}) - insufficient pattern matches"
            )

        matched_patterns = best_matches['patterns']
        reasoning = best_matches['reasons']

        # Create result
        result = ClassificationResult(
            risk_level=best_level,
            confidence=confidence,
            reasoning=reasoning,
            matched_patterns=matched_patterns,
            query_hash=query_hash,
            metadata={
                'total_levels_matched': len(level_matches),
                'best_match_count': best_matches['count'],
                'all_matches': {l.value: m['count'] for l, m in level_matches.items()}
            }
        )

        return result

    def classify_safe(self, query: str) -> Optional[ClassificationResult]:
        """Safe classification that returns None instead of raising exceptions.

        Args:
            query: The query text to classify

        Returns:
            ClassificationResult or None if classification fails
        """
        try:
            return self.classify(query)
        except UnknownRiskError:
            return None

    def get_supported_levels(self) -> List[RiskLevel]:
        """Get list of all supported risk levels.

        Returns:
            List of RiskLevel enums
        """
        return list(self.patterns.keys())

    def get_level_description(self, level: RiskLevel) -> str:
        """Get human-readable description of a risk level.

        Args:
            level: The risk level to describe

        Returns:
            Description string
        """
        descriptions = {
            RiskLevel.LOW: "Low risk - basic operations and queries",
            RiskLevel.MEDIUM: "Medium risk - system modifications and installations",
            RiskLevel.HIGH: "High risk - data destruction and sensitive operations",
            RiskLevel.CRITICAL: "Critical risk - privilege escalation and system compromise",
            RiskLevel.SAFE_INFO: "Safe informational queries",
            RiskLevel.SYSTEM_META: "System metadata and diagnostics",
            RiskLevel.CONFIG_CHANGE: "Configuration modifications",
            RiskLevel.DATA_ACCESS: "Data retrieval and access",
            RiskLevel.DUAL_USE_SECURITY: "Security tools with dual-use potential",
            RiskLevel.PRESSURE_OVERRIDE_ATTEMPT: "Attempts to override safety measures",
            RiskLevel.ILLEGAL_OR_HARMFUL: "Illegal or harmful activities",
            RiskLevel.UNKNOWN: "Cannot classify - treated as error"
        }
        return descriptions.get(level, "Unknown risk level")
