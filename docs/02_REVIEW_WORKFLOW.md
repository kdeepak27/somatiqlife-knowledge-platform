# Review Workflow

## Draft stage

AI-generated content is written to `drafts/`.

Do not use this folder as a customer-facing Amazon Bedrock data source.

## Human review

Review each module for:

- scientific accuracy;
- clinical safety;
- clarity and reading level;
- unsupported claims;
- reference accuracy;
- retrieval quality;
- duplicate or contradictory content;
- suitability of safety notes.

## Approval

After review, copy the complete module folder from `drafts/` to `approved/`.
Update `review_status` and version information in `module.json` before approval.

## Bedrock export

Run the `Build Bedrock export` GitHub Actions workflow.

It copies only approved Markdown and JSONL files into `bedrock-export/`.
