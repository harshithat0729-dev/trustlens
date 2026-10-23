"""The common result contract. Every module maps to this - nothing bypasses it."""
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class RiskLabel(str, Enum):
    high_risk = "high_risk"
    suspicious = "suspicious_signals_found"
    no_warning = "no_known_warning_found"
    inconclusive = "inconclusive"


class Signal(BaseModel):
    name: str
    result: str                       # flagged | ok | unavailable | info
    detail: Optional[str] = None
    severity: str = "medium"          # low | medium | high


class CheckResult(BaseModel):
    risk_label: RiskLabel
    summary: str
    signals: List[Signal] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    safe_next_steps: List[str] = Field(default_factory=list)
    language: str = "tinglish"
    checks_run: List[str] = Field(default_factory=list)
    checks_unavailable: List[str] = Field(default_factory=list)


class LinkRequest(BaseModel):
    url: str
    language: str = "tinglish"


class MessageRequest(BaseModel):
    text: str
    language: str = "tinglish"


class ClaimRequest(BaseModel):
    text: str
    language: str = "tinglish"
