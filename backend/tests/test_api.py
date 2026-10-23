"""API tests. One positive and one negative sample per module."""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_link_high_risk_lookalike():
    r = client.post("/api/check/link", json={"url": "http://paytm-secure-login.xyz/verify"})
    assert r.status_code == 200
    body = r.json()
    assert body["risk_label"] == "high_risk"
    assert any(s["name"] == "lookalike_domain" and s["result"] == "flagged" for s in body["signals"])


def test_link_safe_official():
    r = client.post("/api/check/link", json={"url": "https://www.irctc.co.in/nget/train-search"})
    assert r.status_code == 200
    assert r.json()["risk_label"] in ("no_known_warning_found", "inconclusive")


def test_message_fee_scam():
    text = "Congratulations! Your internship is selected. Pay Rs.999 registration fee within 24 hours. UPI: scam@upi"
    r = client.post("/api/check/message", json={"text": text})
    assert r.status_code == 200
    body = r.json()
    assert body["risk_label"] in ("high_risk", "suspicious_signals_found")
    assert any(s["name"] == "fee_request" and s["result"] == "flagged" for s in body["signals"])


def test_message_benign():
    r = client.post("/api/check/message", json={"text": "Hi, meeting at 5pm today in room 3."})
    assert r.status_code == 200
    assert r.json()["risk_label"] == "no_known_warning_found"


def test_language_switch():
    r = client.post("/api/check/message", json={"text": "pay fee now", "language": "english"})
    assert r.status_code == 200
    assert r.json()["language"] == "english"
