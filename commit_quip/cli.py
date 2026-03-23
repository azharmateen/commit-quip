"""Click CLI for commit-quip."""

from __future__ import annotations

import sys

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from .analyzer import analyze_changes
from .generator import generate, generate_all_styles
from .validator import validate, fix_message
from .hook import install_hook, uninstall_hook, set_style, get_style
from .templates import get_available_styles

console = Console()


@click.group(invoke_without_command=True)
@click.option("--style", "-s", default=None,
              type=click.Choice(["professional", "funny", "pirate", "shakespeare", "emoji", "minimal"]),
              help="Message personality style.")
@click.option("--count", "-n", default=3, help="Number of suggestions.")
@click.pass_context
@click.version_option(version="1.0.0", prog_name="commit-quip")
def main(ctx, style, count):
    """Witty commit message generator with conventional commits.

    Run without a subcommand for interactive mode.
    """
    if ctx.invoked_subcommand is not None:
        return

    # Interactive mode
    if style is None:
        style = get_style()

    analysis = analyze_changes()

    if not analysis.files:
        console.print("[yellow]No staged changes detected.[/yellow]")
        console.print("[dim]Stage some changes with 'git add' first.[/dim]")
        return

    # Show analysis
    console.print(f"\n[bold]Detected:[/bold] {analysis.commit_type}", end="")
    if analysis.scope:
        console.print(f"({analysis.scope})", end="")
    console.print(f" - {analysis.description}")
    console.print(f"[dim]Files: {analysis.total_files} | "
                  f"+{analysis.total_additions} -{analysis.total_deletions} | "
                  f"Confidence: {analysis.confidence:.0%}[/dim]")

    if analysis.is_breaking:
        console.print("[bold red]BREAKING CHANGE detected[/bold red]")

    # Generate suggestions
    suggestions = generate(style=style, analysis=analysis, count=count)

    console.print(f"\n[bold]Suggestions ({style}):[/bold]")
    for i, suggestion in enumerate(suggestions):
        console.print(f"  [cyan]{i + 1}.[/cyan] {suggestion.message}")

    # Interactive selection
    console.print(f"\n[dim]Choose 1-{len(suggestions)}, or 'a' for all styles, 'e' to edit, 'q' to quit:[/dim]")

    while True:
        choice = console.input("[bold]> [/bold]").strip().lower()

        if choice == "q":
            return
        elif choice == "a":
            _show_all_styles(analysis)
            continue
        elif choice == "e":
            msg = console.input("[bold]Enter message: [/bold]").strip()
            if msg:
                _validate_and_show(msg)
            continue
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(suggestions):
                msg = suggestions[idx].message
                console.print(f"\n[green]Selected:[/green] {msg}")
                # Copy to clipboard if available
                _try_copy(msg)
                return
        else:
            console.print("[red]Invalid choice.[/red]")


@main.command()
@click.option("--style", "-s", default=None,
              type=click.Choice(["professional", "funny", "pirate", "shakespeare", "emoji", "minimal"]))
@click.option("--count", "-n", default=3, help="Number of suggestions.")
@click.option("--first-only", is_flag=True, help="Print only the first suggestion (for scripts).")
def generate_cmd(style, count, first_only):
    """Generate commit message suggestions (non-interactive)."""
    if style is None:
        style = get_style()

    analysis = analyze_changes()
    suggestions = generate(style=style, analysis=analysis, count=count)

    if first_only:
        if suggestions:
            click.echo(suggestions[0].message)
    else:
        for s in suggestions:
            click.echo(s.message)


generate_cmd.name = "generate"


@main.command()
@click.argument("message")
def validate_cmd(message):
    """Validate a commit message against conventional commit spec."""
    result = validate(message)

    if result.is_valid:
        console.print(f"[green]Valid conventional commit[/green]")
        console.print(f"  Type: {result.parsed_type}")
        if result.parsed_scope:
            console.print(f"  Scope: {result.parsed_scope}")
        console.print(f"  Description: {result.parsed_description}")
        if result.is_breaking:
            console.print(f"  [red]BREAKING CHANGE[/red]")
    else:
        console.print("[red]Invalid conventional commit[/red]")

    if result.issues:
        for issue in result.issues:
            style = "red" if issue.level == "error" else "yellow"
            console.print(f"  [{style}]{issue.level.upper()}:[/{style}] {issue.message}")
            if issue.suggestion:
                console.print(f"    [dim]Suggestion: {issue.suggestion}[/dim]")

    # Try to fix
    if not result.is_valid:
        fixed = fix_message(message)
        if fixed != message:
            console.print(f"\n[cyan]Auto-fixed:[/cyan] {fixed}")

    sys.exit(0 if result.is_valid else 1)


validate_cmd.name = "validate"


@main.command()
def styles():
    """Show all available message styles with examples."""
    analysis = analyze_changes()

    if not analysis.files:
        # Use a sample analysis for demo
        from .analyzer import ChangeAnalysis, FileChange
        analysis = ChangeAnalysis(
            commit_type="feat",
            scope="auth",
            description="add login endpoint",
            confidence=0.8,
        )

    all_styles = generate_all_styles(analysis)

    table = Table(title="Available Styles")
    table.add_column("Style", style="cyan", width=14)
    table.add_column("Example Message", min_width=50)

    for style_name, msg in all_styles.items():
        table.add_row(style_name, msg)

    console.print(table)


@main.group()
def hook():
    """Manage git hook integration."""
    pass


@hook.command()
def install():
    """Install the prepare-commit-msg git hook."""
    result = install_hook()
    console.print(result)


@hook.command()
def uninstall():
    """Remove the prepare-commit-msg git hook."""
    result = uninstall_hook()
    console.print(result)


@hook.command("set-style")
@click.argument("style",
                type=click.Choice(["professional", "funny", "pirate", "shakespeare", "emoji", "minimal"]))
def hook_set_style(style):
    """Set the default style for the git hook."""
    result = set_style(style)
    console.print(result)


@hook.command("get-style")
def hook_get_style():
    """Show the current default style."""
    current = get_style()
    console.print(f"Current style: [bold]{current}[/bold]")


def _show_all_styles(analysis):
    """Show one example from each style."""
    all_styles = generate_all_styles(analysis)
    console.print()
    for style_name, msg in all_styles.items():
        console.print(f"  [cyan]{style_name:14s}[/cyan] {msg}")
    console.print()


def _validate_and_show(message):
    """Validate and display a message."""
    result = validate(message)
    if result.is_valid:
        console.print(f"  [green]Valid[/green]: {message}")
    else:
        console.print(f"  [red]Invalid[/red]: {message}")
        for issue in result.issues:
            console.print(f"    {issue.message}")
        fixed = fix_message(message)
        if fixed != message:
            console.print(f"  [cyan]Fixed[/cyan]: {fixed}")


def _try_copy(text):
    """Try to copy text to clipboard."""
    try:
        import subprocess
        proc = subprocess.run(
            ["pbcopy"] if sys.platform == "darwin" else ["xclip", "-selection", "clipboard"],
            input=text.encode(), capture_output=True,
        )
        if proc.returncode == 0:
            console.print("[dim]Copied to clipboard.[/dim]")
    except FileNotFoundError:
        pass


if __name__ == "__main__":
    main()
