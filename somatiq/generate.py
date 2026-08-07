from __future__ import annotations

import os
from pathlib import Path

from openai import OpenAI

from .config import ROOT, load_settings
from .curriculum import load_rows, pending_indices, save_rows
from .render import (
    render_docx,
    render_json,
    render_jsonl,
    render_markdown,
    render_metadata,
    safe_name,
)
from .schema import ModuleContent
from .validation import validate


SYSTEM = ROOT / "prompts" / "system.md"
MODULE = ROOT / "prompts" / "module.md"
DRAFTS = ROOT / "drafts"

MAX_ATTEMPTS_PER_MODULE = 3


def generate_one(
    client: OpenAI,
    model: str,
    row: dict[str, str],
    correction: str = "",
) -> ModuleContent:
    prompt = MODULE.read_text(encoding="utf-8").format(**row)

    if correction:
        prompt += f"""

The previous draft failed automated validation.

Correct the following problem and regenerate the entire module:

{correction}

Return a complete replacement module, not a partial correction.
"""

    completion = client.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "system",
                "content": SYSTEM.read_text(encoding="utf-8"),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        response_format=ModuleContent,
    )

    message = completion.choices[0].message

    if message.refusal:
        raise RuntimeError(
            f"Model refused the request: {message.refusal}"
        )

    if message.parsed is None:
        raise RuntimeError(
            "No parsed structured output was returned."
        )

    return message.parsed


def generate_and_validate(
    client: OpenAI,
    model: str,
    row: dict[str, str],
    settings: dict,
) -> ModuleContent:
    correction = ""
    last_error: Exception | None = None

    for attempt in range(1, MAX_ATTEMPTS_PER_MODULE + 1):
        print(
            f"Generating {row['module_id']} "
            f"with {model}; attempt {attempt}"
        )

        module = generate_one(
            client=client,
            model=model,
            row=row,
            correction=correction,
        )

        try:
            validate(
                module,
                row["module_id"],
                settings,
            )
            return module

        except ValueError as exc:
            last_error = exc
            correction = str(exc)

            print(
                f"Validation failed for {row['module_id']} "
                f"on attempt {attempt}:"
            )
            print(correction)

    raise RuntimeError(
        f"{row['module_id']} failed validation after "
        f"{MAX_ATTEMPTS_PER_MODULE} attempts."
    ) from last_error


def save_module(module: ModuleContent) -> None:
    folder = DRAFTS / (
        f"{module.module_id}_{safe_name(module.title)}"
    )
    folder.mkdir(parents=True, exist_ok=True)

    render_json(
        module,
        folder / "module.json",
    )
    render_metadata(
        module,
        folder / "metadata.json",
    )
    render_markdown(
        module,
        folder / "module.md",
    )
    render_jsonl(
        module,
        folder / "rag_chunks.jsonl",
    )
    render_docx(
        module,
        folder / "module.docx",
    )


def main() -> None:
    model = os.environ.get("OPENAI_MODEL", "").strip()

    if not model:
        raise RuntimeError("OPENAI_MODEL is missing.")

    count = int(os.environ.get("MODULE_COUNT", "1"))

    if not 1 <= count <= 50:
        raise ValueError(
            "MODULE_COUNT must be between 1 and 50."
        )

    client = OpenAI(
        api_key=os.environ["OPENAI_API_KEY"]
    )

    settings = load_settings()
    rows = load_rows()
    indices = pending_indices(rows, count)

    if not indices:
        print("No pending modules remain.")
        return

    for index in indices:
        row = rows[index]

        module = generate_and_validate(
            client=client,
            model=model,
            row=row,
            settings=settings,
        )

        save_module(module)

        rows[index]["status"] = "draft-generated"

        # Save after each module so completed work is preserved
        # if a later module fails.
        save_rows(rows)

        print(f"Completed {module.module_id}")
