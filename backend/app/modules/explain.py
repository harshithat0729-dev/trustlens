"""Turn signals into a short, honest explanation in the user's language.

Rule-based by default (no LLM required). An LLM can be layered on later - but it must
only explain the evidence it is given, never invent a verdict.
"""
from app.schemas import CheckResult, RiskLabel, Signal

LABEL_TEXT = {
    "tinglish": {
        RiskLabel.high_risk: "High risk - strong warning signs unnayi",
        RiskLabel.suspicious: "Suspicious signals dorikayi",
        RiskLabel.no_warning: "Ippati varaku warning emi dorakaledu",
        RiskLabel.inconclusive: "Inconclusive - inkonni checks avasaram",
    },
    "english": {
        RiskLabel.high_risk: "High risk - strong warning signs found",
        RiskLabel.suspicious: "Suspicious signals found",
        RiskLabel.no_warning: "No warning found so far",
        RiskLabel.inconclusive: "Inconclusive - more verification needed",
    },
    "telugu": {
        RiskLabel.high_risk: "అధిక ప్రమాదం - బలమైన హెచ్చరిక సంకేతాలు ఉన్నాయి",
        RiskLabel.suspicious: "అనుమానాస్పద సంకేతాలు కనిపించాయి",
        RiskLabel.no_warning: "ఇప్పటివరకు హెచ్చరిక ఏమీ కనిపించలేదు",
        RiskLabel.inconclusive: "నిర్ణయించలేము - మరిన్ని తనిఖీలు అవసరం",
    },
    "hindi": {
        RiskLabel.high_risk: "उच्च जोखिम - मजबूत चेतावनी संकेत मिले",
        RiskLabel.suspicious: "संदिग्ध संकेत मिले",
        RiskLabel.no_warning: "अब तक कोई चेतावनी नहीं मिली",
        RiskLabel.inconclusive: "अनिर्णीत - और जाँच ज़रूरी है",
    },
}

CLOSERS = {
    "tinglish": "Idi 100% fake ani final proof kaadhu - kaani jagratha ga undandi.",
    "english": "This is not a final proof of fake - but stay cautious.",
    "telugu": "ఇది 100% నకిలీ అనే తుది రుజువు కాదు - కానీ జాగ్రత్తగా ఉండండి.",
    "hindi": "यह 100% नकली होने का अंतिम प्रमाण नहीं है - पर सतर्क रहें।",
}

NEXT_STEPS = {
    "tinglish": [
        "Link ni automatic ga open cheyyakandi.",
        "Company official website lo contact details independently verify cheyyandi.",
        "Money/payment cheyyakunda mundhu confirm cheyyandi.",
    ],
    "english": [
        "Do not open the link automatically.",
        "Verify contact details on the company's official website.",
        "Confirm before making any payment.",
    ],
    "telugu": [
        "లింక్‌ను స్వయంగా తెరవకండి.",
        "కంపెనీ అధికారిక వెబ్‌సైట్‌లో సంప్రదింపు వివరాలు నిర్ధారించుకోండి.",
        "పైసా చెల్లించే ముందు నిర్ధారించుకోండి.",
    ],
    "hindi": [
        "लिंक को अपने आप न खोलें।",
        "कंपनी की आधिकारिक वेबसाइट पर संपर्क विवरण जाँचें।",
        "कोई भुगतान करने से पहले पुष्टि करें।",
    ],
}


def _reasons(signals: list[Signal]) -> list[str]:
    out = []
    for s in signals:
        if s.result == "flagged" and s.detail:
            out.append(s.detail)
    return out


def explain(risk_label: RiskLabel, signals: list[Signal], language: str,
            sources: list[str], checks_unavailable: list[str]) -> CheckResult:
    language = language if language in LABEL_TEXT else "tinglish"
    reasons = _reasons(signals)

    parts = [LABEL_TEXT[language][risk_label] + "."]
    if reasons:
        parts.append(" " + " ".join(reasons[:4]))
    if checks_unavailable:
        parts.append(" (Some checks could not run: %s.)" % ", ".join(checks_unavailable))
    if risk_label in (RiskLabel.high_risk, RiskLabel.suspicious):
        parts.append(" " + CLOSERS[language])

    summary = "".join(parts)

    return CheckResult(
        risk_label=risk_label,
        summary=summary,
        signals=signals,
        sources=sources,
        limitations=[f"check unavailable: {c}" for c in checks_unavailable],
        safe_next_steps=NEXT_STEPS[language],
        language=language,
    )
