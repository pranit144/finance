"""
Code Tester Module - Run tests and generate coverage reports.

This module handles:
- Running pytest tests
- Generating code coverage reports
- Running linting checks (pylint, flake8)
- Collecting test results
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class CodeTester:
    """Run tests and generate coverage reports."""
    
    def __init__(self, config: Dict[str, Any], project_root: str):
        """
        Initialize the code tester.
        
        Args:
            config: Configuration dictionary for code tester
            project_root: Root directory of the project
        """
        self.config = config
        self.project_root = Path(project_root)
        self.results = {
            "pytest_results": {},
            "coverage_results": {},
            "pylint_results": {},
            "flake8_results": {},
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "coverage_percentage": 0.0,
            "errors": []
        }
    
    def run(self) -> Dict[str, Any]:
        """
        Run all code tests.
        
        Returns:
            Dictionary containing results of code tests
        """
        logger.info("Starting code tests...")
        
        if not self.config.get("enabled", True):
            logger.info("Code tester is disabled in configuration")
            return self.results
        
        # Run pytest
        if self.config.get("run_pytest", True):
            self._run_pytest()
        
        # Run pylint
        if self.config.get("run_pylint", True):
            self._run_pylint()
        
        # Run flake8
        if self.config.get("run_flake8", True):
            self._run_flake8()
        
        logger.info(f"Code tests completed. {self.results['passed_tests']}/{self.results['total_tests']} tests passed")
        return self.results
    
    def _run_pytest(self):
        """Run pytest with coverage."""
        logger.info("Running pytest...")
        
        try:
            test_dirs = self.config.get("test_directories", ["backend"])
            pytest_args = self.config.get("pytest_args", ["-v"])
            generate_coverage = self.config.get("generate_coverage", True)
            
            # Build pytest command
            cmd = ["pytest"]
            cmd.extend(pytest_args)
            
            if generate_coverage:
                cmd.extend([
                    "--cov=.",
                    "--cov-report=html:quality_reports/coverage",
                    "--cov-report=term"
                ])
            
            # Add test directories
            for test_dir in test_dirs:
                test_path = self.project_root / test_dir
                if test_path.exists():
                    cmd.append(str(test_path))
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            # Parse pytest output
            output_lines = result.stdout.split('\n')
            
            # Look for test results
            for line in output_lines:
                if " passed" in line or " failed" in line:
                    # Extract test counts
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "passed":
                            try:
                                self.results["passed_tests"] = int(parts[i-1])
                            except (ValueError, IndexError):
                                pass
                        elif part == "failed":
                            try:
                                self.results["failed_tests"] = int(parts[i-1])
                            except (ValueError, IndexError):
                                pass
                
                # Look for coverage percentage
                if "TOTAL" in line and "%" in line:
                    parts = line.split()
                    for part in parts:
                        if "%" in part:
                            try:
                                self.results["coverage_percentage"] = float(part.replace("%", ""))
                            except ValueError:
                                pass
            
            self.results["total_tests"] = self.results["passed_tests"] + self.results["failed_tests"]
            
            self.results["pytest_results"] = {
                "status": "PASSED" if result.returncode == 0 else "FAILED",
                "return_code": result.returncode,
                "output": result.stdout,
                "total_tests": self.results["total_tests"],
                "passed": self.results["passed_tests"],
                "failed": self.results["failed_tests"]
            }
            
            if result.returncode == 0:
                logger.info(f"✓ Pytest passed - {self.results['passed_tests']} tests")
            else:
                logger.warning(f"✗ Pytest failed - {self.results['failed_tests']} failures")
            
            if generate_coverage:
                logger.info(f"Code coverage: {self.results['coverage_percentage']}%")
                
        except FileNotFoundError:
            error_msg = "pytest is not installed. Install with: pip install pytest pytest-cov"
            logger.error(error_msg)
            self.results["errors"].append(error_msg)
        except Exception as e:
            logger.error(f"Error running pytest: {str(e)}")
            self.results["errors"].append(f"pytest error: {str(e)}")
    
    def _run_pylint(self):
        """Run pylint for code quality checks."""
        logger.info("Running pylint...")
        
        try:
            # Find Python files
            python_files = []
            for test_dir in self.config.get("test_directories", ["backend"]):
                test_path = self.project_root / test_dir
                if test_path.exists():
                    python_files.extend(test_path.glob("**/*.py"))
            
            if not python_files:
                logger.warning("No Python files found for pylint")
                return
            
            cmd = [
                "pylint",
                *[str(f) for f in python_files[:20]]  # Limit to first 20 files
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            # Parse pylint output for score
            output_lines = result.stdout.split('\n')
            score = 0.0
            
            for line in output_lines:
                if "Your code has been rated at" in line:
                    try:
                        score_str = line.split("rated at ")[1].split("/")[0]
                        score = float(score_str)
                    except (IndexError, ValueError):
                        pass
            
            threshold = self.config.get("pylint_threshold", 7.0)
            
            self.results["pylint_results"] = {
                "status": "PASSED" if score >= threshold else "FAILED",
                "score": score,
                "threshold": threshold,
                "output": result.stdout[:1000]  # Limit output
            }
            
            if score >= threshold:
                logger.info(f"✓ Pylint passed - Score: {score}/10")
            else:
                logger.warning(f"✗ Pylint failed - Score: {score}/10 (threshold: {threshold})")
                
        except FileNotFoundError:
            error_msg = "pylint is not installed. Install with: pip install pylint"
            logger.error(error_msg)
            self.results["errors"].append(error_msg)
        except Exception as e:
            logger.error(f"Error running pylint: {str(e)}")
            self.results["errors"].append(f"pylint error: {str(e)}")
    
    def _run_flake8(self):
        """Run flake8 for style checks."""
        logger.info("Running flake8...")
        
        try:
            test_dirs = self.config.get("test_directories", ["backend"])
            
            cmd = ["flake8"]
            
            for test_dir in test_dirs:
                test_path = self.project_root / test_dir
                if test_path.exists():
                    cmd.append(str(test_path))
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            # Count issues
            issues = result.stdout.split('\n')
            issue_count = len([line for line in issues if line.strip()])
            
            self.results["flake8_results"] = {
                "status": "PASSED" if result.returncode == 0 else "FAILED",
                "issue_count": issue_count,
                "output": result.stdout[:1000]  # Limit output
            }
            
            if result.returncode == 0:
                logger.info("✓ Flake8 passed - No style issues")
            else:
                logger.warning(f"✗ Flake8 found {issue_count} style issues")
                
        except FileNotFoundError:
            error_msg = "flake8 is not installed. Install with: pip install flake8"
            logger.error(error_msg)
            self.results["errors"].append(error_msg)
        except Exception as e:
            logger.error(f"Error running flake8: {str(e)}")
            self.results["errors"].append(f"flake8 error: {str(e)}")
    
    def get_summary(self) -> str:
        """Get a summary of code test results."""
        summary = f"""
Code Test Summary:
- Total tests: {self.results['total_tests']}
- Passed: {self.results['passed_tests']}
- Failed: {self.results['failed_tests']}
- Code coverage: {self.results['coverage_percentage']}%

Quality Checks:
- Pylint score: {self.results.get('pylint_results', {}).get('score', 'N/A')}/10
- Flake8 issues: {self.results.get('flake8_results', {}).get('issue_count', 'N/A')}
"""
        return summary
