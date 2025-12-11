# tests/conftest.py
import sys
from pathlib import Path

# Añadir el directorio raíz del proyecto al sys.path
ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))