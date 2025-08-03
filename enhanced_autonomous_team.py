#!/usr/bin/env python3
"""
Enhanced Autonomous Dev Team with Self-Improvement and Auto-Scaling
"""

import subprocess
import json
import time
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
import threading
import queue
from datetime import datetime

class EnhancedAutonomousTeam:
    def add_development_task(self, description: str, repo_path: str):
        """Queue a new development task for the team."""
        self.add_task({
            'type': 'development',
            'description': description,
            'repo_path': repo_path
        })
    def start_periodic_updates(self, repo_path: str, interval: int = 600):
        """Periodically update status.log and sync to GitHub."""
        def periodic():
            while True:
                self.update_status_log(repo_path, "Periodic update from autonomous team.")
                time.sleep(interval)
        thread = threading.Thread(target=periodic, daemon=True)
        thread.start()

    def update_status_log(self, repo_path: str, message: str):
        """Create or update a status.log file in the repo."""
        # Ensure directory exists
        if not os.path.exists(repo_path):
            os.makedirs(repo_path)
        # Ensure it's a git repo
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print(f"⚠️ Initializing git repository in {repo_path}")
            subprocess.run(['git', 'init'], cwd=repo_path)
        log_path = os.path.join(repo_path, "status.log")
        with open(log_path, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {message}\n")
        print(f"📝 Updated status.log in {repo_path}")
        # Queue a sync task with absolute repo path
        self.add_task({'type': 'github_sync', 'repo_path': repo_path})
    def __init__(self, base_config: dict = None):
        self.base_config = base_config or {}
        self.session_name = self.base_config.get('session_name', 'enhanced-dev-team')
        self.performance_metrics = {
            'tasks_completed': 0,
            'tasks_failed': 0,
            'optimization_cycles': 0
        }
        self.task_queue = queue.Queue()
        self.worker_threads = []
        self.monitoring_thread = None
        self.optimization_thread = None
        # Import GitHubManager from orchestrator
        sys.path.append(str(Path(__file__).parent))
        try:
            from github_manager import GitHubManager
            token = os.getenv('GITHUB_TOKEN')
            self.github_manager = GitHubManager(".", token)  # Initialize with current directory and token
            print("✅ GitHub manager initialized successfully")
        except Exception as e:
            print(f"⚠️ Could not import GitHubManager: {e}")
            self.github_manager = None

    def start_monitoring(self):
        """Start the monitoring thread."""
        def monitor():
            while True:
                self.analyze_performance()
                time.sleep(300)  # Check every 5 minutes

        self.monitoring_thread = threading.Thread(target=monitor, daemon=True)
        self.monitoring_thread.start()

    def start_optimization(self):
        """Start the optimization thread."""
        def optimize():
            while True:
                self.optimize_performance()
                time.sleep(3600)  # Optimize every hour

        self.optimization_thread = threading.Thread(target=optimize, daemon=True)
        self.optimization_thread.start()

    def analyze_performance(self):
        """Analyze team performance and suggest improvements."""
        total_tasks = self.performance_metrics['tasks_completed'] + self.performance_metrics['tasks_failed']
        if total_tasks == 0:
            return

        success_rate = (self.performance_metrics['tasks_completed'] / total_tasks) * 100
        print(f"\n🔍 Performance Analysis ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})")
        print(f"Success Rate: {success_rate:.2f}%")
        print(f"Tasks Completed: {self.performance_metrics['tasks_completed']}")
        print(f"Tasks Failed: {self.performance_metrics['tasks_failed']}")
        print(f"Optimization Cycles: {self.performance_metrics['optimization_cycles']}")

        if success_rate < 90:
            print("⚠️ Performance below target. Triggering optimization...")
            self.optimize_performance()

    def optimize_performance(self):
        """Implement performance optimizations."""
        print("\n🔄 Running optimization cycle...")
        
        # Scale workers based on task queue size
        queue_size = self.task_queue.qsize()
        current_workers = len(self.worker_threads)
        
        if queue_size > current_workers * 2:
            self.scale_up()
        elif queue_size < current_workers / 2:
            self.scale_down()

        # Implement other optimizations
        self.performance_metrics['optimization_cycles'] += 1

    def scale_up(self):
        """Add more worker threads."""
        new_workers = min(5, self.task_queue.qsize())  # Add up to 5 workers at once
        print(f"📈 Scaling up: Adding {new_workers} workers...")
        for _ in range(new_workers):
            self.add_worker()

    def scale_down(self):
        """Remove excess worker threads."""
        excess = len(self.worker_threads) - max(1, self.task_queue.qsize())
        if excess > 0:
            print(f"📉 Scaling down: Removing {excess} workers...")
            for _ in range(excess):
                if self.worker_threads:
                    worker = self.worker_threads.pop()
                    # Signal worker to stop
                    self.task_queue.put(None)

    def add_worker(self):
        """Add a new worker thread."""
        def worker():
            while True:
                task = self.task_queue.get()
                if task is None:  # Stop signal
                    break
                try:
                    self.execute_task(task)
                    self.performance_metrics['tasks_completed'] += 1
                except Exception as e:
                    print(f"❌ Task failed: {str(e)}")
                    self.performance_metrics['tasks_failed'] += 1
                finally:
                    self.task_queue.task_done()

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
        self.worker_threads.append(thread)

    def execute_task(self, task: Dict):
        """Execute a development task."""
        task_type = task.get('type')
        print(f"📋 Executing task: {task_type}")
        
        if task_type == 'code_review':
            self.review_code(task)
        elif task_type == 'testing':
            self.run_tests(task)
        elif task_type == 'deployment':
            self.deploy_changes(task)
        elif task_type == 'github_sync':
            self.sync_with_github(task)
        elif task_type == 'monitoring':
            self.monitor_repositories(task)
        elif task_type == 'development':
            self.handle_development_task(task)
        # Add more task types as needed

    def handle_development_task(self, task: Dict):
        """Handle a development task."""
        description = task.get('description')
        repo_path = task.get('repo_path')
        print(f"🛠️ Working on development task: {description} in {repo_path}")
        # Here, you can implement logic to call AI agents, refactor code, or run scripts
        # For now, just log the action
        
    def review_code(self, task: Dict):
        """Perform automated code review."""
        repo = task.get('repo')
        pr_number = task.get('pr_number')
        print(f"🔍 Reviewing code for PR #{pr_number} in {repo}")
        # Implement code review logic
        
    def run_tests(self, task: Dict):
        """Run automated tests."""
        repo = task.get('repo')
        test_path = task.get('test_path')
        print(f"🧪 Running tests in {repo}: {test_path}")
        # Implement test execution logic
        
    def deploy_changes(self, task: Dict):
        """Deploy code changes."""
        repo = task.get('repo')
        environment = task.get('environment', 'development')
        print(f"🚀 Deploying {repo} to {environment}")
        # Implement deployment logic
        
    def sync_with_github(self, task: Dict):
        """Synchronize with GitHub repository."""
        repo_path = task.get('repo_path')
        remote_url = task.get('remote_url')
        print(f"🔄 Syncing with GitHub repo: {repo_path}")
        if self.github_manager and repo_path:
            commit_message = f"Automated sync by EnhancedAutonomousTeam at {datetime.now().isoformat()}"
            try:
                # Check if remote is set
                result = subprocess.run(['git', 'remote'], cwd=repo_path, capture_output=True, text=True)
                if 'origin' not in result.stdout and remote_url:
                    print(f"🔗 Adding remote origin: {remote_url}")
                    subprocess.run(['git', 'remote', 'add', 'origin', remote_url], cwd=repo_path)
                self.github_manager.push_changes(repo_path, commit_message)
                # Push to remote
                subprocess.run(['git', 'push', '-u', 'origin', 'main'], cwd=repo_path)
                print(f"✅ Synced {repo_path} to GitHub.")
            except Exception as e:
                print(f"❌ Failed to sync {repo_path}: {e}")
        else:
            print("⚠️ GitHubManager not available or repo_path missing. Skipping sync.")
        
    def monitor_repositories(self, task: Dict):
        """Monitor repository activities."""
        repos = task.get('repos', [])
        print(f"👀 Monitoring repositories: {repos}")
        # Implement repository monitoring logic

    def add_task(self, task: Dict):
        """Add a task to the queue."""
        self.task_queue.put(task)
        print(f"📋 Task added: {task.get('type')}")
        
    def cleanup(self):
        """Clean up threads before shutdown."""
        print("\n🧹 Cleaning up threads...")
        # Signal all workers to stop
        for _ in self.worker_threads:
            self.task_queue.put(None)
        # Wait for all workers to finish
        for thread in self.worker_threads:
            thread.join(timeout=1)
        print("✅ Cleanup complete")

    def start(self):
        """Start the enhanced autonomous team."""
        print("🚀 Starting Enhanced Autonomous Dev Team...")
        self.add_worker()  # Start with one worker
        self.start_monitoring()
        self.start_optimization()
        
        try:
            # Update status.log in both repos and queue sync
            repo_dirs = [os.path.expanduser('~/InsightFactory'), os.path.expanduser('~/Downloads/Tmux-Orchestrator-modified')]
            for repo_dir in repo_dirs:
                self.update_status_log(repo_dir, "Autonomous team running and scaling!")
                self.start_periodic_updates(repo_dir, interval=600)

            # Add initial monitoring tasks
            initial_tasks = [
                {
                    'type': 'monitoring',
                    'repos': ['InsightFactory', 'Tmux-Orchestrator-modified']
                }
            ]
            for task in initial_tasks:
                self.add_task(task)

            print("✅ Team is running and will auto-scale based on workload.")

            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⚠️ Received shutdown signal...")
            self.cleanup()
            sys.exit(0)

if __name__ == "__main__":
    team = EnhancedAutonomousTeam()
    team.start()
