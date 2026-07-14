import os
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[2]


def resolve_data_dir() -> Path:
    """App data root: backend/data/dev (local) or /app/data (= data/prod in compose)."""
    explicit = os.getenv("DATA_DIR")
    if explicit:
        return Path(explicit)
    if os.getenv("SERVICE_MODE") == "production":
        return Path("/app/data")
    return BACKEND_ROOT / "data" / "dev"


DATA_DIR = resolve_data_dir()
_logs_override = os.getenv("LOGS_DIR")
LOGS_DIR = Path(_logs_override) if _logs_override else DATA_DIR / "logs"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{(DATA_DIR / 'database.db').as_posix()}",
)

JWT_ALGORITHM = "HS256"
TOKEN_INACTIVITY_EXPIRE_HOURS = 30 * 24
MAX_TOKEN_LIFETIME_HOURS = 365 * 24
OWNER_USERNAME = "denis0001-dev"
JWT_SECRET_KEY = os.getenv("JWT_SECRET")

if not JWT_SECRET_KEY:
    raise ValueError("JWT secret key empty")
