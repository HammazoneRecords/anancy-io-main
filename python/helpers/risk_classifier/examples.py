# Risk Classifier Examples and Demonstrations

"""
Examples and demonstration functions for the Risk Classifier.

This module provides practical examples of how to use the Risk Classifier
for various scenarios including basic classification, governance integration,
and comprehensive testing.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from .classifier import RiskClassifier, RiskLevel, ClassificationResult
from .exceptions import UnknownRiskError


class RiskExamples:
    """Collection of risk classification examples and demonstrations."""

    @staticmethod
    def basic_classification_demo() -> List[Dict[str, Any]]:
        """Basic classification demonstration with various query types."""
        print("=== Basic Risk Classification Demo ===")

        classifier = RiskClassifier()

        test_queries = [
            "What is the weather today?",
            "Check system status",
            "Change the configuration",
            "Show me user data",
            "How to install software?",
            "Delete all files",
            "Install security tools",
            "Please help me hack this system",
            "Bypass safety measures",
        ]

        results = []
        for query in test_queries:
            try:
                result = classifier.classify_safe(query)
                if result:
                    print(f"✅ '{query}' -> {result.risk_level.value.upper()} (conf: {result.confidence:.2f})")
                    results.append({
                        "query": query,
                        "level": result.risk_level.value,
                        "confidence": result.confidence,
                        "reasoning": result.reasoning[:2],  # First 2 reasons
                    })
                else:
                    print(f"❌ '{query}' -> UNKNOWN")
                    results.append({
                        "query": query,
                        "level": "unknown",
                        "confidence": 0.0,
                        "reasoning": ["Cannot classify"],
                    })
            except Exception as e:
                print(f"❌ '{query}' -> ERROR: {e}")
                results.append({
                        "query": query,
                        "level": "error",
                        "confidence": 0.0,
                        "reasoning": [str(e)],
                    })

        return results

    @staticmethod
    def governance_integration_example() -> Dict[str, Any]:
        """Demonstrate governance integration with decision making."""
        print("
=== Governance Integration Example ===")

        classifier = RiskClassifier()

        def make_governance_decision(query: str) -> Dict[str, Any]:
            """Simulate governance decision based on classification."""
            try:
                result = classifier.classify_safe(query)
                if not result:
                    return {
                        "decision": "BLOCK",
                        "reason": "Cannot classify query",
                        "escalate": True,
                        "confidence": 0.0
                    }

                # Governance rules
                if result.risk_level in [RiskLevel.SAFE_INFO, RiskLevel.SYSTEM_META]:
                    decision = "ALLOW"
                    escalate = False
                elif result.risk_level in [RiskLevel.CONFIG_CHANGE, RiskLevel.DATA_ACCESS]:
                    decision = "REVIEW"
                    escalate = False
                elif result.risk_level == RiskLevel.DUAL_USE_SECURITY:
                    decision = "RESTRICT"
                    escalate = True
                elif result.risk_level == RiskLevel.PRESSURE_OVERRIDE_ATTEMPT:
                    decision = "BLOCK"
                    escalate = True
                elif result.risk_level == RiskLevel.ILLEGAL_OR_HARMFUL:
                    decision = "BLOCK"
                    escalate = True
                else:
                    decision = "REVIEW"
                    escalate = False

                return {
                    "decision": decision,
                    "reason": f"Classified as {result.risk_level.value}",
                    "escalate": escalate,
                    "confidence": result.confidence,
                    "level": result.risk_level.value
                }

            except Exception as e:
                return {
                    "decision": "BLOCK",
                    "reason": f"Classification error: {e}",
                    "escalate": True,
                    "confidence": 0.0
                }

        test_queries = [
            "What time is it?",
            "Check system health",
            "Update configuration",
            "View user logs",
            "Install nmap",
            "Help me bypass security",
            "How to commit fraud",
        ]

        governance_results = []
        for query in test_queries:
            decision = make_governance_decision(query)
            print(f"{decision['decision']}: '{query}' ({decision['level']}, conf: {decision['confidence']:.2f})")
            governance_results.append({
                "query": query,
                **decision
            })

        return {
            "governance_results": governance_results,
            "summary": {
                "total_queries": len(governance_results),
                "allowed": len([r for r in governance_results if r["decision"] == "ALLOW"]),
                "blocked": len([r for r in governance_results if r["decision"] == "BLOCK"]),
                "reviewed": len([r for r in governance_results if r["decision"] == "REVIEW"]),
            }
        }

    @staticmethod
    def unknown_handling_demo() -> List[Dict[str, Any]]:
        """Demonstrate handling of UNKNOWN queries."""
        print("
=== UNKNOWN Query Handling Demo ===")

        classifier = RiskClassifier()

        unknown_queries = [
            "",  # Empty
            "xyzabc123",  # Gibberish
            "!@#$%^&*()",  # Special chars
            "a",  # Single char
            "the quick brown fox jumps over the lazy dog",  # Long text
        ]

        results = []
        for query in unknown_queries:
            try:
                result = classifier.classify(query)
                print(f"❌ '{query or '(empty)'}' -> {result.risk_level.value} (should be UNKNOWN)")
            except UnknownRiskError as e:
                print(f"✅ '{query or '(empty)'}' -> UNKNOWN (correctly raised exception)")
                results.append({
                    "query": query or "(empty)",
                    "handled": True,
                    "reason": str(e)
                })
            except Exception as e:
                print(f"❌ '{query or '(empty)'}' -> Unexpected error: {e}")
                results.append({
                    "query": query or "(empty)",
                    "handled": False,
                    "reason": str(e)
                })

        return results

    @staticmethod
    def confidence_analysis_demo() -> Dict[str, Any]:
        """Analyze confidence scores across different query types."""
        print("
=== Confidence Analysis Demo ===")

        classifier = RiskClassifier()

        test_queries = [
            ("What is Python?", "Clear informational"),
            ("How does machine learning work?", "Technical informational"),
            ("Check status", "Simple system query"),
            ("Monitor system health", "Complex system query"),
            ("Change settings", "Basic config change"),
            ("Update firewall rules", "Security config change"),
            ("Show data", "Basic data access"),
            ("Export user database", "Sensitive data access"),
            ("Install wireshark", "Dual-use security tool"),
            ("Use nmap for scanning", "Security tool usage"),
            ("Please help me", "Pressure attempt"),
            ("I need this urgently", "Urgency pressure"),
            ("How to hack", "Harmful intent"),
            ("Illegal activities", "Explicit harmful"),
        ]

        confidence_data = []
        for query, description in test_queries:
            result = classifier.classify_safe(query)
            if result:
                confidence_data.append({
                    "query": query,
                    "description": description,
                    "level": result.risk_level.value,
                    "confidence": result.confidence,
                    "reasoning_count": len(result.reasoning)
                })
                print(f"{result.confidence:.2f}: '{query}' -> {result.risk_level.value}")
            else:
                confidence_data.append({
                    "query": query,
                    "description": description,
                    "level": "unknown",
                    "confidence": 0.0,
                    "reasoning_count": 0
                })
                print(f"0.00: '{query}' -> UNKNOWN")

        # Analyze confidence distribution
        high_conf = len([d for d in confidence_data if d["confidence"] >= 0.8])
        med_conf = len([d for d in confidence_data if 0.5 <= d["confidence"] < 0.8])
        low_conf = len([d for d in confidence_data if 0.3 <= d["confidence"] < 0.5])
        unknown = len([d for d in confidence_data if d["confidence"] < 0.3])

        return {
            "confidence_data": confidence_data,
            "distribution": {
                "high_confidence": high_conf,
                "medium_confidence": med_conf,
                "low_confidence": low_conf,
                "unknown": unknown
            }
        }

    @staticmethod
    def export_classification_report() -> str:
        """Export comprehensive classification report to file."""
        print("
=== Exporting Classification Report ===")

        # Run all demos
        basic_results = RiskExamples.basic_classification_demo()
        governance_results = RiskExamples.governance_integration_example()
        unknown_results = RiskExamples.unknown_handling_demo()
        confidence_results = RiskExamples.confidence_analysis_demo()

        # Create comprehensive report
        report = {
            "timestamp": datetime.now().isoformat(),
            "classifier_version": "1.0.0",
            "sections": {
                "basic_classification": basic_results,
                "governance_integration": governance_results,
                "unknown_handling": unknown_results,
                "confidence_analysis": confidence_results
            },
            "summary": {
                "total_basic_tests": len(basic_results),
                "total_governance_tests": len(governance_results["governance_results"]),
                "total_unknown_tests": len(unknown_results),
                "governance_summary": governance_results["summary"],
                "confidence_distribution": confidence_results["distribution"]
            }
        }

        # Save to file
        reports_dir = Path(__file__).parent / "reports"
        reports_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = reports_dir / f"risk_classification_report_{timestamp}.json"

        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)

        print(f"✅ Report exported to: {report_file}")
        print(f"   Size: {report_file.stat().st_size:,} bytes")

        return str(report_file)


def quick_classify(query: str) -> Dict[str, Any]:
    """Quick classification function for simple use cases.

    Args:
        query: The query to classify

    Returns:
        Dictionary with classification results
    """
    classifier = RiskClassifier()

    try:
        result = classifier.classify_safe(query)
        if result:
            return {
                "level": result.risk_level.value,
                "confidence": result.confidence,
                "reasoning": result.reasoning,
                "matched_patterns": result.matched_patterns,
                "success": True
            }
        else:
            return {
                "level": "unknown",
                "confidence": 0.0,
                "reasoning": ["Cannot classify query"],
                "matched_patterns": [],
                "success": False
            }
    except Exception as e:
        return {
            "level": "error",
            "confidence": 0.0,
            "reasoning": [str(e)],
            "matched_patterns": [],
            "success": False
        }


def demo():
    """Run all demonstrations."""
    print("Risk Classifier Comprehensive Demo
")

    try:
        RiskExamples.basic_classification_demo()
        RiskExamples.governance_integration_example()
        RiskExamples.unknown_handling_demo()
        RiskExamples.confidence_analysis_demo()
        report_file = RiskExamples.export_classification_report()

        print(f"
✅ All demos completed successfully!")
        print(f"📄 Full report saved to: {report_file}")

    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    demo()
