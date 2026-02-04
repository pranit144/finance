---
description: Weekly comprehensive code quality audit
---

# Weekly Code Quality Audit Workflow

Run this workflow weekly to maintain code quality and track improvements over time.

## Steps

### 1. Update Dependencies

Check for outdated packages:
```bash
pip list --outdated
```

### 2. Run Full Quality Check

Execute all quality modules:
```bash
python code_quality_agent.py --all
```

### 3. Start Backend Server

For connection tests:
```bash
cd backend
uvicorn app.main:app --reload
```

### 4. Run Connection Tests

In a new terminal:
```bash
python code_quality_agent.py --module connections
```

### 5. Review Security Issues

Open the HTML report and focus on security section:
```bash
start quality_reports\latest_report.html
```

**Review**:
- Any new CRITICAL or HIGH severity issues?
- Are there vulnerable dependencies?
- Is CORS configuration appropriate?
- Is DEBUG mode disabled for production?

### 6. Check Code Coverage

Review test coverage percentage:
- **Target**: >70% coverage
- **Good**: >80% coverage
- **Excellent**: >90% coverage

If coverage is low, identify untested modules and add tests.

### 7. Review Code Quality Scores

Check Pylint score:
- **Target**: >7.0/10
- **Good**: >8.0/10
- **Excellent**: >9.0/10

### 8. Compare with Previous Week

Check historical reports:
```bash
explorer quality_reports\history
```

**Track trends**:
- Is coverage improving?
- Are security issues decreasing?
- Is code quality score stable or improving?

### 9. Create Action Items

Based on the report, create tasks for:
- Fixing CRITICAL/HIGH security issues
- Improving test coverage
- Addressing code quality issues
- Updating vulnerable dependencies

### 10. Document Findings

Create a summary of:
- Issues found and fixed
- Coverage improvements
- Quality score changes
- Action items for next week

## Quick Weekly Check

For a faster audit:
```bash
python code_quality_agent.py --all
start quality_reports\latest_report.html
```

Then review the summary dashboard for key metrics.
