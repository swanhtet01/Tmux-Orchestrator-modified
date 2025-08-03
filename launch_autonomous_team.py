#!/usr/bin/env python3
"""
Enhanced Autonomous Dev Team Launcher
Uses team_config.py to create customized development teams
"""

import subprocess
import json
import time
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Import configuration
try:
    from team_config import PROJECTS, TEAM_CONFIG, ROLE_DEFINITIONS, DEV_STANDARDS
except ImportError:
    print("❌ Error: team_config.py not found. Please ensure it's in the same directory.")
    sys.exit(1)

class EnhancedAutonomousTeam:
    def __init__(self):
        self.base_dir = TEAM_CONFIG["base_dir"]
        self.session_name = TEAM_CONFIG["session_name"]
        self.projects = {}
        self.active_windows = 0
        
    def check_dependencies(self):
        """Check if required tools are available"""
        print("🔍 Checking dependencies...")
        
        dependencies = ["tmux", "git", "python3"]
        missing = []
        
        for dep in dependencies:
            if subprocess.run(["which", dep], capture_output=True).returncode != 0:
                missing.append(dep)
        
        if missing:
            print(f"❌ Missing dependencies: {', '.join(missing)}")
            print("Please install them and try again.")
            return False
            
        print("✅ All dependencies available")
        return True
    
    def create_project_directories(self):
        """Create project directories if they don't exist"""
        print("📁 Setting up project directories...")
        
        for project in PROJECTS:
            repo_path = Path(project["repo_path"])
            if not repo_path.exists():
                print(f"   Creating: {repo_path}")
                repo_path.mkdir(parents=True, exist_ok=True)
                
                # Initialize git repo if needed
                if not (repo_path / ".git").exists():
                    subprocess.run(["git", "init"], cwd=repo_path, check=True)
                    
                    # Create basic project structure
                    self._create_project_structure(repo_path, project)
        
        print("✅ Project directories ready")
    
    def _create_project_structure(self, repo_path: Path, project: dict):
        """Create basic project structure based on project type"""
        project_type = project["type"].lower()
        
        # Create README
        readme_content = f"""# {project['name']}

**Type**: {project['type']}
**Status**: In Development (Autonomous AI Team)

## Requirements
{chr(10).join([f"- {req}" for req in project['requirements']])}

## Team
This project is being developed by an autonomous AI development team:
- Project Manager: Coordinates development and ensures requirements are met
- Engineers: Implement features based on specialization
- QA: Ensures quality and testing standards
- DevOps: Handles deployment and infrastructure

## Development
The team follows these standards:
- Commits every {DEV_STANDARDS['commit_frequency']} minutes
- Code review required: {DEV_STANDARDS['code_review_required']}
- Testing required: {DEV_STANDARDS['testing_required']}

Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
        (repo_path / "README.md").write_text(readme_content)
        
        # Create basic structure based on project type
        if "website" in project_type or "frontend" in project_type:
            (repo_path / "src").mkdir(exist_ok=True)
            (repo_path / "public").mkdir(exist_ok=True)
            (repo_path / "src" / "components").mkdir(exist_ok=True)
            (repo_path / "src" / "styles").mkdir(exist_ok=True)
            
        elif "api" in project_type or "backend" in project_type:
            (repo_path / "src").mkdir(exist_ok=True)
            (repo_path / "tests").mkdir(exist_ok=True)
            (repo_path / "docs").mkdir(exist_ok=True)
            
        elif "mobile" in project_type:
            (repo_path / "src").mkdir(exist_ok=True)
            (repo_path / "assets").mkdir(exist_ok=True)
            (repo_path / "tests").mkdir(exist_ok=True)
        
        # Always create these
        (repo_path / "docs").mkdir(exist_ok=True)
        (repo_path / "tests").mkdir(exist_ok=True)
        (repo_path / ".github" / "workflows").mkdir(parents=True, exist_ok=True)
        
        # Initial commit
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", "Initial project setup by AI team"], cwd=repo_path, check=True)
    
    def create_orchestrator(self):
        """Create master orchestrator"""
        print("🎯 Creating Master Orchestrator...")
        
        # Create session
        cmd = ["tmux", "new-session", "-d", "-s", self.session_name]
        subprocess.run(cmd, check=True)
        
        # Rename window
        subprocess.run(["tmux", "rename-window", "-t", f"{self.session_name}:0", "Orchestrator"], check=True)
        
        # Send orchestrator prompt
        orchestrator_prompt = self._get_enhanced_orchestrator_prompt()
        self._send_message_to_window(f"{self.session_name}:0", orchestrator_prompt)
        
        self.active_windows = 1
        print("✅ Master Orchestrator online")
    
    def setup_projects(self):
        """Set up all projects from configuration"""
        print(f"🏗️  Setting up {len(PROJECTS)} projects...")
        
        for project in PROJECTS:
            self.setup_single_project(project)
            time.sleep(2)  # Small delay between project setups
    
    def setup_single_project(self, project: dict):
        """Set up a single project with its team"""
        project_name = project["name"]
        print(f"   📋 Setting up {project_name}...")
        
        # Create PM window
        pm_window_num = self.active_windows
        pm_window = f"{self.session_name}:{pm_window_num}"
        subprocess.run(["tmux", "new-window", "-t", self.session_name, "-n", f"PM-{project_name}"], check=True)
        
        # Create developer windows based on project team roles
        dev_windows = {}
        for role in project.get("team_roles", ["frontend", "backend", "devops", "qa"]):
            self.active_windows += 1
            dev_window_num = self.active_windows
            dev_window = f"{self.session_name}:{dev_window_num}"
            window_name = f"{ROLE_DEFINITIONS[role]['title'].replace(' ', '')}-{project_name}"
            subprocess.run(["tmux", "new-window", "-t", self.session_name, "-n", window_name], check=True)
            dev_windows[role] = dev_window
        
        # Store project info
        self.projects[project_name] = {
            **project,
            "pm_window": pm_window,
            "dev_windows": dev_windows,
            "pm_window_num": pm_window_num
        }
        
        # Initialize PM
        pm_prompt = self._get_enhanced_pm_prompt(project, dev_windows)
        self._send_message_to_window(pm_window, pm_prompt)
        
        # Initialize developers
        for role, window in dev_windows.items():
            dev_prompt = self._get_enhanced_developer_prompt(role, project)
            self._send_message_to_window(window, dev_prompt)
        
        self.active_windows += 1  # Account for PM window
        print(f"      ✅ {project_name} team ready ({len(dev_windows) + 1} agents)")
    
    def _get_enhanced_orchestrator_prompt(self) -> str:
        return f"""🎯 MASTER ORCHESTRATOR INITIALIZATION

You are the Master Orchestrator for an autonomous development organization.

CONFIGURATION:
- Session: {self.session_name}
- Projects: {len(PROJECTS)} active projects
- Total Team Size: {sum(len(p.get('team_roles', [])) + 1 for p in PROJECTS)} agents
- Check-in Frequency: Every {TEAM_CONFIG['orchestrator_checkin']} minutes

YOUR PROJECTS:
{chr(10).join([f"- {p['name']}: {p['type']} (Priority: {p.get('priority', 'normal')})" for p in PROJECTS])}

RESPONSIBILITIES:
1. 🎛️  Strategic oversight across all projects
2. 🔄 Cross-project coordination and dependency management  
3. 📊 Resource allocation and priority management
4. 🚨 Escalation handling and critical decision making
5. 📈 Progress monitoring and quality assurance
6. 🤖 Team health monitoring and optimization

AUTONOMOUS CAPABILITIES:
- Self-schedule check-ins every {TEAM_CONFIG['orchestrator_checkin']} minutes
- Monitor project health and intervene when needed
- Coordinate cross-project dependencies automatically
- Escalate to human when critical decisions needed
- Optimize team performance based on metrics

AVAILABLE COMMANDS:
- `python3 {self.base_dir}/claude_control.py status` - Get team status
- `python3 {self.base_dir}/claude_control.py snapshot` - Detailed monitoring
- `{self.base_dir}/schedule_with_note.sh <min> "<note>"` - Schedule check-ins
- `{self.base_dir}/send-claude-message.sh <window> "<msg>"` - Send messages

IMMEDIATE ACTIONS:
1. Acknowledge your role as Master Orchestrator
2. Review all project windows and team status
3. Set up your first automated check-in schedule
4. Begin strategic oversight of development progress

🚀 INITIATE AUTONOMOUS ORCHESTRATION MODE"""

    def _get_enhanced_pm_prompt(self, project: dict, dev_windows: dict) -> str:
        team_list = chr(10).join([
            f"- {ROLE_DEFINITIONS[role]['title']}: {window} (Specializes in {', '.join(ROLE_DEFINITIONS[role]['specializations'][:2])})" 
            for role, window in dev_windows.items()
        ])
        
        return f"""📋 PROJECT MANAGER INITIALIZATION

You are the Project Manager for {project['name']}.

PROJECT OVERVIEW:
- Name: {project['name']}
- Type: {project['type']}
- Repository: {project['repo_path']}
- Priority: {project.get('priority', 'normal').upper()}

REQUIREMENTS TO DELIVER:
{chr(10).join([f"{i+1}. {req}" for i, req in enumerate(project['requirements'])])}

YOUR DEVELOPMENT TEAM:
{team_list}

MANAGEMENT RESPONSIBILITIES:
1. 📋 Break down requirements into specific, actionable tasks
2. 👥 Assign tasks to appropriate team members based on specialization
3. 🔄 Monitor progress and remove blockers proactively
4. 🧪 Ensure testing and quality standards are met
5. 📦 Coordinate deployments and releases
6. 📊 Report progress to Master Orchestrator regularly

AUTONOMOUS BEHAVIORS:
- Check team progress every {TEAM_CONFIG['pm_checkin']} minutes
- Automatically reassign tasks if developers are blocked
- Enforce git discipline (commits every {DEV_STANDARDS['commit_frequency']} minutes)
- Request code reviews before merging
- Escalate to Orchestrator if project timeline is at risk

QUALITY STANDARDS:
- Code review required: {DEV_STANDARDS['code_review_required']}
- Testing required: {DEV_STANDARDS['testing_required']}
- Documentation required: {DEV_STANDARDS['documentation_required']}
- Max work session: {DEV_STANDARDS['max_work_session']} hours

COMMUNICATION COMMANDS:
- `{self.base_dir}/send-claude-message.sh <window> "<message>"` - Message team members
- `{self.base_dir}/schedule_with_note.sh {TEAM_CONFIG['pm_checkin']} "Check {project['name']} progress"` - Schedule check-ins

IMMEDIATE ACTIONS:
1. Acknowledge your role as PM for {project['name']}
2. Analyze requirements and create initial task breakdown
3. Assign first round of tasks to your development team
4. Set up your automated progress monitoring schedule

🎯 BEGIN PROJECT MANAGEMENT FOR {project['name'].upper()}"""

    def _get_enhanced_developer_prompt(self, role: str, project: dict) -> str:
        role_info = ROLE_DEFINITIONS[role]
        
        return f"""👨‍💻 {role_info['title'].upper()} INITIALIZATION

You are a {role_info['title']} on the {project['name']} project.

PROJECT CONTEXT:
- Project: {project['name']} ({project['type']})
- Repository: {project['repo_path']}
- Your Role: {role_info['title']}

YOUR SPECIALIZATIONS:
{chr(10).join([f"• {spec}" for spec in role_info['specializations']])}

TOOLS & TECHNOLOGIES:
{chr(10).join([f"• {tool}" for tool in role_info['tools']])}

DEVELOPMENT RESPONSIBILITIES:
1. 🔨 Implement features assigned by your Project Manager
2. 🧪 Write comprehensive tests for your code
3. 📖 Document your work clearly
4. 🔍 Conduct code reviews for team members
5. 🐛 Debug and fix issues in your area of expertise
6. 🚀 Optimize performance and maintain quality standards

AUTONOMOUS BEHAVIORS:
- Work independently on assigned tasks
- Research solutions when blocked (web search after 10 minutes)
- Commit progress every {DEV_STANDARDS['commit_frequency']} minutes with descriptive messages
- Request help from PM if blocked for more than 60 minutes
- Take initiative on improvements and optimizations
- Suggest better approaches or technologies when appropriate

GIT DISCIPLINE (MANDATORY):
- `git add -A && git commit -m "feat: <description>"` every {DEV_STANDARDS['commit_frequency']} minutes
- Always commit before switching tasks or taking breaks
- Use conventional commit format: {DEV_STANDARDS['commit_message_format']}
- Create feature branches: {DEV_STANDARDS['branch_naming']}
- Never leave uncommitted changes

QUALITY STANDARDS:
- Write tests for all new functionality
- Ensure code coverage meets project standards
- Follow team coding conventions
- Document complex logic and APIs
- Optimize for performance and maintainability

COMMUNICATION:
- Report blockers immediately to PM
- Provide clear status updates when requested
- Collaborate effectively with other team members
- Suggest improvements to processes and architecture

IMMEDIATE ACTIONS:
1. Acknowledge your role as {role_info['title']} for {project['name']}
2. Navigate to repository and assess current codebase
3. Set up your development environment
4. Wait for task assignment from your Project Manager
5. Begin autonomous development work

🚀 {role.upper()} ENGINEER READY FOR {project['name'].upper()}"""

    def _send_message_to_window(self, window: str, message: str):
        """Send message to tmux window with claude"""
        # Clear any existing content
        subprocess.run(["tmux", "send-keys", "-t", window, "C-c"], check=False)
        time.sleep(0.5)
        
        # Start claude
        subprocess.run(["tmux", "send-keys", "-t", window, "claude"], check=True)
        time.sleep(2)
        
        # Send the message
        subprocess.run(["tmux", "send-keys", "-t", window, message, "Enter"], check=True)
    
    def setup_monitoring(self):
        """Set up autonomous monitoring and health checks"""
        print("📊 Activating monitoring systems...")
        
        # Create enhanced monitoring script
        monitor_script = self.base_dir / "enhanced_monitor.py"
        self._create_enhanced_monitor(monitor_script)
        
        # Schedule orchestrator check-ins
        schedule_cmd = [
            str(self.base_dir / "schedule_with_note.sh"),
            str(TEAM_CONFIG["orchestrator_checkin"]),
            f"🎯 ORCHESTRATOR: Review all {len(PROJECTS)} projects and coordinate teams"
        ]
        subprocess.run(schedule_cmd, check=True)
        
        print("✅ Autonomous monitoring activated")
    
    def _create_enhanced_monitor(self, script_path: Path):
        """Create enhanced monitoring script"""
        monitor_code = f'''#!/usr/bin/env python3
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
        self.session_name = "{self.session_name}"
        self.last_health_check = datetime.now()
        self.alert_cooldown = {{}}  # Prevent spam alerts
        
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
                                issues.append(f"🔴 INACTIVE: {{window_name}}")
                        
                        # Check for error patterns (if available)
                        # This would require additional tmux content checking
                        
            if issues:
                self._log_issues(issues)
            else:
                self._log_success()
                
        except Exception as e:
            self._log_error(f"Health check failed: {{e}}")
    
    def check_git_activity(self):
        """Monitor git activity across all projects"""
        projects = {PROJECTS}
        
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
                            self._log_issues([f"⚠️  NO COMMITS: {{project['name']}} ({{time_since_commit}})"])
                            
                except Exception as e:
                    self._log_error(f"Git check failed for {{project['name']}}: {{e}}")
    
    def _should_alert(self, alert_type: str, identifier: str) -> bool:
        """Prevent alert spam with cooldown"""
        key = f"{{alert_type}}_{{identifier}}"
        now = datetime.now()
        
        if key in self.alert_cooldown:
            if now - self.alert_cooldown[key] < timedelta(minutes=30):
                return False
        
        self.alert_cooldown[key] = now
        return True
    
    def _log_issues(self, issues: list):
        """Log issues with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{{timestamp}}] 🚨 TEAM HEALTH ISSUES:")
        for issue in issues:
            print(f"  {{issue}}")
    
    def _log_success(self):
        """Log successful health check"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{{timestamp}}] ✅ All team members active and healthy")
    
    def _log_error(self, error: str):
        """Log monitoring errors"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{{timestamp}}] ❌ MONITOR ERROR: {{error}}")
    
    def run_monitoring_loop(self):
        """Main monitoring loop"""
        print("🤖 Enhanced Team Monitor starting...")
        print(f"Monitoring session: {{self.session_name}}")
        print(f"Check interval: {TEAM_CONFIG['monitoring_interval']} seconds")
        
        while True:
            self.check_team_health()
            self.check_git_activity()
            time.sleep({TEAM_CONFIG['monitoring_interval']})

if __name__ == "__main__":
    monitor = TeamMonitor()
    monitor.run_monitoring_loop()
'''
        
        script_path.write_text(monitor_code)
        script_path.chmod(0o755)
    
    def show_final_summary(self):
        """Show comprehensive setup summary"""
        print("\n" + "="*80)
        print("🎉 AUTONOMOUS DEVELOPMENT TEAM DEPLOYMENT COMPLETE")
        print("="*80)
        
        print(f"\n📋 TEAM OVERVIEW:")
        print(f"  Session Name: {self.session_name}")
        print(f"  Total Projects: {len(PROJECTS)}")
        print(f"  Total Agents: {sum(len(p.get('team_roles', [])) + 1 for p in PROJECTS) + 1}")  # +1 for orchestrator
        print(f"  Active Windows: {self.active_windows}")
        
        print(f"\n🏗️  PROJECT BREAKDOWN:")
        window_num = 0
        print(f"  Window {window_num}: 🎯 Master Orchestrator")
        
        for project_name, project_info in self.projects.items():
            window_num = project_info['pm_window_num']
            print(f"  Window {window_num}: 📋 PM-{project_name} ({project_info['type']})")
            for role, window in project_info['dev_windows'].items():
                window_num = int(window.split(':')[1])
                role_title = ROLE_DEFINITIONS[role]['title']
                print(f"  Window {window_num}: 👨‍💻 {role_title}-{project_name}")
        
        print(f"\n🚀 QUICK START COMMANDS:")
        print(f"  tmux attach -t {self.session_name}     # Connect to your team")
        print(f"  tmux list-windows -t {self.session_name}  # See all team members")
        print(f"  python3 claude_control.py status          # Check team status")
        print(f"  python3 enhanced_monitor.py &             # Start monitoring (background)")
        
        print(f"\n⚙️  TEAM CONFIGURATION:")
        print(f"  Auto-commit frequency: {DEV_STANDARDS['commit_frequency']} minutes")
        print(f"  PM check-ins: Every {TEAM_CONFIG['pm_checkin']} minutes")
        print(f"  Orchestrator check-ins: Every {TEAM_CONFIG['orchestrator_checkin']} minutes")
        print(f"  Code review required: {DEV_STANDARDS['code_review_required']}")
        print(f"  Testing required: {DEV_STANDARDS['testing_required']}")
        
        print(f"\n🎯 YOUR PROJECTS:")
        for project in PROJECTS:
            status_emoji = "🔴" if project.get('priority') == 'high' else "🟡" if project.get('priority') == 'medium' else "🟢"
            print(f"  {status_emoji} {project['name']}: {project['type']}")
            print(f"     📁 {project['repo_path']}")
            print(f"     👥 Team: {', '.join([ROLE_DEFINITIONS[role]['title'] for role in project.get('team_roles', [])])}")
        
        print(f"\n🤖 AUTONOMOUS FEATURES ACTIVE:")
        print("  ✅ Self-scheduling agents with automatic check-ins")
        print("  ✅ Cross-project coordination and dependency management")
        print("  ✅ Automatic git commits and progress tracking")
        print("  ✅ Quality assurance and code review processes")
        print("  ✅ Health monitoring and issue escalation")
        print("  ✅ 24/7 development without human intervention")
        
        print(f"\n🎉 Your autonomous development team is now working around the clock!")
        print("   They will coordinate, develop, test, and deploy your projects automatically.")
        print("   Check in periodically or let them work independently. Happy coding! 🚀")
        print("\n" + "="*80)

def main():
    """Main setup function"""
    print("🤖 AUTONOMOUS DEVELOPMENT TEAM LAUNCHER")
    print("="*50)
    
    team = EnhancedAutonomousTeam()
    
    # Pre-flight checks
    if not team.check_dependencies():
        return False
    
    # Setup sequence
    try:
        team.create_project_directories()
        team.create_orchestrator()
        team.setup_projects()
        team.setup_monitoring()
        team.show_final_summary()
        
        return True
        
    except KeyboardInterrupt:
        print("\n❌ Setup interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
