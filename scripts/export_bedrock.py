from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVED = ROOT / "approved"
EXPORT = ROOT / "bedrock-export"


def main() -> None:
    EXPORT.mkdir(parents=True, exist_ok=True)

    for old_file in EXPORT.glob("*"):
        if old_file.is_file():
            old_file.unlink()

    count = 0
    for module_folder in sorted(APPROVED.iterdir()):
        if not module_folder.is_dir():
            continue

        module_id = module_folder.name.split("_", 1)[0]

        for source_name, suffix in [
            ("module.md", ".md"),
            ("rag_chunks.jsonl", ".jsonl"),
        ]:
            source = module_folder / source_name
            if source.exists():
                shutil.copy2(source, EXPORT / f"{module_id}{suffix}")
                count += 1

    print(f"Exported {count} files to {EXPORT}")


if __name__ == "__main__":
    main()
