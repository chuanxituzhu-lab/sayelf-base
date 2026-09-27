#!/usr/bin/env python3
"""Local cache-prefix layout linter for Codex/code agents and LLM adapters.

This tool never calls a model or network and never prints segment text. It
checks the provider-neutral invariant: stable segments first, dynamic segments
last, and a cache key scoped without raw prompt data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_DYNAMIC_NAME = re.compile(
    r"(?:timestamp|request[_ -]?id|trace[_ -]?id|nonce|random|current[_ -]?date|"
    r"git[_ -]?diff|working[_ -]?tree|runtime[_ -]?log|temp(?:orary)?|时间戳|请求.?id|"
    r"随机|当前日期|工作区|实时日志)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Segment:
    name: str
    text: str
    stable: bool


def stable_cache_key(provider: str, model: str, scope: str, prompt_version: str) -> str:
    """Return a stable routing/accounting key with no raw prompt content."""
    fields = [provider.strip(), model.strip(), scope.strip(), prompt_version.strip()]
    if not all(fields):
        raise ValueError("provider、model、scope、prompt_version 不能为空")
    if any(any(char.isspace() for char in field) for field in fields):
        raise ValueError("缓存键字段不能包含空白字符")
    return ":".join(fields)


def prefix_fingerprint(segments: list[Segment]) -> str:
    """Hash stable segment metadata/content without returning the content."""
    stable = [
        {"name": segment.name, "text": segment.text}
        for segment in segments
        if segment.stable
    ]
    payload = json.dumps(stable, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def lint_request(request: dict[str, Any]) -> dict[str, Any]:
    raw_segments = request.get("segments")
    if not isinstance(raw_segments, list) or not raw_segments:
        raise ValueError("request.segments 必须是非空数组")

    segments: list[Segment] = []
    for index, raw in enumerate(raw_segments):
        if not isinstance(raw, dict):
            raise ValueError(f"segments[{index}] 必须是对象")
        name = str(raw.get("name", "")).strip()
        text = raw.get("text", "")
        stable = raw.get("stable")
        if not name or not isinstance(text, str) or not isinstance(stable, bool):
            raise ValueError(f"segments[{index}] 需要 name、text、stable 字段")
        segments.append(Segment(name=name, text=text, stable=stable))

    warnings: list[str] = []
    errors: list[str] = []
    dynamic_seen = False
    breakpoint_index: int | None = None
    for index, segment in enumerate(segments):
        if not segment.stable:
            dynamic_seen = True
            if breakpoint_index is None:
                breakpoint_index = index
            continue
        if dynamic_seen:
            errors.append(f"稳定段出现在动态段之后: {segment.name}")
        if _DYNAMIC_NAME.search(segment.name):
            warnings.append(f"稳定段名称疑似包含动态字段: {segment.name}")

    key = stable_cache_key(
        str(request.get("provider", "")),
        str(request.get("model", "")),
        str(request.get("scope", "")),
        str(request.get("prompt_version", "")),
    )
    result = {
        "code": 0 if not errors else 2,
        "msg": "ok" if not errors else "blocked",
        "data": {
            "stable_prefix_segments": [segment.name for segment in segments if segment.stable],
            "dynamic_suffix_segments": [segment.name for segment in segments if not segment.stable],
            "recommended_breakpoint_before_index": breakpoint_index,
            "cache_key": key,
            "stable_prefix_sha256": prefix_fingerprint(segments),
            "warnings": warnings,
            "errors": errors,
        },
    }
    return result


def _self_test() -> dict[str, Any]:
    good = {
        "provider": "openai",
        "model": "gpt-5.6",
        "scope": "fde-project-a",
        "prompt_version": "base-v1",
        "segments": [
            {"name": "shared-rules", "text": "stable", "stable": True},
            {"name": "tool-schema", "text": "stable", "stable": True},
            {"name": "current-task", "text": "dynamic", "stable": False},
        ],
    }
    good_result = lint_request(good)
    if good_result["code"] != 0 or good_result["data"]["recommended_breakpoint_before_index"] != 2:
        raise AssertionError(f"good request failed: {good_result}")

    bad = dict(good)
    bad["segments"] = [
        {"name": "current-task", "text": "dynamic", "stable": False},
        {"name": "tool-schema", "text": "stable", "stable": True},
    ]
    bad_result = lint_request(bad)
    if bad_result["code"] == 0 or not bad_result["data"]["errors"]:
        raise AssertionError(f"bad request was not blocked: {bad_result}")

    return {
        "status": "ok",
        "checks": ["stable-prefix-first", "dynamic-suffix-order", "scoped-cache-key", "prefix-hash"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint a provider-neutral prompt cache layout.")
    parser.add_argument("--request", type=Path, help="JSON request layout")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    try:
        if args.self_test:
            result = _self_test()
        elif args.request:
            with args.request.open("r", encoding="utf-8") as handle:
                result = lint_request(json.load(handle))
        else:
            parser.error("请提供 --self-test 或 --request <request.json>")
            return 2
    except (OSError, ValueError, json.JSONDecodeError, AssertionError) as exc:
        print(json.dumps({"code": 2, "msg": str(exc), "data": {}}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return int(result.get("code", 0))


if __name__ == "__main__":
    raise SystemExit(main())
