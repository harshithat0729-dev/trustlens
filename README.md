# TrustLens

> **Before you trust it, check it.**

TrustLens is a multimodal, multilingual **digital trust & safety assistant**. A user
pastes or uploads a **link, message, image, video or claim**, and TrustLens analyses it
and returns an honest, evidence-based read-out in the user's own language
(Telugu / Tinglish / Hindi / English).

TrustLens does **not** shout "fake" or "real" blindly. It tells the user:

- is there **risk** here?
- is this content **trustworthy / worth acting on**?
- **could it be fake** (and how strong is that signal)?
- and when the evidence is not enough, it plainly says **Inconclusive — verify more**.

## Status

Working-prototype scaffold. The 30-day, ~6-hours-a-day build plan lives in
[`docs/BUILD_PLAN.md`](docs/BUILD_PLAN.md). Architecture is in
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Tech stack

| Layer | Tool |
|---|---|
| Mobile UI | React + Vite (installable PWA) |
| Backend | Python + FastAPI |
| Text / OCR | Tesseract (optional) |
| Media | Pillow metadata + pluggable forensic detector |
| Sources | official / trusted-domain checks |
| Explanation | rule-based Tinglish/English/Telugu/Hindi generator (LLM optional) |
| Tests | pytest + labelled sample set (CSV metrics) |

## Repository layout

```
trustlens/
├── backend/                 FastAPI service
│   ├── app/
│   │   ├── main.py          app factory, CORS, routers, /health
│   │   ├── config.py        env-driven settings
│   │   ├── schemas.py       common result schema (the contract)
│   │   ├── routers/         link, message, media, claim endpoints
│   │   └── modules/         url_checks, message_checks, ocr, media_checks,
│   │                        source_checks, combine, explain
│   └── tests/               pytest
├── frontend/                React + Vite PWA
│   └── src/                 Home, ResultCard, LanguageSelector, api client
├── docs/                    ARCHITECTURE.md, BUILD_PLAN.md, TEST_PLAN.md
└── .github/workflows/       CI
```

## Quick start

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example .env          # then edit if needed
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs for the interactive API.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## The common result schema

Every module returns the same shape (see `backend/app/schemas.py`):

```json
{
  "risk_label": "needs_verification",
  "summary": "user-language explanation",
  "signals": [{"name": "source_check", "result": "not_matched"}],
  "sources": [],
  "limitations": ["source unavailable"],
  "safe_next_steps": ["official site independently open cheyyandi"],
  "checks_run": ["url_structure", "lookalike_domain"],
  "checks_unavailable": ["reputation_api"]
}
```

### Result labels

| Label | Meaning |
|---|---|
| `high_risk` | Strong risk indicators found. Verify before you act. |
| `suspicious_signals_found` | Some warning signs. Further checking needed. |
| `no_known_warning_found` | No warning in the checks that ran — **not** a safety guarantee. |
| `inconclusive` | Not enough evidence to decide real vs fake. |

## Safety & ethics

- AI-generated does **not** mean automatically false; real-looking does **not** mean true.
- A detector score alone is **not** proof.
- Never auto-open a suspicious link.
- Do not monitor calls/messages without user permission.
- Handle private uploads with consent; define a clear retention/deletion policy.
- Report a check as **not run** when its API/model is unavailable — never invent a result.

## License

MIT — see [`LICENSE`](LICENSE).
