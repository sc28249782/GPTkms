from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import json
from itertools import combinations
from pathlib import Path, PurePosixPath
import re
from typing import Any


FRONTMATTER_BOUNDARY = "---"
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


@dataclass(frozen=True)
class BaseInfo:
    base_id: str
    scope: str
    path: Path


class KmsStore:
    def __init__(self, kms_root: Path, project_dir: Path) -> None:
        self.kms_root = kms_root.resolve()
        self.project_dir = project_dir.resolve()
        self.project_config_path = self.project_dir / ".codex" / "kms.json"
        self.project_config = self._load_project_config()

    def _load_project_config(self) -> dict[str, Any]:
        if not self.project_config_path.exists():
            return {
                "project_id": self.project_dir.name,
                "attached_bases": ["global", f"projects/{self.project_dir.name}"],
                "write_policy": {
                    "global": "review",
                    f"projects/{self.project_dir.name}": "auto",
                },
            }
        return json.loads(self.project_config_path.read_text(encoding="utf-8"))

    def list_bases(self) -> list[dict[str, Any]]:
        bases: list[dict[str, Any]] = []
        global_path = self.kms_root / "global"
        if global_path.exists():
            bases.append(
                {
                    "base_id": "global",
                    "scope": "global",
                    "path": str(global_path),
                }
            )

        projects_path = self.kms_root / "projects"
        if projects_path.exists():
            for child in sorted(projects_path.iterdir()):
                if child.is_dir():
                    bases.append(
                        {
                            "base_id": f"projects/{child.name}",
                            "scope": "project",
                            "path": str(child),
                        }
                    )
        return bases

    def get_active_context(self) -> dict[str, Any]:
        return {
            "project_dir": str(self.project_dir),
            "project_id": self.project_config["project_id"],
            "attached_bases": self.project_config.get("attached_bases", []),
            "write_policy": self.project_config.get("write_policy", {}),
            "kms_root": str(self.kms_root),
        }

    def resolve_base(self, base_id: str) -> BaseInfo:
        if base_id == "global":
            path = self.kms_root / "global"
            return BaseInfo(base_id=base_id, scope="global", path=path)

        if base_id.startswith("projects/"):
            project_id = base_id.split("/", 1)[1]
            path = self.kms_root / "projects" / project_id
            return BaseInfo(base_id=base_id, scope="project", path=path)

        raise ValueError(f"Unsupported base_id: {base_id}")

    def _safe_markdown_path(self, relative_path: str) -> PurePosixPath:
        rel = PurePosixPath(relative_path)
        if rel.is_absolute():
            raise ValueError("Path must be relative.")
        if ".." in rel.parts:
            raise ValueError("Path traversal is not allowed.")
        if rel.suffix != ".md":
            raise ValueError("Only .md files are allowed.")
        return rel

    def _page_file_path(self, base_id: str, page_path: str) -> Path:
        base = self.resolve_base(base_id)
        rel = self._safe_markdown_path(page_path)
        return base.path / "pages" / Path(*rel.parts)

    def _raw_file_path(self, base_id: str, source_path: str) -> Path:
        base = self.resolve_base(base_id)
        rel = self._safe_markdown_path(source_path)
        return base.path / "raw" / Path(*rel.parts)

    def _list_markdown_files(self, base_id: str) -> list[Path]:
        base = self.resolve_base(base_id)
        pages_dir = base.path / "pages"
        if not pages_dir.exists():
            return []
        return sorted(pages_dir.rglob("*.md"))

    def search(
        self,
        query: str,
        limit: int = 10,
        base_ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        base_ids = base_ids or self.project_config.get("attached_bases", [])
        query_norm = query.strip().lower()
        if not query_norm:
            return []

        hits: list[dict[str, Any]] = []
        for base_id in base_ids:
            base = self.resolve_base(base_id)
            for page_file in self._list_markdown_files(base_id):
                page = self._read_markdown_file(page_file)
                title = str(page["frontmatter"].get("title", page_file.stem))
                body = page["body"]
                title_score = title.lower().count(query_norm) * 5
                body_score = body.lower().count(query_norm)
                score = title_score + body_score
                if score <= 0:
                    continue

                rel = page_file.relative_to(base.path / "pages").as_posix()
                snippet = self._make_snippet(body, query_norm)
                hits.append(
                    {
                        "base_id": base_id,
                        "page_path": rel,
                        "title": title,
                        "score": score,
                        "scope": base.scope,
                        "snippet": snippet,
                    }
                )

        def sort_key(item: dict[str, Any]) -> tuple[int, int, str]:
            scope_rank = 1 if item["scope"] == "project" else 0
            return (scope_rank, item["score"], item["title"].lower())

        hits.sort(key=sort_key, reverse=True)
        return hits[:limit]

    def read_page(self, base_id: str, page_path: str) -> dict[str, Any]:
        file_path = self._page_file_path(base_id, page_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Page not found: {base_id}/{page_path}")
        payload = self._read_markdown_file(file_path)
        payload["base_id"] = base_id
        payload["page_path"] = page_path
        payload["path"] = str(file_path)
        return payload

    def create_page(
        self,
        base_id: str,
        page_path: str,
        frontmatter: dict[str, Any],
        body: str,
    ) -> dict[str, Any]:
        file_path = self._page_file_path(base_id, page_path)
        if file_path.exists():
            raise FileExistsError(f"Page already exists: {base_id}/{page_path}")
        self._write_markdown_file(file_path, frontmatter, body)
        return {
            "base_id": base_id,
            "page_path": page_path,
            "path": str(file_path),
            "created": True,
        }

    def update_page(
        self,
        base_id: str,
        page_path: str,
        frontmatter: dict[str, Any],
        body: str,
    ) -> dict[str, Any]:
        file_path = self._page_file_path(base_id, page_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Page not found: {base_id}/{page_path}")
        self._write_markdown_file(file_path, frontmatter, body)
        return {
            "base_id": base_id,
            "page_path": page_path,
            "path": str(file_path),
            "updated": True,
        }

    def append_log(self, base_id: str, entry: str) -> dict[str, Any]:
        base = self.resolve_base(base_id)
        log_path = base.path / "log.md"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        line = f"- {date.today().isoformat()}: {entry.strip()}\n"
        with log_path.open("a", encoding="utf-8") as handle:
            handle.write(line)
        return {
            "base_id": base_id,
            "path": str(log_path),
            "entry": line.strip(),
        }

    def ingest_source(
        self,
        base_id: str,
        source_path: str,
        title: str,
        content: str,
    ) -> dict[str, Any]:
        file_path = self._raw_file_path(base_id, source_path)
        if file_path.exists():
            raise FileExistsError(f"Raw source already exists: {base_id}/{source_path}")
        frontmatter = {
            "title": title,
            "source_type": "captured-note",
            "captured_at": date.today().isoformat(),
        }
        self._write_markdown_file(file_path, frontmatter, content)
        return {
            "base_id": base_id,
            "source_path": source_path,
            "path": str(file_path),
            "created": True,
        }

    def promote_candidate(
        self,
        source_base_id: str,
        source_page_path: str,
        target_page_path: str,
        title: str | None = None,
        additional_tags: list[str] | None = None,
        note: str | None = None,
    ) -> dict[str, Any]:
        source_base = self.resolve_base(source_base_id)
        if source_base.scope != "project":
            raise ValueError("Only project pages can be promoted to global in the current prototype.")

        source_page = self.read_page(source_base_id, source_page_path)
        target_base_id = "global"
        target_file = self._page_file_path(target_base_id, target_page_path)
        if target_file.exists():
            raise FileExistsError(f"Target page already exists: {target_base_id}/{target_page_path}")

        frontmatter = dict(source_page["frontmatter"])
        frontmatter["scope"] = "global"
        frontmatter["status"] = frontmatter.get("status", "draft")
        if title:
            frontmatter["title"] = title

        tags = list(frontmatter.get("tags", []))
        tags.extend(additional_tags or [])
        if "promoted" not in tags:
            tags.append("promoted")
        frontmatter["tags"] = dedupe_preserve_order(tags)

        sources = list(frontmatter.get("sources", []))
        source_reference = f"{source_base_id}/pages/{source_page_path}"
        if source_reference not in sources:
            sources.append(source_reference)
        frontmatter["sources"] = dedupe_preserve_order(sources)
        frontmatter["last_reviewed"] = date.today().isoformat()
        frontmatter["promoted_from"] = f"{source_base_id}:{source_page_path}"

        body = source_page["body"].rstrip()
        promotion_note = note.strip() if note else "Promoted from project scope into global scope."
        body = f"{body}\n\n## Promotion Note\n\n{promotion_note}\n"

        self._write_markdown_file(target_file, frontmatter, body)
        self.append_log(
            "global",
            f"Promoted {source_base_id}/{source_page_path} to global page {target_page_path}",
        )

        return {
            "source_base_id": source_base_id,
            "source_page_path": source_page_path,
            "target_base_id": target_base_id,
            "target_page_path": target_page_path,
            "path": str(target_file),
            "promoted": True,
        }

    def build_context_pack(
        self,
        query: str,
        limit: int = 5,
        base_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        hits = self.search(query=query, limit=limit, base_ids=base_ids)
        selected_pages: list[dict[str, Any]] = []

        for hit in hits:
            page = self.read_page(hit["base_id"], hit["page_path"])
            selected_pages.append(
                {
                    "base_id": hit["base_id"],
                    "page_path": hit["page_path"],
                    "title": page["frontmatter"].get("title", hit["title"]),
                    "scope": hit["scope"],
                    "frontmatter": page["frontmatter"],
                    "excerpt": self._make_snippet(page["body"], query.lower().strip()),
                    "citation": f"{hit['base_id']}/pages/{hit['page_path']}",
                }
            )

        summary_lines = [
            f"- [{item['scope']}] {item['title']} ({item['citation']})"
            for item in selected_pages
        ]

        return {
            "query": query,
            "active_context": self.get_active_context(),
            "result_count": len(selected_pages),
            "pages": selected_pages,
            "summary_markdown": "\n".join(summary_lines),
        }

    def lint_links(self, base_ids: list[str] | None = None) -> dict[str, Any]:
        base_ids = base_ids or self.project_config.get("attached_bases", [])
        issues: list[dict[str, Any]] = []
        checked_pages = 0

        for base_id in base_ids:
            base = self.resolve_base(base_id)
            for page_file in self._list_markdown_files(base_id):
                checked_pages += 1
                rel_page_path = page_file.relative_to(base.path / "pages").as_posix()
                page = self._read_markdown_file(page_file)
                for target in extract_markdown_links(page["body"]):
                    if is_external_link(target):
                        continue
                    if target.startswith("#"):
                        continue

                    candidate = normalize_internal_link(target)
                    if candidate is None:
                        continue

                    resolved = (page_file.parent / candidate).resolve()
                    if not resolved.exists():
                        issues.append(
                            {
                                "type": "broken_link",
                                "base_id": base_id,
                                "page_path": rel_page_path,
                                "target": target,
                            }
                        )

        return {
            "base_ids": base_ids,
            "checked_pages": checked_pages,
            "issue_count": len(issues),
            "issues": issues,
        }

    def find_conflicts(self, base_ids: list[str] | None = None) -> dict[str, Any]:
        base_ids = base_ids or self.project_config.get("attached_bases", [])
        page_entries: list[dict[str, Any]] = []

        for base_id in base_ids:
            base = self.resolve_base(base_id)
            for page_file in self._list_markdown_files(base_id):
                rel_page_path = page_file.relative_to(base.path / "pages").as_posix()
                page = self._read_markdown_file(page_file)
                title = str(page["frontmatter"].get("title", page_file.stem))
                page_entries.append(
                    {
                        "base_id": base_id,
                        "page_path": rel_page_path,
                        "title": title,
                        "title_norm": normalize_text(title),
                        "body_norm": normalize_text(page["body"]),
                    }
                )

        issues: list[dict[str, Any]] = []
        for left, right in combinations(page_entries, 2):
            if left["title_norm"] == right["title_norm"]:
                issues.append(
                    {
                        "type": "duplicate_title",
                        "left": describe_entry(left),
                        "right": describe_entry(right),
                    }
                )
                continue

            if left["body_norm"] and left["body_norm"] == right["body_norm"]:
                issues.append(
                    {
                        "type": "duplicate_body",
                        "left": describe_entry(left),
                        "right": describe_entry(right),
                    }
                )
                continue

            title_similarity = token_overlap(left["title_norm"], right["title_norm"])
            body_similarity = token_overlap(left["body_norm"], right["body_norm"])
            if title_similarity >= 0.6 and body_similarity >= 0.6:
                issues.append(
                    {
                        "type": "overlapping_pages",
                        "left": describe_entry(left),
                        "right": describe_entry(right),
                        "title_similarity": round(title_similarity, 3),
                        "body_similarity": round(body_similarity, 3),
                    }
                )

        return {
            "base_ids": base_ids,
            "page_count": len(page_entries),
            "issue_count": len(issues),
            "issues": issues,
        }

    def _read_markdown_file(self, file_path: Path) -> dict[str, Any]:
        text = file_path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)
        return {"frontmatter": frontmatter, "body": body}

    def _write_markdown_file(
        self,
        file_path: Path,
        frontmatter: dict[str, Any],
        body: str,
    ) -> None:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(render_frontmatter(frontmatter, body), encoding="utf-8")

    def _make_snippet(self, body: str, query: str) -> str:
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        for line in lines:
            if query in line.lower():
                return line[:240]
        return lines[0][:240] if lines else ""


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith(f"{FRONTMATTER_BOUNDARY}\n"):
        return {}, text

    lines = text.splitlines()
    frontmatter_lines: list[str] = []
    body_start = 0

    for index in range(1, len(lines)):
        line = lines[index]
        if line == FRONTMATTER_BOUNDARY:
            body_start = index + 1
            break
        frontmatter_lines.append(line)

    frontmatter = parse_simple_yaml(frontmatter_lines)
    body = "\n".join(lines[body_start:]).lstrip("\n")
    return frontmatter, body


def parse_simple_yaml(lines: list[str]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_list_key: str | None = None

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line:
            continue
        if line.startswith("  - ") and current_list_key:
            data.setdefault(current_list_key, []).append(line[4:].strip())
            continue

        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not match:
            current_list_key = None
            continue

        key, value = match.groups()
        if value == "":
            data[key] = []
            current_list_key = key
        else:
            data[key] = parse_scalar(value)
            current_list_key = None

    return data


def parse_scalar(value: str) -> Any:
    if value in {"true", "false"}:
        return value == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    return value


def render_frontmatter(frontmatter: dict[str, Any], body: str) -> str:
    lines = [FRONTMATTER_BOUNDARY]
    for key, value in frontmatter.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    lines.append(FRONTMATTER_BOUNDARY)
    lines.append("")
    lines.append(body.rstrip())
    lines.append("")
    return "\n".join(lines)


def dedupe_preserve_order(values: list[Any]) -> list[Any]:
    seen: set[Any] = set()
    result: list[Any] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def extract_markdown_links(body: str) -> list[str]:
    return [match.group(1).strip() for match in MARKDOWN_LINK_RE.finditer(body)]


def is_external_link(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith("http://") or lowered.startswith("https://") or lowered.startswith("mailto:")


def normalize_internal_link(target: str) -> Path | None:
    cleaned = target.split("#", 1)[0].strip()
    if not cleaned:
        return None
    return Path(cleaned)


def normalize_text(value: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", value.lower()))


def token_overlap(left: str, right: str) -> float:
    left_tokens = set(left.split())
    right_tokens = set(right.split())
    if not left_tokens or not right_tokens:
        return 0.0
    intersection = left_tokens & right_tokens
    union = left_tokens | right_tokens
    return len(intersection) / len(union)


def describe_entry(entry: dict[str, Any]) -> dict[str, str]:
    return {
        "base_id": entry["base_id"],
        "page_path": entry["page_path"],
        "title": entry["title"],
    }
