from __future__ import annotations

from argparse import ArgumentParser
from datetime import date
from pathlib import Path
import json
import re


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "session-summary"


def render_frontmatter(title: str) -> str:
    today = date.today().isoformat()
    return (
        "---\n"
        f"title: {title}\n"
        "source_type: session\n"
        f"captured_at: {today}\n"
        "scope: project\n"
        "---\n\n"
    )


def main() -> int:
    parser = ArgumentParser(description="Create a raw project KMS session note from a content file.")
    parser.add_argument("--project-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--title", required=True)
    parser.add_argument("--content-file", required=True)
    parser.add_argument("--slug")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    kms_config = json.loads((project_dir / ".codex" / "kms.json").read_text(encoding="utf-8"))
    project_id = kms_config["project_id"]
    kms_root = project_dir / "sample_kms"
    raw_dir = kms_root / "projects" / project_id / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    slug = args.slug or slugify(args.title)
    output_path = raw_dir / f"{today}-{slug}.md"
    if output_path.exists():
        raise SystemExit(f"Refusing to overwrite existing file: {output_path}")

    content = Path(args.content_file).read_text(encoding="utf-8").strip()
    output_path.write_text(render_frontmatter(args.title) + content + "\n", encoding="utf-8")
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

