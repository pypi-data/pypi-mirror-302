"""Config module.

Raises:
    ValueError: if MMTX_HOST, MMTX_API_PORT, MMTX_USER or MMTX_PASS are not set
        in the environment variables or .env file
"""

import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "dev")

DEBUG = os.getenv("DEBUG", ENV == "dev")

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_FORMAT = os.getenv(
    "LOG_FORMAT",
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

USE_SSL: bool = os.getenv("USE_SSL", "False").lower() in [
    "true",
    "1",
    "t",
    "y",
    "yes",
    "on",
    "enable",
    "enabled",
]
MMTX_HOST = os.getenv("MMTX_HOST", "localhost")
MMTX_API_PORT = int(os.getenv("MMTX_API_PORT", "9997"))
MMTX_API_BASE_PATH = os.getenv("MMTX_API_ROOT_PATH", "/v3")
MMTX_USER = os.getenv("MMTX_USER", "admin")
MMTX_PASS = os.getenv("MMTX_PASS", "")


if not MMTX_HOST or not MMTX_API_PORT or not MMTX_USER or not MMTX_PASS:
    raise ValueError(
        "MMTX_HOST, MMTX_API_PORT, MMTX_USER and MMTX_PASS are required, "
        "set in .env file or environment variable"
    )

MMTX_API_URL = (
    f"http{'s' if USE_SSL else ''}://{MMTX_HOST}:{MMTX_API_PORT}{MMTX_API_BASE_PATH}"
)
