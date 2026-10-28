# Lab 5 — Reflection

**Student:** Rachit S Mane · **SRN:** PES1UG24AM214

> **Note:** The README asks for answers to "the four reflection questions from the handout". The handout was not available in the repository or workspace when this file was written, so its exact questions could not be answered here. Below is a **reflection based on the experiment**, organised by theme. It is **not** a set of answers to the handout's questions. Before submitting, check the handout's four questions against this file and rewrite it to answer them directly if needed.

## 1. Which problems were easiest to fix, and which were hardest

**Easiest.** The Flake8 style findings (E203, E261) and Pylint's docstring and naming conventions were mechanical. Each one tells you exactly what to change and has no effect on behaviour.

**Hardest.** Two kinds took real decisions:

- **The security findings.** For the shell injection (B605), simply wrapping the command in `subprocess` would have been a weaker fix. I had to choose a replacement that avoids a shell entirely, works on every operating system, and validates the path first. I chose the standard-library `webbrowser` module with a `file://` URI.
- **The `global` warning (W0603).** The quick option would have been to rename variables. Moving the state into an `ExpenseTracker` class removed the warning properly and made the code testable. The hard part was doing this without changing the program's output.

## 2. What the tools caught that I might have missed

- **Bandit flagged risks in code the demo never runs.** All four security issues were in helpers or constants that normal runs never exercise, including the High-severity shell injection. Running the program, and even reading it casually, would not have revealed them.
- **The temporary-file race (B306) is easy to overlook.** `tempfile.mktemp()` looks harmless, and nothing in its name suggests a race condition. Bandit's CWE reference explained why it is unsafe.

## 3. What the tools missed or got wrong

- **Real bugs went unreported.** None of the three tools reported that `main()` could index into `None`, that importing the module ran the demo, or that `NaN`, infinity and `True` were accepted as expense amounts. I found these by reading the code and confirmed them with tests.
- **Some findings needed judgement:**
  - **B105** flagged a value that was clearly a lab placeholder. It was still worth fixing, because the same pattern leaks real credentials.
  - **The C0103 naming warning on `monthly_budget`** assumed every module-level name is a constant. The real issue was mutable global state, which renaming alone would not have fixed.
- **Overlapping tools made commits less tidy.** One restructuring change cleared both Pylint findings and two Flake8 findings (E302, E501), so each commit could not cover exactly one tool's findings.

## 4. Static analysis in a real workflow

- **Fast and repeatable feedback.** Rerunning all three tools after every change confirmed each fix and caught regressions immediately. This would work well as a pre-commit hook or a CI step.
- **A score is not quality.** A 10.00/10 Pylint score can be reached with empty docstrings or disabled checks. It meant something here only because no checks were disabled, no `# nosec` was used, and the behaviour was verified separately: the demo output matched the baseline and 18 tests passed.
- **It complements testing and review.** Static analysis is a cheap first filter, especially strong for security patterns and consistency. It does not replace tests, which found behaviour bugs, or human review, which decided which findings mattered.
