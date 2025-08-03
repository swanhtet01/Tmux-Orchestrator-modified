#!/usr/bin/env python3
"""
claude_control.py - simple command‑line helper for the Tmux Orchestrator

This script exposes a few basic commands to interrogate a running tmux
orchestrator.  It is intentionally minimal so that it can run without
additional dependencies beyond Python's standard library.  It leverages
the ``tmux_utils`` module that ships with the orchestrator to inspect
current sessions and windows.  You can extend this script further to add
new commands (for example to rename windows automatically or to send
predefined messages).

Usage::

    python3 claude_control.py status [detailed]
        Print a summary of sessions and windows.  If ``detailed`` is
        supplied, dump a JSON document containing the full window status.

    python3 claude_control.py snapshot
        Produce a human‑readable snapshot suitable for feeding back into
        an AI agent.  This uses the ``create_monitoring_snapshot()``
        method of the ``TmuxOrchestrator`` class.

All output is printed to standard output.  The script exits with
non‑zero status on error or if an unknown command is supplied.
"""

from __future__ import annotations

import json
import sys
from typing import List

# Import the orchestrator utilities.  ``tmux_utils.py`` resides in the
# same directory as this script; modifying ``sys.path`` ensures Python
# discovers it regardless of the current working directory.
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from tmux_utils import TmuxOrchestrator  # type: ignore
except Exception as exc:
    print(f"Error importing tmux_utils: {exc}", file=sys.stderr)
    sys.exit(1)


def cmd_status(args: List[str]) -> int:
    """Display a summary of tmux sessions and windows.

    If the optional ``detailed`` argument is present, a JSON document is
    printed instead of the human‑readable summary.  The JSON includes
    captured pane contents which may be voluminous.

    Returns a process exit code (0 on success).
    """
    orchestrator = TmuxOrchestrator()
    if args and args[0] == "detailed":
        status = orchestrator.get_all_windows_status()
        print(json.dumps(status, indent=2))
        return 0

    sessions = orchestrator.get_tmux_sessions()
    if not sessions:
        print("No tmux sessions found.")
        return 0

    for sess in sessions:
        attached = "attached" if sess.attached else "detached"
        print(f"Session '{sess.name}' ({attached}):")
        for win in sess.windows:
            active = "*" if win.active else " "
            print(f"  [{active}] {win.window_index}: {win.window_name}")
    return 0


def cmd_snapshot(args: List[str]) -> int:
    """Generate a monitoring snapshot for AI agents to consume."""
    orchestrator = TmuxOrchestrator()
    snapshot = orchestrator.create_monitoring_snapshot()
    print(snapshot)
    return 0


def main(argv: List[str]) -> int:
    if not argv:
        print(__doc__)
        return 1

    cmd = argv[0]
    args = argv[1:]
    if cmd == "status":
        return cmd_status(args)
    if cmd == "snapshot":
        return cmd_snapshot(args)
    print(f"Unknown command: {cmd}", file=sys.stderr)
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))