from __future__ import annotations

from pydantic import BaseModel, Field


class Section(BaseModel):
    heading: str
    content: str


class Misconception(BaseModel):
    misconception: str
    reality: str


class IllustrationSpec(BaseModel):
    illustration_id: str
    title: str
    illustration_type: str
    description: str
    alt_text: str


class Reference(BaseModel):
    title: str
    organization_or_authors: str = ""
    year: str = ""
    identifier: str = ""
    verification_status: str = "unverified"


class ModuleContent(BaseModel):
    module_id: str
    title: str
    subtitle: str
    domain: str
    category: str

    som_stages: list[str] = Field(
        default_factory=lambda: ["Stabilize", "Optimize", "Maximize"]
    )
    audience: list[str] = Field(default_factory=lambda: ["General adults"])
    reading_level: str = "General public"

    keywords: list[str]
    customer_questions: list[str]
    retrieval_summary: str
    learning_objectives: list[str]

    definition: str
    why_this_matters: str
    sections: list[Section]

    practical_guidance: list[str]
    safety_notes: list[str]
    misconceptions: list[Misconception]
    clinical_pearls: list[str]
    key_takeaways: list[str]

    glossary: dict[str, str]
    related_modules: list[str]
    illustrations: list[IllustrationSpec]
    references: list[Reference]

    evidence_strength: str
    version: str = "1.0"
    review_status: str = (
        "AI draft - scientific, clinical, and editorial review required"
    )
