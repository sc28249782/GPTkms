from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import traceback
from typing import Any

from gptkms_mcp.kms_store import KmsStore


PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "gptkms-prototype"
SERVER_VERSION = "0.1.0"


TOOL_DEFS = [
    {
        "name": "kms_list_bases",
        "title": "List KMS Bases",
        "description": "List global and project knowledge bases available under the configured KMS root.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "kms_get_active_context",
        "title": "Get Active KMS Context",
        "description": "Return the active project, attached bases, write policies, and KMS root.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "kms_search",
        "title": "Search KMS",
        "description": "Search page titles and page content across attached knowledge bases.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 50},
                "base_ids": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "kms_read_page",
        "title": "Read KMS Page",
        "description": "Read one compiled markdown page from a selected base.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_id": {"type": "string"},
                "page_path": {"type": "string"},
            },
            "required": ["base_id", "page_path"],
            "additionalProperties": False,
        },
    },
    {
        "name": "kms_create_page",
        "title": "Create KMS Page",
        "description": "Create a new compiled markdown page under pages/ in a selected base.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_id": {"type": "string"},
                "page_path": {"type": "string"},
                "frontmatter": {"type": "object"},
                "body": {"type": "string"},
            },
            "required": ["base_id", "page_path", "frontmatter", "body"],
            "additionalProperties": False,
        },
    },
    {
        "name": "kms_update_page",
        "title": "Update KMS Page",
        "description": "Update an existing compiled markdown page in a selected base.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_id": {"type": "string"},
                "page_path": {"type": "string"},
                "frontmatter": {"type": "object"},
                "body": {"type": "string"},
            },
            "required": ["base_id", "page_path", "frontmatter", "body"],
            "additionalProperties": False,
        },
    },
    {
        "name": "kms_append_log",
        "title": "Append KMS Log",
        "description": "Append a dated entry to log.md in a selected base.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_id": {"type": "string"},
                "entry": {"type": "string"},
            },
            "required": ["base_id", "entry"],
            "additionalProperties": False,
        },
    },
    {
        "name": "kms_ingest_source",
        "title": "Ingest Raw Source",
        "description": "Create a raw evidence file under raw/ in a selected base.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_id": {"type": "string"},
                "source_path": {"type": "string"},
                "title": {"type": "string"},
                "content": {"type": "string"},
            },
            "required": ["base_id", "source_path", "title", "content"],
            "additionalProperties": False,
        },
    },
    {
        "name": "kms_promote_candidate",
        "title": "Promote Candidate To Global",
        "description": "Promote a project page into the global knowledge base with provenance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "source_base_id": {"type": "string"},
                "source_page_path": {"type": "string"},
                "target_page_path": {"type": "string"},
                "title": {"type": "string"},
                "additional_tags": {"type": "array", "items": {"type": "string"}},
                "note": {"type": "string"},
            },
            "required": ["source_base_id", "source_page_path", "target_page_path"],
            "additionalProperties": False,
        },
    },
    {
        "name": "kms_build_context_pack",
        "title": "Build KMS Context Pack",
        "description": "Build a compact context pack from the best matching pages across attached bases.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 20},
                "base_ids": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["query"],
            "additionalProperties": False,
        },
    },
    {
        "name": "kms_lint_links",
        "title": "Lint KMS Links",
        "description": "Detect broken internal markdown links across selected bases.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_ids": {"type": "array", "items": {"type": "string"}}
            },
            "additionalProperties": False,
        },
    },
    {
        "name": "kms_find_conflicts",
        "title": "Find KMS Conflicts",
        "description": "Detect duplicate or strongly overlapping pages across selected bases.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "base_ids": {"type": "array", "items": {"type": "string"}}
            },
            "additionalProperties": False,
        },
    },
]


def make_success_result(payload: Any) -> dict[str, Any]:
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    return {
        "content": [{"type": "text", "text": text}],
        "structuredContent": payload,
    }


def make_error_result(message: str, details: Any | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"error": message}
    if details is not None:
        payload["details"] = details
    return {
        "content": [{"type": "text", "text": json.dumps(payload, indent=2, ensure_ascii=False)}],
        "structuredContent": payload,
        "isError": True,
    }


class McpJsonRpcServer:
    def __init__(self, store: KmsStore) -> None:
        self.store = store

    def run(self) -> None:
        while True:
            request = read_message(sys.stdin.buffer)
            if request is None:
                break

            response = self.handle_message(request)
            if response is not None:
                write_message(sys.stdout.buffer, response)

    def handle_message(self, request: dict[str, Any]) -> dict[str, Any] | None:
        if "method" not in request:
            return self._error_response(request.get("id"), -32600, "Invalid Request")

        method = request["method"]
        request_id = request.get("id")
        params = request.get("params", {})

        try:
            if method == "initialize":
                result = {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": SERVER_NAME,
                        "version": SERVER_VERSION,
                    },
                    "instructions": (
                        "GPTKMS exposes a local-first knowledge store. Prefer compiled pages "
                        "under pages/ over raw sources under raw/. Use project bases first, and "
                        "treat global writes as higher-scrutiny operations."
                    ),
                }
                return self._success_response(request_id, result)

            if method == "notifications/initialized":
                return None

            if method == "ping":
                return self._success_response(request_id, {})

            if method == "tools/list":
                return self._success_response(request_id, {"tools": TOOL_DEFS})

            if method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = self._call_tool(tool_name, arguments)
                return self._success_response(request_id, result)

            return self._error_response(request_id, -32601, f"Method not found: {method}")

        except Exception as exc:  # noqa: BLE001
            details = {
                "message": str(exc),
                "traceback": traceback.format_exc(),
            }
            if method == "tools/call" and request_id is not None:
                return self._success_response(request_id, make_error_result(str(exc), details))
            return self._error_response(request_id, -32000, str(exc), details)

    def _call_tool(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        if tool_name == "kms_list_bases":
            return make_success_result({"bases": self.store.list_bases()})

        if tool_name == "kms_get_active_context":
            return make_success_result(self.store.get_active_context())

        if tool_name == "kms_search":
            query = arguments["query"]
            limit = int(arguments.get("limit", 10))
            base_ids = arguments.get("base_ids")
            return make_success_result(
                {
                    "query": query,
                    "hits": self.store.search(query=query, limit=limit, base_ids=base_ids),
                }
            )

        if tool_name == "kms_read_page":
            return make_success_result(
                self.store.read_page(
                    base_id=arguments["base_id"],
                    page_path=arguments["page_path"],
                )
            )

        if tool_name == "kms_create_page":
            return make_success_result(
                self.store.create_page(
                    base_id=arguments["base_id"],
                    page_path=arguments["page_path"],
                    frontmatter=arguments["frontmatter"],
                    body=arguments["body"],
                )
            )

        if tool_name == "kms_update_page":
            return make_success_result(
                self.store.update_page(
                    base_id=arguments["base_id"],
                    page_path=arguments["page_path"],
                    frontmatter=arguments["frontmatter"],
                    body=arguments["body"],
                )
            )

        if tool_name == "kms_append_log":
            return make_success_result(
                self.store.append_log(
                    base_id=arguments["base_id"],
                    entry=arguments["entry"],
                )
            )

        if tool_name == "kms_ingest_source":
            return make_success_result(
                self.store.ingest_source(
                    base_id=arguments["base_id"],
                    source_path=arguments["source_path"],
                    title=arguments["title"],
                    content=arguments["content"],
                )
            )

        if tool_name == "kms_promote_candidate":
            return make_success_result(
                self.store.promote_candidate(
                    source_base_id=arguments["source_base_id"],
                    source_page_path=arguments["source_page_path"],
                    target_page_path=arguments["target_page_path"],
                    title=arguments.get("title"),
                    additional_tags=arguments.get("additional_tags"),
                    note=arguments.get("note"),
                )
            )

        if tool_name == "kms_build_context_pack":
            return make_success_result(
                self.store.build_context_pack(
                    query=arguments["query"],
                    limit=int(arguments.get("limit", 5)),
                    base_ids=arguments.get("base_ids"),
                )
            )

        if tool_name == "kms_lint_links":
            return make_success_result(
                self.store.lint_links(
                    base_ids=arguments.get("base_ids"),
                )
            )

        if tool_name == "kms_find_conflicts":
            return make_success_result(
                self.store.find_conflicts(
                    base_ids=arguments.get("base_ids"),
                )
            )

        raise ValueError(f"Unknown tool: {tool_name}")

    def _success_response(self, request_id: Any, result: Any) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result,
        }

    def _error_response(
        self,
        request_id: Any,
        code: int,
        message: str,
        data: Any | None = None,
    ) -> dict[str, Any]:
        error = {"code": code, "message": message}
        if data is not None:
            error["data"] = data
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": error,
        }


def read_message(stream: Any) -> dict[str, Any] | None:
    headers: dict[str, str] = {}
    while True:
        line = stream.readline()
        if not line:
            return None
        if line in {b"\r\n", b"\n"}:
            break
        key, _, value = line.decode("utf-8").partition(":")
        headers[key.strip().lower()] = value.strip()

    length_header = headers.get("content-length")
    if not length_header:
        raise ValueError("Missing Content-Length header.")

    body = stream.read(int(length_header))
    return json.loads(body.decode("utf-8"))


def write_message(stream: Any, message: dict[str, Any]) -> None:
    payload = json.dumps(message, ensure_ascii=False).encode("utf-8")
    header = f"Content-Length: {len(payload)}\r\n\r\n".encode("utf-8")
    stream.write(header)
    stream.write(payload)
    stream.flush()


def main() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    kms_root = Path(os.environ.get("GPTKMS_ROOT", repo_root / "sample_kms"))
    project_dir = Path(os.environ.get("GPTKMS_PROJECT_DIR", repo_root))
    store = KmsStore(kms_root=kms_root, project_dir=project_dir)
    server = McpJsonRpcServer(store=store)
    server.run()


if __name__ == "__main__":
    main()
