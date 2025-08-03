#!/bin/bash
# Dynamic scheduler with note for next check
# Usage: ./schedule_with_note.sh <minutes> "<note>" [target_window]

MINUTES=${1:-3}
NOTE=${2:-"Standard check-in"}
TARGET=${3:-"tmux-orc:0"}

###
# The original implementation used hard‑coded absolute paths to write the next
# check note and to call ``claude_control.py``.  This made it difficult to run
# the script on other machines or from other directories.  Instead, compute
# everything relative to the location of this script.  ``DIR`` points at the
# directory containing ``schedule_with_note.sh`` and ``NOTE_FILE`` points at
# ``next_check_note.txt`` inside that directory.  ``CLAUDE_CTL`` similarly
# points at ``claude_control.py`` in the same folder.

# Determine the directory containing this script.  ``dirname $0`` returns the
# directory portion of the script name, ``cd`` changes into it and ``pwd``
# reports the absolute path.  Quoting and ``$(...)`` ensure spaces are
# handled correctly.
DIR="$(cd "$(dirname "$0")" && pwd)"
NOTE_FILE="$DIR/next_check_note.txt"
CLAUDE_CTL="$DIR/claude_control.py"

# Create a note file for the next check.  Use ``printf`` instead of multiple
# ``echo`` calls to avoid trailing spaces and to make quoting easier.  The
# date will vary by platform, but the note content is always written to
# ``NOTE_FILE``.
printf '=== Next Check Note (%s) ===\n' "$(date)" > "$NOTE_FILE"
printf 'Scheduled for: %s minutes\n\n' "$MINUTES" >> "$NOTE_FILE"
printf '%s\n' "$NOTE" >> "$NOTE_FILE"

echo "Scheduling check in $MINUTES minutes with note: $NOTE"

# Calculate the exact time when the check will run.  macOS' BSD ``date``
# supports ``-v +${MINUTES}M``, while GNU ``date`` uses ``-d "+${MINUTES}
# minutes"``.  Try the BSD syntax first and fall back to GNU if it fails.
CURRENT_TIME=$(date +"%H:%M:%S")
RUN_TIME=$(date -v +${MINUTES}M +"%H:%M:%S" 2>/dev/null || date -d "+${MINUTES} minutes" +"%H:%M:%S" 2>/dev/null)

# Use ``bc`` to compute the number of seconds to sleep.  ``bc`` handles
# floating point numbers if fractional minutes are ever supplied.
SECONDS=$(echo "$MINUTES * 60" | bc)

# Launch the scheduler in the background using ``nohup`` to detach it
# completely.  After sleeping the computed number of seconds the scheduler
# sends a message to the target tmux window.  The message prints the note
# file, runs ``claude_control.py status detailed`` from the orchestrator
# directory and presses Enter to execute the commands.  Quotes are escaped
# carefully to ensure the entire command is passed correctly to tmux.
nohup bash -c "sleep $SECONDS && tmux send-keys -t \"$TARGET\" 'Time for orchestrator check! cat \"$NOTE_FILE\" && python3 \"$CLAUDE_CTL\" status detailed' && sleep 1 && tmux send-keys -t \"$TARGET\" Enter" > /dev/null 2>&1 &

# Get the PID of the background process
SCHEDULE_PID=$!

echo "Scheduled successfully - process detached (PID: $SCHEDULE_PID)"
echo "SCHEDULED TO RUN AT: $RUN_TIME (in $MINUTES minutes from $CURRENT_TIME)"