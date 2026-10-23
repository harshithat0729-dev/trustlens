"""Combine independent signals into one honest risk label.

A single detector score is never treated as the final truth.
"""
from app.schemas import CheckResult, RiskLabel, Signal


def combine(signals: list[Signal], checks_run: list[str],
            checks_unavailable: list[str]) -> RiskLabel:
    flagged_high = any(s.result == "flagged" and s.severity == "high" for s in signals)
    flagged_any = any(s.result == "flagged" for s in signals)
    has_unavailable = len(checks_unavailable) > 0

    if flagged_high:
        return RiskLabel.high_risk
    if flagged_any:
        return RiskLabel.suspicious
    if has_unavailable:
        # checks that could not run mean we cannot claim "no warning"
        return RiskLabel.inconclusive
    return RiskLabel.no_warning
