# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def require_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        raise RuntimeError(f"Missing required env var: {name}")
    return val

MARKETAUX_API_KEY = require_env("MARKETAUX_API_KEY")