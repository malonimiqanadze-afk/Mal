import os
import sys

# When packaged by PyInstaller, look for .env next to the .exe, not inside
# the temporary extraction folder.
if getattr(sys, "frozen", False):
  _BASE_DIR = os.path.dirname(sys.executable)
else:
  _BASE_DIR = os.path.dirname(os.path.abspath(__file__))

_ENV_FILE = os.path.join(_BASE_DIR, ".env")


def load_dotenv():
  """Load KEY=VALUE pairs from .env into os.environ (without overriding
  values already set in the real environment)."""
  if not os.path.isfile(_ENV_FILE):
    return

  with open(_ENV_FILE, encoding="utf-8") as f:
    for line in f:
      line = line.strip()
      if not line or line.startswith("#") or "=" not in line:
        continue
      key, value = line.split("=", 1)
      key = key.strip()
      value = value.strip().strip('"').strip("'")
      os.environ.setdefault(key, value)
