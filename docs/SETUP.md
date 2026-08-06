# Setup

1. In GitHub Desktop, open the existing repository.
2. Delete the old files without deleting the hidden `.git` directory.
3. Copy all contents of `somatiq-studio-v2` into the repository folder.
4. Commit and push to `main`.
5. Add repository secret `OPENAI_API_KEY`.
6. Enable **Settings → Actions → General → Read and write permissions**.
7. Run **Validate SOMatiq Studio V2** using `gpt-4.1-mini`.
8. Run **Generate SOMatiq modules** with count `1`.

The model is a workflow input, so an outdated repository variable cannot override it.
