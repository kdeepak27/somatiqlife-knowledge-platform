from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
from .config import ROOT

CURRICULA_DIR = ROOT / "config" / "curricula"
LEGACY_PATH = ROOT / "config" / "curriculum.csv"

@dataclass(frozen=True)
class CurriculumItem:
    source_path: Path
    row_index: int
    row: dict[str, str]

def _read(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as h:
        return list(csv.DictReader(h))

def _write(path: Path, rows: list[dict[str, str]]) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as h:
        w = csv.DictWriter(h, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    tmp.replace(path)

def curriculum_files() -> list[Path]:
    files = sorted(CURRICULA_DIR.glob("*.csv")) if CURRICULA_DIR.exists() else []
    if files: return files
    if LEGACY_PATH.exists(): return [LEGACY_PATH]
    raise FileNotFoundError("No curriculum files found.")

def load_all() -> list[CurriculumItem]:
    result=[]; seen=set()
    for path in curriculum_files():
        for idx,row in enumerate(_read(path)):
            mid=row.get("module_id","").strip()
            if not mid: raise ValueError(f"Missing module_id in {path} row {idx+2}")
            if mid in seen: raise ValueError(f"Duplicate module_id: {mid}")
            seen.add(mid); result.append(CurriculumItem(path,idx,row))
    return result

def pending_items(limit: int) -> list[CurriculumItem]:
    out=[]
    for item in load_all():
        if item.row.get("status","").strip().lower()=="pending":
            out.append(item)
            if len(out)>=limit: break
    return out

def set_status(item: CurriculumItem, status: str) -> None:
    rows=_read(item.source_path)
    if rows[item.row_index]["module_id"] != item.row["module_id"]:
        raise RuntimeError("Curriculum changed during generation.")
    rows[item.row_index]["status"]=status
    _write(item.source_path, rows)
