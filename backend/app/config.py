"""Environment-driven settings. Secrets stay server-side."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    def __init__(self) -> None:
        self.allowed_origins = [
            o.strip() for o in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",") if o.strip()
        ]
        self.max_upload_mb = int(os.getenv("MAX_UPLOAD_MB", "15"))
        self.llm_api_key = os.getenv("LLM_API_KEY", "")
        self.llm_api_url = os.getenv("LLM_API_URL", "")
        self.tesseract_cmd = os.getenv("TESSERACT_CMD", "")

    @property
    def max_upload_bytes(self) -> int:
        return self.max_upload_mb * 1024 * 1024


settings = Settings()

# Official / trusted domains used by source checks (extend carefully).
TRUSTED_DOMAINS = {
    "gov.in", "nic.in", "rbi.org.in", "cert-in.org.in", "cybercrime.gov.in",
    "sancharsaathi.gov.in", "uidai.gov.in", "epfindia.gov.in", "irctc.co.in",
    "incometax.gov.in", "npci.org.in", "adityauniversity.in",
}
