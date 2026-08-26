# gw-ci-monitor-loop

GWCPEngine 项目 CI 全流水线监控与编译/测试问题自动修复闭环。

Windows 本地无法复现 iOS(clang/arm64)、Android 设备、视觉回归等问题时，靠 GitLab CI
验证。本 skill 自动化「监控流水线全部 Job → 检测失败 → 自动取回 Job 日志并分类错误 →
定位修复 → 提交代码 → 等待 CI 新结果」的循环。

## 前置条件

- Python 3.9+
- 一个 GitLab Personal Access Token —— **仅 scope: `read_api`**（强制）。
  本 skill 全部功能均为读操作；严禁配置 `api` 等写权限 token，写操作（建 MR / 合并 / 触发流水线）
  由用户本人执行（2026-08-17 事故教训：agent 曾绕开 MR 评审直接推送 develop）。
  - 创建地址：`https://git-rd.office.gritworld.cn/-/profile/personal_access_tokens`

## 配置 Token（重要）

Token **不写入仓库、不提交到 git**。脚本按以下顺序查找：

1. 命令行参数 `--token <PAT>`（临时覆盖用）
2. 环境变量 `GITLAB_TOKEN`
3. **本地配置文件 `~/.config/gwci/config.json`（推荐，参考 atlassian MCP 方式）**

### 推荐：本地配置文件

配置文件在用户主目录下，完全位于 git 仓库之外，不会（也不应）被提交。

一个 json 文件可配置**多个 GitLab 服务器**（多域名场景，如公司 git-rd 与 git-prod 并存）：

```json
{
  "default": "git-rd",
  "servers": {
    "git-rd": {
      "gitlab_host": "https://git-rd.office.gritworld.cn",
      "gitlab_project": "AndroidEngine/GWCPEngine",
      "gitlab_token": "<你的 PAT>"
    },
    "git-prod": {
      "gitlab_host": "https://git-prod.office.gritworld.cn",
      "gitlab_project": "gm/GritMobile",
      "gitlab_token": "<你的 PAT>"
    }
  }
}
```

- 服务器选择：`--server <名字>` 显式指定 > `"default"` 字段 > 只有一个服务器时自动选中
- 旧的扁平单服务器格式（顶层 `gitlab_host`/`gitlab_project`/`gitlab_token`）仍兼容，无需迁移
- 路径：`~/.config/gwci/config.json`（Windows 即 `%USERPROFILE%\.config\gwci\config.json`）
- `gitlab_host` / `gitlab_project` 可省略，缺省用脚本内建默认值
- 若通过环境变量 `GWCI_CONFIG` 指定了配置文件路径，则优先使用该路径
- 也可用 `--config <路径>` 临时指定其他配置文件

### 验证配置

```bash
PY=python   # 或你的 Python 解释器路径
S=path/to/ci_monitor.py

$PY $S status                        # 默认服务器（config["default"]）
$PY $S --server git-prod status      # 指定另一个服务器
```

能看到流水线概览即配置成功；报 `No GitLab token found` 则按上面方式补配。

## 命令

```bash
$PY $S status                         # 当前 MR 流水线概览 + 各 Job 状态
$PY $S lint                           # 校验分支 CI YAML（含 include 解析），有 yaml_errors 立即报出
$PY $S jobs                           # 列出流水线 Job id/name/status
$PY $S log --job <名字> --out x.log   # 下载指定 Job 日志（默认 Build_iOS）
$PY $S errors x.log                   # 从日志提取并分类错误（编译/测试/环境/API）
$PY $S watch --job <名字>             # 等单个 Job 结束，抓日志+摘要（--sha 匹配 commit）
$PY $S monitor [--exclude <名,名>]    # 监控全流水线，任一 Job 失败即立即处理
```

`lint` 走 GitLab CI Lint API（`content_ref` + `include_merged_yaml=true`），在
**push 之前/刚 push 之后**就能发现配置问题（rules 拒绝所有 job、hooks 嵌套超
10 层、include 缺失等）——这类问题会让流水线 0 秒创建即失败、0 个 job，普通
监控根本等不到 job 出现。`monitor` 启动时也会自动做一次 lint 预检，CONFIG-FAIL
检测路径同样会附上精确的 yaml_errors。

常用参数：

- `--server <名字>`：选择多服务器配置中的某个 GitLab 服务器（config["servers"] 的 key）
- `--sha <commit>`：匹配指定 commit 的流水线（避免监控到旧 push 的流水线）
- `--pipeline <id>`：直接指定流水线 id（跳过 sha 匹配）
- `--exclude ""`：恢复监控默认排除的 Job；`--exclude A,B` 自定义
- `--interval <秒>`：轮询间隔（默认 30）
- `--timeout <秒>`：超时（默认 7200，超时后列出 still-pending 的 Job）
- `--out-dir <目录>`：失败 Job 日志保存目录（默认 `ci_failures/`）

## monitor 行为（fail-fast）

`monitor` **不是**等所有 Job 跑完才动手，而是：

- 轮询期间任一**非排除** Job 状态变为 `failed` → **立即**停止等待，马上拉取该 Job
  日志 + 分类错误，并列出仍在运行中的 Job（early-fail）。
- 只有当所有非排除 Job 都到终态且无失败时，才判定全绿（退出码 0）。
- 有阻塞失败时退出码为 2（`allow_failure` 的失败不阻塞）。
- 默认排除 `Code_Review`（无 script 定义，会把流水线卡在 running 数小时）。

## 闭环工作流

1. `monitor --sha <commit>` 监控全流水线，得到失败 Job 列表 + 分类 + 日志（存 `ci_failures/`）。
2. 分析失败：编译/链接类（compile/linker/undefined-symbol/vtable）→ 改代码；
   测试崩溃（test-crash/test-fail）→ 查代码或判 flaky；环境类（env-device/robocopy）→
   报给 owner，不阻塞代码。
3. 最小化修复 → commit → **只 push 开发分支**（严禁 push develop 等受保护分支；
   分支已关联 MR，push 自动触发新 MR 流水线）。
4. 回到第 1 步循环，直到全绿。
5. 收尾时清理调试代码并单独提交。

## Git 操作纪律（强制）

- **严禁直接 push develop/master**（含 force-push）；只 push `liuguoyuan/jira/PAI-XXX` 类开发分支。
- **新建 MR 必须 squash**：合并时把分支全部 commit 压成一个（MR 页勾选 "Squash commits"），
  保持 develop 历史干净。
- 分支重建需 force 时只用 `--force-with-lease`，且须经用户确认。

## 已知坑

- 日志噪音（`DVTPortal`、`ld: warning`、`section_start/end` 等）已被 `errors` 过滤。
- iOS 独有根因：`SafeCombineLibraries.py` 合并静态库时多个第三方库 `.o` 重名互踩丢符号
  （undefined symbol / missing vtable），解法 = 把被内联的 external OBJECT 库改成 STATIC。
- 子模块推送：external 在独立仓库，本地 HEAD 可能 detached，`git push <branch>` 报
  "src refspec does not match" 时改用 `git push origin <sha>:refs/heads/<branch>`；
  主仓库更新子模块指针用 `git update-index --cacheinfo 160000,<sha>,external`。
- Windows 控制台默认 GBK，脚本已内部将 stdout/stderr 重设为 UTF-8，日志含 emoji 也不会崩。

## 参考

- CI 配置：仓库根 `.gitlab-ci.yml`；`Build_iOS` 走 `scripts/Apple/CI/BuildExportIOS.zsh -t IOS`。
- 合并脚本：`scripts/Apple/Developer/IOS/SafeCombineLibraries.py`。
- Skill 详细工作流：同目录 `SKILL.md`。
