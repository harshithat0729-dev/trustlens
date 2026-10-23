import os
import tempfile
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from app.config import settings
from app.schemas import CheckResult
from app.modules import ocr, media_checks, message_checks, combine, explain

router = APIRouter(prefix="/api/check", tags=["media"])

IMAGE_TYPES = {"image/png", "image/jpeg", "image/jpg", "image/webp", "image/tiff"}


@router.post("/media", response_model=CheckResult)
async def check_media(file: UploadFile = File(...), language: str = Form("tinglish")) -> CheckResult:
    if file.content_type not in IMAGE_TYPES:
        raise HTTPException(status_code=415, detail=f"Unsupported type: {file.content_type}")

    data = await file.read()
    if len(data) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="File too large.")

    suffix = os.path.splitext(file.filename or "upload")[1] or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(data)
        path = tmp.name

    try:
        signals, run, unavail = media_checks.check_image(path)
        text, ocr_signals, ocr_run, ocr_unavail = ocr.extract_text(path)
        signals += ocr_signals
        run += ocr_run
        unavail += ocr_unavail

        if text.strip():
            msg_signals, msg_run, msg_unavail, _ = message_checks.check_message(text)
            signals += msg_signals
            run += msg_run
            unavail += msg_unavail

        label = combine.combine(signals, run, unavail)
        result = explain.explain(label, signals, language, [], unavail)
        result.checks_run = run
        result.checks_unavailable = unavail
        return result
    finally:
        try:
            os.unlink(path)
        except OSError:
            pass
