from __future__ import annotations

from pathlib import Path
import sys

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / ".codex" / "skills"


def main() -> int:
    errors: list[str] = []

    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        errors.extend(validate_skill(skill_dir))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Repository validation passed.")
    return 0


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_file = skill_dir / "SKILL.md"
    agents_file = skill_dir / "agents" / "openai.yaml"

    if not skill_file.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    frontmatter = load_frontmatter(skill_file)
    if not isinstance(frontmatter, dict):
        errors.append(f"{skill_dir.name}: invalid SKILL.md frontmatter")
        return errors

    name = frontmatter.get("name")
    description = frontmatter.get("description")

    if name != skill_dir.name:
        errors.append(f"{skill_dir.name}: frontmatter name must match folder name")
    if not description or not isinstance(description, str):
        errors.append(f"{skill_dir.name}: description is required")

    if not agents_file.exists():
        errors.append(f"{skill_dir.name}: missing agents/openai.yaml")
        return errors

    agents_data = yaml.safe_load(agents_file.read_text(encoding="utf-8"))
    interface = agents_data.get("interface", {}) if isinstance(agents_data, dict) else {}
    default_prompt = interface.get("default_prompt")
    short_description = interface.get("short_description")

    if not default_prompt or f"${skill_dir.name}" not in default_prompt:
        errors.append(f"{skill_dir.name}: default_prompt must mention ${skill_dir.name}")
    if not short_description or not isinstance(short_description, str):
        errors.append(f"{skill_dir.name}: short_description is required")

    return errors


def load_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    _, _, remainder = text.partition("---\n")
    frontmatter_text, _, _ = remainder.partition("\n---")
    return yaml.safe_load(frontmatter_text)


if __name__ == "__main__":
    raise SystemExit(main())
