"""
Connection Tester Module - Test database and API connections.

This module handles:
- Database connection testing
- API endpoint availability checks
- Health endpoint verification
- Authentication flow testing
"""

import logging
import requests
from pathlib import Path
from typing import Dict, Any, List
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


class ConnectionTester:
    """Test database and API connections."""
    
    def __init__(self, config: Dict[str, Any], project_root: str):
        """
        Initialize the connection tester.
        
        Args:
            config: Configuration dictionary for connection tester
            project_root: Root directory of the project
        """
        self.config = config
        self.project_root = Path(project_root)
        self.results = {
            "database_tests": [],
            "api_tests": [],
            "health_tests": [],
            "auth_tests": [],
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "errors": []
        }
    
    def run(self) -> Dict[str, Any]:
        """
        Run all connection tests.
        
        Returns:
            Dictionary containing results of connection tests
        """
        logger.info("Starting connection tests...")
        
        if not self.config.get("enabled", True):
            logger.info("Connection tester is disabled in configuration")
            return self.results
        
        # Test database connection
        if self.config.get("test_database", True):
            self._test_database()
        
        # Test API endpoints
        if self.config.get("test_api_endpoints", True):
            self._test_api_endpoints()
        
        # Test health endpoints
        if self.config.get("test_health_endpoints", True):
            self._test_health_endpoints()
        
        # Test authentication
        if self.config.get("test_authentication", True):
            self._test_authentication()
        
        # Calculate totals
        self.results["total_tests"] = (
            len(self.results["database_tests"]) +
            len(self.results["api_tests"]) +
            len(self.results["health_tests"]) +
            len(self.results["auth_tests"])
        )
        
        logger.info(f"Connection tests completed. {self.results['passed_tests']}/{self.results['total_tests']} passed")
        return self.results
    
    def _test_database(self):
        """Test database connection."""
        logger.info("Testing database connection...")
        
        try:
            # Try to find .env file to get DATABASE_URL
            env_file = self.project_root / "backend" / ".env"
            database_url = None
            
            if env_file.exists():
                with open(env_file, 'r') as f:
                    for line in f:
                        if line.startswith("DATABASE_URL="):
                            database_url = line.split("=", 1)[1].strip()
                            break
            
            if not database_url:
                # Try to find SQLite database
                db_files = list(self.project_root.glob("**/*.db"))
                if db_files:
                    database_url = f"sqlite:///{db_files[0]}"
            
            if database_url:
                # Test connection
                engine = create_engine(database_url)
                with engine.connect() as conn:
                    # Try a simple query
                    result = conn.execute(text("SELECT 1"))
                    result.fetchone()
                
                self.results["database_tests"].append({
                    "test": "Database Connection",
                    "status": "PASSED",
                    "database": database_url.split("://")[0],
                    "message": "Successfully connected to database"
                })
                self.results["passed_tests"] += 1
                logger.info("✓ Database connection successful")
                
            else:
                self.results["database_tests"].append({
                    "test": "Database Connection",
                    "status": "SKIPPED",
                    "message": "Could not find DATABASE_URL"
                })
                logger.warning("Database URL not found, skipping test")
                
        except Exception as e:
            self.results["database_tests"].append({
                "test": "Database Connection",
                "status": "FAILED",
                "error": str(e)
            })
            self.results["failed_tests"] += 1
            logger.error(f"✗ Database connection failed: {str(e)}")
    
    def _test_api_endpoints(self):
        """Test configured API endpoints."""
        logger.info("Testing API endpoints...")
        
        base_url = self.config.get("api_base_url", "http://localhost:8000")
        timeout = self.config.get("timeout", 10)
        endpoints = self.config.get("endpoints_to_test", [])
        
        for endpoint_config in endpoints:
            path = endpoint_config.get("path", "/")
            method = endpoint_config.get("method", "GET")
            expected_status = endpoint_config.get("expected_status", 200)
            
            try:
                url = f"{base_url}{path}"
                
                if method == "GET":
                    response = requests.get(url, timeout=timeout)
                elif method == "POST":
                    response = requests.post(url, timeout=timeout)
                else:
                    logger.warning(f"Unsupported method: {method}")
                    continue
                
                if response.status_code == expected_status:
                    self.results["api_tests"].append({
                        "test": f"{method} {path}",
                        "status": "PASSED",
                        "status_code": response.status_code,
                        "message": f"Endpoint returned expected status {expected_status}"
                    })
                    self.results["passed_tests"] += 1
                    logger.info(f"✓ {method} {path} - Status {response.status_code}")
                else:
                    self.results["api_tests"].append({
                        "test": f"{method} {path}",
                        "status": "FAILED",
                        "status_code": response.status_code,
                        "expected_status": expected_status,
                        "message": f"Expected {expected_status}, got {response.status_code}"
                    })
                    self.results["failed_tests"] += 1
                    logger.warning(f"✗ {method} {path} - Expected {expected_status}, got {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                self.results["api_tests"].append({
                    "test": f"{method} {path}",
                    "status": "FAILED",
                    "error": "Connection refused - API server may not be running"
                })
                self.results["failed_tests"] += 1
                logger.error(f"✗ {method} {path} - Connection refused")
            except requests.exceptions.Timeout:
                self.results["api_tests"].append({
                    "test": f"{method} {path}",
                    "status": "FAILED",
                    "error": f"Request timed out after {timeout}s"
                })
                self.results["failed_tests"] += 1
                logger.error(f"✗ {method} {path} - Timeout")
            except Exception as e:
                self.results["api_tests"].append({
                    "test": f"{method} {path}",
                    "status": "FAILED",
                    "error": str(e)
                })
                self.results["failed_tests"] += 1
                logger.error(f"✗ {method} {path} - {str(e)}")
    
    def _test_health_endpoints(self):
        """Test health check endpoints."""
        logger.info("Testing health endpoints...")
        
        base_url = self.config.get("api_base_url", "http://localhost:8000")
        timeout = self.config.get("timeout", 10)
        
        health_endpoints = ["/", "/health"]
        
        for path in health_endpoints:
            try:
                url = f"{base_url}{path}"
                response = requests.get(url, timeout=timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    self.results["health_tests"].append({
                        "test": f"Health Check {path}",
                        "status": "PASSED",
                        "status_code": response.status_code,
                        "response": data
                    })
                    self.results["passed_tests"] += 1
                    logger.info(f"✓ Health check {path} - OK")
                else:
                    self.results["health_tests"].append({
                        "test": f"Health Check {path}",
                        "status": "FAILED",
                        "status_code": response.status_code
                    })
                    self.results["failed_tests"] += 1
                    logger.warning(f"✗ Health check {path} - Status {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                self.results["health_tests"].append({
                    "test": f"Health Check {path}",
                    "status": "FAILED",
                    "error": "API server not running"
                })
                self.results["failed_tests"] += 1
                logger.error(f"✗ Health check {path} - Server not running")
            except Exception as e:
                self.results["health_tests"].append({
                    "test": f"Health Check {path}",
                    "status": "FAILED",
                    "error": str(e)
                })
                self.results["failed_tests"] += 1
                logger.error(f"✗ Health check {path} - {str(e)}")
    
    def _test_authentication(self):
        """Test authentication flow."""
        logger.info("Testing authentication flow...")
        
        base_url = self.config.get("api_base_url", "http://localhost:8000")
        timeout = self.config.get("timeout", 10)
        
        try:
            # Test if auth endpoints exist
            endpoints_to_check = [
                "/auth/signup",
                "/auth/login",
                "/auth/me"
            ]
            
            for endpoint in endpoints_to_check:
                url = f"{base_url}{endpoint}"
                
                # Just check if endpoint exists (we expect 422 for missing body, not 404)
                response = requests.post(url, json={}, timeout=timeout)
                
                if response.status_code in [200, 201, 401, 422]:
                    # Endpoint exists
                    self.results["auth_tests"].append({
                        "test": f"Auth Endpoint {endpoint}",
                        "status": "PASSED",
                        "message": "Endpoint is accessible"
                    })
                    self.results["passed_tests"] += 1
                    logger.info(f"✓ Auth endpoint {endpoint} exists")
                elif response.status_code == 404:
                    self.results["auth_tests"].append({
                        "test": f"Auth Endpoint {endpoint}",
                        "status": "FAILED",
                        "message": "Endpoint not found"
                    })
                    self.results["failed_tests"] += 1
                    logger.warning(f"✗ Auth endpoint {endpoint} not found")
                    
        except requests.exceptions.ConnectionError:
            self.results["auth_tests"].append({
                "test": "Authentication Endpoints",
                "status": "FAILED",
                "error": "API server not running"
            })
            self.results["failed_tests"] += 1
            logger.error("✗ Authentication test - Server not running")
        except Exception as e:
            self.results["auth_tests"].append({
                "test": "Authentication Endpoints",
                "status": "FAILED",
                "error": str(e)
            })
            self.results["failed_tests"] += 1
            logger.error(f"✗ Authentication test - {str(e)}")
    
    def get_summary(self) -> str:
        """Get a summary of connection test results."""
        summary = f"""
Connection Test Summary:
- Total tests: {self.results['total_tests']}
- Passed: {self.results['passed_tests']}
- Failed: {self.results['failed_tests']}

Test Breakdown:
- Database tests: {len(self.results['database_tests'])}
- API endpoint tests: {len(self.results['api_tests'])}
- Health check tests: {len(self.results['health_tests'])}
- Authentication tests: {len(self.results['auth_tests'])}
"""
        return summary
