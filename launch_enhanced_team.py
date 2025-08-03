#!/usr/bin/env python3
"""
Launch Script for Enhanced Autonomous Development Environment
Starts both the autonomous team and InsightFactory integration
"""

import os
import sys
from pathlib import Path
from enhanced_autonomous_team import EnhancedAutonomousTeam

# Add paths for both projects
SCRIPT_DIR = Path(__file__).resolve().parent
INSIGHT_FACTORY_DIR = SCRIPT_DIR.parent / 'InsightFactory'
sys.path.extend([str(SCRIPT_DIR), str(INSIGHT_FACTORY_DIR)])

try:
    from helpers.github_uploader import upload_report_to_github
except ImportError:
    print("Note: InsightFactory integration not available, continuing with core functionality...")

def main():
    # Check for GitHub token
    if not os.getenv("GITHUB_TOKEN"):
        print("❌ GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
        sys.exit(1)

    # Configure and start the enhanced autonomous team
    team_config = {
        'session_name': 'enhanced-dev-team',
        'base_dir': str(Path(__file__).parent),
        'github_token': os.getenv("GITHUB_TOKEN"),
        'auto_optimize': True,
        'min_workers': 1,
        'max_workers': 10
    }

    print("🚀 Launching Enhanced Autonomous Development Environment...")
    
    # Start the enhanced autonomous team
    team = EnhancedAutonomousTeam(team_config)
    team.start()

    print("""
✨ Enhanced Autonomous Development Environment is running!
   - Auto-scaling enabled
   - Self-improvement active
   - GitHub integration ready
   - Performance monitoring active
    """)

if __name__ == "__main__":
    main()
