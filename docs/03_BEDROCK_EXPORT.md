# Amazon Bedrock Export

The `bedrock-export/` folder is the clean source intended for transfer to the
data source connected to an Amazon Bedrock Knowledge Base.

Each approved module exports:

- `BIO-xxx.md`
- `BIO-xxx.jsonl`

Use Markdown when you want natural document chunking and human readability.
Use JSONL when you have a custom ingestion or preprocessing pipeline.

Do not ingest unreviewed content from `drafts/`.
