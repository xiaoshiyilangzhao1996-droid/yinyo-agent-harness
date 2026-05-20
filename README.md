# 🦁 HARNESS.md + AHE.skill

> **将复旦&北大的 Agentic Harness Engineering 论文，蒸馏成一份可落地的 Harness 规范和一个可运行的 Hermes Skill。**

---

## 这是什么

2026 年，行业共识已经形成：**决定 AI Agent 能不能稳定干活的，不是模型本身，而是模型外面的那套 Harness（外挂系统）。**

复旦 & 北大的 [AHE 论文](https://arxiv.org/abs/2604.25850) 证明：用三层可观测性驱动 Harness 自动演化，可以把 coding agent 的 Terminal-Bench 2 成绩从 69.7% 推到 77.0%，超越了人类手写的 Codex CLI。

但论文是论文，落地是另一回事。

这个仓库把 AHE 的核心洞察蒸馏成了两样东西：

### 📄 HARNESS.md — Agent Harness 规范 v1.0

一份**跨 Agent 的 Harness 结构规范**。任何 Agent（Hermes / OpenClaw / Claude Code / Codex / Cursor）都可以声明"遵循 HARNESS.md v1.0"，让 harness 组件有统一的语言、结构和可演化能力。

**核心内容：**
- 7 个正交组件的定义和职责
- 标准目录结构
- 组件注册格式
- **Change Manifest 标准** — 每次修改带 falsifiable 预测，可验证、可归因、可回滚
- 演化循环标准流程（Evaluate → Analyze → Improve → Verify）
- 合规检查清单

### 🔧 AHE.skill — Hermes 上的 Harness Evolution Skill

把 HARNESS.md 规范在 Hermes Agent 上落地为可执行的 Skill。

**功能：**
- **Harness Audit** — 检查当前 workspace 是否符合 HARNESS.md 规范
- **Generate Manifest** — 修改组件时生成标准化的 Change Manifest
- **Verify Changes** — 验证修改预测是否准确，自动判定 keep / revert
- **Harness Init** — 从零创建符合规范的 workspace

---

## 快速开始

### 1. 阅读规范

```bash
# 直接看
cat HARNESS.md

# 或者用 validate 脚本检查你的 workspace
python AHE.skill/scripts/validate_harness.py /path/to/your/agent/workspace
```

### 2. 安装 AHE.skill（如果使用 Hermes Agent）

```bash
# 安装到 Hermes skills 目录
cp -r AHE.skill /d/hermes/data/skills/ahe/

# 或者通过 skillhub
skillhub install ahe
```

### 3. 在你的 AGENTS.md 中声明遵循

```markdown
# AGENTS.md

> 🏷️ 遵循 HARNESS.md v1.0
```

### 4. 开始管理你的 Change Manifest

每次修改核心组件时，创建 `manifests/change_<timestamp>.json`，按规范填写。

---

## 项目结构

```
├── HARNESS.md                              # 规范文档（跨 Agent）
├── AHE.skill/
│   ├── SKILL.md                            # Hermes Skill 定义
│   ├── references/
│   │   ├── HARNESS.md                      # 规范副本
│   │   ├── change-manifest-schema.json     # Manifest JSON Schema
│   │   └── directory-template.md           # 目录模板
│   └── scripts/
│       └── validate_harness.py             # 合规检查脚本
└── README.md
```

---

## 背景

这份工作基于以下研究：

- **[Agentic Harness Engineering](https://arxiv.org/abs/2604.25850)** — Jiahang Lin, Shichun Liu, Chengjun Pan 等（复旦 & 北大, 2026）
  - 论文提出三层可观测性框架（组件 / 经验 / 决策），让 coding agent 的 Harness 可以自动演化
  - Terminal-Bench 2 #3（84.7% pass@1），超过手写 Codex CLI 和 ACE/TF-GRPO
  - 冻结的 Harness 跨 benchmark、跨模型迁移

- **[Agent Harness for LLM Agents: A Survey](https://huggingface.co/datasets/GloriaaaM/LLM-Agent-Harness-Survey)** — Harness 六组件形式化定义 H=(E,T,C,S,L,V)

---

## 许可

MIT
