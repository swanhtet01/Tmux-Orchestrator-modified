#!/usr/bin/env python3
"""
Autonomous Dev Team Setup Script
Creates a complete autonomous development team that works 24/7

This script sets up:
1. Master Orchestrator - High-level project oversight
2. Project Managers - Per-project coordination  
3. Development Teams - Specialized roles (Frontend, Backend, DevOps, QA)
4. Automated scheduling and monitoring
"""

import subprocess
import json
import time
import os
from pathlib import Path
from typing import Dict, List, Optional
from github_manager import GitHubManager

class AutonomousDevTeam:
    def __init__(self, base_dir: str = None):
        self.base_dir = Path(base_dir) if base_dir else Path(__file__).parent
        self.session_name = "autonomous-dev-team"
        self.projects = {}
        self.github_manager = GitHubManager(os.getenv("GITHUB_TOKEN"))

    def create_master_orchestrator(self):
        """Create the master orchestrator session"""
        print("🚀 Creating Master Orchestrator...")
        
        # Create main orchestrator session
        cmd = ["tmux", "new-session", "-d", "-s", self.session_name, "-x", "120", "-y", "30"]
        subprocess.run(cmd, check=True)
        
        # Rename window to Orchestrator
        subprocess.run(["tmux", "rename-window", "-t", f"{self.session_name}:0", "Orchestrator"], check=True)
        
        # Send initial orchestrator prompt
        orchestrator_prompt = self._get_orchestrator_prompt()
        self._send_to_window(f"{self.session_name}:0", orchestrator_prompt)
        
        print("✅ Master Orchestrator created in session 'autonomous-dev-team:0'")
        
    def add_project(self, project_name: str, project_type: str, repo_path: str, requirements: List[str]):
        """Add a new project with its own PM and dev team"""
        print(f"📁 Setting up project: {project_name}")
        
        # Find next available window
        window_num = len(self.projects) + 1
        
        # Create project manager window
        pm_window = f"{self.session_name}:{window_num}"
        subprocess.run(["tmux", "new-window", "-t", self.session_name, "-n", f"PM-{project_name}"], check=True)
        
        # Create development team windows
        dev_windows = {}
        for i, role in enumerate(["Frontend", "Backend", "DevOps", "QA"], 1):
            dev_window_num = window_num + i
            dev_window = f"{self.session_name}:{dev_window_num}"
            subprocess.run(["tmux", "new-window", "-t", self.session_name, "-n", f"{role}-{project_name}"], check=True)
            dev_windows[role.lower()] = dev_window
        
        # Store project info
        self.projects[project_name] = {
            "type": project_type,
            "repo_path": repo_path,
            "requirements": requirements,
            "pm_window": pm_window,
            "dev_windows": dev_windows,
            "window_base": window_num
        }
        
        # Initialize Project Manager
        pm_prompt = self._get_pm_prompt(project_name, project_type, repo_path, requirements, dev_windows)
        self._send_to_window(pm_window, pm_prompt)
        
        # Initialize Developer agents
        for role, window in dev_windows.items():
            dev_prompt = self._get_developer_prompt(role, project_name, project_type, repo_path)
            self._send_to_window(window, dev_prompt)
        
        print(f"✅ Project {project_name} team created:")
        print(f"   PM: {pm_window}")
        for role, window in dev_windows.items():
            print(f"   {role.title()}: {window}")
    
    def setup_monitoring(self):
        """Set up automated monitoring and scheduling"""
        print("📊 Setting up autonomous monitoring...")
        
        # Create monitoring script
        monitor_script = self.base_dir / "autonomous_monitor.py"
        self._create_monitoring_script(monitor_script)
        
        # Schedule regular check-ins
        self._schedule_orchestrator_checkins()
        
        print("✅ Monitoring system activated")
    
    def _get_orchestrator_prompt(self) -> str:
        return f"""You are the Master Orchestrator for an autonomous development team.

ROLE: High-level oversight and coordination across all projects
RESPONSIBILITIES:
- Monitor all project managers and their teams
- Resolve cross-project dependencies and conflicts  
- Make architectural decisions that affect multiple projects
- Ensure quality standards and best practices
- Escalate critical issues requiring human intervention

CURRENT SETUP:
- Session: {self.session_name}
- Window: 0 (Orchestrator)
- Projects: {list(self.projects.keys()) if self.projects else "None yet"}

COMMANDS AVAILABLE:
- Use `python3 {self.base_dir}/claude_control.py status` to check all team status
- Use `python3 {self.base_dir}/claude_control.py snapshot` for detailed monitoring
- Use `./schedule_with_note.sh <minutes> "<note>"` to schedule your own check-ins

AUTONOMOUS BEHAVIORS:
1. Check project status every 2 hours automatically
2. Intervene if any project is blocked for >1 hour  
3. Coordinate cross-project dependencies
4. Schedule human escalation for critical decisions

NEXT ACTIONS:
1. Acknowledge your role as Master Orchestrator
2. Review current project portfolio (check windows 1+)
3. Set up your first 2-hour check-in schedule
4. Begin monitoring project progress

Start by saying "ORCHESTRATOR ONLINE" and then proceed with setup."""

    def _get_pm_prompt(self, project_name: str, project_type: str, repo_path: str, 
                      requirements: List[str], dev_windows: Dict[str, str]) -> str:
        return f"""You are the Project Manager for {project_name}.

PROJECT DETAILS:
- Name: {project_name}
- Type: {project_type}
- Repository: {repo_path}
- Requirements: {', '.join(requirements)}

YOUR TEAM:
{chr(10).join([f"- {role.title()}: {window}" for role, window in dev_windows.items()])}

RESPONSIBILITIES:
- Coordinate development across your team
- Break down requirements into specific tasks
- Assign work to appropriate team members
- Monitor progress and remove blockers
- Ensure code quality and testing standards
- Report status to Master Orchestrator

AUTONOMOUS BEHAVIORS:
1. Check team progress every 30 minutes
2. Reassign tasks if developers are blocked
3. Request code reviews before merging
4. Escalate to Orchestrator if project is at risk

COMMANDS:
- Use `python3 {self.base_dir}/send-claude-message.sh <window> "<message>"` to communicate with team
- Use `./schedule_with_note.sh 30 "Check team progress on {project_name}"` for scheduling

IMMEDIATE ACTIONS:
1. Acknowledge your role as PM for {project_name}
2. Review project requirements and create initial task breakdown
3. Assign initial tasks to your development team
4. Set up your first 30-min check-in schedule

Start by saying "PM {project_name.upper()} ONLINE" and begin coordinating your team."""

    def _get_developer_prompt(self, role: str, project_name: str, project_type: str, repo_path: str) -> str:
        role_specific_tasks = {
            "frontend": "UI/UX implementation, client-side logic, responsive design, user interactions",
            "backend": "Server-side logic, APIs, database design, authentication, performance optimization", 
            "devops": "Infrastructure, deployment pipelines, monitoring, security, environment management",
            "qa": "Test planning, automated testing, manual testing, bug reporting, quality assurance"
        }
        
        return f"""You are a {role.title()} Engineer on the {project_name} project.

PROJECT: {project_name} ({project_type})
REPOSITORY: {repo_path}
SPECIALIZATION: {role_specific_tasks.get(role.lower(), "General development tasks")}

RESPONSIBILITIES:
- Implement features assigned by your Project Manager
- Follow coding best practices and team standards
- Write tests for your code
- Commit progress every 30 minutes
- Communicate blockers immediately to PM
- Review code from other team members when requested

AUTONOMOUS BEHAVIORS:
1. Work on assigned tasks independently
2. Research solutions when blocked (use web search after 10min)
3. Commit and push code regularly
4. Request help if stuck for >1 hour
5. Take initiative on optimizations and improvements

GIT DISCIPLINE (CRITICAL):
- `git add -A && git commit -m "Progress: <description>"` every 30 minutes
- Always commit before switching tasks
- Use descriptive commit messages
- Create feature branches for major changes

NEXT ACTIONS:
1. Acknowledge your role as {role.title()} Engineer  
2. Check repository status and current codebase
3. Wait for task assignment from your PM
4. Set up development environment if needed

Start by saying "{role.upper()} ENGINEER ONLINE - {project_name.upper()}" and await instructions from your PM."""

    def _send_to_window(self, window: str, message: str):
        """Send a message to a specific tmux window"""
        # Clear any existing content
        subprocess.run(["tmux", "send-keys", "-t", window, "C-c"], check=False)
        time.sleep(0.5)
        
        # Send claude command to start AI
        subprocess.run(["tmux", "send-keys", "-t", window, "claude"], check=True)
        time.sleep(2)
        
        # Send the prompt
        subprocess.run(["tmux", "send-keys", "-t", window, message, "Enter"], check=True)
        
    def _schedule_orchestrator_checkins(self):
        """Schedule automatic check-ins for the orchestrator"""
        schedule_cmd = [
            str(self.base_dir / "schedule_with_note.sh"),
            "120",  # 2 hours
            "Master Orchestrator: Check all project status and coordinate teams"
        ]
        subprocess.run(schedule_cmd, check=True)
        
    def _create_monitoring_script(self, script_path: Path):
        """Create autonomous monitoring script"""
        monitoring_code = '''#!/usr/bin/env python3
"""
Autonomous Team Monitor
Runs continuously to monitor team health and progress
"""

import time
import subprocess
import json
from datetime import datetime

def check_team_health():
    """Check if all agents are responsive and making progress"""
    try:
        result = subprocess.run(
            ["python3", "claude_control.py", "status", "detailed"],
            capture_output=True, text=True, check=True
        )
        status = json.loads(result.stdout)
        
        # Analyze team health
        issues = []
        for session in status.get("sessions", []):
            for window in session.get("windows", []):
                # Check for inactive windows (no recent activity)
                if not window.get("active", False):
                    issues.append(f"Inactive: {window.get('name', 'unknown')}")
        
        if issues:
            print(f"[{datetime.now()}] Team health issues detected:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"[{datetime.now()}] All team members active and healthy")
            
    except Exception as e:
        print(f"[{datetime.now()}] Monitoring error: {e}")

def main():
    """Main monitoring loop"""
    print("🤖 Autonomous Team Monitor starting...")
    
    while True:
        check_team_health()
        time.sleep(600)  # Check every 10 minutes

if __name__ == "__main__":
    main()
'''
        
        script_path.write_text(monitoring_code)
        script_path.chmod(0o755)
    
    def get_status(self):
        """Get current status of all teams"""
        try:
            result = subprocess.run([
                "python3", str(self.base_dir / "claude_control.py"), "status"
            ], capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error getting status: {e}"
    
    def show_setup_summary(self):
        """Display setup summary"""
        print("\n" + "="*60)
        print("🤖 AUTONOMOUS DEV TEAM SETUP COMPLETE")
        print("="*60)
        print(f"Master Session: {self.session_name}")
        print("Windows:")
        print("  0: Master Orchestrator")
        
        for project_name, project_info in self.projects.items():
            base_window = project_info["window_base"]
            print(f"  {base_window}: PM-{project_name}")
            for i, role in enumerate(["Frontend", "Backend", "DevOps", "QA"], 1):
                print(f"  {base_window + i}: {role}-{project_name}")
        
        print("\nCOMMANDS:")
        print(f"  tmux attach -t {self.session_name}  # Connect to team")
        print(f"  python3 {self.base_dir}/claude_control.py status  # Check status")
        print(f"  python3 {self.base_dir}/autonomous_monitor.py &  # Start monitoring")
        
        print("\nYour autonomous dev team is now working 24/7! 🚀")

    def push_project_updates(self, project_name: str, commit_message: str):
        """Push updates for a specific project to GitHub."""
        if project_name in self.projects:
            repo_path = self.projects[project_name]["repo_path"]
            self.github_manager.push_changes(repo_path, commit_message)
        else:
            print(f"❌ Project {project_name} not found.")

    def create_project_issue(self, project_name: str, title: str, body: str):
        """Create an issue for a specific project."""
        if project_name in self.projects:
            repo = self.projects[project_name]["github_repo"]
            self.github_manager.create_issue(repo, title, body)
        else:
            print(f"❌ Project {project_name} not found.")

    def add_project_collaborator(self, project_name: str, username: str, permission: str = "push"):
        """Add a collaborator to a project's GitHub repository."""
        if project_name in self.projects:
            repo = self.projects[project_name]["github_repo"]
            self.github_manager.add_collaborator(repo, username, permission)
        else:
            print(f"❌ Project {project_name} not found.")

    def update_project_repo_settings(self, project_name: str, settings: dict):
        """Update repository settings for a project."""
        if project_name in self.projects:
            repo = self.projects[project_name]["github_repo"]
            self.github_manager.update_repo_settings(repo, settings)
        else:
            print(f"❌ Project {project_name} not found.")

    def monitor_project_repo_events(self, project_name: str):
        """Monitor recent events for a project's repository."""
        if project_name in self.projects:
            repo = self.projects[project_name]["github_repo"]
            self.github_manager.get_repo_events(repo)
        else:
            print(f"❌ Project {project_name} not found.")

def main():
    """Main setup function"""
    team = AutonomousDevTeam()
    
    print("🤖 Setting up Autonomous Development Team...")
    print("This will create a complete AI dev team that works 24/7\n")
    
    # Create master orchestrator
    team.create_master_orchestrator()
    time.sleep(2)
    
    # Example project setup - you can customize these
    sample_projects = [
        {
            "name": "WebApp",
            "type": "Full-Stack Application", 
            "repo_path": "/home/swanhtet/projects/webapp",
            "requirements": ["User authentication", "Dashboard", "API endpoints", "Responsive design"]
        },
        {
            "name": "MobileAPI",
            "type": "REST API Service",
            "repo_path": "/home/swanhtet/projects/mobile-api", 
            "requirements": ["JWT auth", "Data validation", "Rate limiting", "Documentation"]
        }
    ]
    
    # Set up sample projects (you can modify or add more)
    for project in sample_projects:
        team.add_project(
            project["name"],
            project["type"],
            project["repo_path"], 
            project["requirements"]
        )
        time.sleep(1)
    
    # Set up monitoring
    team.setup_monitoring()
    
    # Show summary
    team.show_setup_summary()

if __name__ == "__main__":
    main()
