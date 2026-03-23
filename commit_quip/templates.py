"""Message templates per style and commit type. 200+ templates, no AI needed."""

from __future__ import annotations

import random
from typing import Dict, List


# Template format: {scope} is replaced with the detected scope,
# {desc} with the description. If scope is None, the (scope) part is omitted.

TEMPLATES: Dict[str, Dict[str, List[str]]] = {
    # ─── PROFESSIONAL ───────────────────────────────────
    "professional": {
        "feat": [
            "feat({scope}): implement {desc}",
            "feat({scope}): add {desc}",
            "feat({scope}): introduce {desc}",
            "feat({scope}): add support for {desc}",
            "feat({scope}): enable {desc}",
            "feat({scope}): create {desc} functionality",
        ],
        "fix": [
            "fix({scope}): resolve {desc}",
            "fix({scope}): correct {desc}",
            "fix({scope}): address {desc}",
            "fix({scope}): patch {desc}",
            "fix({scope}): repair {desc}",
            "fix({scope}): rectify {desc} issue",
        ],
        "refactor": [
            "refactor({scope}): restructure {desc}",
            "refactor({scope}): simplify {desc}",
            "refactor({scope}): improve {desc} architecture",
            "refactor({scope}): clean up {desc}",
            "refactor({scope}): reorganize {desc}",
            "refactor({scope}): extract {desc} into separate module",
        ],
        "docs": [
            "docs({scope}): update {desc}",
            "docs({scope}): add documentation for {desc}",
            "docs({scope}): clarify {desc}",
            "docs({scope}): improve {desc} documentation",
            "docs({scope}): document {desc}",
        ],
        "test": [
            "test({scope}): add tests for {desc}",
            "test({scope}): improve test coverage for {desc}",
            "test({scope}): add unit tests for {desc}",
            "test({scope}): verify {desc}",
            "test({scope}): add integration tests for {desc}",
        ],
        "chore": [
            "chore({scope}): update {desc}",
            "chore({scope}): maintain {desc}",
            "chore({scope}): configure {desc}",
            "chore({scope}): update dependencies for {desc}",
            "chore({scope}): clean up {desc}",
        ],
        "style": [
            "style({scope}): format {desc}",
            "style({scope}): apply consistent formatting to {desc}",
            "style({scope}): fix linting issues in {desc}",
            "style({scope}): standardize code style in {desc}",
        ],
        "perf": [
            "perf({scope}): optimize {desc}",
            "perf({scope}): improve performance of {desc}",
            "perf({scope}): reduce latency in {desc}",
            "perf({scope}): speed up {desc}",
        ],
        "ci": [
            "ci({scope}): update {desc}",
            "ci({scope}): configure {desc}",
            "ci({scope}): add {desc} pipeline",
            "ci({scope}): fix {desc} workflow",
        ],
        "build": [
            "build({scope}): update {desc}",
            "build({scope}): configure {desc}",
            "build({scope}): upgrade {desc}",
            "build({scope}): add {desc} to build system",
        ],
    },

    # ─── FUNNY ──────────────────────────────────────────
    "funny": {
        "feat": [
            "feat({scope}): teach the app a new trick - {desc}",
            "feat({scope}): drop {desc} like it's hot",
            "feat({scope}): summon {desc} from the feature factory",
            "feat({scope}): {desc} just entered the chat",
            "feat({scope}): level up with {desc}",
            "feat({scope}): unwrap the shiny new {desc}",
            "feat({scope}): {desc} has been unlocked, achievement earned",
        ],
        "fix": [
            "fix({scope}): put a band-aid on {desc}",
            "fix({scope}): patch the {desc} black hole that swallowed user sessions",
            "fix({scope}): stop {desc} from being drunk on a Tuesday",
            "fix({scope}): convince {desc} to behave like an adult",
            "fix({scope}): bribe {desc} into working correctly",
            "fix({scope}): {desc} was on a coffee break, dragged it back",
            "fix({scope}): {desc} had one job... now it does it",
        ],
        "refactor": [
            "refactor({scope}): give {desc} a well-deserved makeover",
            "refactor({scope}): {desc} goes to the spa for deep cleansing",
            "refactor({scope}): Marie Kondo would be proud of {desc}",
            "refactor({scope}): reorganize {desc} so future-me doesn't cry",
            "refactor({scope}): untangle the spaghetti in {desc}",
            "refactor({scope}): {desc} before vs after looks like a glow-up",
        ],
        "docs": [
            "docs({scope}): explain {desc} like I'm five",
            "docs({scope}): add a love letter to future developers about {desc}",
            "docs({scope}): document {desc} so aliens can understand it",
            "docs({scope}): write the README that {desc} always deserved",
            "docs({scope}): {desc} now comes with instructions, revolutionary",
        ],
        "test": [
            "test({scope}): poke {desc} with a stick to see if it flinches",
            "test({scope}): add trust issues for {desc}",
            "test({scope}): interrogate {desc} until it confesses",
            "test({scope}): make sure {desc} doesn't secretly plot world domination",
            "test({scope}): {desc} must prove its innocence in court",
        ],
        "chore": [
            "chore({scope}): take out the {desc} trash",
            "chore({scope}): do the dishes in {desc}",
            "chore({scope}): sweep {desc} under the... wait, clean it properly",
            "chore({scope}): {desc} housekeeping, no one notices but everyone benefits",
            "chore({scope}): feed the {desc} hamster that runs our infra",
        ],
        "style": [
            "style({scope}): dress up {desc} for the prom",
            "style({scope}): {desc} gets a haircut and a fresh outfit",
            "style({scope}): the linter said {desc} was ugly, so we fixed that",
            "style({scope}): {desc} now looks like it was written by a professional",
        ],
        "perf": [
            "perf({scope}): feed {desc} some energy drinks",
            "perf({scope}): strap a rocket to {desc}",
            "perf({scope}): {desc} went from turtle to cheetah",
            "perf({scope}): remove the speed bumps from {desc}",
        ],
        "ci": [
            "ci({scope}): teach the robots about {desc}",
            "ci({scope}): automate {desc} because humans are unreliable",
            "ci({scope}): {desc} pipeline is now self-aware (jk, just faster)",
        ],
        "build": [
            "build({scope}): oil the gears in {desc}",
            "build({scope}): {desc} build system now sparks joy",
            "build({scope}): upgrade {desc} because npm said so",
        ],
    },

    # ─── PIRATE ─────────────────────────────────────────
    "pirate": {
        "feat": [
            "feat({scope}): hoist the sails, {desc} be on the horizon",
            "feat({scope}): plunder new {desc} from the feature seas",
            "feat({scope}): bury the treasure of {desc} in the codebase",
            "feat({scope}): commandeer {desc} for our fleet, arr",
            "feat({scope}): chart a course for {desc}, ye scallywags",
        ],
        "fix": [
            "fix({scope}): patch the hull where {desc} be leakin'",
            "fix({scope}): keelhaul the bug in {desc}, send it to Davy Jones",
            "fix({scope}): repair {desc} before the ship sinks",
            "fix({scope}): the {desc} kraken has been slain, yer welcome",
            "fix({scope}): {desc} tried to mutiny, we set it straight",
        ],
        "refactor": [
            "refactor({scope}): swab the deck of {desc}",
            "refactor({scope}): rearrange the cargo hold of {desc}",
            "refactor({scope}): chart a better course through {desc}",
        ],
        "docs": [
            "docs({scope}): update the ship's log for {desc}",
            "docs({scope}): scribble the map for {desc} so no one gets lost",
            "docs({scope}): engrave {desc} on the captain's scroll",
        ],
        "test": [
            "test({scope}): make {desc} walk the plank to prove its worth",
            "test({scope}): send {desc} to Davy Jones if it fails",
            "test({scope}): interrogate {desc} like a captured spy",
        ],
        "chore": [
            "chore({scope}): polish the cannons of {desc}",
            "chore({scope}): restock the rum for {desc}",
            "chore({scope}): tidy the captain's quarters of {desc}",
        ],
        "style": [
            "style({scope}): dress {desc} in proper pirate garb",
            "style({scope}): raise the Jolly Roger over {desc}",
        ],
        "perf": [
            "perf({scope}): add more wind to {desc}'s sails",
            "perf({scope}): lighten the ballast in {desc}",
        ],
        "ci": [
            "ci({scope}): train the parrots to automate {desc}",
        ],
        "build": [
            "build({scope}): reinforce the mast of {desc}",
        ],
    },

    # ─── SHAKESPEARE ────────────────────────────────────
    "shakespeare": {
        "feat": [
            "feat({scope}): bestow upon thy server the gift of {desc}",
            "feat({scope}): lo, {desc} doth grace our humble codebase",
            "feat({scope}): hark, a new {desc} emerges from the digital ether",
            "feat({scope}): 'twas but a dream, now {desc} lives and breathes",
            "feat({scope}): to {desc} or not to {desc}, that is no longer the question",
        ],
        "fix": [
            "fix({scope}): mend the broken heart of {desc}",
            "fix({scope}): alas, poor {desc}, we knew it was broken",
            "fix({scope}): vanquish the foul demon plaguing {desc}",
            "fix({scope}): the tragedy of {desc} hath been averted",
            "fix({scope}): {desc} hath been cured of its ailments",
        ],
        "refactor": [
            "refactor({scope}): {desc} emerges anew, like a phoenix from the ashes",
            "refactor({scope}): give {desc} a soliloquy of clarity",
            "refactor({scope}): untangle the web of deceit woven by {desc}",
        ],
        "docs": [
            "docs({scope}): pen the definitive chronicle of {desc}",
            "docs({scope}): inscribe the wisdom of {desc} for future generations",
            "docs({scope}): compose a sonnet explaining {desc}",
        ],
        "test": [
            "test({scope}): put {desc} on trial before the royal court",
            "test({scope}): summon {desc} to prove its honor",
            "test({scope}): question the very essence of {desc}",
        ],
        "chore": [
            "chore({scope}): attend to the mundane affairs of {desc}",
            "chore({scope}): {desc} receives its quarterly grooming",
        ],
        "style": [
            "style({scope}): adorn {desc} in its finest vestments",
        ],
        "perf": [
            "perf({scope}): grant {desc} the swiftness of Mercury",
            "perf({scope}): unburden {desc} of its mortal sluggishness",
        ],
        "ci": [
            "ci({scope}): command the mechanical servants to tend {desc}",
        ],
        "build": [
            "build({scope}): fortify the castle walls of {desc}",
        ],
    },

    # ─── EMOJI ──────────────────────────────────────────
    "emoji": {
        "feat": [
            "feat({scope}): add {desc}",
            "feat({scope}): introduce {desc}",
            "feat({scope}): launch {desc}",
        ],
        "fix": [
            "fix({scope}): squash bug in {desc}",
            "fix({scope}): resolve {desc}",
            "fix({scope}): patch {desc}",
        ],
        "refactor": [
            "refactor({scope}): clean up {desc}",
            "refactor({scope}): restructure {desc}",
        ],
        "docs": [
            "docs({scope}): update {desc}",
            "docs({scope}): add docs for {desc}",
        ],
        "test": [
            "test({scope}): add tests for {desc}",
            "test({scope}): verify {desc}",
        ],
        "chore": [
            "chore({scope}): update {desc}",
            "chore({scope}): maintain {desc}",
        ],
        "style": [
            "style({scope}): format {desc}",
        ],
        "perf": [
            "perf({scope}): optimize {desc}",
        ],
        "ci": [
            "ci({scope}): update {desc}",
        ],
        "build": [
            "build({scope}): update {desc}",
        ],
    },

    # ─── MINIMAL ────────────────────────────────────────
    "minimal": {
        "feat": [
            "feat({scope}): {desc}",
        ],
        "fix": [
            "fix({scope}): {desc}",
        ],
        "refactor": [
            "refactor({scope}): {desc}",
        ],
        "docs": [
            "docs({scope}): {desc}",
        ],
        "test": [
            "test({scope}): {desc}",
        ],
        "chore": [
            "chore({scope}): {desc}",
        ],
        "style": [
            "style({scope}): {desc}",
        ],
        "perf": [
            "perf({scope}): {desc}",
        ],
        "ci": [
            "ci({scope}): {desc}",
        ],
        "build": [
            "build({scope}): {desc}",
        ],
    },
}

# Emoji prefixes per type
EMOJI_MAP = {
    "feat": "sparkles",
    "fix": "bug",
    "refactor": "recycle",
    "docs": "memo",
    "test": "white_check_mark",
    "chore": "wrench",
    "style": "art",
    "perf": "zap",
    "ci": "construction_worker",
    "build": "hammer",
}


def get_available_styles() -> List[str]:
    """Return list of available styles."""
    return list(TEMPLATES.keys())


def get_template(commit_type: str, style: str = "professional",
                 scope: str | None = None,
                 description: str = "changes") -> str:
    """Get a random template for the given type and style.

    Args:
        commit_type: The conventional commit type.
        style: The personality style.
        scope: Optional scope (module/directory).
        description: Short description of changes.

    Returns:
        A formatted commit message.
    """
    style_templates = TEMPLATES.get(style, TEMPLATES["professional"])
    type_templates = style_templates.get(commit_type, style_templates.get("chore", ["chore: {desc}"]))

    template = random.choice(type_templates)

    # Format scope
    if scope:
        message = template.replace("{scope}", scope).replace("{desc}", description)
    else:
        # Remove (scope) part
        message = template.replace("({scope})", "").replace("{desc}", description)
        # Clean up double spaces
        message = message.replace("  ", " ")

    return message


def get_multiple_suggestions(commit_type: str, style: str = "professional",
                             scope: str | None = None,
                             description: str = "changes",
                             count: int = 3) -> List[str]:
    """Get multiple unique message suggestions."""
    seen = set()
    results: List[str] = []
    attempts = 0

    while len(results) < count and attempts < count * 5:
        msg = get_template(commit_type, style, scope, description)
        if msg not in seen:
            seen.add(msg)
            results.append(msg)
        attempts += 1

    return results
