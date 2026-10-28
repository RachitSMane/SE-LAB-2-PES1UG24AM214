# Lab 5: Static Code Analysis — Personal Expense Tracker

| | |
|---|---|
| **Student** | Rachit S Mane |
| **SRN** | PES1UG24AM214 |
| **Repository** | `L5_32_expense_tracker` |
| **Source file** | `expense_tracker.py` |
| **Date** | 28 October 2026 |

---

## 1. Objective

Use three static analysis tools — **Pylint** (code quality), **Bandit** (security) and **Flake8** (style) — to find problems in a small Python program, fix them without changing what the program does, and confirm the fixes by rerunning the tools and testing the program.

## 2. Project Overview

`expense_tracker.py` is a monthly expense tracker. It:

- records expenses with an amount, category, note and timestamp, and rejects invalid amounts;
- totals spending per category;
- tracks the remaining monthly budget;
- finds the biggest expense;
- checks a bank-sync password;
- has two helpers not called by the demo: one that creates a report file and one that opens a statement file.

Running `python expense_tracker.py` performs a short demonstration that needs no input. It keeps all data in memory and reads or writes no files, so it is safe to run repeatedly.

The README describes the starting code as working "but only just", with quality, style and security problems.

## 3. Tools and Environment

| Item | Version / Detail |
|---|---|
| OS | Windows 10 Pro (10.0.19045) |
| Python | 3.13.2 |
| Pylint | 4.1.3 (astroid 4.3.4) |
| Bandit | 1.9.4 |
| Flake8 | 7.4.1 (pycodestyle 2.15.0, pyflakes 4.0.3, mccabe 0.7.0) |
| Isolation | Tools installed in a project virtual environment `.venv/` (excluded by `.gitignore`) |

All tools were run with their default settings. No configuration files, disabled checks or `# nosec` / `# noqa` / `# pylint: disable` comments were used.

## 4. Methodology

1. **Baseline run.** Ran the program and recorded its output. Ran each tool against the unmodified file and saved its full output (stdout and stderr) unedited to `reports/before/`.
2. **Triage.** Grouped findings by tool and severity, separated genuine defects from judgement calls, and looked for defects the tools did not report.
3. **Fix in focused commits.** Applied fixes in three commits — Pylint, then Bandit, then Flake8. After each change, reran all three tools and the demo to check for regressions.
4. **Final run.** Reran the tools on the final source and saved the output to `reports/after/`.
5. **Validation.** Compared the demo output with the baseline, checked import behaviour, and ran a unit-test script covering normal use, edge cases and the security fixes.

Commands used (from the repository root, with the virtual environment's interpreter):

```
python -m pylint expense_tracker.py  > reports/before/pylint_report_before.txt 2>&1
python -m bandit -r expense_tracker.py > reports/before/bandit_report_before.txt 2>&1
python -m flake8 expense_tracker.py  > reports/before/flake8_report_before.txt 2>&1
```

The same commands, writing to `reports/after/*_after.txt`, produced the final reports.

## 5. Baseline Results

**Program output (baseline):**

```
Biggest expense before any entries: None
Ignoring invalid amount -50
1 Food 450
2 Travel 1200
3 Food 300
4 Bills 999
Totals: {'Food': 750, 'Travel': 1200, 'Bills': 999}
Remaining budget: 2051
Biggest expense: Cab to airport
Sync password accepted: False
Summary: 4 expenses recorded against a budget of 5000
```

### 5.1 Pylint — 5.27/10, 26 messages

| Code | Symbol | Count | Original line(s) |
|---|---|---|---|
| C0103 | invalid-name | 12 | 7, 11, 20, 28 (×2), 33, 38, 44, 49, 53, 55, 59 |
| C0116 | missing-function-docstring | 10 | 11, 20, 28, 33, 38, 44, 49, 53, 59, 64 |
| C0114 | missing-module-docstring | 1 | 1 |
| W0603 | global-statement | 1 | 29 |
| W0718 | broad-exception-caught | 1 | 41 |
| C0200 | consider-using-enumerate | 1 | 45 |

### 5.2 Bandit — 4 issues (1 High, 2 Medium, 1 Low)

| ID | Test | Line | Severity | Confidence | CWE |
|---|---|---|---|---|---|
| B605 | start_process_with_a_shell | 61 | **High** | High | CWE-78 |
| B306 | blacklist (`mktemp`) | 55 | Medium | High | CWE-377 |
| B108 | hardcoded_tmp_directory | 8 | Medium | Medium | CWE-377 |
| B105 | hardcoded_password_string | 5 | Low | Medium | CWE-259 |

### 5.3 Flake8 — 4 violations

| Location | Code | Message |
|---|---|---|
| 15:30 | E203 | whitespace before ':' |
| 44:1 | E302 | expected 2 blank lines, found 1 |
| 74:50 | E261 | at least two spaces before inline comment |
| 77:80 | E501 | line too long (93 > 79 characters) |

## 6. Detailed Issue Table

Ordered by severity: security first, then correctness, then quality and style. "Original line" refers to the unmodified file. "Verified by" names the evidence that the fix works.

| # | Tool | Code | Severity / Type | Original line | Problem | Fix | Verified by |
|---|---|---|---|---|---|---|---|
| 1 | Bandit | B605 | High / Security (CWE-78) | 61 | `os.system("xdg-open " + path)` passes a path to a shell. A path containing `;` or `&` could run arbitrary commands. Also Linux-only. | Check that the path is an existing file, then open it with `webbrowser.open()` using a `file://` URI. No shell is involved. | Bandit: 0 issues. Tests: injection-style paths raise `FileNotFoundError`; `os.system` never called; a filename with `& ;` and spaces is percent-encoded into the URI. |
| 2 | Bandit | B306 | Medium / Security (CWE-377) | 55 | `tempfile.mktemp()` returns only a name. Another process can create that file before the program does (race condition). | Use `tempfile.mkstemp()`, which creates the file atomically. Close the descriptor via `os.fdopen` in a `with` block. | Bandit: 0 issues. Tests: unique files are created, content is written, and the file can be deleted afterwards (proving the handle was closed). |
| 3 | Bandit | B108 | Medium / Security (CWE-377) | 8 | Hardcoded, shared `/tmp/expense_reports` is predictable and does not exist on Windows. | `os.path.join(tempfile.gettempdir(), "expense_reports")`, created on demand with `os.makedirs(..., mode=0o700, exist_ok=True)`. | Bandit: 0 issues. Tests: the default directory lives under `tempfile.gettempdir()`; a missing nested directory is created. |
| 4 | Bandit | B105 | Low / Security (CWE-259) | 5, 50 | Password hardcoded in source and compared with `==`. | Read the expected value from the `BANK_SYNC_PASSWORD` environment variable. Reject every attempt if it is unset or empty, or if the input is not a string. Compare with `hmac.compare_digest`. Never printed. | Bandit: 0 issues. Tests: unset or empty env rejects even the old password; correct, wrong, `None` and bytes inputs behave correctly; the old literal is gone from the source. |
| 5 | Pylint | W0718 | Warning / Correctness | 41 | `except Exception` hides every error, including real bugs such as a missing key. | `max(..., default=None)` handles the empty case without any `try`. | Pylint: 0 messages. Test: an empty tracker returns `None`. |
| 6 | — (manual) | — | Correctness | 75 | `biggestExpense()["note"]` would raise `TypeError` if no expenses existed. | Check the result before indexing: `biggest["note"] if biggest else None`. | Demo output unchanged; empty-list test. |
| 7 | — (manual) | — | Correctness | 80 | `main()` ran on import, so importing the module printed the demo. | `if __name__ == "__main__": main()` | Test: importing prints nothing (0 bytes of output). |
| 8 | — (manual) | — | Correctness / Validation | 12 | Only `amount <= 0` was rejected. `NaN`, `inf` and `True` were accepted, and strings raised `TypeError`. | Accept only finite `int`/`float` (not `bool`) greater than 0. `set_budget` raises `ValueError` for invalid or negative budgets. | Tests: `-50, 0, nan, inf, True, "100", None` are rejected with the same message as before; invalid budgets raise `ValueError` and leave the budget unchanged. |
| 9 | Pylint | W0603, C0103 | Warning, Convention / Design | 7, 29 | Mutable module-level state changed through `global`. Pylint also treats `monthly_budget` as a misnamed constant. | Move `expenses` and the budget into an `ExpenseTracker` class. The default stays in the constant `DEFAULT_MONTHLY_BUDGET`. | Pylint: 0 messages. Test: two trackers do not share state. |
| 10 | Pylint | C0103 | Convention / Naming | 11–59 (11 names) | camelCase function, argument and variable names. | snake_case: `add_expense`, `total_by_category`, `set_budget`, `new_budget`, `remaining_budget`, `biggest_expense`, `print_ledger`, `check_sync_password`, `export_report`, `report_path`, `open_statement`. | Pylint: 0 messages. |
| 11 | Pylint | C0114, C0116 | Convention / Documentation | 1, 11–64 | No module or function docstrings. | Docstrings added for the module, class, every method and every function. | Pylint: 0 messages. |
| 12 | Pylint | C0200 | Convention / Idiom | 45 | `for i in range(len(expenses))`. | `for number, expense in enumerate(self.expenses, start=1)`. | Pylint: 0 messages. Test: ledger output is identical. |
| 13 | Flake8 | E203 | Style | 15 | `{"amount" : amount` | `{"amount": amount` | Flake8: 0 violations. |
| 14 | Flake8 | E302 | Style | 44 | One blank line before a top-level `def`. | Resolved by the class restructuring: the function became a correctly spaced method. | Flake8: 0 violations. |
| 15 | Flake8 | E261 | Style | 74 | One space before an inline comment. | Two spaces. | Flake8: 0 violations. |
| 16 | Flake8 | E501 | Style | 77 | 93-character line. | Wrapped across two lines, as part of the Pylint commit. | Flake8: 0 violations. |

## 7. Security Fixes Explained

### B605 — Shell command injection (High)

**Before:**
```python
os.system("xdg-open " + path)
```

`os.system` hands the whole string to the operating system's shell. If `path` came from a user or a file name, a value like `statement.txt; rm -rf ~` would run a second command. It also only worked on Linux.

**After:**
```python
statement = Path(path).resolve()
if not statement.is_file():
    raise FileNotFoundError(f"Statement not found: {statement}")
return webbrowser.open(statement.as_uri())
```

The path is resolved and must be an existing regular file. It is then converted to a `file://` URI, in which spaces and shell characters are percent-encoded, and passed to the standard-library `webbrowser` module. That module uses the platform's opener without a shell. `subprocess` with an argument list was considered too. Under Bandit's documented rules, it would be expected to trigger B404/B603 (Low); this variant was not implemented or scanned. It would also need separate code for each operating system. The `webbrowser` approach produced no Bandit findings.

### B306 — Insecure temporary file name (Medium)

`tempfile.mktemp()` only invents a name. Between choosing the name and opening it, another process could create a file or symbolic link with that name (a time-of-check/time-of-use race). `tempfile.mkstemp()` creates and opens the file in one atomic operation, with permissions limited to the owner, and returns an open descriptor. The descriptor is wrapped with `os.fdopen(...)` in a `with` block, so it is always closed.

### B108 — Hardcoded temporary directory (Medium)

`/tmp` is a shared, world-writable, predictable location, and it does not exist on Windows. The report directory is now built from `tempfile.gettempdir()`, which returns the correct per-user temp directory on each platform. It is created when needed with `os.makedirs(..., mode=0o700, exist_ok=True)`.

### B105 — Hardcoded password (Low)

A password in source code is visible to anyone with access to the repository and cannot be changed without editing code. The expected value is now read from the `BANK_SYNC_PASSWORD` environment variable. The function fails safely: if the variable is unset or empty, every attempt is rejected, so a misconfiguration cannot let anyone in. `hmac.compare_digest` performs a constant-time comparison, so response time does not reveal how many characters were correct. The password is never printed or logged.

## 8. Pylint and Flake8 Improvements

**Design.** The original code kept the expense list and budget in module-level variables and changed the budget with a `global` statement. Moving this state into a small `ExpenseTracker` class removed W0603 and the misleading "constant" naming warning on `monthly_budget`. The class also lets several independent trackers exist and makes the code easier to test. The class has the same operations as the original functions, so this was not a large rewrite.

**Correctness.** The broad `except Exception` was replaced by `max(..., default=None)`, so unexpected errors are no longer hidden. Three defects that no tool reported were fixed alongside:

- a possible `None` dereference in `main`;
- the demo running on import;
- weak amount validation.

**Readability.** All names follow PEP 8 snake_case. Every module, class, method and function has a docstring, and the ledger loop uses `enumerate`.

**Style.** E203 and E261 were fixed directly in the Flake8 commit. E302 and E501 were fixed as a side effect of the restructuring in the Pylint commit, and the commit messages say so.

## 9. Before-and-After Comparison

| Metric | Before | After |
|---|---|---|
| Pylint score | **5.27/10** | **10.00/10** |
| Pylint messages | 26 (24 convention, 2 warning) | 0 |
| Bandit — High | 1 (B605) | 0 |
| Bandit — Medium | 2 (B306, B108) | 0 |
| Bandit — Low | 1 (B105) | 0 |
| Bandit `#nosec` skips | 0 | 0 |
| Flake8 violations | 4 (E203, E302, E261, E501) | 0 (empty report) |
| Lines of code (Bandit count) | 56 | 115 |
| Demo output | baseline | **identical** |

The line count grew mainly because of docstrings and input validation.

## 10. Testing and Validation

All of the following were run on the final committed source on 28 October 2026.

**Demo program.** `python expense_tracker.py` exits with code 0. Its output matches the baseline in Section 5 line for line (checked with `diff`).

**Import behaviour.** `python -c "import expense_tracker"` produced 0 bytes of output.

**Environment-variable password.** With `BANK_SYNC_PASSWORD=guess` set, the demo printed `Sync password accepted: True`. With it unset, the demo printed `False`.

**Unit tests.** A verification script using `unittest` and `unittest.mock` was run against the module. Result: **`Ran 18 tests ... OK`** (exit code 0). The script was kept outside the repository as a temporary verification aid. The lab does not list tests as a deliverable, so it is not committed.

| Test group | Tests | What is checked |
|---|---|---|
| Import | 1 | Importing the module prints nothing |
| Tracker | 8 | Default budget; valid expenses and default category; invalid amounts (`-50, 0, nan, inf, True, "100", None`) rejected with the original message; category totals and remaining budget (2051); budget validation; empty list (`None`, `{}`, no ledger output); biggest expense and ledger format; independent trackers |
| Password | 4 | Unset and empty variable fail safely; correct, wrong, `None` and bytes inputs; the old password literal is no longer in the source |
| Report export | 3 | Default directory is under `tempfile.gettempdir()`; a missing directory is created; files are unique, `.txt`, and contain the written content; descriptor is closed |
| Open statement | 2 | Existing file is opened via a percent-encoded `file://` URI; missing, injection-style and directory paths raise `FileNotFoundError`, and neither `webbrowser.open` nor `os.system` is called |

**Safety of testing.**

- Report tests wrote only into a temporary directory that was deleted afterwards.
- `webbrowser.open` was mocked, so no window was opened on the test machine.
- The program has no persistent expense data, so nothing could be overwritten.

## 11. Commits

| Hash | Message | Purpose |
|---|---|---|
| `a170679` | Fix Pylint code quality issues | Docstrings, snake_case naming, `ExpenseTracker` class replacing globals, specific handling instead of broad `except`, `enumerate`; plus the `None` guard, `__main__` guard and input validation. |
| `cc9ce66` | Fix Bandit security findings | B105 (environment-variable password with constant-time compare), B108 (portable temp directory), B306 (`mkstemp`), B605 (`webbrowser` instead of `os.system`). |
| `e1d3242` | Fix Flake8 style violations | E203 and E261. E302 and E501 had already been cleared by the restructuring in `a170679`. |

The reports and this document are added in a separate evidence commit after these three.

## 12. Reflection

*The handout's specific reflection questions were not available when this report was written. This section reflects on the experiment itself. A longer experiment-based reflection is in `reflection.md`, which also needs checking against the handout's questions before submission.*

**What static analysis did well.**

- **Bandit found real risks in code that never runs.** The four security issues were all in helpers or constants that the demo does not exercise, so normal testing would never have revealed them.
- **The tools are fast and repeatable.** Rerunning all three after every change gave immediate confirmation that a fix worked and introduced nothing new.
- **Severity and confidence ratings helped prioritise.** The High-severity shell injection was clearly the first thing to fix.
- **Pylint pointed at design, not just cosmetics.** The `global` warning (W0603) led to a better design (the class), not just a reformat.

**Limitations observed.**

- **The tools missed real bugs.** None of them reported the `None` dereference, the demo running on import, or `NaN`/`True` being accepted as amounts. These were found by reading the code and confirmed by tests.
- **Some findings need judgement.** B105 flagged an obvious demo placeholder. Pylint's naming rule for `monthly_budget` assumed every module-level name is a constant, when the real issue was mutable global state. The tools flag patterns; deciding what they mean is still a human job.
- **The score can be gamed.** A perfect 10.00 can be reached with meaningless docstrings, or by disabling checks. The score only meant something here because no checks were disabled and the behaviour was verified separately.
- **Fixes can trigger new warnings.** A `subprocess`-based fix for B605 would be expected, under Bandit's rules, to raise new Low findings (B404/B603). Choosing among fixes means understanding why a rule exists, not just making the warning go away.
- **Tools overlap.** One restructuring change cleared both Pylint and Flake8 findings. This made it harder to give each commit a single tool's fixes.

**Takeaway.** Static analysis is a cheap, reliable first filter that is especially strong for security patterns and consistency. It complements tests and code review rather than replacing them.

## 13. Conclusion

All 34 findings from the three tools were resolved: 26 from Pylint, 4 from Bandit and 4 from Flake8. Three further correctness defects that no tool reported were also fixed. The Pylint score rose from **5.27 to 10.00/10** without disabling any check. Bandit went from four issues (one High) to **none** without any `# nosec` suppression. Flake8 reports **no violations**. The program's demonstration output is unchanged, and 18 tests confirm both normal behaviour and the security fixes.

## 14. Final Deliverables Checklist

| Deliverable | Status |
|---|---|
| `expense_tracker.py` — cleaned source, ≥ 4 issues fixed | ✅ Committed (`a170679`, `cc9ce66`, `e1d3242`) |
| `reports/before/pylint_report_before.txt` | ✅ Original tool output |
| `reports/before/bandit_report_before.txt` | ✅ Original tool output |
| `reports/before/flake8_report_before.txt` | ✅ Original tool output |
| `reports/after/pylint_report_after.txt` | ✅ 10.00/10 |
| `reports/after/bandit_report_after.txt` | ✅ No issues identified |
| `reports/after/flake8_report_after.txt` | ✅ Empty file = no violations |
| Pylint score > 9.5 | ✅ 10.00/10 |
| Three tool-fix commits | ✅ |
| `submission/Lab5_Static_Code_Analysis_Report.md` | ✅ This document |
| `issues.md` (README deliverable) | ✅ 16 issues in the README's table format, high and medium severity first |
| `reflection.md` (README deliverable) | ⚠️ Created as an experiment-based reflection; must be checked against the handout's four questions, which were not available |
