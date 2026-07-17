from pathlib import Path
import json
import os
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gptkms_mcp.kms_store import KmsStore  # noqa: E402


def main() -> int:
    kms_root = Path(os.environ.get("GPTKMS_ROOT", REPO_ROOT / "sample_kms"))
    project_dir = Path(os.environ.get("GPTKMS_PROJECT_DIR", REPO_ROOT))
    store = KmsStore(kms_root=kms_root, project_dir=project_dir)

    active = store.get_active_context()
    search = store.search("mcp", limit=5)
    page = store.read_page("global", "concepts/mcp-first-kms-architecture.md")
    context_pack = store.build_context_pack("promotion", limit=3)
    lint = store.lint_links()
    conflicts = store.find_conflicts()

    print(
        json.dumps(
            {
                "active_context": active,
                "search_hits": search,
                "page_title": page["frontmatter"].get("title"),
                "context_pack_count": context_pack["result_count"],
                "lint_issue_count": lint["issue_count"],
                "conflict_issue_count": conflicts["issue_count"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
