#!/usr/bin/env python3
"""sayelf-base 规则轨评分器（零依赖，仅标准库）。

用法：
    python tests/eval_scorer.py --self-test
    python tests/eval_scorer.py --cases tests/golden-cases.json
    python tests/eval_scorer.py --cases tests/golden-cases.json --outputs outputs.json
    python tests/eval_scorer.py --cases tests/edge-cases.json --outputs outputs.json --json

outputs.json 支持两种形态：
    1) 列表，按 cases 顺序一一对应：["<输出文本或对象>", ...]
    2) 字典，按 id 映射：{"fde_scene_001": "<输出文本或对象>", ...]

只做规则轨（硬门槛）。LLM-as-Judge 语义轨不在本文件实现，仅留接口位 judge_score()。
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

REFUSE_FALLBACK = ("拒绝", "不建议", "不得", "禁止", "阻断", "不可跳过", "严禁")


@dataclass
class EvalResult:
    case_id: str
    passed: bool
    score: float
    reasons: List[str] = field(default_factory=list)

    def as_dict(self) -> Dict[str, Any]:
        return {
            "case_id": self.case_id,
            "passed": self.passed,
            "score": self.score,
            "reasons": self.reasons,
        }


def as_text(output: Any) -> str:
    """把任意输出压成可匹配文本；dict/list 走 JSON，保证中文不被转义丢失。"""
    if isinstance(output, str):
        return output
    return json.dumps(output, ensure_ascii=False)


def evaluate(case: Dict[str, Any], output: Any) -> EvalResult:
    text = as_text(output)
    reasons: List[str] = []

    # 1) 关键词覆盖
    keywords: List[str] = list(case.get("expected_output_keywords", []) or [])
    missing = [kw for kw in keywords if kw not in text]
    if missing:
        reasons.append("缺少关键内容: %s" % missing)

    # 2) 必要资产
    for asset in list(case.get("required_assets", []) or []):
        if asset not in text:
            reasons.append("未沉淀必要资产: %s" % asset)

    # 3) 必要步骤 / 门禁标记
    for step in list(case.get("required_steps", []) or []):
        if step not in text:
            reasons.append("缺少必要步骤或门禁标记: %s" % step)

    # 4) 边界拒识（fail-closed：声明应拒识而未拒识 = 失败）
    constraints: Dict[str, Any] = case.get("constraints") or {}
    if constraints.get("should_refuse"):
        refuse_words = list(constraints.get("refuse_keywords") or REFUSE_FALLBACK)
        if not any(word in text for word in refuse_words):
            reasons.append(
                "异常/越界场景未正确拒识（需出现之一: %s）" % "、".join(refuse_words)
            )

    # 5) 工具调用（可选）
    expected_tool = case.get("expected_tool_call")
    if expected_tool:
        tools = _called_tools(output)
        expected_list = expected_tool if isinstance(expected_tool, list) else [expected_tool]
        for exp in expected_list:
            if exp.get("tool") not in tools:
                reasons.append("未调用期望工具: %s" % exp.get("tool"))

    # 6) 长度约束（仅提示性扣分，不单独判失败以外的硬错）
    max_length = constraints.get("max_length")
    if isinstance(max_length, int) and len(text) > max_length:
        reasons.append("输出超长: %d > %d" % (len(text), max_length))

    denominator = max(len(keywords), 1)
    score = round(max(0.0, 1.0 - len(reasons) / denominator), 2)
    return EvalResult(
        case_id=str(case.get("id", "?")), passed=len(reasons) == 0, score=score, reasons=reasons
    )


def _called_tools(output: Any) -> List[str]:
    if isinstance(output, dict):
        raw = output.get("tools") or output.get("tool_calls") or []
        if isinstance(raw, list):
            return [t.get("tool") for t in raw if isinstance(t, dict) and t.get("tool")]
    return []


def judge_score(case: Dict[str, Any], output: Any) -> Optional[float]:
    """LLM-as-Judge 语义轨接口位：本底座不实现，返回 None 表示未启用。

    接入时在此返回 0.0-1.0，由 batch_evaluate 与规则轨合并。
    """
    return None


def load_outputs(path: str, cases: List[Dict[str, Any]]) -> List[Any]:
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        return [data.get(str(c.get("id")), "") for c in cases]
    if isinstance(data, list):
        return list(data) + [""] * (len(cases) - len(data))
    raise SystemExit("outputs 必须是 list 或 dict，实际: %s" % type(data).__name__)


def batch_evaluate(cases: List[Dict[str, Any]], outputs: List[Any]) -> Dict[str, Any]:
    results = [evaluate(c, o) for c, o in zip(cases, outputs)]
    passed = sum(1 for r in results if r.passed)
    total = len(results) or 1
    return {
        "total": len(results),
        "passed": passed,
        "pass_rate": round(passed / total, 2),
        "avg_score": round(sum(r.score for r in results) / total, 2),
        "details": [r.as_dict() for r in results],
    }


# --------------------------------------------------------------------------
# 自检：验证评分器本身有效（含"必须能判失败"的负例）
# --------------------------------------------------------------------------
SELF_CASES: List[Dict[str, Any]] = [
    {
        "id": "self_pass_001",
        "type": "golden",
        "expected_output_keywords": ["进门标准", "优先级"],
        "required_steps": ["进门标准"],
    },
    {
        "id": "self_fail_001",
        "type": "golden",
        "expected_output_keywords": ["黄金样本集", "评分机制"],
    },
    {
        "id": "self_refuse_001",
        "type": "edge",
        "expected_output_keywords": ["终局决策"],
        "constraints": {"should_refuse": True},
    },
]

SELF_OUTPUTS: List[Any] = [
    "进门标准五项全过，列为 P0 优先级。",  # 期望：通过
    "我们已经上线了。",  # 期望：失败（缺关键词）
    "该场景建议保留人工复核。",  # 期望：失败（应拒识而未拒识）
]

SELF_EXPECT_PASS = [True, False, False]


def self_test() -> int:
    report = batch_evaluate(SELF_CASES, SELF_OUTPUTS)
    failures: List[str] = []
    for result, expect in zip(report["details"], SELF_EXPECT_PASS):
        if result["passed"] != expect:
            failures.append(
                "自检失效: %s 期望 passed=%s 实际 %s（%s）"
                % (result["case_id"], expect, result["passed"], result["reasons"])
            )
    print("[self-test] 用例数=%d 通过=%d" % (report["total"], report["passed"]))
    for line in report["details"]:
        print(
            "  %-16s passed=%-5s score=%.2f reasons=%s"
            % (line["case_id"], line["passed"], line["score"], line["reasons"] or "-")
        )
    if failures:
        for line in failures:
            print("FAIL " + line)
        return 1
    print("[self-test] OK：正例通过、负例被判失败、拒识门控生效")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="sayelf-base 规则轨评分器")
    parser.add_argument("--cases", help="评测集 JSON 路径")
    parser.add_argument("--outputs", help="被测输出 JSON 路径；缺省则全空输出（用于校验用例可解析）")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出报告")
    parser.add_argument("--self-test", action="store_true", help="运行评分器自检")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.cases:
        parser.error("需要 --cases，或使用 --self-test")

    with open(args.cases, "r", encoding="utf-8") as fh:
        cases = json.load(fh)
    outputs = load_outputs(args.outputs, cases) if args.outputs else [""] * len(cases)

    report = batch_evaluate(cases, outputs)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("用例数=%d 通过=%d 通过率=%.2f 平均分=%.2f" % (
            report["total"], report["passed"], report["pass_rate"], report["avg_score"]))
        for line in report["details"]:
            print("  %-22s passed=%-5s score=%.2f %s" % (
                line["case_id"], line["passed"], line["score"], line["reasons"] or "-"))
    return 0 if report["passed"] == report["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
