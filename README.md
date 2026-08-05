# SOMatiq Knowledge Platform

Private, repository-backed authoring and publishing pipeline for a consumer-health
knowledge base designed for Amazon Bedrock Knowledge Bases and RAG applications.

## What this starter includes

- A structured curriculum file
- A reusable Pydantic content schema
- A production-oriented module prompt
- A Python generator using the OpenAI Responses API
- Markdown, JSON, JSONL, and DOCX renderers
- Automated validation
- A manually triggered GitHub Actions workflow
- Draft, approved, and Bedrock-export stages
- Basic tests
- A Word style template
- Documentation for setup, review, and Bedrock export

## Repository layout

```text
.github/workflows/        GitHub Actions workflows
approved/                 Human-reviewed modules
bedrock-export/           Only approved files intended for Bedrock
config/                   Curriculum and pipeline settings
docs/                     Setup and operating instructions
drafts/                   AI-generated drafts
indexes/                  Generated indexes
prompts/                  Generation prompts
references/               Controlled reference resources
schemas/                  Pydantic schemas
scripts/                  Generation and export scripts
templates/                DOCX and Markdown templates
tests/                    Automated tests
```

## Fast setup

1. Create a private GitHub repository.
2. Upload the **contents** of this folder to the repository root.
3. In GitHub, open **Settings → Secrets and variables → Actions**.
4. Create a repository secret named `OPENAI_API_KEY`.
5. Create a repository variable named `OPENAI_MODEL`, or use the workflow default.
6. Open **Settings → Actions → General → Workflow permissions**.
7. Select **Read and write permissions**.
8. Open the **Actions** tab.
9. Run **Generate next SOMatiq module** manually.

The first run generates the first curriculum row whose status is `pending`.

## Review status

Generated health content is a draft and must receive scientific, clinical, and
editorial review before it is moved to `approved/` or `bedrock-export/`.
