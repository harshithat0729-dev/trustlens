"""Optional OCR: extract text from an image/screenshot using Tesseract.

If Tesseract is not installed, this reports the check as unavailable rather than failing.
"""
from app.config import settings
from app.schemas import Signal

try:
    import pytesseract
    from PIL import Image
    if settings.tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd
    _HAVE_OCR = True
except Exception:  # pragma: no cover
    _HAVE_OCR = False


def extract_text(path: str):
    """Return (text, signals, checks_run, checks_unavailable)."""
    if not _HAVE_OCR:
        return "", [Signal(name="ocr", result="unavailable",
                           detail="Tesseract not installed.")], [], ["ocr"]
    try:
        text = pytesseract.image_to_string(Image.open(path))
        return text, [Signal(name="ocr", result="ok", detail="Text extracted.")], ["ocr"], []
    except Exception as e:  # pragma: no cover
        return "", [Signal(name="ocr", result="unavailable", detail=str(e))], [], ["ocr"]
