---
name: project-launcher
description: 自动识别项目类型并应用 ~/.gemini/rules/ 下的规则模版。
triggers: ["init project", "初始化项目", "开始新项目", "new project"]
---

# 执行逻辑

当你检测到用户想要开始一个新项目，或者当前目录缺少 `GEMINI.md` 时，必须执行以下流程：

## 1. 模版扫描 (Scan)
- 自动读取 `~/.gemini/rules/` 目录下的所有以 `template_` 开头的 `.md` 文件。
- 提取每个文件的标题（# 之后的内容）作为选项名称。

## 2. 交互决策 (Interaction)
- 向用户展示可用的项目模版列表。
- 询问用户：“这是一个新项目，请选择一个适合的规则模版，或者描述你的需求让我为你新建一个。”

## 3. 环境部署 (Deployment)
一旦用户做出选择：
- **创建 GEMINI.md**：将选中的模版内容完整拷贝到当前目录的 `GEMINI.md`。
- **结构初始化**：根据 `GEMINI.md` 中 [ ] 标记的“必备初始化清单”，自动创建对应的子目录（如 `src/`, `include/`, `notes/` 等）。
- **同步设置**：如果在 `~/.gemini/rules/` 下存在同名的 `.json` 或 `.yaml` 配置文件，将其应用到本地 `.gemini/settings.md`。

## 4. 持续进化 (Feedback Loop)
- 在交互过程中，如果用户修改了本地的 `GEMINI.md` 并认为其具有通用性，你必须提供“同步回全局”的功能，更新 `~/.gemini/rules/` 下的源模版。

---
*Status: Ready to deploy*