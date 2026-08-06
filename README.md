# SOMatiq Studio V2

GitHub Actions pipeline for generating structured SOMatiq health modules and
producing JSON, Markdown, JSONL, DOCX, metadata, indexes, and Bedrock exports.

## First run

1. Replace the old repository contents with this folder's contents.
2. Add the repository secret `OPENAI_API_KEY`.
3. Enable **Settings → Actions → General → Read and write permissions**.
4. Run **Validate SOMatiq Studio V2** with `gpt-4.1-mini`.
5. Run **Generate SOMatiq modules** with count `1`.

`module.json` is the authoritative source. Drafts require scientific, clinical,
and editorial review before being copied to `approved/`.
