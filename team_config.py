# Autonomous Dev Team Configuration
# Customize your projects and team structure here

import os
from pathlib import Path

# Base configuration
TEAM_CONFIG = {
    "session_name": "autonomous-dev-team",
    "base_dir": Path(__file__).parent,
    "monitoring_interval": 600,  # seconds between health checks
    "orchestrator_checkin": 120,  # minutes between orchestrator check-ins
    "pm_checkin": 30,  # minutes between PM check-ins
}

# Your Projects - Customize these for your actual work
PROJECTS = [
    {
        "name": "AITaskManager",
        "type": "Full-Stack Task Management App",
        "repo_path": os.path.expanduser("~/dev-projects/ai-task-manager"),
        "github_repo": "swanhtet01/ai-task-manager",
        "requirements": [
            "User authentication with JWT",
            "Task CRUD operations with React frontend", 
            "Real-time collaboration features",
            "Docker containerization and deployment",
            "Complete CI/CD pipeline with GitHub Actions",
            "Monitoring with Prometheus and Grafana"
        ],
        "priority": "high",
        "team_roles": ["frontend", "backend", "devops", "qa"],
        "github_issues": [1, 2, 3]  # Track the issues we just created
    },
    {
        "name": "DemoProject", 
        "type": "Learning & Experimentation",
        "repo_path": os.path.expanduser("~/dev-projects/demo-experiments"),
        "requirements": [
            "Test new technologies and frameworks",
            "Prototype innovative features",
            "Performance benchmarking",
            "Code quality experiments"
        ],
        "priority": "low",
        "team_roles": ["backend", "frontend"]
    }
]

# Team Role Definitions
ROLE_DEFINITIONS = {
    "frontend": {
        "title": "Frontend Engineer",
        "specializations": [
            "React/Vue/Angular development",
            "CSS/SCSS styling and responsive design", 
            "JavaScript/TypeScript",
            "UI/UX implementation",
            "Performance optimization",
            "Cross-browser compatibility"
        ],
        "tools": ["npm/yarn", "webpack/vite", "browser dev tools", "figma/sketch"]
    },
    "backend": {
        "title": "Backend Engineer", 
        "specializations": [
            "API design and development",
            "Database design and optimization",
            "Authentication and security",
            "Server-side logic and architecture",
            "Third-party integrations", 
            "Performance and scalability"
        ],
        "tools": ["Node.js/Python/Go", "databases", "API testing tools", "cloud services"]
    },
    "devops": {
        "title": "DevOps Engineer",
        "specializations": [
            "CI/CD pipeline setup",
            "Infrastructure as code",
            "Container orchestration",
            "Monitoring and logging",
            "Security and compliance",
            "Cloud deployment and scaling"
        ],
        "tools": ["docker", "kubernetes", "terraform", "jenkins/github-actions", "monitoring tools"]
    },
    "qa": {
        "title": "QA Engineer",
        "specializations": [
            "Test planning and strategy",
            "Automated testing frameworks",
            "Manual testing and exploratory testing",
            "Performance and load testing",
            "Bug reporting and tracking",
            "Quality metrics and documentation"
        ],
        "tools": ["selenium/cypress", "jest/mocha", "postman", "jira/linear", "performance testing tools"]
    }
}

# Git and Development Standards
DEV_STANDARDS = {
    "commit_frequency": 30,  # minutes
    "code_review_required": True,
    "testing_required": True,
    "documentation_required": True,
    "branch_naming": "feature/task-description",
    "commit_message_format": "type(scope): description",
    "max_work_session": 4,  # hours before mandatory break
}

# Escalation Rules
ESCALATION_RULES = {
    "blocked_time_limit": 60,  # minutes before escalating to PM
    "pm_blocked_time_limit": 120,  # minutes before escalating to orchestrator  
    "critical_issues": [
        "Security vulnerabilities",
        "Data loss or corruption",
        "Production outages",
        "Legal/compliance issues"
    ],
    "human_intervention_triggers": [
        "Project deadline at risk",
        "Budget concerns", 
        "Scope changes needed",
        "External dependencies blocking progress"
    ]
}

# Monitoring and Reporting
MONITORING_CONFIG = {
    "health_check_interval": 300,  # seconds
    "progress_report_interval": 3600,  # seconds (1 hour)
    "daily_summary": True,
    "weekly_summary": True,
    "metrics_to_track": [
        "commits_per_day",
        "issues_resolved",
        "code_coverage",
        "build_success_rate",
        "deployment_frequency"
    ]
}

# Slack/Discord Integration (optional)
NOTIFICATIONS = {
    "enabled": False,
    "webhook_url": "",  # Add your webhook URL here
    "channels": {
        "general": "#dev-team",
        "alerts": "#dev-alerts", 
        "deployments": "#deployments"
    },
    "notification_types": [
        "project_completed",
        "critical_errors",
        "deployment_status",
        "daily_summaries"
    ]
}
