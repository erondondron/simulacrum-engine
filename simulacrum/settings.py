import os
from pathlib import Path

from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv(), verbose=True)

STORAGE = Path(os.getenv("STORAGE", ""))
STORAGE.mkdir(parents=True, exist_ok=True)
