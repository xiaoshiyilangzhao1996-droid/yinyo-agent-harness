# HARNESS.md Directory Template

以下是一个符合 HARNESS.md v1.0 标准的空模板目录结构。用于初始化新 Agent workspace。

```
<project-root>/
│
├── AGENTS.md                   # [System Rules] 核心行为规则
├── SOUL.md                     # [System Rules] 身份宣言（可选）
│
├── MEMORY.md                   # [Long-Term Memory] 长期稳定事实
├── experiences.md              # [Long-Term Memory] 经验教训（可选）
│
├── tool_descriptions/          # [Tool Descriptions]
│   └── .gitkeep
│
├── tools/                      # [Tool Implementations]
│   └── .gitkeep
│
├── middleware/                 # [Middleware]（可选，需要时添加）
│   └── .gitkeep
│
├── skills/                     # [Skills]（可选，需要时添加）
│   └── .gitkeep
│
├── sub_agents/                 # [Sub-Agents]（可选，需要时添加）
│   └── .gitkeep
│
├── manifests/                  # Change Manifest 存储目录
│   └── .gitkeep
│
├── agent.yaml                  # [Registry] 组件注册中心（视框架而定）
│
└── .gitignore
```

### AGENTS.md 示例头

```markdown
# AGENTS.md

> 遵循 HARNESS.md v1.0
> 本 Agent 的 Harness 结构符合 Agent Harness Specification v1.0

## 组件概述

- System Rules → AGENTS.md + SOUL.md
- Tool Descriptions → tool_descriptions/
- Tool Implementations → tools/
- Long-Term Memory → MEMORY.md + experiences.md

<!-- 其他 Agent 规则... -->
```

### 最小化 .gitignore

```
# HARNESS.md
manifests/*.json
```
