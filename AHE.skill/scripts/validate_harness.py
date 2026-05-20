#!/usr/bin/env python3
"""
Harness Compliance Checker — 验证 Agent workspace 是否符合 HARNESS.md v1.0 规范。

用法:
  python validate_harness.py /path/to/workspace

输出:
  合规审计报告 (JSON 格式 + 可读摘要)
"""

import os
import sys
import json
from pathlib import Path


def audit_workspace(workspace_root: str) -> dict:
    root = Path(workspace_root)
    if not root.exists():
        return {"error": f"Path does not exist: {workspace_root}"}

    report = {
        "workspace": str(root.resolve()),
        "compliance_score": 0,
        "max_score": 10,
        "components": {},
        "issues": [],
        "warnings": [],
    }

    # 7 个组件的检查定义
    checks = {
        "system_rules": {
            "files": ["AGENTS.md", "SOUL.md", "systemprompt.md", "CLAUDE.md", ".cursorrules"],
            "required": True,
            "weight": 2,
        },
        "tool_descriptions": {
            "dir": "tool_descriptions",
            "extensions": [".yaml", ".yml", ".json"],
            "required": True,
            "weight": 2,
        },
        "tool_implementations": {
            "dir": "tools",
            "extensions": [".py", ".js", ".ts", ".sh"],
            "required": True,
            "weight": 2,
        },
        "middleware": {
            "dir": "middleware",
            "extensions": [".py", ".js", ".ts"],
            "required": False,
            "weight": 1,
        },
        "skills": {
            "dir": "skills",
            "indicator": "SKILL.md",
            "required": False,
            "weight": 1,
        },
        "sub_agents": {
            "dir": "sub_agents",
            "required": False,
            "weight": 1,
        },
        "long_term_memory": {
            "files": ["MEMORY.md", "experiences.md", "LongTermMEMORY.md"],
            "required": False,
            "weight": 1,
        },
    }

    score = 0
    max_score = sum(c["weight"] for c in checks.values())

    # Manifest 检查
    has_manifest_dir = (root / "manifests").is_dir()
    has_manifest_files = list(root.glob("*manifest*")) + list(root.glob("manifests/*.json"))
    has_manifest = bool(has_manifest_files)

    for name, check in checks.items():
        component_report = {"status": "missing", "detail": "", "files_found": []}

        # Check by directory
        if "dir" in check:
            dir_path = root / check["dir"]
            if dir_path.is_dir():
                files = []
                if "extensions" in check:
                    files = [f for f in dir_path.iterdir() if f.suffix in check["extensions"]]
                elif "indicator" in check:
                    files = list(dir_path.rglob(check["indicator"]))

                if files:
                    component_report["status"] = "ok"
                    component_report["detail"] = f"Found {len(files)} file(s) in {check['dir']}/"
                    component_report["files_found"] = [str(f.relative_to(root)) for f in files[:10]]
                else:
                    component_report["status"] = "empty"
                    component_report["detail"] = f"Directory {check['dir']}/ exists but no matching files"
                    if not check["required"]:
                        report["warnings"].append(f"{name}: {check['dir']}/ exists but is empty")
            else:
                if check["required"]:
                    component_report["detail"] = f"Missing required directory: {check['dir']}/"
                    report["issues"].append(f"MISSING: {name} — required directory {check['dir']}/ not found")
                else:
                    component_report["status"] = "optional"
                    component_report["detail"] = f"Optional directory {check['dir']}/ not found"

        # Check by file list
        if "files" in check:
            found = [f for f in check["files"] if (root / f).is_file()]
            if found:
                component_report["status"] = "ok"
                component_report["detail"] = f"Found files: {', '.join(found)}"
                component_report["files_found"] = found
            else:
                if check["required"]:
                    component_report["detail"] = f"Missing required file(s): {', '.join(check['files'])}"
                    report["issues"].append(f"MISSING: {name} — required file not found")
                    component_report["status"] = "missing"
                else:
                    component_report["status"] = "optional"
                    component_report["detail"] = "No files found (optional)"

        if component_report["status"] == "ok":
            score += check["weight"]

        report["components"][name] = component_report

    # Manifest 检查
    report["manifest_check"] = {
        "has_manifest_dir": has_manifest_dir,
        "has_manifest_files": has_manifest_files,
        "count": len(has_manifest_files),
    }
    if has_manifest:
        score += 1  # Bonus point for having manifests

    report["compliance_score"] = score
    report["max_score"] = max_score + 1  # +1 for manifest bonus
    report["compliance_pct"] = round(score / (max_score + 1) * 100, 1)

    return report


def print_report(report: dict):
    if "error" in report:
        print(f"❌ ERROR: {report['error']}")
        return

    print(f"\n{'='*60}")
    print(f"  HARNESS.md Compliance Audit")
    print(f"  Workspace: {report['workspace']}")
    print(f"  Score: {report['compliance_score']}/{report['max_score']} ({report['compliance_pct']}%)")
    print(f"{'='*60}")

    print(f"\n📋 Components:")
    for name, comp in report["components"].items():
        icon = {"ok": "✅", "missing": "❌", "empty": "⚠️", "optional": "⬜"}.get(comp["status"], "❓")
        print(f"  {icon} {name}: {comp['detail']}")

    print(f"\n📦 Manifests:")
    m = report["manifest_check"]
    if m["has_manifest_files"]:
        print(f"  ✅ {m['count']} manifest file(s) found")
    else:
        print(f"  ⬜ No change manifests found (optional but recommended)")

    if report["issues"]:
        print(f"\n🔴 Issues ({len(report['issues'])}):")
        for i in report["issues"]:
            print(f"  ❌ {i}")

    if report["warnings"]:
        print(f"\n🟡 Warnings ({len(report['warnings'])}):")
        for w in report["warnings"]:
            print(f"  ⚠️  {w}")

    if not report["issues"] and not report["warnings"]:
        print(f"\n🎉 Perfect compliance with HARNESS.md v1.0!")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    report = audit_workspace(target)

    if "--json" in sys.argv:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print_report(report)
