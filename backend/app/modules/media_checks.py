"""Image / video metadata checks. Forensic detection is a pluggable add-on."""
from app.schemas import Signal

try:
    from PIL import Image
    _HAVE_PIL = True
except Exception:  # pragma: no cover
    _HAVE_PIL = False


def check_image(path: str):
    """Return (signals, checks_run, checks_unavailable)."""
    signals: list[Signal] = []
    checks_run: list[str] = []

    if not _HAVE_PIL:
        return ([Signal(name="image_metadata", result="unavailable", detail="Pillow missing.")],
                [], ["image_metadata"])

    checks_run.append("image_metadata")
    try:
        img = Image.open(path)
        exif = img.getexif()
        if not exif:
            signals.append(Signal(name="image_metadata", result="info",
                                  detail="No EXIF metadata - source cannot be confirmed.", severity="medium"))
        else:
            signals.append(Signal(name="image_metadata", result="ok",
                                  detail="EXIF metadata present."))
    except Exception as e:
        signals.append(Signal(name="image_metadata", result="unavailable", detail=str(e)))

    # No forensic model wired yet - report honestly.
    checks_unavailable = ["forensic_detector"]
    return signals, checks_run, checks_unavailable
