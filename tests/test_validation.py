import pytest

from schemas.module_schema import (
    IllustrationSpec,
    Misconception,
    ModuleContent,
    Section,
)
from scripts.validation import validate_module


def make_valid_module() -> ModuleContent:
    return ModuleContent(
        module_id="BIO-001",
        title="What Is Health?",
        subtitle="A test module",
        domain="Human Biology",
        category="Health Foundations",
        keywords=["health"],
        customer_questions=[f"Question {i}?" for i in range(8)],
        retrieval_summary=" ".join(["summary"] * 160),
        learning_objectives=["Understand health."],
        definition="Health is multidimensional.",
        why_this_matters="Health affects function and quality of life.",
        sections=[
            Section(heading=f"Section {i}", content="Complete context.")
            for i in range(8)
        ],
        practical_guidance=["Use evidence-based habits."],
        safety_notes=["Seek professional care for urgent symptoms."],
        misconceptions=[
            Misconception(
                misconception="Health means no diagnosis.",
                reality="Health also includes function and well-being.",
            )
        ],
        clinical_pearls=["Function matters."],
        key_takeaways=[f"Takeaway {i}" for i in range(5)],
        glossary={"Health": "A multidimensional state."},
        related_modules=["BIO-002"],
        illustrations=[
            IllustrationSpec(
                illustration_id=f"IMG-BIO-001-00{i}",
                title="Figure",
                illustration_type="Infographic",
                description="Description",
                alt_text="Alt text",
            )
            for i in range(3)
        ],
        references=[],
        evidence_strength="High",
    )


def test_valid_module_passes() -> None:
    validate_module(make_valid_module())


def test_short_section_list_fails() -> None:
    module = make_valid_module()
    module.sections = module.sections[:2]
    with pytest.raises(ValueError):
        validate_module(module)
