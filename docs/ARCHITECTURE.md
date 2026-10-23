# Architecture

## Flow

```
User (mobile PWA)
   │  paste text / upload file / share
   ▼
FastAPI  ──► validate (type, size)
   │
   ├─► Extract   : text, OCR, EXIF metadata, video frames
   ├─► Check     : type-specific modules (url, message, media, claim)
   ├─► Verify    : source / official-domain cross-check
   ├─► Combine   : independent signals -> one risk_label
   └─► Explain   : evidence + unknowns + safe next steps in user language
   ▼
Common CheckResult JSON  ──►  Result card (mobile UI)
```

## Modules

| Module | File | Responsibility |
|---|---|---|
| URL checks | `modules/url_checks.py` | structure, lookalike domains, shorteners, IP hosts, punycode |
| Message checks | `modules/message_checks.py` | urgency, fee demand, impersonation wording, links, contacts |
| OCR | `modules/ocr.py` | extract text from screenshots/images (Tesseract, optional) |
| Media checks | `modules/media_checks.py` | EXIF/metadata, edit clues; pluggable forensic detector |
| Source checks | `modules/source_checks.py` | trusted/official domain match; records what it could not check |
| Combine | `modules/combine.py` | signals -> `risk_label` (never one detector = truth) |
| Explain | `modules/explain.py` | rule-based Tinglish/English/Telugu/Hindi explanation |

## Design rules

1. **One contract.** Every module returns `Signal` objects; `combine` builds the
   `CheckResult`. Nothing bypasses the schema.
2. **Honesty over confidence.** A check that cannot run is reported in
   `checks_unavailable`; never fabricate a result.
3. **Language-independent signals.** Signals are stored language-neutral; only the
   final `summary` is localised. This keeps safety meaning intact across translation.
4. **No single point of truth.** A forensic score, a source match and the explainer
   each play a different role.
5. **Privacy.** Validate file type/size; do not persist uploads by default; document a
   retention policy. API keys live server-side only.

## Adding a new check (recipe)

1. Write a function `check_x(...) -> list[Signal]` in `modules/`.
2. Call it from the relevant router; append its name to `checks_run` (or
   `checks_unavailable`).
3. Add a test in `backend/tests/` with one positive and one negative sample.
4. Update `docs/TEST_PLAN.md` sample table.
