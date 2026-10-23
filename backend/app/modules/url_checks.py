"""Heuristic URL checks. No external API required (reputation API is a later add-on)."""
import re
from urllib.parse import urlparse
from app.schemas import Signal

BRANDS = [
    "paytm", "phonepe", "sbi", "hdfc", "icici", "axis", "kotak", "amazon", "flipkart",
    "google", "facebook", "instagram", "whatsapp", "netflix", "microsoft", "apple",
    "irctc", "epfo", "uidai", "npci", "gpay", "myntra", "swiggy", "zomato", "zerodha",
]
SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "buff.ly",
    "rebrand.ly", "cutt.ly", "rb.gy", "shorturl.at",
}
SUSPICIOUS_TLDS = {
    "xyz", "top", "club", "online", "site", "link", "click", "work", "gq", "tk",
    "ml", "cf", "ga", "buzz", "rest", "cam", "loan", "mom", "icu",
}


def _lev(a: str, b: str) -> int:
    if a == b:
        return 0
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def check_url(raw_url: str):
    """Return (signals, checks_run, checks_unavailable)."""
    signals: list[Signal] = []
    checks_run: list[str] = []

    url = raw_url.strip()
    if "://" not in url:
        url = "http://" + url
    p = urlparse(url)
    host = (p.hostname or "").lower()

    # scheme
    checks_run.append("url_scheme")
    if p.scheme != "https":
        signals.append(Signal(name="url_scheme", result="flagged",
                              detail="Not HTTPS - credentials may be sent in the clear.",
                              severity="medium"))
    else:
        signals.append(Signal(name="url_scheme", result="ok", detail="Uses HTTPS."))

    # raw-IP host
    checks_run.append("host_is_ip")
    if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", host):
        signals.append(Signal(name="host_is_ip", result="flagged",
                              detail="Host is a raw IP address, not a domain.", severity="high"))
    else:
        signals.append(Signal(name="host_is_ip", result="ok"))

    # '@' trick
    checks_run.append("at_in_url")
    if "@" in (p.netloc or ""):
        signals.append(Signal(name="at_in_url", result="flagged",
                              detail="'@' in URL can hide the real host.", severity="high"))
    else:
        signals.append(Signal(name="at_in_url", result="ok"))

    # punycode
    checks_run.append("punycode")
    if "xn--" in host:
        signals.append(Signal(name="punycode", result="flagged",
                              detail="Punycode host - can mimic a real brand.", severity="high"))
    else:
        signals.append(Signal(name="punycode", result="ok"))

    # subdomain depth
    checks_run.append("subdomain_depth")
    if host.count(".") >= 4:
        signals.append(Signal(name="subdomain_depth", result="flagged",
                              detail="Unusually many subdomains.", severity="medium"))
    else:
        signals.append(Signal(name="subdomain_depth", result="ok"))

    # shortener
    checks_run.append("url_shortener")
    if host in SHORTENERS:
        signals.append(Signal(name="url_shortener", result="flagged",
                              detail="Shortened URL hides the destination.", severity="medium"))
    else:
        signals.append(Signal(name="url_shortener", result="ok"))

    # suspicious TLD
    checks_run.append("suspicious_tld")
    tld = host.rsplit(".", 1)[-1] if "." in host else ""
    if tld in SUSPICIOUS_TLDS:
        signals.append(Signal(name="suspicious_tld", result="flagged",
                              detail=f"'.{tld}' is frequently abused.", severity="medium"))
    else:
        signals.append(Signal(name="suspicious_tld", result="ok"))

    # lookalike brand
    checks_run.append("lookalike_domain")
    core = host[4:] if host.startswith("www.") else host
    lookalike = None
    for brand in BRANDS:
        if brand in core and not core.startswith(brand + "."):
            lookalike = brand
            break
        if brand not in core:
            label = core.split(".")[0]
            if _lev(label, brand) in (1, 2) and len(brand) >= 4:
                lookalike = brand
                break
    if lookalike:
        signals.append(Signal(name="lookalike_domain", result="flagged",
                              detail=f"Resembles brand '{lookalike}' but is not its official domain.",
                              severity="high"))
    else:
        signals.append(Signal(name="lookalike_domain", result="ok"))

    # reputation API not wired yet - honest reporting
    checks_unavailable = ["reputation_api"]
    return signals, checks_run, checks_unavailable
