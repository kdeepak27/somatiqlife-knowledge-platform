# GitHub Setup

1. Create a **private** repository.
2. Keep the default `main` branch.
3. Upload the contents of the starter folder to the repository root.
4. Commit the upload.
5. Open **Settings → Secrets and variables → Actions**.
6. Add a repository secret:
   - Name: `OPENAI_API_KEY`
   - Value: your OpenAI API key
7. Add a repository variable:
   - Name: `OPENAI_MODEL`
   - Value: a model available to your API project
8. Open **Settings → Actions → General**.
9. Under **Workflow permissions**, choose **Read and write permissions**.
10. Open the **Actions** tab and run:
    - `Generate next SOMatiq module`

The workflow generates only one pending module per run.
