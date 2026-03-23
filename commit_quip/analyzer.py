"""Analyze staged git changes to detect commit type and scope."""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class FileChange:
    """A single staged file change."""
    status: str        # A (added), M (modified), D (deleted), R (renamed)
    filepath: str
    old_filepath: Optional[str] = None  # for renames
    additions: int = 0
    deletions: int = 0

    @property
    def extension(self) -> str:
        return Path(self.filepath).suffix.lstrip(".")

    @property
    def directory(self) -> str:
        parts = Path(self.filepath).parts
        if len(parts) > 1:
            return parts[0]
        return ""

    @property
    def filename(self) -> str:
        return Path(self.filepath).name


@dataclass
class ChangeAnalysis:
    """Analysis result for staged changes."""
    commit_type: str                    # feat, fix, refactor, docs, test, chore, style, perf, ci, build
    scope: Optional[str] = None         # detected scope (module/directory)
    description: str = ""               # short description of changes
    files: List[FileChange] = field(default_factory=list)
    affected_modules: Set[str] = field(default_factory=set)
    is_breaking: bool = False
    confidence: float = 0.0             # 0-1 how confident we are in the type

    @property
    def total_additions(self) -> int:
        return sum(f.additions for f in self.files)

    @property
    def total_deletions(self) -> int:
        return sum(f.deletions for f in self.files)

    @property
    def total_files(self) -> int:
        return len(self.files)


# File patterns for type detection
TYPE_PATTERNS: Dict[str, List[str]] = {
    "test": [
        r"test[_s]?/", r"__tests__/", r"\.test\.", r"\.spec\.",
        r"test_\w+\.py", r"\w+_test\.go", r"tests\.py",
    ],
    "docs": [
        r"\.md$", r"\.rst$", r"\.txt$", r"docs?/", r"README",
        r"CHANGELOG", r"LICENSE", r"CONTRIBUTING", r"\.adoc$",
    ],
    "ci": [
        r"\.github/workflows/", r"\.gitlab-ci", r"Jenkinsfile",
        r"\.circleci/", r"\.travis\.yml", r"azure-pipelines",
        r"\.drone\.yml", r"bitbucket-pipelines",
    ],
    "build": [
        r"Dockerfile", r"docker-compose", r"Makefile", r"CMakeLists",
        r"setup\.py", r"setup\.cfg", r"pyproject\.toml", r"package\.json",
        r"go\.mod", r"go\.sum", r"Cargo\.toml", r"pom\.xml",
        r"build\.gradle", r"\.gemspec", r"requirements.*\.txt",
    ],
    "style": [
        r"\.css$", r"\.scss$", r"\.less$", r"\.styled\.",
        r"\.prettierrc", r"\.eslintrc", r"\.stylelintrc",
        r"\.editorconfig",
    ],
    "chore": [
        r"\.gitignore", r"\.env\.example", r"\.npmrc",
        r"\.nvmrc", r"\.tool-versions", r"\.husky/",
    ],
}


def get_staged_changes() -> List[FileChange]:
    """Get the list of staged changes from git."""
    try:
        # Get staged file list with status
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-status"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            return []

        files: List[FileChange] = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            parts = line.split("\t")
            status = parts[0][0]  # First char: A, M, D, R
            filepath = parts[-1]
            old_path = parts[1] if len(parts) > 2 else None

            files.append(FileChange(
                status=status,
                filepath=filepath,
                old_filepath=old_path,
            ))

        # Get addition/deletion counts
        stat_result = subprocess.run(
            ["git", "diff", "--cached", "--numstat"],
            capture_output=True, text=True,
        )
        if stat_result.returncode == 0:
            stat_map: Dict[str, Tuple[int, int]] = {}
            for line in stat_result.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                parts = line.split("\t")
                if len(parts) >= 3:
                    adds = int(parts[0]) if parts[0] != "-" else 0
                    dels = int(parts[1]) if parts[1] != "-" else 0
                    stat_map[parts[2]] = (adds, dels)

            for fc in files:
                if fc.filepath in stat_map:
                    fc.additions, fc.deletions = stat_map[fc.filepath]

        return files

    except FileNotFoundError:
        return []


def analyze_changes(files: Optional[List[FileChange]] = None) -> ChangeAnalysis:
    """Analyze staged changes to determine commit type and scope.

    If files is None, reads from git staging area.
    """
    if files is None:
        files = get_staged_changes()

    if not files:
        return ChangeAnalysis(
            commit_type="chore",
            description="no staged changes detected",
            confidence=0.0,
        )

    # Detect type from file patterns
    type_scores: Dict[str, float] = {
        "feat": 0, "fix": 0, "refactor": 0, "docs": 0,
        "test": 0, "chore": 0, "style": 0, "perf": 0,
        "ci": 0, "build": 0,
    }

    modules: Set[str] = set()

    for fc in files:
        path = fc.filepath.lower()
        module = fc.directory
        if module:
            modules.add(module)

        # Pattern matching
        for ctype, patterns in TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, path, re.IGNORECASE):
                    type_scores[ctype] += 1
                    break

        # Heuristics based on file status
        if fc.status == "A":
            type_scores["feat"] += 0.5
        elif fc.status == "D":
            type_scores["refactor"] += 0.3
            type_scores["chore"] += 0.3
        elif fc.status == "M":
            # Check diff content for clues
            type_scores["feat"] += 0.2
            type_scores["fix"] += 0.2

    # Get diff content for additional analysis
    diff_clues = _analyze_diff_content()
    for ctype, score in diff_clues.items():
        type_scores[ctype] = type_scores.get(ctype, 0) + score

    # Find best type
    best_type = max(type_scores, key=type_scores.get)
    best_score = type_scores[best_type]

    # If no strong signal, default based on change pattern
    if best_score < 0.5:
        if all(f.status == "A" for f in files):
            best_type = "feat"
        elif len(files) == 1 and files[0].status == "M":
            best_type = "fix"
        else:
            best_type = "chore"

    confidence = min(best_score / max(len(files), 1), 1.0)

    # Detect scope
    scope = _detect_scope(files, modules)

    # Generate description
    description = _generate_description(files, best_type)

    # Check for breaking changes
    is_breaking = _check_breaking(files)

    return ChangeAnalysis(
        commit_type=best_type,
        scope=scope,
        description=description,
        files=files,
        affected_modules=modules,
        is_breaking=is_breaking,
        confidence=confidence,
    )


def _analyze_diff_content() -> Dict[str, float]:
    """Analyze the diff content for type clues."""
    scores: Dict[str, float] = {}

    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "-U0"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            return scores

        diff = result.stdout.lower()

        # Fix indicators
        fix_words = ["fix", "bug", "patch", "resolve", "issue", "error", "crash", "broken"]
        fix_count = sum(diff.count(w) for w in fix_words)
        if fix_count > 0:
            scores["fix"] = min(fix_count * 0.3, 2.0)

        # Performance indicators
        perf_words = ["performance", "optimize", "cache", "speed", "fast", "slow", "memory"]
        perf_count = sum(diff.count(w) for w in perf_words)
        if perf_count > 0:
            scores["perf"] = min(perf_count * 0.3, 1.5)

        # Refactor indicators
        refactor_words = ["refactor", "rename", "extract", "reorganize", "simplify", "cleanup"]
        refactor_count = sum(diff.count(w) for w in refactor_words)
        if refactor_count > 0:
            scores["refactor"] = min(refactor_count * 0.3, 1.5)

    except FileNotFoundError:
        pass

    return scores


def _detect_scope(files: List[FileChange], modules: Set[str]) -> Optional[str]:
    """Detect the scope from file paths."""
    if not files:
        return None

    # Single file -> use directory or filename
    if len(files) == 1:
        fc = files[0]
        parts = Path(fc.filepath).parts
        if len(parts) > 1:
            # Use first meaningful directory
            for part in parts:
                if part not in ("src", "lib", "app", "pkg", "internal", "cmd"):
                    return part
            return parts[0]
        return Path(fc.filepath).stem

    # Multiple files in same directory
    dirs = set(Path(f.filepath).parent.as_posix() for f in files)
    if len(dirs) == 1:
        dir_parts = list(Path(list(dirs)[0]).parts)
        if dir_parts:
            for part in dir_parts:
                if part not in ("src", "lib", "app", ".", ""):
                    return part

    # Common parent directory
    if modules and len(modules) == 1:
        return modules.pop()

    # Multiple modules
    if len(modules) <= 3:
        return ",".join(sorted(modules))

    return None


def _generate_description(files: List[FileChange], commit_type: str) -> str:
    """Generate a short description of the changes."""
    if len(files) == 1:
        fc = files[0]
        action = {"A": "add", "M": "update", "D": "remove", "R": "rename"}.get(fc.status, "modify")
        return f"{action} {fc.filename}"

    # Group by status
    added = [f for f in files if f.status == "A"]
    modified = [f for f in files if f.status == "M"]
    deleted = [f for f in files if f.status == "D"]

    parts = []
    if added:
        parts.append(f"add {len(added)} file(s)")
    if modified:
        parts.append(f"update {len(modified)} file(s)")
    if deleted:
        parts.append(f"remove {len(deleted)} file(s)")

    return ", ".join(parts)


def _check_breaking(files: List[FileChange]) -> bool:
    """Check if changes might be breaking."""
    for fc in files:
        name = fc.filename.lower()
        if name in ("breaking.md", "migration.md"):
            return True
        # Large deletions in public API files
        if fc.deletions > 20 and any(
            keyword in fc.filepath.lower()
            for keyword in ("api", "public", "interface", "types", "schema")
        ):
            return True

    return False
