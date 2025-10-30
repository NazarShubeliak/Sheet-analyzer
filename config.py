import logging
import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variable from .env file
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH)

# Mode
DEBUG_MODE: bool = os.getenv("DEBUG_MODE", "false").lower() == "true"

# General Path
LOG_DIR: Path = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

DATA_DIR: Path = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Google Sheet
GOOGLE_CREDENTIALS_PATH: str = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
GOOGLE_SHEET_NAME: str = os.getenv("GOOGLE_SHEET_NAME", "")
WORKSHEET_NAME: str = os.getenv("WORKSHEET_NAME", "")

# Logging Configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: str = "%(asctime)s [%(level)s] %(name)s: %(message)s"
LOG_FILE: Path = LOG_DIR / "analyz.log"


logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format=LOG_FORMAT,
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)

logger = logging.getLogger("analyz")
