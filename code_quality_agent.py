"""
Code Quality Agent - Main orchestration script.

This is the main entry point for the automated code quality agent.
It coordinates all modules and generates comprehensive quality reports.

Usage:
    python code_quality_agent.py [options]
    
Options:
    --dry-run           Preview changes without applying them
    --module <name>     Run specific module only (clean, security, connections, test)
    --all               Run all modules (default)
    --config <path>     Path to custom config file
    --help              Show this help message
"""

import sys
import argparse
import logging
import yaml
from pathlib import Path
from typing import Dict, Any

from modules import (
    CodeCleaner,
    VulnerabilityChecker,
    ConnectionTester,
    CodeTester,
    ReportGenerator
)


class CodeQualityAgent:
    """Main code quality agent orchestrator."""
    
    def __init__(self, config_path: str = "agent_config.yaml"):
        """
        Initialize the code quality agent.
        
        Args:
            config_path: Path to configuration file
        """
        self.project_root = Path(__file__).parent
        self.config = self._load_config(config_path)
        self._setup_logging()
        
        self.results = {}
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_file = self.project_root / config_path
        
        if not config_file.exists():
            print(f"Warning: Config file {config_path} not found. Using defaults.")
            return self._get_default_config()
        
        try:
            with open(config_file, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            print(f"Error loading config: {e}. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
            "general": {
                "project_name": "Project",
                "project_root": ".",
                "output_dir": "quality_reports",
                "log_level": "INFO"
            },
            "modules": {
                "code_cleaner": True,
                "vulnerability_checker": True,
                "connection_tester": True,
                "code_tester": True
            },
            "code_cleaner": {"enabled": True},
            "vulnerability_checker": {"enabled": True},
            "connection_tester": {"enabled": True},
            "code_tester": {"enabled": True},
            "reporting": {
                "generate_html": True,
                "generate_json": True,
                "generate_console_summary": True
            }
        }
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_level = self.config.get("general", {}).get("log_level", "INFO")
        output_dir = self.project_root / self.config.get("general", {}).get("output_dir", "quality_reports")
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler(output_dir / "agent.log")
            ]
        )
        
        self.logger = logging.getLogger(__name__)
    
    def run_all(self, dry_run: bool = False):
        """
        Run all enabled modules.
        
        Args:
            dry_run: If True, preview changes without applying them
        """
        self.logger.info("="*70)
        self.logger.info("CODE QUALITY AGENT STARTED")
        self.logger.info("="*70)
        
        project_name = self.config.get("general", {}).get("project_name", "Project")
        self.logger.info(f"Project: {project_name}")
        self.logger.info(f"Dry run: {dry_run}")
        
        # Run Code Cleaner
        if self.config.get("modules", {}).get("code_cleaner", True):
            self.logger.info("\n" + "-"*70)
            self.logger.info("MODULE: Code Cleaner")
            self.logger.info("-"*70)
            cleaner = CodeCleaner(
                self.config.get("code_cleaner", {}),
                str(self.project_root)
            )
            self.results["code_cleaner"] = cleaner.run(dry_run=dry_run)
            self.logger.info(cleaner.get_summary())
        
        # Run Vulnerability Checker
        if self.config.get("modules", {}).get("vulnerability_checker", True):
            self.logger.info("\n" + "-"*70)
            self.logger.info("MODULE: Vulnerability Checker")
            self.logger.info("-"*70)
            vuln_checker = VulnerabilityChecker(
                self.config.get("vulnerability_checker", {}),
                str(self.project_root)
            )
            self.results["vulnerability_checker"] = vuln_checker.run()
            self.logger.info(vuln_checker.get_summary())
        
        # Run Connection Tester
        if self.config.get("modules", {}).get("connection_tester", True):
            self.logger.info("\n" + "-"*70)
            self.logger.info("MODULE: Connection Tester")
            self.logger.info("-"*70)
            conn_tester = ConnectionTester(
                self.config.get("connection_tester", {}),
                str(self.project_root)
            )
            self.results["connection_tester"] = conn_tester.run()
            self.logger.info(conn_tester.get_summary())
        
        # Run Code Tester
        if self.config.get("modules", {}).get("code_tester", True):
            self.logger.info("\n" + "-"*70)
            self.logger.info("MODULE: Code Tester")
            self.logger.info("-"*70)
            code_tester = CodeTester(
                self.config.get("code_tester", {}),
                str(self.project_root)
            )
            self.results["code_tester"] = code_tester.run()
            self.logger.info(code_tester.get_summary())
        
        # Generate Reports
        self.logger.info("\n" + "-"*70)
        self.logger.info("Generating Reports")
        self.logger.info("-"*70)
        report_gen = ReportGenerator(
            self.config.get("reporting", {}),
            str(self.project_root)
        )
        report_gen.generate_reports(self.results)
        
        self.logger.info("\n" + "="*70)
        self.logger.info("CODE QUALITY AGENT COMPLETED")
        self.logger.info("="*70)
    
    def run_module(self, module_name: str, dry_run: bool = False):
        """
        Run a specific module.
        
        Args:
            module_name: Name of module to run (clean, security, connections, test)
            dry_run: If True, preview changes without applying them
        """
        self.logger.info(f"Running module: {module_name}")
        
        if module_name == "clean":
            cleaner = CodeCleaner(
                self.config.get("code_cleaner", {}),
                str(self.project_root)
            )
            self.results["code_cleaner"] = cleaner.run(dry_run=dry_run)
            self.logger.info(cleaner.get_summary())
            
        elif module_name == "security":
            vuln_checker = VulnerabilityChecker(
                self.config.get("vulnerability_checker", {}),
                str(self.project_root)
            )
            self.results["vulnerability_checker"] = vuln_checker.run()
            self.logger.info(vuln_checker.get_summary())
            
        elif module_name == "connections":
            conn_tester = ConnectionTester(
                self.config.get("connection_tester", {}),
                str(self.project_root)
            )
            self.results["connection_tester"] = conn_tester.run()
            self.logger.info(conn_tester.get_summary())
            
        elif module_name == "test":
            code_tester = CodeTester(
                self.config.get("code_tester", {}),
                str(self.project_root)
            )
            self.results["code_tester"] = code_tester.run()
            self.logger.info(code_tester.get_summary())
            
        else:
            self.logger.error(f"Unknown module: {module_name}")
            return
        
        # Generate report for single module
        report_gen = ReportGenerator(
            self.config.get("reporting", {}),
            str(self.project_root)
        )
        report_gen.generate_reports(self.results)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Automated Code Quality Agent",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python code_quality_agent.py --all
  python code_quality_agent.py --dry-run
  python code_quality_agent.py --module clean
  python code_quality_agent.py --module security
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview changes without applying them"
    )
    
    parser.add_argument(
        "--module",
        choices=["clean", "security", "connections", "test"],
        help="Run specific module only"
    )
    
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all modules (default)"
    )
    
    parser.add_argument(
        "--config",
        default="agent_config.yaml",
        help="Path to custom config file"
    )
    
    args = parser.parse_args()
    
    # Create agent
    agent = CodeQualityAgent(config_path=args.config)
    
    # Run agent
    if args.module:
        agent.run_module(args.module, dry_run=args.dry_run)
    else:
        agent.run_all(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
