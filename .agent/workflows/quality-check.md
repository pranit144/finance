---
description: Run code quality checks with the automated agent
---

# Code Quality Check Workflow

This workflow runs the automated code quality agent to check your code for issues, vulnerabilities, and test coverage.

## Prerequisites

Ensure dependencies are installed:
```bash
pip install -r requirements-dev.txt
```

## Steps

### 1. Quick Security Scan

Run a fast security check to find vulnerabilities:
```bash
python code_quality_agent.py --module security
```

This checks for:
- Security vulnerabilities with Bandit
- Vulnerable dependencies with Safety
- CORS configuration issues
- DEBUG mode in production
- Weak secret keys

### 2. Format and Clean Code

// turbo
Clean and format all Python files:
```bash
python code_quality_agent.py --module clean
```

This will:
- Format code with Black (PEP 8)
- Sort imports with isort
- Remove unused imports and variables

### 3. Test Database and API Connections

// turbo
Verify all connections are working:
```bash
python code_quality_agent.py --module connections
```

**Note**: Make sure your backend is running first:
```bash
cd backend
uvicorn app.main:app --reload
```

### 4. Run All Tests with Coverage

// turbo
Execute all tests and generate coverage reports:
```bash
python code_quality_agent.py --module test
```

### 5. Full Quality Check (All Modules)

Run everything at once:
```bash
python code_quality_agent.py --all
```

### 6. View Reports

// turbo
Open the HTML report in your browser:
```bash
start quality_reports\latest_report.html
```

## Quick Commands

**Dry Run (Preview Only)**:
```bash
python code_quality_agent.py --dry-run
```

**Before Committing**:
```bash
python code_quality_agent.py --module clean
python code_quality_agent.py --module security
```

**CI/CD Integration**:
```bash
python code_quality_agent.py --all
```

## Understanding Results

- **Green/PASSED**: Everything is good ✅
- **Yellow/WARNING**: Minor issues to review ⚠️
- **Red/FAILED**: Critical issues to fix ❌

### Security Severity Levels

- **CRITICAL**: Fix immediately (e.g., hardcoded secrets)
- **HIGH**: Fix soon (e.g., SQL injection risks)
- **MEDIUM**: Should fix (e.g., DEBUG mode enabled)
- **LOW**: Nice to fix (e.g., minor best practices)

## Customization

Edit `agent_config.yaml` to customize:
- Enable/disable specific modules
- Set coverage thresholds
- Configure excluded directories
- Adjust severity levels

## Troubleshooting

**"Module not found" errors**:
```bash
pip install -r requirements-dev.txt
```

**Connection tests failing**:
- Ensure backend server is running on port 8000
- Check if database file exists

**No files found**:
- Verify you're in the project root directory
- Check `exclude_dirs` in `agent_config.yaml`
