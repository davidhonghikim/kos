"""
kOS Agent Tracking System - Live Monitoring and Validation
=========================================================

Real-time tracking system that monitors agent work, validates against immutable rules,
and provides automated enforcement similar to Git Actions.

Author: kOS Kitchen System
Version: 1.0.0
Created: 2025-07-08T23:45:00Z
"""

import os
import sys
import json
import sqlite3
import logging
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from datetime import datetime, timedelta
import threading
import time
import ast
import re

class AgentTrackingSystem:
    """
    Live tracking system for monitoring agent work and enforcing quality standards.
    
    Features:
    - Real-time file monitoring and validation
    - Database-driven tracking of all agent activities
    - Automated rule enforcement (file size, code quality, etc.)
    - Git Actions-style validation checks
    - Performance metrics and compliance reporting
    """
    
    def __init__(self, db_path: Optional[str] = None, config_path: Optional[str] = None):
        """
        Initialize the agent tracking system.
        
        Args:
            db_path: Path to SQLite database for tracking
            config_path: Path to tracking configuration
        """
        self.logger = self._setup_logging()
        self.logger.info("Initializing kOS Agent Tracking System")
        
        # Setup database
        self.db_path = db_path or "kitchen/data/agent_tracking.db"
        self._init_database()
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Initialize monitoring
        self.monitoring_active = False
        self.monitor_thread = None
        self.file_watchers = {}
        
        # Tracking state
        self.current_agent = None
        self.session_start = None
        self.violations = []
        self.validations = []
        
        self.logger.info("Agent Tracking System initialized successfully")
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the tracking system."""
        logger = logging.getLogger('agent_tracking')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler
            log_dir = Path("kitchen/logs")
            log_dir.mkdir(exist_ok=True)
            file_handler = logging.FileHandler(log_dir / "agent_tracking.log")
            file_handler.setLevel(logging.DEBUG)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
        
        return logger
    
    def _init_database(self):
        """Initialize SQLite database for tracking."""
        db_path = Path(self.db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Agent sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS agent_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent_name TEXT NOT NULL,
                    session_start TIMESTAMP NOT NULL,
                    session_end TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    violations_count INTEGER DEFAULT 0,
                    validations_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # File tracking table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS file_tracking (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    file_path TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    line_count INTEGER NOT NULL,
                    token_count INTEGER,
                    validation_status TEXT DEFAULT 'pending',
                    violations TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES agent_sessions (id)
                )
            ''')
            
            # Validation rules table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS validation_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    rule_name TEXT NOT NULL UNIQUE,
                    rule_type TEXT NOT NULL,
                    rule_config TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Violations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS violations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    file_id INTEGER,
                    rule_name TEXT NOT NULL,
                    violation_type TEXT NOT NULL,
                    violation_details TEXT,
                    severity TEXT DEFAULT 'warning',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES agent_sessions (id),
                    FOREIGN KEY (file_id) REFERENCES file_tracking (id)
                )
            ''')
            
            # Performance metrics table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    metric_name TEXT NOT NULL,
                    metric_value REAL NOT NULL,
                    metric_unit TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES agent_sessions (id)
                )
            ''')
            
            conn.commit()
        
        self.logger.info(f"Database initialized at {self.db_path}")
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load tracking configuration."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "agent_tracking_config.json"
        
        config_path = Path(config_path)
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.logger.info(f"Loaded tracking config from {config_path}")
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load tracking config: {e}")
        
        # Default configuration
        default_config = {
            "monitoring": {
                "enabled": True,
                "scan_interval_seconds": 5,
                "watch_directories": [
                    "kitchen/",
                    "agents/",
                    "src/"
                ],
                "exclude_patterns": [
                    "*.pyc",
                    "__pycache__",
                    "*.log",
                    ".git",
                    "venv"
                ]
            },
            "validation_rules": {
                "file_size_limit": 250,
                "min_file_size": 50,
                "target_file_size": "150-250",
                "max_tokens_per_file": 30000,
                "target_tokens_per_file": "15000-25000",
                "require_type_hints": True,
                "require_error_handling": True,
                "require_logging": True,
                "forbid_monolithic_files": True,
                "forbid_metadata_only": True
            },
            "enforcement": {
                "auto_fix": False,
                "block_on_critical": True,
                "notify_on_violation": True,
                "generate_reports": True
            },
            "reporting": {
                "real_time_dashboard": True,
                "session_summaries": True,
                "trend_analysis": True,
                "compliance_reports": True
            }
        }
        
        self.logger.info("Using default tracking configuration")
        return default_config
    
    def start_session(self, agent_name: str) -> Dict[str, Any]:
        """
        Start a new agent tracking session.
        
        Args:
            agent_name: Name of the agent starting the session
            
        Returns:
            Session information and status
        """
        try:
            self.logger.info(f"Starting tracking session for agent: {agent_name}")
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create new session
                cursor.execute('''
                    INSERT INTO agent_sessions (agent_name, session_start)
                    VALUES (?, ?)
                ''', (agent_name, datetime.utcnow()))
                
                session_id = cursor.lastrowid
                conn.commit()
            
            # Update state
            self.current_agent = agent_name
            self.session_start = datetime.utcnow()
            self.violations = []
            self.validations = []
            
            # Start monitoring if enabled
            if self.config["monitoring"]["enabled"]:
                self._start_monitoring()
            
            result = {
                "status": "success",
                "session_id": session_id,
                "agent_name": agent_name,
                "session_start": self.session_start.isoformat(),
                "message": f"Tracking session started for {agent_name}"
            }
            
            self.logger.info(f"Tracking session {session_id} started successfully")
            return result
            
        except Exception as e:
            self.logger.error(f"Failed to start tracking session: {e}")
            return {
                "status": "error",
                "message": f"Failed to start tracking session: {str(e)}"
            }
    
    def end_session(self) -> Dict[str, Any]:
        """
        End the current agent tracking session.
        
        Returns:
            Session summary and final status
        """
        try:
            if not self.current_agent:
                return {"status": "error", "message": "No active session to end"}
            
            self.logger.info(f"Ending tracking session for agent: {self.current_agent}")
            
            # Stop monitoring
            if self.monitoring_active:
                self._stop_monitoring()
            
            # Update session in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get session ID
                cursor.execute('''
                    SELECT id FROM agent_sessions 
                    WHERE agent_name = ? AND status = 'active'
                    ORDER BY session_start DESC LIMIT 1
                ''', (self.current_agent,))
                
                result = cursor.fetchone()
                if result:
                    session_id = result[0]
                    
                    # Update session end
                    cursor.execute('''
                        UPDATE agent_sessions 
                        SET session_end = ?, status = 'completed',
                            violations_count = ?, validations_count = ?
                        WHERE id = ?
                    ''', (datetime.utcnow(), len(self.violations), len(self.validations), session_id))
                    
                    conn.commit()
                    
                    # Generate session summary
                    summary = self._generate_session_summary(session_id)
                    
                    result = {
                        "status": "success",
                        "session_id": session_id,
                        "agent_name": self.current_agent,
                        "session_duration": str(datetime.utcnow() - self.session_start),
                        "violations_count": len(self.violations),
                        "validations_count": len(self.validations),
                        "summary": summary,
                        "message": f"Tracking session ended for {self.current_agent}"
                    }
                    
                    self.logger.info(f"Session {session_id} ended successfully")
                    return result
            
            return {"status": "error", "message": "Session not found in database"}
            
        except Exception as e:
            self.logger.error(f"Failed to end tracking session: {e}")
            return {
                "status": "error",
                "message": f"Failed to end tracking session: {str(e)}"
            }
    
    def track_file_creation(self, file_path: str, content: str) -> Dict[str, Any]:
        """
        Track a newly created file and validate it against rules.
        
        Args:
            file_path: Path to the created file
            content: File content for analysis
            
        Returns:
            Validation results and tracking information
        """
        try:
            self.logger.info(f"Tracking file creation: {file_path}")
            
            # Calculate file metrics
            metrics = self._calculate_file_metrics(file_path, content)
            
            # Validate against rules
            validation_result = self._validate_file(file_path, content, metrics)
            
            # Store in database
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get current session ID
                cursor.execute('''
                    SELECT id FROM agent_sessions 
                    WHERE agent_name = ? AND status = 'active'
                    ORDER BY session_start DESC LIMIT 1
                ''', (self.current_agent,))
                
                session_result = cursor.fetchone()
                if session_result:
                    session_id = session_result[0]
                    
                    # Insert file tracking record
                    cursor.execute('''
                        INSERT INTO file_tracking 
                        (session_id, file_path, file_hash, file_size, line_count, 
                         token_count, validation_status, violations)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        session_id,
                        file_path,
                        metrics["file_hash"],
                        metrics["file_size"],
                        metrics["line_count"],
                        metrics["token_count"],
                        validation_result["status"],
                        json.dumps(validation_result["violations"])
                    ))
                    
                    file_id = cursor.lastrowid
                    
                    # Record violations if any
                    for violation in validation_result["violations"]:
                        cursor.execute('''
                            INSERT INTO violations 
                            (session_id, file_id, rule_name, violation_type, 
                             violation_details, severity)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                            session_id,
                            file_id,
                            violation["rule"],
                            violation["type"],
                            violation["details"],
                            violation["severity"]
                        ))
                    
                    conn.commit()
                    
                    # Update tracking state
                    if validation_result["violations"]:
                        self.violations.extend(validation_result["violations"])
                    else:
                        self.validations.append({
                            "file_path": file_path,
                            "status": "passed",
                            "timestamp": datetime.utcnow()
                        })
                    
                    result = {
                        "status": "success",
                        "file_id": file_id,
                        "file_path": file_path,
                        "validation_result": validation_result,
                        "metrics": metrics,
                        "message": f"File {file_path} tracked and validated"
                    }
                    
                    self.logger.info(f"File {file_path} tracked successfully")
                    return result
            
            return {"status": "error", "message": "No active session found"}
            
        except Exception as e:
            self.logger.error(f"Failed to track file creation: {e}")
            return {
                "status": "error",
                "message": f"Failed to track file creation: {str(e)}"
            }
    
    def _calculate_file_metrics(self, file_path: str, content: str) -> Dict[str, Any]:
        """Calculate comprehensive file metrics."""
        try:
            # Basic metrics
            file_size = len(content.encode('utf-8'))
            line_count = len(content.splitlines())
            
            # Estimate token count (rough approximation)
            token_count = len(content.split())
            
            # Calculate file hash
            file_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # Code analysis metrics
            code_metrics = self._analyze_code_quality(content)
            
            return {
                "file_path": file_path,
                "file_size": file_size,
                "line_count": line_count,
                "token_count": token_count,
                "file_hash": file_hash,
                "code_metrics": code_metrics
            }
            
        except Exception as e:
            self.logger.error(f"Failed to calculate file metrics: {e}")
            return {
                "file_path": file_path,
                "file_size": 0,
                "line_count": 0,
                "token_count": 0,
                "file_hash": "",
                "code_metrics": {}
            }
    
    def _analyze_code_quality(self, content: str) -> Dict[str, Any]:
        """Analyze code quality metrics."""
        try:
            metrics = {
                "has_type_hints": False,
                "has_error_handling": False,
                "has_logging": False,
                "function_count": 0,
                "class_count": 0,
                "complexity_score": 0
            }
            
            # Check for type hints
            if ":" in content and "->" in content:
                metrics["has_type_hints"] = True
            
            # Check for error handling
            if any(keyword in content for keyword in ["try:", "except:", "finally:", "raise"]):
                metrics["has_error_handling"] = True
            
            # Check for logging
            if any(keyword in content for keyword in ["logging", "logger", "log"]):
                metrics["has_logging"] = True
            
            # Count functions and classes
            try:
                tree = ast.parse(content)
                metrics["function_count"] = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
                metrics["class_count"] = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            except:
                pass
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Failed to analyze code quality: {e}")
            return {}
    
    def _validate_file(self, file_path: str, content: str, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Validate file against all rules."""
        violations = []
        rules = self.config["validation_rules"]
        
        # File size validation
        if metrics["line_count"] > rules["file_size_limit"]:
            violations.append({
                "rule": "file_size_limit",
                "type": "CRITICAL_FILE_SIZE_VIOLATION",
                "details": f"File has {metrics['line_count']} lines, limit is {rules['file_size_limit']}",
                "severity": "critical"
            })
        elif metrics["line_count"] < rules["min_file_size"]:
            violations.append({
                "rule": "min_file_size",
                "type": "MIN_FILE_SIZE_VIOLATION",
                "details": f"File has {metrics['line_count']} lines, minimum is {rules['min_file_size']}",
                "severity": "warning"
            })
        
        # Token count validation
        if metrics["token_count"] > rules["max_tokens_per_file"]:
            violations.append({
                "rule": "max_tokens_per_file",
                "type": "TOKEN_COUNT_VIOLATION",
                "details": f"File has {metrics['token_count']} tokens, limit is {rules['max_tokens_per_file']}",
                "severity": "critical"
            })
        
        # Code quality validation
        code_metrics = metrics.get("code_metrics", {})
        
        if rules["require_type_hints"] and not code_metrics.get("has_type_hints", False):
            violations.append({
                "rule": "require_type_hints",
                "type": "MISSING_TYPE_HINTS",
                "details": "File lacks type hints",
                "severity": "warning"
            })
        
        if rules["require_error_handling"] and not code_metrics.get("has_error_handling", False):
            violations.append({
                "rule": "require_error_handling",
                "type": "MISSING_ERROR_HANDLING",
                "details": "File lacks error handling",
                "severity": "warning"
            })
        
        if rules["require_logging"] and not code_metrics.get("has_logging", False):
            violations.append({
                "rule": "require_logging",
                "type": "MISSING_LOGGING",
                "details": "File lacks logging",
                "severity": "warning"
            })
        
        # Check for monolithic files
        if rules["forbid_monolithic_files"]:
            function_count = code_metrics.get("function_count", 0)
            if function_count > 10:  # Arbitrary threshold
                violations.append({
                    "rule": "forbid_monolithic_files",
                    "type": "MONOLITHIC_FILE_DETECTED",
                    "details": f"File has {function_count} functions, may be monolithic",
                    "severity": "warning"
                })
        
        # Check for metadata-only files
        if rules["forbid_metadata_only"]:
            if len(content.strip()) < 100 and "metadata" in content.lower():
                violations.append({
                    "rule": "forbid_metadata_only",
                    "type": "METADATA_ONLY_FILE",
                    "details": "File appears to be metadata-only",
                    "severity": "critical"
                })
        
        return {
            "status": "passed" if not violations else "failed",
            "violations": violations,
            "metrics": metrics
        }
    
    def _start_monitoring(self):
        """Start real-time file monitoring."""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_files, daemon=True)
        self.monitor_thread.start()
        self.logger.info("File monitoring started")
    
    def _stop_monitoring(self):
        """Stop real-time file monitoring."""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.logger.info("File monitoring stopped")
    
    def _monitor_files(self):
        """Background thread for monitoring file changes."""
        while self.monitoring_active:
            try:
                # Scan watched directories
                for directory in self.config["monitoring"]["watch_directories"]:
                    self._scan_directory(directory)
                
                # Wait for next scan
                time.sleep(self.config["monitoring"]["scan_interval_seconds"])
                
            except Exception as e:
                self.logger.error(f"Error in file monitoring: {e}")
                time.sleep(10)  # Wait longer on error
    
    def _scan_directory(self, directory: str):
        """Scan directory for new or modified files."""
        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                return
            
            for file_path in dir_path.rglob("*"):
                if file_path.is_file() and self._should_track_file(file_path):
                    self._check_file_changes(file_path)
                    
        except Exception as e:
            self.logger.error(f"Error scanning directory {directory}: {e}")
    
    def _should_track_file(self, file_path: Path) -> bool:
        """Determine if file should be tracked."""
        # Check exclude patterns
        for pattern in self.config["monitoring"]["exclude_patterns"]:
            if pattern in str(file_path):
                return False
        
        # Only track certain file types
        tracked_extensions = [".py", ".js", ".ts", ".json", ".yml", ".yaml", ".md"]
        return file_path.suffix in tracked_extensions
    
    def _check_file_changes(self, file_path: Path):
        """Check if file has changed and needs tracking."""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Calculate current hash
            current_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # Check if we've seen this file before
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT file_hash FROM file_tracking 
                    WHERE file_path = ? 
                    ORDER BY created_at DESC LIMIT 1
                ''', (str(file_path),))
                
                result = cursor.fetchone()
                if not result or result[0] != current_hash:
                    # File is new or changed, track it
                    self.track_file_creation(str(file_path), content)
                    
        except Exception as e:
            self.logger.error(f"Error checking file changes for {file_path}: {e}")
    
    def _generate_session_summary(self, session_id: int) -> Dict[str, Any]:
        """Generate comprehensive session summary."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get session details
                cursor.execute('''
                    SELECT agent_name, session_start, session_end, 
                           violations_count, validations_count
                    FROM agent_sessions WHERE id = ?
                ''', (session_id,))
                
                session_data = cursor.fetchone()
                if not session_data:
                    return {}
                
                # Get file statistics
                cursor.execute('''
                    SELECT COUNT(*) as total_files,
                           SUM(CASE WHEN validation_status = 'passed' THEN 1 ELSE 0 END) as passed_files,
                           SUM(CASE WHEN validation_status = 'failed' THEN 1 ELSE 0 END) as failed_files,
                           AVG(line_count) as avg_lines,
                           AVG(token_count) as avg_tokens
                    FROM file_tracking WHERE session_id = ?
                ''', (session_id,))
                
                file_stats = cursor.fetchone()
                
                # Get violation breakdown
                cursor.execute('''
                    SELECT rule_name, COUNT(*) as count
                    FROM violations WHERE session_id = ?
                    GROUP BY rule_name
                ''', (session_id,))
                
                violation_breakdown = dict(cursor.fetchall())
                
                return {
                    "session_info": {
                        "agent_name": session_data[0],
                        "session_start": session_data[1],
                        "session_end": session_data[2],
                        "duration": str(session_data[2] - session_data[1]) if session_data[2] else None
                    },
                    "file_statistics": {
                        "total_files": file_stats[0] or 0,
                        "passed_files": file_stats[1] or 0,
                        "failed_files": file_stats[2] or 0,
                        "pass_rate": (file_stats[1] / file_stats[0] * 100) if file_stats[0] else 0,
                        "average_lines": file_stats[3] or 0,
                        "average_tokens": file_stats[4] or 0
                    },
                    "violation_breakdown": violation_breakdown,
                    "overall_compliance": {
                        "total_violations": session_data[3] or 0,
                        "total_validations": session_data[4] or 0,
                        "compliance_rate": (session_data[4] / (session_data[3] + session_data[4]) * 100) if (session_data[3] + session_data[4]) > 0 else 100
                    }
                }
                
        except Exception as e:
            self.logger.error(f"Failed to generate session summary: {e}")
            return {}
    
    def get_current_status(self) -> Dict[str, Any]:
        """Get current tracking system status."""
        return {
            "system_status": "active" if self.monitoring_active else "inactive",
            "current_agent": self.current_agent,
            "session_start": self.session_start.isoformat() if self.session_start else None,
            "session_duration": str(datetime.utcnow() - self.session_start) if self.session_start else None,
            "violations_count": len(self.violations),
            "validations_count": len(self.validations),
            "monitoring_active": self.monitoring_active,
            "config": self.config
        }
    
    def get_compliance_report(self, session_id: Optional[int] = None) -> Dict[str, Any]:
        """Generate compliance report for current or specified session."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if session_id is None:
                    # Get current session
                    if not self.current_agent:
                        return {"status": "error", "message": "No active session"}
                    
                    cursor.execute('''
                        SELECT id FROM agent_sessions 
                        WHERE agent_name = ? AND status = 'active'
                        ORDER BY session_start DESC LIMIT 1
                    ''', (self.current_agent,))
                    
                    result = cursor.fetchone()
                    if not result:
                        return {"status": "error", "message": "No active session found"}
                    
                    session_id = result[0]
                
                # Generate comprehensive report
                summary = self._generate_session_summary(session_id)
                
                # Get recent violations
                cursor.execute('''
                    SELECT v.rule_name, v.violation_type, v.violation_details, 
                           v.severity, v.created_at, f.file_path
                    FROM violations v
                    JOIN file_tracking f ON v.file_id = f.id
                    WHERE v.session_id = ?
                    ORDER BY v.created_at DESC
                    LIMIT 20
                ''', (session_id,))
                
                recent_violations = [
                    {
                        "rule": row[0],
                        "type": row[1],
                        "details": row[2],
                        "severity": row[3],
                        "timestamp": row[4],
                        "file": row[5]
                    }
                    for row in cursor.fetchall()
                ]
                
                return {
                    "status": "success",
                    "session_id": session_id,
                    "summary": summary,
                    "recent_violations": recent_violations,
                    "compliance_score": summary.get("overall_compliance", {}).get("compliance_rate", 0),
                    "recommendations": self._generate_recommendations(summary)
                }
                
        except Exception as e:
            self.logger.error(f"Failed to generate compliance report: {e}")
            return {"status": "error", "message": f"Failed to generate report: {str(e)}"}
    
    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on session summary."""
        recommendations = []
        
        compliance_rate = summary.get("overall_compliance", {}).get("compliance_rate", 100)
        if compliance_rate < 80:
            recommendations.append("Focus on reducing violations to improve compliance rate")
        
        avg_lines = summary.get("file_statistics", {}).get("average_lines", 0)
        if avg_lines > 200:
            recommendations.append("Consider breaking down larger files to meet size requirements")
        
        violation_breakdown = summary.get("violation_breakdown", {})
        if "file_size_limit" in violation_breakdown:
            recommendations.append("Monitor file sizes more closely to avoid size violations")
        
        if "missing_type_hints" in violation_breakdown:
            recommendations.append("Add type hints to improve code quality and maintainability")
        
        if "missing_error_handling" in violation_breakdown:
            recommendations.append("Implement proper error handling in all functions")
        
        return recommendations

# Global tracking system instance
tracking_system = None

def get_tracking_system() -> AgentTrackingSystem:
    """Get or create global tracking system instance."""
    global tracking_system
    if tracking_system is None:
        tracking_system = AgentTrackingSystem()
    return tracking_system

def start_agent_session(agent_name: str) -> Dict[str, Any]:
    """Start a new agent tracking session."""
    return get_tracking_system().start_session(agent_name)

def end_agent_session() -> Dict[str, Any]:
    """End the current agent tracking session."""
    return get_tracking_system().end_session()

def track_file(file_path: str, content: str) -> Dict[str, Any]:
    """Track a file creation or modification."""
    return get_tracking_system().track_file_creation(file_path, content)

def get_compliance_report() -> Dict[str, Any]:
    """Get current compliance report."""
    return get_tracking_system().get_compliance_report() 