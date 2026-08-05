from __future__ import annotations

from schemas.module_schema import ModuleContent


def validate_module(
    module: ModuleContent,
    *,
    minimum_customer_questions: int = 8,
    minimum_sections: int = 8,
    minimum_key_takeaways: int = 5,
    minimum_illustrations: int = 3,
) -> None:
    errors: list[str] = []

    if len(module.customer_questions) < minimum_customer_questions:
        errors.append(
            f"Expected at least {minimum_customer_questions} customer questions."
        )

    if len(module.sections) < minimum_sections:
        errors.append(f"Expected at least {minimum_sections} main sections.")

    if len(module.key_takeaways) < minimum_key_takeaways:
        errors.append(
            f"Expected at least {minimum_key_takeaways} key takeaways."
        )

    if len(module.illustrations) < minimum_illustrations:
        errors.append(
            f"Expected at least {minimum_illustrations} illustration specifications."
        )

    if len(module.retrieval_summary.split()) < 150:
        errors.append("Retrieval summary should contain at least 150 words.")

    if not module.safety_notes:
        errors.append("Safety notes are required.")

    if "review required" not in module.review_status.lower():
        errors.append("Review status must state that review is required.")

    if errors:
        raise ValueError("Module validation failed:\n- " + "\n- ".join(errors))
