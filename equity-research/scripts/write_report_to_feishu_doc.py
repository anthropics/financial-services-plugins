#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path


def _load_default_feishu_credentials() -> tuple[str, str]:
    env_path = os.getenv("OPENCLAW_CONFIG_PATH", "").strip()
    candidates = []
    if env_path:
        candidates.append(Path(env_path))
    candidates.append(Path.home() / ".openclaw" / "openclaw.json")
    for path in candidates:
        if not path.exists():
            continue
        try:
            obj = json.loads(path.read_text(encoding="utf-8"))
            feishu = (((obj.get("channels") or {}).get("feishu") or {}))
            default_account = feishu.get("defaultAccount") or "default"
            account = (((feishu.get("accounts") or {}).get(default_account) or {}))
            app_id = str(account.get("appId") or "").strip()
            app_secret = str(account.get("appSecret") or "").strip()
            if app_id and app_secret:
                return app_id, app_secret
        except Exception:
            continue
    return "", ""


def _post_json(url: str, payload: dict, headers: dict[str, str] | None = None) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _get_json(url: str, headers: dict[str, str] | None = None) -> dict:
    req = urllib.request.Request(url, method="GET")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _tenant_token(app_id: str, app_secret: str) -> str:
    obj = _post_json(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        {"app_id": app_id, "app_secret": app_secret},
    )
    token = obj.get("tenant_access_token", "")
    if obj.get("code") != 0 or not token:
        raise RuntimeError(f"tenant_token_failed: {obj}")
    return token


def _create_doc(title: str, token: str) -> str:
    obj = _post_json(
        "https://open.feishu.cn/open-apis/docx/v1/documents",
        {"title": title},
        {"Authorization": f"Bearer {token}"},
    )
    data = obj.get("data") or {}
    doc = data.get("document") or {}
    doc_id = doc.get("document_id") or data.get("document_id") or ""
    if obj.get("code") != 0 or not doc_id:
        raise RuntimeError(f"create_doc_failed: {obj}")
    return str(doc_id)


def _line_to_block(line: str) -> dict:
    text = line.strip()
    if text.startswith("# "):
        return {
            "block_type": 3,
            "heading1": {"elements": [{"text_run": {"content": text[2:].strip()[:2000]}}]},
        }
    if text.startswith("## "):
        return {
            "block_type": 4,
            "heading2": {"elements": [{"text_run": {"content": text[3:].strip()[:2000]}}]},
        }
    return {
        "block_type": 2,
        "text": {"elements": [{"text_run": {"content": text[:2000]}}]},
    }


def _append_markdown(doc_id: str, markdown_text: str, token: str) -> None:
    lines = [line.rstrip() for line in markdown_text.splitlines()]
    lines = [line for line in lines if line.strip()]
    if not lines:
        raise RuntimeError("append_markdown_failed: no_content")
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"
    headers = {"Authorization": f"Bearer {token}"}
    for i in range(0, len(lines), 50):
        blocks = [_line_to_block(line) for line in lines[i : i + 50]]
        obj = _post_json(url, {"children": blocks, "index": -1}, headers)
        if obj.get("code") != 0:
            raise RuntimeError(f"append_blocks_failed: {obj}")


def _verify_body(doc_id: str, token: str) -> int:
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children?page_size=20"
    obj = _get_json(url, {"Authorization": f"Bearer {token}"})
    items = ((obj.get("data") or {}).get("items") or [])
    if obj.get("code") != 0:
        raise RuntimeError(f"verify_doc_failed: {obj}")
    if not items:
        raise RuntimeError("verify_doc_failed: title_only_or_empty")
    return len(items)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID", ""))
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET", ""))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.app_id or not args.app_secret:
        app_id, app_secret = _load_default_feishu_credentials()
        args.app_id = args.app_id or app_id
        args.app_secret = args.app_secret or app_secret

    if not args.app_id or not args.app_secret:
        raise RuntimeError("missing_feishu_credentials")

    markdown = Path(args.input).read_text(encoding="utf-8")
    token = _tenant_token(args.app_id, args.app_secret)
    doc_id = _create_doc(args.title, token)
    _append_markdown(doc_id, markdown, token)
    block_count = _verify_body(doc_id, token)

    result = {
        "ok": True,
        "document_id": doc_id,
        "document_url": f"https://feishu.cn/docx/{doc_id}",
        "verified_block_count": block_count,
        "input_path": args.input,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(result["document_url"])
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"ok": False, "error": str(exc)}, ensure_ascii=False))
        raise
