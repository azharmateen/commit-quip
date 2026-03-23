"""Validate messages against conventional commit spec."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


VALID_TYPES = {
    "feat", "fix", "docs", "style", "refactor",
    "perf", "test", "build", "ci", "chore", "revert",
}

# Conventional commit regex:
# type(scope)!: description
# type!: description
# type(scope): description
# type: description
CONVENTIONAL_PATTERN = re.compile(
    r"^(?P<type>[a-z]+)"        # type
    r"(?:\((?P<scope>[^)]+)\))?" # optional scope in parens
    r"(?P<breaking>!)?"          # optional breaking indicator
    r":\s+"                      # colon and space
    r"(?P<description>.+)$"      # description
)


@dataclass
class ValidationIssue:
    """A single validation issue."""
    level: str  # "error" or "warning"
    message: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of validating a commit message."""
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    parsed_type: Optional[str] = None
    parsed_scope: Optional[str] = None
    parsed_description: Optional[str] = None
    is_breaking: bool = False


def validate(message: str) -> ValidationResult:
    """Validate a commit message against the Conventional Commits spec.

    Checks:
    1. Matches conventional commit format
    2. Type is one of the standard types
    3. Description starts with lowercase
    4. No trailing period in subject line
    5. Subject line length <= 72 characters
    6. Scope is a single word (no spaces)
    """
    result = ValidationResult(is_valid=True)

    if not message or not message.strip():
        result.is_valid = False
        result.issues.append(ValidationIssue(
            level="error",
            message="Commit message is empty",
        ))
        return result

    # Split into subject and body
    lines = message.strip().split("\n")
    subject = lines[0].strip()
    body = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

    # Check basic format
    match = CONVENTIONAL_PATTERN.match(subject)

    if not match:
        result.is_valid = False
        result.issues.append(ValidationIssue(
            level="error",
            message="Does not match conventional commit format: type(scope): description",
            suggestion="Example: feat(auth): add login endpoint",
        ))

        # Try to suggest fixes
        _suggest_fixes(subject, result)
        return result

    commit_type = match.group("type")
    scope = match.group("scope")
    breaking = match.group("breaking")
    description = match.group("description")

    result.parsed_type = commit_type
    result.parsed_scope = scope
    result.parsed_description = description
    result.is_breaking = breaking == "!"

    # Validate type
    if commit_type not in VALID_TYPES:
        result.is_valid = False
        result.issues.append(ValidationIssue(
            level="error",
            message=f"Unknown type '{commit_type}'",
            suggestion=f"Valid types: {', '.join(sorted(VALID_TYPES))}",
        ))

    # Validate description
    if not description:
        result.is_valid = False
        result.issues.append(ValidationIssue(
            level="error",
            message="Description is empty",
        ))
    else:
        # Should start with lowercase
        if description[0].isupper():
            result.issues.append(ValidationIssue(
                level="warning",
                message="Description should start with lowercase",
                suggestion=f"'{description[0].lower()}{description[1:]}'",
            ))

        # No trailing period
        if description.endswith("."):
            result.issues.append(ValidationIssue(
                level="warning",
                message="Description should not end with a period",
                suggestion=f"'{description[:-1]}'",
            ))

    # Subject line length
    if len(subject) > 72:
        result.issues.append(ValidationIssue(
            level="warning",
            message=f"Subject line is {len(subject)} chars (max recommended: 72)",
            suggestion="Move details to the commit body",
        ))

    # Scope validation
    if scope and " " in scope:
        result.issues.append(ValidationIssue(
            level="warning",
            message=f"Scope should not contain spaces: '{scope}'",
            suggestion=f"Use '{scope.replace(' ', '-')}' instead",
        ))

    # Body formatting
    if body:
        body_lines = body.split("\n")
        if body_lines and body_lines[0].strip():
            # Should have blank line between subject and body
            if lines[1].strip():
                result.issues.append(ValidationIssue(
                    level="warning",
                    message="Add a blank line between subject and body",
                ))

    return result


def _suggest_fixes(subject: str, result: ValidationResult) -> None:
    """Try to suggest fixes for non-conforming messages."""

    # Missing colon after type
    for t in VALID_TYPES:
        if subject.lower().startswith(t + " "):
            result.issues.append(ValidationIssue(
                level="error",
                message=f"Missing colon after type",
                suggestion=f"{t}: {subject[len(t) + 1:]}",
            ))
            return

    # Capitalized type
    m = re.match(r"^([A-Z][a-z]+)(\(.+?\))?:\s+(.+)$", subject)
    if m:
        result.issues.append(ValidationIssue(
            level="error",
            message="Type must be lowercase",
            suggestion=f"{m.group(1).lower()}{m.group(2) or ''}: {m.group(3)}",
        ))
        return

    # No type at all
    if not any(subject.lower().startswith(t) for t in VALID_TYPES):
        result.issues.append(ValidationIssue(
            level="error",
            message="Message must start with a valid type",
            suggestion=f"feat: {subject}",
        ))


def fix_message(message: str) -> str:
    """Attempt to auto-fix common conventional commit issues.

    Returns the fixed message, or the original if unfixable.
    """
    subject = message.strip().split("\n")[0]

    # Try to match
    m = CONVENTIONAL_PATTERN.match(subject)
    if m:
        # Already valid format, just fix minor issues
        commit_type = m.group("type")
        scope = m.group("scope")
        breaking = m.group("breaking") or ""
        description = m.group("description")

        # Fix description casing
        if description and description[0].isupper():
            description = description[0].lower() + description[1:]

        # Remove trailing period
        description = description.rstrip(".")

        if scope:
            return f"{commit_type}({scope}){breaking}: {description}"
        return f"{commit_type}{breaking}: {description}"

    # Try common fixes
    for t in VALID_TYPES:
        # Missing colon
        if subject.lower().startswith(t + " "):
            rest = subject[len(t) + 1:]
            return f"{t}: {rest}"

        # Capitalized type
        if subject.lower().startswith(t):
            rest = subject[len(t):]
            return f"{t}{rest}"

    # Last resort: wrap as chore
    return f"chore: {subject}"
