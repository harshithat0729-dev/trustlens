"""Heuristic message checks for WhatsApp / SMS / pasted text."""
import re
from app.schemas import Signal

FEE = re.compile(r"(registration|joining|security|processing|refundable|training)\s*(fee|amount|deposit|charge)", re.I)
MONEY = re.compile(r"(₹|\brs\.?\s*\d|\binr\b|\b\d{3,}\s*(rupees|rs)\b)", re.I)
URGENCY = re.compile(r"(urgent|immediately|within\s+\d+\s*(hours|minutes|hrs)|last\s+date|expir|act\s+now|hurry|today\s+only)", re.I)
IMPERSONATE = re.compile(r"(official|company\s*hr|bank|government|police|customer\s*care|income\s*tax|kyc)", re.I)
PAYMENT = re.compile(r"(upi|gpay|google\s*pay|phonepe|paytm|bank\s*transfer|account\s*number|ifsc|neft|imps)", re.I)
LINK = re.compile(r"(https?://\S+|www\.\S+)", re.I)
CONTACT = re.compile(r"\b(\+?\d[\d\s-]{8,}\d)\b")


def _flag(name, hit, detail, severity="medium"):
    return Signal(name=name, result="flagged" if hit else "ok",
                  detail=detail if hit else None, severity=severity)


def check_message(text: str):
    signals: list[Signal] = []
    checks_run: list[str] = []

    checks_run.append("fee_request")
    signals.append(_flag("fee_request", bool(FEE.search(text)),
                         "Asks for a fee/deposit before joining or processing.", "high"))
    checks_run.append("money_amount")
    signals.append(_flag("money_amount", bool(MONEY.search(text)),
                         "Contains an explicit money amount.", "medium"))
    checks_run.append("urgency")
    signals.append(_flag("urgency", bool(URGENCY.search(text)),
                         "Uses urgency/pressure wording.", "medium"))
    checks_run.append("impersonation")
    signals.append(_flag("impersonation", bool(IMPERSONATE.search(text)),
                         "Claims to be an official body/company.", "medium"))
    checks_run.append("payment_channel")
    signals.append(_flag("payment_channel", bool(PAYMENT.search(text)),
                         "Asks for payment via UPI/bank transfer.", "high"))
    checks_run.append("embedded_link")
    signals.append(_flag("embedded_link", bool(LINK.search(text)),
                         "Contains a link to verify separately.", "low"))
    checks_run.append("contact_number")
    signals.append(_flag("contact_number", bool(CONTACT.search(text)),
                         "Contains a phone number.", "low"))

    links = LINK.findall(text)
    return signals, checks_run, [], links
