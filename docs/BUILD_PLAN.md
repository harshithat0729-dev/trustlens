# TrustLens - 30-day build plan (6 hours / day)

**Window:** 22 Oct 2026 -> 20 Nov 2026 (hackathon deadline ~25 Nov, keep the tail as buffer).
**Budget:** 30 days x 6 h = ~180 hours.
**Assume:** you (the lead) build the core solo. If teammates are active, split the
module work per the team table and treat the day tasks as the *team's* checklist.

---

## How to run each day

| Slot | Time | What |
|---|---|---|
| Review | 0:00-0:15 | re-read yesterday's log, pick today's one goal |
| Build | 0:15-4:00 | the day's core task |
| Test | 4:00-5:00 | run / write tests, try a real sample |
| Ship | 5:00-5:30 | commit + push (at least 1 commit/day) |
| Plan | 5:30-6:00 | write tomorrow's goal + blockers in `docs/LOG.md` |

Rules: one branch per feature (`feat/...`), never commit `.env`, and **no new features
in the last 3 days** (freeze).

## Milestones

| # | Day | Milestone |
|---|---|---|
| M1 | 7 | skeleton works end-to-end (input -> result screen) |
| M2 | 12 | link + message modules live with tests |
| M3 | 17 | image + video checks live with limitations shown |
| M4 | 21 | 4 languages, sources, uncertainty, security |
| M5 | 25 | all modules integrated + 40-60 test cases measured |
| M6 | 28 | demo (3 cases) + README + demo video |
| M7 | 30 | freeze + submission ready |

---

## Day 0 - Setup (2-3 h, do today)

- Goal: repo running locally.
- Tasks: `git clone` the scaffold -> `cd backend && pip install -r requirements.txt` ->
  `uvicorn app.main:app --reload` -> open `/docs`, hit `POST /api/check/link`.
  Then `cd frontend && npm install && npm run dev`.
- Deliverable: both servers run; you get a JSON result from a test URL.
- Done when: `/health` returns ok and the frontend shows the home screen.

## Days 1-3 - Research & scope (M1 prep)

**Day 1** - Competitor scan. Goal: a 3-5 row comparison table. Tasks: study CyberWall,
SafeMeAI, Sanchar Saathi, AI4TRUST, SynthID; note features + limits. Deliverable:
`docs/COMPETITORS.md`. Done when: table has source links.
**Day 2** - MVP freeze. Goal: exact scope. Tasks: confirm link + message + image first,
video as sampled frames, audio optional; write `docs/MVP.md`. Done when: in-scope /
out-of-scope lists written.
**Day 3** - Sample set v1. Goal: 10-15 samples per category. Tasks: collect safe,
suspicious, inconclusive samples; strip personal data; label each with a source.
Deliverable: `backend/data/samples.csv`. Done when: >=30 labelled rows.

## Days 4-7 - Skeleton (M1)

**Day 4** - Result schema + UI wireframe. Tasks: finalise `schemas.py`; sketch Home /
Upload / Result screens. Done when: schema frozen, wireframe in `docs/`.
**Day 5** - Backend endpoints. Tasks: wire `routers/link.py` + `routers/message.py` to
their modules; return the common result. Done when: both return valid JSON for samples.
**Day 6** - Frontend wiring. Tasks: Home buttons + language selector -> `api.js` ->
ResultCard. Done when: paste a message, see a result card.
**Day 7** - M1 demo. Tasks: error states + "checks not run" display. Deliverable: screen
recording of input -> result. Done when: structured result renders with limitations.

## Days 8-12 - Link & message modules (M2)

**Day 8** - URL structure checks. Tasks: parse scheme/host/path; flag IP hosts, `@`,
punycode, too many subdomains, shorteners. Done when: unit tests pass.
**Day 9** - Lookalike domains. Tasks: edit-distance vs a brand list; flag near-misses.
Done when: `paytm` vs `paytmm-secure` style cases caught.
**Day 10** - Message cues. Tasks: regex for urgency, fee-before-joining, impersonation,
contact details. Done when: samples labelled correctly.
**Day 11** - Source checks. Tasks: trusted/official domain match; record
`checks_unavailable` when an API is missing. Done when: mismatch -> signal + source note.
**Day 12** - M2 tests. Tasks: add legit + suspicious tests; measure false alarms.
Deliverable: link/message test report. Done when: false-alarm count documented.

## Days 13-17 - Image & video (M3)

**Day 13** - OCR. Tasks: extract text from screenshots (Tesseract); feed to message checks.
Done when: a fee-scam screenshot yields its text.
**Day 14** - Image metadata. Tasks: read EXIF via Pillow; flag missing/edited metadata.
Done when: signals emitted.
**Day 15** - Forensic detector. Tasks: trial one detector/API; verify license, limits,
speed. Done when: decision recorded (use / skip) in `docs/`.
**Day 16** - Video frames. Tasks: sample frames; run image checks on them; cap cost.
Done when: a video returns per-frame signals.
**Day 17** - M3 limits. Tasks: show which checks ran / were unavailable. Deliverable:
media test report with limitations. Done when: limitations render on the result card.

## Days 18-21 - Multilingual + sources (M4)

**Day 18** - Tinglish/Telugu test cases. Tasks: write 4-language samples; check meaning
survives translation. Done when: `data/samples.csv` has a language column.
**Day 19** - Explainer. Tasks: rule-based templates per language (fallback when no LLM);
LLM path optional + server-side key. Done when: same signal set -> 4 languages.
**Day 20** - Sources + uncertainty. Tasks: add source links, unknowns, safe next steps.
Done when: every result shows evidence + limitations.
**Day 21** - Security pass. Tasks: file type/size validation, key handling, no auto-open,
consent note. Deliverable: `docs/SECURITY.md`. Done when: checklist all green.

## Days 22-25 - Integration & evaluation (M5)

**Day 22** - Integrate. Tasks: all modules behind one schema; end-to-end on all types.
Done when: one input -> one combined result.
**Day 23** - Test set v2. Tasks: grow to 40-60 curated cases. Done when: CSV complete.
**Day 24** - Metrics. Tasks: `scripts/eval.py` prints accuracy, FP, FN, inconclusive,
response time. Done when: numbers reproducible.
**Day 25** - M5 report. Tasks: write `docs/TEST_REPORT.md`; debug mismatches. Deliverable:
measured results. Done when: report has the metric table.

## Days 26-28 - Demo & docs (M6)

**Day 26** - 3 demos. Tasks: internship scam message, suspicious link, known-provenance
media. Done when: each reproducible from a clean start.
**Day 27** - README + disclosure. Tasks: setup, env vars, sources, AI-tool disclosure,
limitations. Done when: a fresh reader can run it.
**Day 28** - Demo video. Tasks: record 3 minutes; no private data. Deliverable: video +
`docs/DEMO.md`. Done when: video shows real checks + metrics.

## Days 29-30 - Freeze (M7)

**Day 29** - Fresh-env test. Tasks: clone to a new folder/profile; follow README exactly.
Done when: it runs with no missing steps.
**Day 30** - Freeze + submit. Tasks: fix only critical bugs; verify GitHub, tests, demo,
AI disclosure, official deadline + rules. Deliverable: submission checklist signed off.
Done when: everything on the final checklist is ticked.

---

## Final checklist

- [ ] 3 input categories work end-to-end
- [ ] language selection works (Tinglish / Telugu / Hindi / English)
- [ ] every result shows evidence / source links
- [ ] safe file handling + no auto-open of links
- [ ] test metrics recorded (accuracy, FP, FN, inconclusive, response time)
- [ ] limitations documented
- [ ] README + setup guide
- [ ] demo video
- [ ] AI tools/models disclosed
- [ ] official hackathon deadline + rules re-checked
