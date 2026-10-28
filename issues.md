# Lab 5 — Issues Found and Fixed

**Student:** Rachit S Mane · **SRN:** PES1UG24AM214 · **File:** `expense_tracker.py`

The findings come from the baseline reports in `reports/before/`, which are the original Pylint 4.1.3, Bandit 1.9.4 and Flake8 7.4.1 output for the unmodified file. "Line(s)" are original line numbers. Rows are ordered by severity: Bandit High and Medium first, then the remaining findings. Issues 6–8 were found by manual review; no tool reported them. The numbering matches Section 6 of `submission/Lab5_Static_Code_Analysis_Report.md`.

## Issue Table

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| 1. Bandit **B605** start_process_with_a_shell | Security — **High** severity, High confidence (CWE-78) | 61 | `os.system("xdg-open " + path)` runs the path through a shell. Characters like `;` or `&` in a path could run extra commands. Also Linux-only. | Resolve the path and require an existing file, else raise `FileNotFoundError`. Open it with `webbrowser.open(Path(...).as_uri())`, so no shell is involved and it works on any OS. |
| 2. Bandit **B306** blacklist (`mktemp`) | Security — **Medium** severity, High confidence (CWE-377) | 55 | `tempfile.mktemp()` returns a name without creating the file. Another process can create that file first (race condition). | Use `tempfile.mkstemp()`, which creates the file atomically with owner-only permissions. Wrap the descriptor in `os.fdopen(...)` inside `with` so it is always closed. |
| 3. Bandit **B108** hardcoded_tmp_directory | Security — **Medium** severity, Medium confidence (CWE-377) | 8 | Hardcoded, shared `/tmp/expense_reports` path is predictable and does not exist on Windows. | Build it from `tempfile.gettempdir()`. Create it on demand with `os.makedirs(..., mode=0o700, exist_ok=True)`. |
| 4. Bandit **B105** hardcoded_password_string | Security — Low severity, Medium confidence (CWE-259) | 5, 50 | The bank-sync password is a string literal in the source, compared with `==`. | Read it from the `BANK_SYNC_PASSWORD` environment variable. Reject every attempt if it is unset or empty, or if the input is not a string. Compare with `hmac.compare_digest`. Never print it. |
| 5. Pylint **W0718** broad-exception-caught | Correctness — Warning | 41 | `except Exception` around `max()` hides every error, not just the empty-list case. | Replace the `try/except` with `max(..., default=None)`. |
| 6. `None` dereference (manual review) | Correctness — Bug | 75 | `biggestExpense()["note"]` raises `TypeError` when there are no expenses. | Check first: `biggest["note"] if biggest else None`. |
| 7. Demo runs on import (manual review) | Correctness — Bug | 80 | `main()` was called at module level, so importing the module ran the demo. | `if __name__ == "__main__": main()` |
| 8. Weak amount validation (manual review) | Correctness — Validation | 12 | Only `amount <= 0` was rejected. `NaN`, infinity and `True` were accepted, and strings raised `TypeError`. | Accept only finite `int`/`float` values (not `bool`) greater than 0. `set_budget` raises `ValueError` for invalid or negative values. |
| 9. Pylint **W0603** global-statement, **C0103** on `monthly_budget` | Design — Warning / Convention | 7, 29 | Module-level mutable state changed through `global`. Pylint also treats `monthly_budget` as a misnamed constant. | Move `expenses` and the budget into an `ExpenseTracker` class. The default becomes the constant `DEFAULT_MONTHLY_BUDGET`. |
| 10. Pylint **C0103** invalid-name (11 names) | Convention — Naming | 11, 20, 28, 33, 38, 44, 49, 53, 55, 59 | camelCase function, argument and variable names, e.g. `addExpense`, `newBudget`, `reportPath`. | Rename to snake_case, e.g. `add_expense`, `new_budget`, `report_path`. |
| 11. Pylint **C0114** / **C0116** missing docstrings | Convention — Documentation | 1; 11, 20, 28, 33, 38, 44, 49, 53, 59, 64 | No module docstring; 10 functions without docstrings. | Add docstrings to the module, class, all methods and all functions. |
| 12. Pylint **C0200** consider-using-enumerate | Convention — Idiom | 45 | `for i in range(len(expenses))` with indexing. | `for number, expense in enumerate(self.expenses, start=1)` |
| 13. Flake8 **E203** | Style | 15 | Whitespace before `:` in `{"amount" : amount`. | Remove the space. |
| 14. Flake8 **E302** | Style | 44 | One blank line before a top-level `def` (two expected). | Resolved by the class restructuring: it is now a correctly spaced method. |
| 15. Flake8 **E261** | Style | 74 | One space before an inline comment (two expected). | Use two spaces. |
| 16. Flake8 **E501** | Style | 77 | Line of 93 characters (limit 79). | Wrap the `print` call over two lines. |

## Verified Final Status

All 16 issues are fixed in the committed source. The final reports are in `reports/after/`.

| Check | Result |
|---|---|
| Pylint | **10.00/10** (baseline 5.27/10); 0 messages; no checks disabled |
| Bandit | **No issues identified** (baseline: 1 High, 2 Medium, 1 Low); 0 `#nosec` skips |
| Flake8 | **0 violations** (baseline: 4); the report file is empty |
| Demo output | Identical to the baseline output |
| Import | `import expense_tracker` prints nothing |
| Verification tests | 18 tests run, all passed (details in `submission/Lab5_Static_Code_Analysis_Report.md`, Section 10) |

| Commit | Issues addressed |
|---|---|
| `a170679` Fix Pylint code quality issues | 5–12, plus 14 and 16 as a side effect of the restructuring |
| `cc9ce66` Fix Bandit security findings | 1–4 |
| `e1d3242` Fix Flake8 style violations | 13, 15 |
