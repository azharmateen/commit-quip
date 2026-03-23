# commit-quip

Witty commit message generator that enforces conventional commits with personality. Analyzes your staged changes, detects the commit type, and suggests messages in 6 different styles -- all offline, no AI required.

## Features

- **Auto-detection**: Analyzes staged files to determine commit type (feat, fix, refactor, docs, test, etc.) and scope
- **6 Personality styles**: Professional, Funny, Pirate, Shakespeare, Emoji, Minimal
- **200+ templates**: Rich template library per type and style
- **Conventional commit validation**: Validates messages against the spec, suggests fixes
- **Git hook**: Install as prepare-commit-msg hook for seamless workflow
- **Breaking change detection**: Automatically flags potential breaking changes

## Installation

```bash
pip install -e .
```

## Usage

### Interactive mode (default)

```bash
# Stage your changes first
git add .

# Run commit-quip
commit-quip
commit-quip --style funny
commit-quip --style pirate --count 5
```

### Generate (non-interactive)

```bash
commit-quip generate --style shakespeare
commit-quip generate --first-only  # single message, good for scripts
```

### Validate a message

```bash
commit-quip validate "feat(auth): add login endpoint"
commit-quip validate "Updated the thing"  # will suggest fixes
```

### Browse styles

```bash
commit-quip styles
```

### Git hook

```bash
commit-quip hook install      # adds prepare-commit-msg hook
commit-quip hook uninstall    # removes the hook
commit-quip hook set-style funny  # set default style
commit-quip hook get-style
```

## Styles

| Style | Example |
|-------|---------|
| professional | `feat(auth): add login endpoint` |
| funny | `feat(auth): auth just entered the chat` |
| pirate | `feat(auth): plunder new auth from the feature seas` |
| shakespeare | `feat(auth): bestow upon thy server the gift of auth` |
| emoji | `feat(auth): introduce auth` |
| minimal | `feat(auth): add login endpoint` |

## Commit Types

| Type | When to use |
|------|------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation changes |
| `style` | Formatting, CSS, linting |
| `refactor` | Code restructuring (no feature/fix) |
| `perf` | Performance improvement |
| `test` | Adding/updating tests |
| `build` | Build system, dependencies |
| `ci` | CI/CD configuration |
| `chore` | Maintenance tasks |

## License

MIT
