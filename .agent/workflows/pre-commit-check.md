---
description: Pre-commit quality checks before pushing code
---

# Pre-Commit Quality Check Workflow

Run this workflow before committing code to ensure quality and catch issues early.

// turbo-all

## Steps

### 1. Format Code

Clean and format all Python files:
```bash
python code_quality_agent.py --module clean
```

### 2. Security Scan

Check for security vulnerabilities:
```bash
python code_quality_agent.py --module security
```

### 3. Run Tests

Execute tests with coverage:
```bash
python code_quality_agent.py --module test
```

### 4. Review Report

Open the quality report:
```bash
start quality_reports\latest_report.html
```

### 5. Check for Critical Issues

Review the console output for any CRITICAL or HIGH severity issues.

**If any CRITICAL issues found**: Fix them before committing!

**If any HIGH issues found**: Consider fixing before committing.

**If tests fail**: Fix failing tests before committing.

### 6. Stage and Commit

Once all checks pass:
```bash
git add .
git commit -m "Your commit message"
```

## Quick Pre-Commit

For a fast check, run:
```bash
python code_quality_agent.py --module clean
python code_quality_agent.py --module security
```

## Full Pre-Commit

For comprehensive check:
```bash
python code_quality_agent.py --all
```
