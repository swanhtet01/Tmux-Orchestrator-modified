#!/usr/bin/env python3
"""
Enhanced Autonomous Team Monitor
Continuously monitors team health, progress, and performance
"""

import time
import subprocess
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

class TeamMonitor:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.session_name = "autonomous-dev-team"
        self.last_health_check = datetime.now()
        self.alert_cooldown = {}  # Prevent spam alerts
        
    def check_team_health(self):
        """Comprehensive team health monitoring"""
        try:
            result = subprocess.run([
                "python3", str(self.base_dir / "claude_control.py"), "status", "detailed"
            ], capture_output=True, text=True, check=True)
            
            status = json.loads(result.stdout)
            issues = []
            
            # Check each session and window
            for session in status.get("sessions", []):
                if session["name"] == self.session_name:
                    for window in session.get("windows", []):
                        window_name = window.get("name", "unknown")
                        
                        # Check for inactive windows
                        if not window.get("active", False):
                            if self._should_alert("inactive", window_name):
                                issues.append(f"🔴 INACTIVE: {window_name}")
                        
                        # Check for error patterns (if available)
                        # This would require additional tmux content checking
                        
            if issues:
                self._log_issues(issues)
            else:
                self._log_success()
                
        except Exception as e:
            self._log_error(f"Health check failed: {e}")
    
    def check_git_activity(self):
        """Monitor git activity across all projects"""
        projects = [{'name': 'AITaskManager', 'type': 'Full-Stack Task Management App', 'repo_path': '/home/swanhtet/dev-projects/ai-task-manager', 'github_repo': 'swanhtet01/ai-task-manager', 'requirements': ['User authentication with JWT', 'Task CRUD operations with React frontend', 'Real-time collaboration features', 'Docker containerization and deployment', 'Complete CI/CD pipeline with GitHub Actions', 'Monitoring with Prometheus and Grafana'], 'priority': 'high', 'team_roles': ['frontend', 'backend', 'devops', 'qa'], 'github_issues': [1, 2, 3]}, {'name': 'DemoProject', 'type': 'Learning & Experimentation', 'repo_path': '/home/swanhtet/dev-projects/demo-experiments', 'requirements': ['Test new technologies and frameworks', 'Prototype innovative features', 'Performance benchmarking', 'Code quality experiments'], 'priority': 'low', 'team_roles': ['backend', 'frontend']}]
        
        for project in projects:
            repo_path = Path(project["repo_path"])
            if repo_path.exists():
                try:
                    # Check last commit time
                    result = subprocess.run([
                        "git", "log", "-1", "--format=%ct"
                    ], cwd=repo_path, capture_output=True, text=True, check=True)
                    
                    last_commit_time = datetime.fromtimestamp(int(result.stdout.strip()))
                    time_since_commit = datetime.now() - last_commit_time
                    
                    # Alert if no commits in over 2 hours
                    if time_since_commit > timedelta(hours=2):
                        if self._should_alert("no_commits", project["name"]):
                            self._log_issues([f"⚠️  NO COMMITS: {project['name']} ({time_since_commit})"])
                            
                except Exception as e:
                    self._log_error(f"Git check failed for {project['name']}: {e}")
    
    def _should_alert(self, alert_type: str, identifier: str) -> bool:
        """Prevent alert spam with cooldown"""
        key = f"{alert_type}_{identifier}"
        now = datetime.now()
        
        if key in self.alert_cooldown:
            if now - self.alert_cooldown[key] < timedelta(minutes=30):
                return False
        
        self.alert_cooldown[key] = now
        return True
    
    def _log_issues(self, issues: list):
        """Log issues with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] 🚨 TEAM HEALTH ISSUES:")
        for issue in issues:
            print(f"  {issue}")
    
    def _log_success(self):
        """Log successful health check"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ✅ All team members active and healthy")
    
    def _log_error(self, error: str):
        """Log monitoring errors"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] ❌ MONITOR ERROR: {error}")
    
    def run_monitoring_loop(self):
        """Main monitoring loop"""
        print("🤖 Enhanced Team Monitor starting...")
        print(f"Monitoring session: {self.session_name}")
        print(f"Check interval: 600 seconds")
        
        while True:
            self.check_team_health()
            self.check_git_activity()
            time.sleep(600)

if __name__ == "__main__":
    monitor = TeamMonitor()
    monitor.run_monitoring_loop()
