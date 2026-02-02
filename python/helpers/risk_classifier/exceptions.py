"""Risk Classifier Exception Classes"""

class RiskClassificationError(Exception):
    """Raised when risk classification fails."""
    pass

class UnknownRiskError(RiskClassificationError):
    """Raised when query cannot be classified (UNKNOWN state)."""
    def __init__(self, query, reason="Query cannot be classified into known risk levels"):
        self.query = query
        self.reason = reason
        super().__init__(f"UNKNOWN risk for query: {query[:100]}... Reason: {reason}")
