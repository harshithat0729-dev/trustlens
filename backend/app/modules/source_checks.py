"""Cross-check a claim/link against trusted, official domains."""
from urllib.parse import urlparse
from app.config import TRUSTED_DOMAINS
from app.schemas import Signal


def _host(url: str) -> str:
    if "://" not in url:
        url = "http://" + url
    return (urlparse(url).hostname or "").lower()


def check_source(text_or_url: str):
    """Return (signals, checks_run, checks_unavailable, sources)."""
    signals: list[Signal] = []
    sources: list[str] = []

    host = _host(text_or_url)
    matched = None
    for d in TRUSTED_DOMAINS:
        if host == d or host.endswith("." + d):
            matched = d
            break

    if matched:
        signals.append(Signal(name="source_check", result="ok",
                              detail=f"Host matches a trusted domain ({matched})."))
        sources.append(f"https://{matched}")
    else:
        signals.append(Signal(name="source_check", result="info",
                              detail="No trusted-domain match found in the checks that ran."))

    # No live fact-check / reputation API in the prototype - say so honestly.
    checks_unavailable = ["reputation_api", "fact_check_api"]
    return signals, ["source_check"], checks_unavailable, sources
