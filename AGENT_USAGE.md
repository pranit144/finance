# Code Quality Agent - Usage Guide

## Overview

The Code Quality Agent is an automated tool that performs comprehensive code quality checks including:
- **Code Cleaning**: Format code with Black, sort imports, remove unused code
- **Security Scanning**: Check for vulnerabilities with Bandit and Safety
- **Connection Testing**: Verify database and API connections
- **Code Testing**: Run tests with coverage reporting

## Installation

1. **Install Development Dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Verify Installation**:
   ```bash
   python code_quality_agent.py --help
   ```

## Quick Start

### Run All Checks
```bash
python code_quality_agent.py --all
```

### Preview Changes (Dry Run)
```bash
python code_quality_agent.py --dry-run
```

### Run Specific Module
```bash
# Code cleaning only
python code_quality_agent.py --module clean

# Security checks only
python code_quality_agent.py --module security

# Connection tests only
python code_quality_agent.py --module connections

# Code tests only
python code_quality_agent.py --module test
```

## Configuration

Edit `agent_config.yaml` to customize behavior:

```yaml
# Enable/disable modules
modules:
  code_cleaner: true
  vulnerability_checker: true
  connection_tester: true
  code_tester: true

# Customize thresholds
code_tester:
  coverage_threshold: 70  # minimum percentage
  pylint_threshold: 7.0   # minimum score

# Exclude directories
code_cleaner:
  exclude_dirs:
    - "venv"
    - "__pycache__"
```

## Understanding Reports

### HTML Report
- Open `quality_reports/latest_report.html` in your browser
- Interactive dashboard with charts and metrics
- Color-coded severity levels

### JSON Report
- Located at `quality_reports/latest_report.json`
- Machine-readable format for CI/CD integration
- Contains all raw data

### Console Summary
- Quick overview printed to terminal
- Shows key metrics and pass/fail status

## Common Workflows

### Before Committing Code
```bash
# Check everything
python code_quality_agent.py --all

# Review the HTML report
# Fix any issues found
# Commit your changes
```

### CI/CD Integration
```bash
# In your CI pipeline
python code_quality_agent.py --all

# Check exit code
if [ $? -ne 0 ]; then
    echo "Quality checks failed"
    exit 1
fi
```

### Code Review Preparation
```bash
# Clean code first
python code_quality_agent.py --module clean

# Then run all checks
python code_quality_agent.py --all
```

## Interpreting Results

### Code Cleaning
- **Files Processed**: Total Python files scanned
- **Formatted**: Files modified by Black
- **Errors**: Issues encountered during cleaning

### Security
- **CRITICAL**: Immediate attention required (e.g., hardcoded secrets)
- **HIGH**: Serious issues (e.g., SQL injection risks)
- **MEDIUM**: Important to fix (e.g., DEBUG mode enabled)
- **LOW**: Minor issues or best practices

### Connections
- **PASSED**: Connection successful
- **FAILED**: Connection failed (check if server is running)
- **SKIPPED**: Test was not applicable

### Code Tests
- **Coverage**: Percentage of code covered by tests (aim for >70%)
- **Pylint Score**: Code quality score out of 10 (aim for >7.0)
- **Flake8**: Style issues found

## Troubleshooting

### "Module not found" errors
```bash
# Reinstall dependencies
pip install -r requirements-dev.txt
```

### Connection tests failing
```bash
# Make sure your backend is running
cd backend
uvicorn app.main:app --reload
```

### No Python files found
- Check `exclude_dirs` in config
- Verify you're running from project root

## Advanced Usage

### Custom Config File
```bash
python code_quality_agent.py --config my_config.yaml
```

### Dry Run with Specific Module
```bash
python code_quality_agent.py --module clean --dry-run
```

### View Historical Reports
```bash
# Reports are saved in quality_reports/history/
ls quality_reports/history/
```

## Tips

1. **Run dry-run first** to preview changes before applying
2. **Fix CRITICAL issues immediately** - they're security risks
3. **Aim for >70% coverage** for good test coverage
4. **Run before every commit** to maintain code quality
5. **Review HTML report** for detailed insights

## Support

For issues or questions:
1. Check the logs in `quality_reports/agent.log`
2. Review the configuration in `agent_config.yaml`
3. Ensure all dependencies are installed
