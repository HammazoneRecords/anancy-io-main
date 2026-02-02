# Risk Scorer for Suitability Risk Assessment

"""
Risk Scorer for calculating comprehensive suitability risk scores.

This module evaluates pipeline configurations to determine their suitability
for adversarial exploitation and assigns risk scores with detailed breakdowns.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class RiskLevel(Enum):
    """Risk level classifications."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class SuitabilityRiskScore:
    """Comprehensive risk score assessment."""
    overall_score: float
    breakdown: Dict[str, float]
    risk_level: str
    confidence: float
    assessment_factors: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SuitabilityRiskScore':
        """Create from dictionary."""
        return cls(**data)


class RiskScorer:
    """Engine for calculating suitability risk scores."""

    def __init__(self):
        """Initialize risk scorer."""
        self.risk_factors = self._load_risk_factors()

    def _load_risk_factors(self) -> Dict[str, Any]:
        """Load risk factor definitions."""
        return {
            'authentication': {
                'weight': 0.15,
                'factors': {
                    'multi_factor': -0.3,
                    'weak_passwords': 0.4,
                    'no_auth': 0.8
                }
            },
            'authorization': {
                'weight': 0.15,
                'factors': {
                    'role_based': -0.2,
                    'excessive_permissions': 0.3,
                    'no_authorization': 0.7
                }
            },
            'input_validation': {
                'weight': 0.12,
                'factors': {
                    'sanitization': -0.25,
                    'no_validation': 0.6,
                    'trust_user_input': 0.4
                }
            },
            'data_protection': {
                'weight': 0.12,
                'factors': {
                    'encryption_at_rest': -0.2,
                    'encryption_in_transit': -0.2,
                    'no_encryption': 0.5
                }
            },
            'monitoring': {
                'weight': 0.1,
                'factors': {
                    'comprehensive_logging': -0.3,
                    'no_monitoring': 0.6,
                    'incomplete_coverage': 0.2
                }
            },
            'governance': {
                'weight': 0.15,
                'factors': {
                    'automated_controls': -0.4,
                    'manual_only': 0.5,
                    'no_governance': 0.8
                }
            },
            'supply_chain': {
                'weight': 0.1,
                'factors': {
                    'verified_dependencies': -0.2,
                    'untrusted_sources': 0.4,
                    'no_verification': 0.6
                }
            },
            'infrastructure': {
                'weight': 0.11,
                'factors': {
                    'isolated_networks': -0.3,
                    'public_exposure': 0.5,
                    'no_segmentation': 0.4
                }
            }
        }

    def calculate_suitability_score(self, pipeline_config: Dict[str, Any], 
                                   analysis_mode: Any, context: Dict[str, Any]) -> SuitabilityRiskScore:
        """Calculate comprehensive suitability risk score.

        Args:
            pipeline_config: Pipeline configuration to analyze
            analysis_mode: Analysis mode (affects scoring)
            context: Additional context for scoring

        Returns:
            Comprehensive risk score assessment
        """
        try:
            # Calculate individual factor scores
            factor_scores = {}
            total_weighted_score = 0.0
            total_weight = 0.0

            for factor_name, factor_config in self.risk_factors.items():
                factor_score = self._calculate_factor_score(factor_name, factor_config, pipeline_config)
                factor_scores[factor_name] = factor_score

                weight = factor_config['weight']
                total_weighted_score += factor_score * weight
                total_weight += weight

            # Normalize overall score
            overall_score = total_weighted_score / total_weight if total_weight > 0 else 0.5
            overall_score = max(0.0, min(1.0, overall_score))

            # Determine risk level
            risk_level = self._determine_risk_level(overall_score)

            # Calculate confidence based on available data
            confidence = self._calculate_confidence(pipeline_config, factor_scores)

            # Assessment factors
            assessment_factors = {
                'analysis_mode': str(analysis_mode),
                'pipeline_type': pipeline_config.get('type', 'unknown'),
                'security_features_count': len([k for k, v in factor_scores.items() if v < 0.3]),
                'vulnerability_count': len([k for k, v in factor_scores.items() if v > 0.7]),
                'context_influences': context
            }

            return SuitabilityRiskScore(
                overall_score=overall_score,
                breakdown=factor_scores,
                risk_level=risk_level,
                confidence=confidence,
                assessment_factors=assessment_factors
            )

        except Exception as e:
            # Return default score on error
            return SuitabilityRiskScore(
                overall_score=0.5,
                breakdown={'error': 0.5},
                risk_level='MEDIUM',
                confidence=0.0,
                assessment_factors={'error': str(e)}
            )

    def _calculate_factor_score(self, factor_name: str, factor_config: Dict[str, Any], 
                               pipeline_config: Dict[str, Any]) -> float:
        """Calculate score for individual risk factor."""
        factors = factor_config['factors']

        # Check pipeline configuration for this factor
        config_value = pipeline_config.get(factor_name, {})

        # Calculate base score from configuration
        base_score = 0.5  # Neutral default

        if isinstance(config_value, dict):
            # Complex factor with multiple aspects
            positive_indicators = 0
            negative_indicators = 0

            for indicator, impact in factors.items():
                if config_value.get(indicator, False):
                    if impact > 0:
                        negative_indicators += 1
                    else:
                        positive_indicators += 1

            if positive_indicators + negative_indicators > 0:
                base_score = negative_indicators / (positive_indicators + negative_indicators)

        elif isinstance(config_value, str):
            # Simple string-based factor
            if config_value in factors:
                base_score = max(0.0, min(1.0, 0.5 + factors[config_value]))

        elif isinstance(config_value, bool):
            # Boolean factor
            if config_value:
                # Good security practice
                base_score = 0.2
            else:
                # Missing security practice
                base_score = 0.8

        return base_score

    def _determine_risk_level(self, overall_score: float) -> str:
        """Determine risk level from overall score."""
        if overall_score >= 0.8:
            return RiskLevel.CRITICAL.value
        elif overall_score >= 0.6:
            return RiskLevel.HIGH.value
        elif overall_score >= 0.4:
            return RiskLevel.MEDIUM.value
        else:
            return RiskLevel.LOW.value

    def _calculate_confidence(self, pipeline_config: Dict[str, Any], factor_scores: Dict[str, float]) -> float:
        """Calculate confidence in the risk assessment."""
        # Base confidence from data completeness
        config_keys = set(pipeline_config.keys())
        expected_keys = set(self.risk_factors.keys())
        coverage = len(config_keys.intersection(expected_keys)) / len(expected_keys)

        confidence = coverage * 0.8  # 80% weight on data coverage

        # Adjust based on factor score variance (more diverse data = higher confidence)
        scores = list(factor_scores.values())
        if len(scores) > 1:
            variance = sum((s - sum(scores)/len(scores))**2 for s in scores) / len(scores)
            confidence += (variance * 0.2)  # 20% weight on score diversity

        return min(1.0, confidence)

    def get_risk_factors(self) -> Dict[str, Any]:
        """Get all risk factors configuration."""
        return self.risk_factors.copy()

    def add_custom_risk_factor(self, factor_name: str, weight: float, factors: Dict[str, float]):
        """Add custom risk factor."""
        self.risk_factors[factor_name] = {
            'weight': weight,
            'factors': factors
        }

    def get_risk_trends(self, historical_scores: List[SuitabilityRiskScore]) -> Dict[str, Any]:
        """Analyze risk trends from historical scores."""
        if not historical_scores:
            return {'error': 'No historical data'}

        scores = [s.overall_score for s in historical_scores]
        avg_score = sum(scores) / len(scores)

        # Trend analysis
        if len(scores) >= 2:
            trend = 'increasing' if scores[-1] > scores[0] else 'decreasing' if scores[-1] < scores[0] else 'stable'
        else:
            trend = 'insufficient_data'

        return {
            'average_score': avg_score,
            'trend': trend,
            'min_score': min(scores),
            'max_score': max(scores),
            'score_range': max(scores) - min(scores),
            'data_points': len(scores)
        }
