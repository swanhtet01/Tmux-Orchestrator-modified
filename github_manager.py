#!/usr/bin/env python3
"""
GitHub Manager Script
Automates GitHub tasks like pushing updates, creating issues, and managing repositories.
"""

import subprocess
import os
import requests
from typing import Dict, List

class GitHubManager:
    def __init__(self, repo_path: str, token: str = None):
        self.repo_path = os.path.abspath(repo_path)
        self.token = token
        self.api_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}" if token else None,
            "Accept": "application/vnd.github.v3+json"
        }
        self.performance_metrics = {
            'successful_pushes': 0,
            'failed_pushes': 0,
            'successful_api_calls': 0,
            'failed_api_calls': 0
        }

    def push_changes(self, repo_path: str, commit_message: str):
        """Push local changes to the GitHub repository."""
        repo_path = os.path.abspath(repo_path)
        os.chdir(repo_path)
        
        # Configure git to use token if available
        if self.token:
            subprocess.run(["git", "config", "user.name", "GitHub Action"], check=True)
            subprocess.run(["git", "config", "user.email", "action@github.com"], check=True)
            
        try:
            subprocess.run(["git", "add", "-A"], check=True)
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            if self.token:
                # Use token in the remote URL for authentication
                remote_url = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
                if remote_url:
                    if "https://" in remote_url:
                        new_url = f"https://x-access-token:{self.token}@github.com/{remote_url.split('github.com/')[1]}"
                        subprocess.run(["git", "remote", "set-url", "origin", new_url], check=True)
            
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            self.performance_metrics['successful_pushes'] += 1
        except subprocess.CalledProcessError as e:
            self.performance_metrics['failed_pushes'] += 1
            raise e

    def create_issue(self, repo: str, title: str, body: str):
        """Create a new issue in the specified repository."""
        url = f"{self.api_url}/repos/{repo}/issues"
        data = {"title": title, "body": body}
        response = requests.post(url, json=data, headers=self.headers)
        if response.status_code == 201:
            print(f"✅ Issue created: {response.json().get('html_url')}")
        else:
            print(f"❌ Failed to create issue: {response.status_code}, {response.text}")

    def list_repos(self):
        """List all repositories for the authenticated user."""
        url = f"{self.api_url}/user/repos"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            repos = response.json()
            for repo in repos:
                print(f"- {repo['name']} ({repo['html_url']})")
        else:
            print(f"❌ Failed to list repositories: {response.status_code}, {response.text}")

    def add_collaborator(self, repo: str, username: str, permission: str = "push"):
        """Add a collaborator to a repository."""
        url = f"{self.api_url}/repos/{repo}/collaborators/{username}"
        data = {"permission": permission}
        response = requests.put(url, json=data, headers=self.headers)
        if response.status_code in [201, 204]:
            print(f"✅ Collaborator {username} added to {repo}.")
        else:
            print(f"❌ Failed to add collaborator: {response.status_code}, {response.text}")

    def update_repo_settings(self, repo: str, settings: Dict):
        """Update repository settings (e.g., description, private/public)."""
        url = f"{self.api_url}/repos/{repo}"
        response = requests.patch(url, json=settings, headers=self.headers)
        if response.status_code == 200:
            print(f"✅ Repository settings updated for {repo}.")
        else:
            print(f"❌ Failed to update settings: {response.status_code}, {response.text}")

    def get_repo_events(self, repo: str):
        """Get recent events for a repository."""
        url = f"{self.api_url}/repos/{repo}/events"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            self.performance_metrics['successful_api_calls'] += 1
            events = response.json()
            for event in events:
                print(f"- {event['type']} by {event['actor']['login']} at {event['created_at']}")
        else:
            self.performance_metrics['failed_api_calls'] += 1
            print(f"❌ Failed to get events: {response.status_code}, {response.text}")

    def analyze_performance(self):
        """Analyze performance metrics and suggest improvements."""
        total_operations = sum(self.performance_metrics.values())
        if total_operations == 0:
            return "No operations performed yet."

        success_rate = (
            (self.performance_metrics['successful_pushes'] + self.performance_metrics['successful_api_calls']) /
            total_operations * 100
        )

        report = f"""
Performance Analysis:
-------------------
Success Rate: {success_rate:.2f}%
Total Operations: {total_operations}
Successful Pushes: {self.performance_metrics['successful_pushes']}
Failed Pushes: {self.performance_metrics['failed_pushes']}
Successful API Calls: {self.performance_metrics['successful_api_calls']}
Failed API Calls: {self.performance_metrics['failed_api_calls']}
"""
        if success_rate < 80:
            report += "\n⚠️ Performance is below optimal levels. Consider:"
            if self.performance_metrics['failed_pushes'] > self.performance_metrics['successful_pushes']:
                report += "\n- Checking Git authentication and permissions"
                report += "\n- Validating remote repository configurations"
            if self.performance_metrics['failed_api_calls'] > self.performance_metrics['successful_api_calls']:
                report += "\n- Verifying API token validity and permissions"
                report += "\n- Checking API rate limits"
        return report

    def optimize(self):
        """Implement self-optimization based on performance metrics."""
        if self.performance_metrics['failed_pushes'] > 0:
            print("🔄 Implementing retry mechanism for failed pushes...")
            # Add retry mechanism for failed operations
        if self.performance_metrics['failed_api_calls'] > 0:
            print("🔄 Implementing rate limiting and automatic retries for API calls...")
            # Add rate limiting and automatic retries

if __name__ == "__main__":
    # Example usage
    token = os.getenv("GITHUB_TOKEN")  # Set your GitHub token as an environment variable
    if not token:
        print("❌ GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
        exit(1)

    manager = GitHubManager(token)

    # Example operations
    # manager.push_changes("/path/to/repo", "Automated commit message")
    # manager.create_issue("owner/repo", "Issue Title", "Issue Body")
    # manager.list_repos()
