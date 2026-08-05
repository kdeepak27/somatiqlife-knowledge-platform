from __future__ import annotations

import csv
import json
import os
from pathlib import Path

from openai import OpenAI

from schemas.module_schema import ModuleContent
from scripts.renderers import (
    render_docx,
    render_json,
    render_jsonl_chunks,
    render_markdown,
    safe_filename,
)
from scripts.validation import validate_module


ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = ROOT / "config" / "curriculum.csv"
SETTINGS = ROOT / "config" / "settings.json"
PROMPT = ROOT / "prompts" / "module_prompt.txt"
DRAFTS = ROOT / "drafts"


def load_rows() -> list[dict[str, str]]:
    with CURRICULUM.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def save_rows(rows: list[dict[str, str]]) -> None:
    with CURRICULUM.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def next_pending_index(rows: list[dict[str, str]]) -> int | None:
    for index, row in enumerate(rows):
        if row["status"].strip().lower() == "pending":
            return index
    return None


def generate(row: dict[str, str], settings: dict) -> ModuleContent:
    prompt = PROMPT.read_text(encoding="utf-8").format(
        module_id=row["module_id"],
        title=row["title"],
        subtitle=row["subtitle"],
        domain=row["domain"],
        category=row["category"],
    )

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    model = os.getenv(
        "OPENAI_MODEL",
        settings.get("default_model", "gpt-5.6"),
    )

    response = client.responses.parse(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    "Produce accurate, structured, consumer-health "
                    "educational content."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        text_format=ModuleContent,
    )

    module = response.output_parsed
    if module is None:
        raise RuntimeError("The API response did not contain parsed output.")

    if module.module_id != row["module_id"]:
        raise ValueError(
            f"Expected module ID {row['module_id']}, "
            f"received {module.module_id}."
        )

    validate_module(
        module,
        minimum_customer_questions=settings["minimum_customer_questions"],
        minimum_sections=settings["minimum_sections"],
        minimum_key_takeaways=settings["minimum_key_takeaways"],
        minimum_illustrations=settings["minimum_illustrations"],
    )

    return module


def main() -> None:
    settings = json.loads(SETTINGS.read_text(encoding="utf-8"))
    rows = load_rows()
    index = next_pending_index(rows)

    if index is None:
        print("No pending modules remain.")
        return

    row = rows[index]
    module = generate(row, settings)

    folder = DRAFTS / (
        f"{module.module_id}_{safe_filename(module.title)}"
    )
    folder.mkdir(parents=True, exist_ok=True)

    render_json(module, folder / "module.json")
    render_markdown(module, folder / "module.md")
    render_jsonl_chunks(module, folder / "rag_chunks.jsonl")
    render_docx(module, folder / "module.docx")

    rows[index]["status"] = "draft-generated"
    save_rows(rows)

    print(f"Generated {module.module_id}: {module.title}")


if __name__ == "__main__":
    main()
