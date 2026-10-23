from fastapi import APIRouter
from app.schemas import CheckResult, LinkRequest
from app.modules import url_checks, source_checks, combine, explain

router = APIRouter(prefix="/api/check", tags=["link"])


@router.post("/link", response_model=CheckResult)
def check_link(req: LinkRequest) -> CheckResult:
    signals, run, unavail = url_checks.check_url(req.url)
    src_signals, src_run, src_unavail, sources = source_checks.check_source(req.url)
    signals += src_signals
    run += src_run
    unavail += src_unavail

    label = combine.combine(signals, run, unavail)
    result = explain.explain(label, signals, req.language, sources, unavail)
    result.checks_run = run
    result.checks_unavailable = unavail
    return result
