# Contributing

1. Branch per task: `feat/link-checks`, `fix/ocr-crash`, `docs/readme`.
2. Keep the **common result schema** stable — every module maps to it.
3. Never commit secrets. Copy `.env.example` to `.env`; `.env` is git-ignored.
4. Every new check ships with at least one test in `backend/tests/`.
5. Daily update (even solo): *Yesterday done / Today plan / Blocker*.

## Definition of done for a check

- returns `Signal` objects, not free text
- records itself in `checks_run` **or** `checks_unavailable`
- never invents a result when its source/API is down
- has a test with a labelled sample
