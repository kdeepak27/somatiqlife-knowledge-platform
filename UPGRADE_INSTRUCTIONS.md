# Install this upgrade

1. In GitHub Desktop, Fetch/Pull the latest repository.
2. Copy this package's contents into the matching paths in your repository.
3. BEFORE generating, run locally from the repository root:
   `python -m scripts.migrate_curriculum`
   This splits your existing combined `config/curriculum.csv` into
   `config/curricula/biology.csv` and `config/curricula/nutrition.csv` while
   preserving their current statuses.
4. Verify:
   - config/curricula/biology.csv
   - config/curricula/nutrition.csv
   - config/curricula/exercise.csv
5. Commit and push: `Upgrade generator and add EXE-001 to EXE-250`
6. Run the Validate workflow.
7. Run Generate SOMatiq modules with 5 modules first.
8. If successful, use 25; then 50.

The upgraded generator:
- reads all CSV files in `config/curricula/`;
- supports batches up to 50;
- retries temporary API errors;
- retries validation failures;
- continues past an individual failed module;
- leaves failed modules pending;
- checkpoint-commits every 5 successful modules;
- writes `indexes/last_generation_report.json`.

Do not delete the old combined curriculum until you have verified the split
files. Once `config/curricula/*.csv` exists, the upgraded loader uses them.
