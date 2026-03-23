"""Git hook integration: prepare-commit-msg hook."""

from __future__ import annotations

import os
import stat
import subprocess
import sys
from pathlib import Path
from typing import Optional


HOOK_SCRIPT = '''#!/bin/sh
# commit-quip: prepare-commit-msg hook
# Suggests a witty commit message based on staged changes.
# Accept the suggestion or edit it in your editor.

COMMIT_MSG_FILE="$1"
COMMIT_SOURCE="$2"

# Only run for regular commits (not merges, squashes, etc.)
if [ -n "$COMMIT_SOURCE" ]; then
    exit 0
fi

# Check if commit-quip is available
if ! command -v commit-quip >/dev/null 2>&1; then
    # Try via python -m
    if ! python3 -m commit_quip.cli generate --help >/dev/null 2>&1; then
        exit 0
    fi
fi

# Get the current style from git config (default: professional)
STYLE=$(git config --get commit-quip.style 2>/dev/null || echo "professional")

# Generate suggestion
SUGGESTION=$(commit-quip generate --style "$STYLE" --first-only 2>/dev/null)

if [ -n "$SUGGESTION" ]; then
    # Prepend the suggestion to the commit message file
    # Keep the original content (including the commented-out diff) below
    ORIGINAL=$(cat "$COMMIT_MSG_FILE")
    {
        echo "$SUGGESTION"
        echo ""
        echo "# commit-quip suggestion (style: $STYLE)"
        echo "# Edit the message above, or leave as-is to accept."
        echo "# Delete all non-comment lines to abort the commit."
        echo "#"
        echo "$ORIGINAL"
    } > "$COMMIT_MSG_FILE"
fi
'''


def get_hooks_dir() -> Optional[Path]:
    """Get the git hooks directory for the current repository."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            git_dir = Path(result.stdout.strip())
            return git_dir / "hooks"
    except FileNotFoundError:
        pass
    return None


def install_hook() -> str:
    """Install the prepare-commit-msg hook.

    Returns a status message.
    """
    hooks_dir = get_hooks_dir()
    if not hooks_dir:
        return "Error: Not in a git repository."

    hooks_dir.mkdir(parents=True, exist_ok=True)
    hook_path = hooks_dir / "prepare-commit-msg"

    # Check for existing hook
    if hook_path.exists():
        content = hook_path.read_text(encoding="utf-8")
        if "commit-quip" in content:
            return f"commit-quip hook already installed at {hook_path}"
        else:
            # Backup existing hook
            backup_path = hook_path.with_suffix(".backup")
            hook_path.rename(backup_path)
            msg = f"Existing hook backed up to {backup_path}\n"
    else:
        msg = ""

    # Write hook
    hook_path.write_text(HOOK_SCRIPT, encoding="utf-8")

    # Make executable
    hook_path.chmod(hook_path.stat().st_mode | stat.S_IEXEC)

    return f"{msg}Hook installed at {hook_path}"


def uninstall_hook() -> str:
    """Remove the prepare-commit-msg hook.

    Returns a status message.
    """
    hooks_dir = get_hooks_dir()
    if not hooks_dir:
        return "Error: Not in a git repository."

    hook_path = hooks_dir / "prepare-commit-msg"

    if not hook_path.exists():
        return "No prepare-commit-msg hook found."

    content = hook_path.read_text(encoding="utf-8")
    if "commit-quip" not in content:
        return "Hook exists but was not installed by commit-quip. Not removing."

    hook_path.unlink()

    # Restore backup if exists
    backup_path = hook_path.with_suffix(".backup")
    if backup_path.exists():
        backup_path.rename(hook_path)
        return f"commit-quip hook removed. Previous hook restored from {backup_path}"

    return f"commit-quip hook removed from {hook_path}"


def set_style(style: str) -> str:
    """Set the default commit-quip style in git config.

    Returns a status message.
    """
    valid_styles = ["professional", "funny", "pirate", "shakespeare", "emoji", "minimal"]
    if style not in valid_styles:
        return f"Invalid style '{style}'. Choose from: {', '.join(valid_styles)}"

    try:
        subprocess.run(
            ["git", "config", "commit-quip.style", style],
            capture_output=True, text=True, check=True,
        )
        return f"Default style set to '{style}'"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return f"Error: Could not set git config. Are you in a git repository?"


def get_style() -> str:
    """Get the current commit-quip style from git config."""
    try:
        result = subprocess.run(
            ["git", "config", "--get", "commit-quip.style"],
            capture_output=True, text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return "professional"
