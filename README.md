# Telco Customer Churn — EDS Bootcamp (NOVA IMS)

An initial working project based on the **five original course workbooks**, the
course project guide (`references/project_guide.pdf`), and the *folder conventions*
of the Lending Club lab. The project-specific code is newly written; this is
**not** a copy of the instructor's Lending Club solution.

## What is and isn't part of this starter

- **Done**: raw data kept unchanged, data integrity checks, customer joins,
  initial notebook, target specification and an optional logistic baseline.
- **Not yet done**: agreed prediction timestamp, full EDA, model comparisons,
  threshold choice based on operational capacity, calibration, retention
  economics, uncertainty analysis, explainability and final report.
- The university guide does **not** specify a delivery rubric or mandatory app.
  Any report, dashboard, app or model card is a proposal until requirements are confirmed.

## Start in VS Code (Windows, Python 3.13)

1. Extract this ZIP into a separate folder (e.g. `edsb/telco-churn`), then
   use **File > Open Folder** and select that specific folder.
2. In its integrated terminal:

   ```powershell
   py -3.13 -m venv .venv
   .venv\Scripts\activate
   python -m pip install -r requirements.txt
   ```

   You may instead use **Python: Create Environment** and select `requirements.txt`.
   Select that project's `.venv` as the interpreter and notebook kernel.
3. Check the data import and row grain:

   ```powershell
   python -m unittest discover
   python -m src.data
   ```

4. Open `notebooks/01_data_audit.py`, run the notebook from the top and inspect
   the numbers and charts. **This is the recommended first task.**
5. Only after discussing the feature timing risk, optionally run the illustrative
   model (it uses an untouched test set but only a single candidate model):

   ```powershell
   python -m src.train_baseline
   ```

   Validation metrics appear in `reports/generated/`, which is ignored by Git.
   By default, **the holdout is not scored**. Only when the design is fully
   finalized may you run `python -m src.train_baseline --evaluate-holdout`
   once, to get the final test metrics. Do not use the holdout for tuning.

## Structure

```text
README.md
requirements.txt
.gitignore
data/raw/            original Telco Excel workbooks (do not modify or commit to Git)
data/interim/        intermediate outputs
data/processed/      reproducible cleaned outputs
notebooks/01_data_audit.ipynb
src/data.py          joins, validation, raw data loading
src/features.py      exclusion list + baseline variables
src/train_baseline.py illustrative stratified baseline
models/             not committed
reports/business_brief.md
reports/data_audit.md
reports/generated/   reproducible outputs, not committed
references/project_guide.pdf
tests/test_data.py
```

## Important leakage caution

This is **one end-of-Q3 snapshot without a year**. Neither a customer timeline
nor pre-churn measurements are supplied. The baseline explicitly excludes the
outcome fields and the existing Churn Score, and conservatively excludes
Satisfaction Score, CLTV and Offer. However, even tenure, service status and
current charges may reflect the end-of-quarter (after-churn) snapshot.
Accordingly, the model estimates **retrospective discrimination in this sample**;
its scores cannot be represented as validated prospective predictions.

## Future business extension

Set a contact budget (e.g. top 10% as a scenario) and show: customers targeted,
precision@K, recall@K, lift, and customer groups. An expected-value calculation
would require **assumed or measured** contact costs, effectiveness/uplift,
margin and lifetime value. High churn risk alone is not proof that a customer
can be retained or that a discount is economically rational.

## Alignment with the supplied Class 3 lab (NOVA IMS)

This update applies the Class 3 conventions. The *actual* project uses the original five Telco workbooks, not the Lending Club example.

- Commit notebooks as `notebooks/*.py` (Jupytext percent format); generate `.ipynb` locally with `python -m jupytext --to ipynb notebooks/01_data_audit.py`. The `.gitignore` ignores `*.ipynb`.
- Keep `.venv`, `.env`, datasets (`data/raw`), generated files and fitted models **out of Git**. Each colleague obtains the course data independently and places the five files in `data/raw`.
- Keep human-written reports (including `reports/ai_usage_log.md`) and source code in Git. Record the source of data in the project docs.
- After setting up the environment use `python -m pip freeze > requirements-installed.txt` and commit it after agreeing versions across the team, as the Class 3 instructor suggests. This can include platform-specific packages: investigate inconsistencies rather than blindly installing the full freeze on every OS.
- Optional quality check: `python -m unittest discover` (before creating PRs).
- Do not commit API keys, Hugging Face tokens, or model/data artifacts to a public hosting service. `.env.example` illustrates local settings only.

## GitHub group setup (private; required by Class 3 instructions)

1. In VS Code: Source Control > Initialize Repository (or `git init`), then stage your **code and docs**. Check Source Control: `.venv`, `.env` and `data/raw/*.xlsx` must not appear.
2. Commit: `git add .` then `git commit -m "Initialize Telco churn project"`.
3. Source Control > Publish Branch > publish as **Private** on GitHub.
4. In the GitHub repository settings, invite group members **and both lecturers** as collaborators (Class 3 instruction).
5. Each group member clones the repository, creates their own `.venv`, installs `requirements.txt`, and restores the course data locally to `data/raw`.
6. Use one small branch per task (e.g. `feature/eda`, `feature/model-selection`), open a pull request to `main`, request peer review, and merge once checked.

On the command line, after the repository exists:

```bash
git switch main
git pull origin main
git switch -c feature/eda
# edit and run tests ...
git add notebooks/01_data_audit.py reports/data_audit.md
git commit -m "Audit churn by contract and validate keys"
git push -u origin feature/eda
# Now open a Pull Request on GitHub.
```

`git add .` should only run after checking `.gitignore`, particularly when more files have been added.

## Hugging Face — optional, not part of the Class 3 code

The Class 3 files cover VS Code/Git/GitHub/Jupytext/profiling; they **do not** provide a Hugging Face implementation. A possible later-stage extension is an interactive Gradio demo (locally or on a Hugging Face Space), showing risk estimates and the limits of the retrospective dataset. This is optional and should follow sound model validation. Check current hosting/pricing/visibility conditions and approval to publish artifacts before deployment.
