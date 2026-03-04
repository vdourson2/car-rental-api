# Ruff Configuration Guide

This document outlines how **Ruff** is configured for the *car‑rental‑api* project and the steps we followed to set it up.

---

## 1. Why Ruff?
Ruff is a fast Python linter and formatter written in Rust. It replaces a collection of slower tools (flake8, isort, black, etc.) with a single, high‑performance binary.

---

## 2. Configuration Location
All Ruff settings live in the project's `pyproject.toml` under the `[tool.ruff]` table:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.format]
quote-style = "double"
indent-style = "space"

[tool.ruff.lint]
ignore = ["E501"]
select = [
    "E",  # pycodestyle errors
    "F",  # pyflakes
    "I",  # imports
    "UP", # pyupgrade
    "B",  # bugbear
]
```

---

## 3. How We Added Ruff to the Project
1. **Install Ruff** – added as a development dependency via `pip`:
   ```bash
   pip install ruff
   ```
2. **Add to `pyproject.toml`** – inserted the `[tool.ruff]` table (see section 2).
3. **Integrate with pre‑commit** – updated `.pre-commit-config.yaml`:
   ```yaml
   repos:
     - repo: https://github.com/astral-sh/ruff-pre-commit
       rev: v0.4.0
       hooks:
         - id: ruff
           args: [--fix]
         - id: ruff-format
   ```
   This ensures Ruff runs on every commit and automatically fixes what it can.
4. **Install the git hook** – run the following command to set up the pre-commit hooks in your local repository:
   ```bash
   pre-commit install
   ```
5. **Run locally** – execute `ruff check .` to lint the whole repository or `ruff format .` to format it.
6. **CI Integration** – added a step in the CI pipeline to run `ruff check .` and `ruff format --check .` to fail the build on lint or formatting errors.

---

## 4. Custom Rules & Rationale
| Rule | Reason |
|------|--------|
| `E501` (line too long) | Ignored because we rely on Ruff's `line-length` setting and allow a few longer strings for readability. |
| `D203` (blank line before class docstring) | Ignored to keep docstrings tightly coupled with class definitions, matching our existing style. |
| `C90` (complexity) | Added via `extend-select` to enforce cyclomatic complexity limits. |

---

## 5. Running Ruff
- **Check only** (no modifications): `ruff check .`
- **Auto‑fix** where possible: `ruff check . --fix`
- **Format code**: `ruff format .`
- **Run pre-commit on all files**: `pre-commit run --all-files`
- **Specific files**: `ruff check path/to/file.py`

---

## 6. Tips & Gotchas
- Ruff updates frequently; periodically bump the version in `requirements-dev.txt` or your `pip` environment.
- When adding new third‑party libraries, run `ruff check .` to see if any new lint rules need to be addressed.
- The `fix = true` flag in `pyproject.toml` enables auto‑fix for supported rules during pre‑commit runs.

---

*Document last updated: 2026‑03‑04*
