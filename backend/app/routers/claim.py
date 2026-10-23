from fastapi import APIRouter
from app.schemas import CheckResult, ClaimRequest
from app.modules import message_checks, source_checks, combine, explain

router = APIRouter(prefix="/api/check", tags=["claim"])


@router.post("/claim", response_model=CheckResult)
def check_claim(req: ClaimRequest) -> CheckResult:
    signals, run, unavail, links = message_checks.check_message(req.text)
    src_signals, src_run, src_unavail, sources = source_checks.check_source(
        links[0] if links else req.text
    )
    signals += src_signals
    run += src_run
    unavail += src_unavail

    label = combine.combine(signals, run, unavail)
    result = explain.explain(label, signals, req.language, sources, unavail)
    result.checks_run = run
    result.checks_unavailable = unavail
    return result
