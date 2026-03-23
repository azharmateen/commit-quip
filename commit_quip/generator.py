"""Generate commit messages: conventional commit format with personality."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from .analyzer import ChangeAnalysis, analyze_changes
from .templates import get_template, get_multiple_suggestions, get_available_styles


@dataclass
class CommitSuggestion:
    """A generated commit message suggestion."""
    message: str
    commit_type: str
    scope: Optional[str]
    style: str
    confidence: float
    is_breaking: bool


def generate(style: str = "professional",
             analysis: Optional[ChangeAnalysis] = None,
             count: int = 3) -> List[CommitSuggestion]:
    """Generate commit message suggestions based on staged changes.

    Args:
        style: Personality style (professional, funny, pirate, shakespeare, emoji, minimal).
        analysis: Pre-computed analysis (if None, runs git analysis).
        count: Number of suggestions to generate.

    Returns:
        List of CommitSuggestion objects.
    """
    if analysis is None:
        analysis = analyze_changes()

    messages = get_multiple_suggestions(
        commit_type=analysis.commit_type,
        style=style,
        scope=analysis.scope,
        description=analysis.description,
        count=count,
    )

    suggestions = []
    for msg in messages:
        # Add breaking change indicator
        if analysis.is_breaking:
            msg = msg.replace(f"{analysis.commit_type}(", f"{analysis.commit_type}!(")
            if "(" not in msg:
                msg = msg.replace(f"{analysis.commit_type}:", f"{analysis.commit_type}!:")

        suggestions.append(CommitSuggestion(
            message=msg,
            commit_type=analysis.commit_type,
            scope=analysis.scope,
            style=style,
            confidence=analysis.confidence,
            is_breaking=analysis.is_breaking,
        ))

    return suggestions


def generate_all_styles(analysis: Optional[ChangeAnalysis] = None) -> dict:
    """Generate one message per style for comparison.

    Returns dict mapping style name to message.
    """
    if analysis is None:
        analysis = analyze_changes()

    results = {}
    for style in get_available_styles():
        msg = get_template(
            commit_type=analysis.commit_type,
            style=style,
            scope=analysis.scope,
            description=analysis.description,
        )
        if analysis.is_breaking:
            msg = msg.replace(f"{analysis.commit_type}(", f"{analysis.commit_type}!(")
            if "(" not in msg:
                msg = msg.replace(f"{analysis.commit_type}:", f"{analysis.commit_type}!:")
        results[style] = msg

    return results
