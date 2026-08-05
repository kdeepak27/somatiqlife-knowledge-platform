# Local Development

```bash
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
pip install -r requirements.txt
```

Set the environment variables:

```bash
export OPENAI_API_KEY="..."
export OPENAI_MODEL="..."
```

Run the next pending module:

```bash
python scripts/generate_module.py
```

Run tests:

```bash
pytest
```

Build indexes:

```bash
python scripts/build_indexes.py
```

Build a Bedrock export from approved modules:

```bash
python scripts/export_bedrock.py
```
