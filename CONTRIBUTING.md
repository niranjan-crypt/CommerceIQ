# Contributing to CommerceIQ

Thank you for your interest in contributing to **CommerceIQ**! We welcome contributions from data engineers, analytics engineers, and SQL enthusiasts of all skill levels.

---

## 🧭 Code of Conduct

This project is governed by the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code of conduct.

---

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.9, 3.10, or 3.11
- Git
- SQLite 3 or PostgreSQL 16 (optional: Docker)

### 2. Fork & Clone
```bash
git clone https://github.com/niranjan-crypt/CommerceIQ.git
cd CommerceIQ
git checkout develop
```

### 3. Environment Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🌿 Git Branching Workflow

We adhere to a structured GitFlow branching strategy:
- `main`: Production release branch. Only updated via release PRs or tags.
- `develop`: Primary integration branch for new features and bugfixes.
- `feature/<name>`: New analytical models, pipelines, or UI modules.
- `fix/<issue-name>`: Bug fixes and schema corrections.
- `docs/<topic>`: Documentation enhancements.

### Commit Conventions
Commits must follow the [Conventional Commits](https://www.conventionalcommits.org/) format:
- `feat(scope)`: A new feature (e.g. `feat(sql): add customer churn prediction model`)
- `fix(scope)`: A bug fix (e.g. `fix(loader): resolve foreign key ordering constraint`)
- `docs(scope)`: Documentation updates
- `perf(scope)`: Performance optimization or query tuning
- `test(scope)`: Adding or updating tests
- `chore(scope)`: Tooling, dependency, or configuration updates

---

## 📊 Proposing & Adding Analytical SQL Models

1. Add your query file under `sql/` (e.g. `sql/14_customer_churn.sql`).
2. Include extensive inline comments explaining the business hypothesis, mathematical formulas, and window function logic.
3. Test your query locally:
   ```bash
   python run_query.py sql/14_customer_churn.sql
   ```
4. Export the markdown query output under `outputs/`.
5. Run the regression test suite:
   ```bash
   python -m unittest tests/test_data_quality.py -v
   ```

---

## 🚀 Pull Request Checklist

Before submitting a PR to `develop`:
- [ ] Code follows existing PEP 8 formatting and SQL naming standards.
- [ ] All 22 automated data quality checks pass (`python python/data_validation.py`).
- [ ] Regression unit tests pass (`python -m unittest tests/test_data_quality.py`).
- [ ] Documentation updated in `README.md` or `docs/` where applicable.
