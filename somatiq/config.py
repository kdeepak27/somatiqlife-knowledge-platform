import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load_settings():
    return json.loads((ROOT/'config'/'settings.json').read_text(encoding='utf-8'))
