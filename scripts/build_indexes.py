from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "drafts"
APPROVED = ROOT / "approved"
INDEXES = ROOT / "indexes"


def collect(base: Path, status: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted(base.glob("*/module.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append(
            {
                "module_id": data["module_id"],
                "title": data["title"],
                "domain": data["domain"],
                "category": data["category"],
                "version": data.get("version", ""),
                "status": status,
                "path": str(path.relative_to(ROOT)),
            }
        )
    return rows


def main() -> None:
    INDEXES.mkdir(parents=True, exist_ok=True)
    rows = collect(DRAFTS, "draft") + collect(APPROVED, "approved")

    destination = INDEXES / "module_index.csv"
    with destination.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = [
            "module_id",
            "title",
            "domain",
            "category",
            "version",
            "status",
            "path",
        ]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {destination}")


if __name__ == "__main__":
    main()
