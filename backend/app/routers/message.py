from fastapi import APIRouter
from app.schemas import CheckResult, MessageRequest
from app.modules import message_checks, source_checks, combine, explain

router = APIRouter(prefix="/api/check", tags=["message"])


@router.post("/message", response_model=CheckResult)
def check_message(req: MessageRequest) -> CheckResult:
    signals, run, unavail, links = message_checks.check_message(req.text)

    sources: list[str] = []
    # If the message carries links, also run source checks on the first one.
    if links:
        src_signals, src_run, src_unavail, sources = source_checks.check_source(links[0])
        signals += src_signals
        run += src_run
        unavail += src_unavail

    label = combine.combine(signals, run, unavail)
    result = explain.explain(label, signals, req.language, sources, unavail)
    result.checks_run = run
    result.checks_unavailable = unavail
    return result
