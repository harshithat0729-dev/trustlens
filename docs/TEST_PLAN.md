# Test plan

## Goal

Show judges **measured** behaviour, not claims. Report total cases, correct labels,
false alarms, missed risks, inconclusive count, language issues and average response time.

## Sample set (target 40-60 cases)

| Category | Examples | Count |
|---|---|---|
| Safe / legitimate | real company page, genuine offer letter, normal WhatsApp | 10-12 |
| Suspicious | fee-before-joining message, lookalike domain, fake invoice | 12-15 |
| Inconclusive | claim with no available source, low-res screenshot | 8-10 |
| Media | known-provenance image, AI-generated sample (ground truth known) | 8-10 |
| Misleading context | real photo used with a false caption | 5-8 |

Rules:
- Remove personal data (phone numbers, bank details, private docs).
- Record each sample's label source: official warning / provenance / trusted fact-check /
  manually verified.
- One CSV row per case: `id,type,label_source,expected_label,actual_label,notes,response_ms`.

## Metrics to report

- accuracy on the labelled set
- false positives (safe flagged as risky) — the costly error
- false negatives (risky missed)
- inconclusive rate
- language-quality notes (Tinglish / Telugu / Hindi / English)
- average + p95 response time

## How to run

```bash
cd backend
pytest -q                 # unit + API tests
python scripts/eval.py    # (add later) runs the labelled CSV and prints metrics
```
