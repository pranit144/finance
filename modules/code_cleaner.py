"""
Code Cleaner Module - Automated code formatting and cleaning.

This module handles:
- Code formatting with Black
- Import sorting with isort
- Removing unused imports with autoflake
- Fixing trailing whitespace and line endings
"""

import os
import subprocess
import logging
from pathlib import Path
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class CodeCleaner:
    """Automated code cleaning and formatting."""
    
    def __init__(self, config: Dict[str, Any], project_root: str):
        """
        Initialize the code cleaner.
        
        Args:
            config: Configuration dictionary for code cleaner
            project_root: Root directory of the project
        """
        self.config = config
        self.project_root = Path(project_root)
        self.results = {
            "formatted_files": [],
            "sorted_imports": [],
            "removed_unused": [],
            "errors": [],
            "total_files_processed": 0
        }
    
    def run(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        Run all code cleaning operations.
        
        Args:
            dry_run: If True, preview changes without applying them
            
        Returns:
            Dictionary containing results of cleaning operations
        """
        logger.info("Starting code cleaning...")
        
        if not self.config.get("enabled", True):
            logger.info("Code cleaner is disabled in configuration")
            return self.results
        
        # Find all Python files
        python_files = self._find_python_files()
        self.results["total_files_processed"] = len(python_files)
        
        logger.info(f"Found {len(python_files)} Python files to process")
        
        # Run Black formatter
        if self.config.get("format_with_black", True):
            self._run_black(python_files, dry_run)
        
        # Sort imports with isort
        if self.config.get("sort_imports", True):
            self._run_isort(python_files, dry_run)
        
        # Remove unused imports
        if self.config.get("remove_unused_imports", True):
            self._run_autoflake(python_files, dry_run)
        
        logger.info("Code cleaning completed")
        return self.results
    
    def _find_python_files(self) -> List[Path]:
        """Find all Python files in the project."""
        python_files = []
        exclude_dirs = set(self.config.get("exclude_dirs", []))
        exclude_files = self.config.get("exclude_files", [])
        
        for root, dirs, files in os.walk(self.project_root):
            # Remove excluded directories from search
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    # Check if file matches exclude patterns
                    if not any(file.endswith(pattern.replace('*', '')) for pattern in exclude_files):
                        python_files.append(Path(root) / file)
        
        return python_files
    
    def _run_black(self, files: List[Path], dry_run: bool):
        """Run Black formatter on Python files."""
        logger.info("Running Black formatter...")
        
        try:
            line_length = self.config.get("line_length", 100)
            cmd = ["black"]
            
            if dry_run:
                cmd.append("--check")
            
            cmd.extend([
                "--line-length", str(line_length),
                *[str(f) for f in files]
            ])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                if not dry_run:
                    self.results["formatted_files"] = [str(f) for f in files]
                    logger.info(f"Successfully formatted {len(files)} files with Black")
                else:
                    logger.info("Black check passed - all files are properly formatted")
            else:
                if dry_run:
                    logger.warning("Some files would be reformatted by Black")
                    logger.debug(result.stdout)
                else:
                    logger.error(f"Black formatting failed: {result.stderr}")
                    self.results["errors"].append(f"Black error: {result.stderr}")
                    
        except FileNotFoundError:
            error_msg = "Black is not installed. Install with: pip install black"
            logger.error(error_msg)
            self.results["errors"].append(error_msg)
        except Exception as e:
            logger.error(f"Error running Black: {str(e)}")
            self.results["errors"].append(f"Black error: {str(e)}")
    
    def _run_isort(self, files: List[Path], dry_run: bool):
        """Run isort to sort imports."""
        logger.info("Running isort for import sorting...")
        
        try:
            cmd = ["isort"]
            
            if dry_run:
                cmd.append("--check-only")
            
            cmd.extend([
                "--profile", "black",  # Compatible with Black
                *[str(f) for f in files]
            ])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                if not dry_run:
                    self.results["sorted_imports"] = [str(f) for f in files]
                    logger.info(f"Successfully sorted imports in {len(files)} files")
                else:
                    logger.info("isort check passed - all imports are properly sorted")
            else:
                if dry_run:
                    logger.warning("Some imports would be reordered by isort")
                    logger.debug(result.stdout)
                    
        except FileNotFoundError:
            error_msg = "isort is not installed. Install with: pip install isort"
            logger.error(error_msg)
            self.results["errors"].append(error_msg)
        except Exception as e:
            logger.error(f"Error running isort: {str(e)}")
            self.results["errors"].append(f"isort error: {str(e)}")
    
    def _run_autoflake(self, files: List[Path], dry_run: bool):
        """Run autoflake to remove unused imports."""
        logger.info("Running autoflake to remove unused imports...")
        
        try:
            cmd = ["autoflake"]
            
            if not dry_run:
                cmd.append("--in-place")
            
            cmd.extend([
                "--remove-all-unused-imports",
                "--remove-unused-variables",
                *[str(f) for f in files]
            ])
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                if not dry_run:
                    self.results["removed_unused"] = [str(f) for f in files]
                    logger.info(f"Successfully cleaned {len(files)} files with autoflake")
                else:
                    logger.info("autoflake check completed")
                    if result.stdout:
                        logger.debug(f"Would remove unused imports:\n{result.stdout}")
                        
        except FileNotFoundError:
            error_msg = "autoflake is not installed. Install with: pip install autoflake"
            logger.error(error_msg)
            self.results["errors"].append(error_msg)
        except Exception as e:
            logger.error(f"Error running autoflake: {str(e)}")
            self.results["errors"].append(f"autoflake error: {str(e)}")
    
    def get_summary(self) -> str:
        """Get a summary of cleaning results."""
        summary = f"""
Code Cleaning Summary:
- Total files processed: {self.results['total_files_processed']}
- Files formatted: {len(self.results['formatted_files'])}
- Files with sorted imports: {len(self.results['sorted_imports'])}
- Files with removed unused code: {len(self.results['removed_unused'])}
- Errors encountered: {len(self.results['errors'])}
"""
        return summary
