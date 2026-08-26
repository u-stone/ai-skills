---
name: gw-ci-monitor-loop
agent_created: true
description: >
  GWCPEngine 项目 CI 全流水线监控与编译/测试问题自动修复闭环。Windows 本地无法复现
  iOS(clang/arm64) 等问题时，靠 GitLab CI 验证。本 skill 自动化「监控流水线全部 Job →
  检测失败 → 自动取回 Job 日志并分类错误 → 定位修复 → 提交代码 → 等待 CI 新结果」的循环。
  创建 MR 后监控构建是否开始：流水线未开始（manual）时 agent 主动触发构建；Job 失败时
  agent 调查根因并修复；最终合并操作由用户本人执行，agent 永不代点。提供 GitLab API
  客户端脚本（status/jobs/log/errors/watch/monitor）。触发词：CI 编译错误、Build_iOS、
  SafeCombine、linker 错误、undefined symbol、missing vtable、监控 CI、Job 失败、
  测试失败、自动修 CI、开 MR、创建 MR。（原 gw-ios-ci-loop，已更名）
---

# GWCPEngine CI 监控与自动修复闭环

## 策略：优先本地验证，CI 兜底

1. **本地优先**：任何 CMake/源码改动，先在 Windows 本地跑
   `python scripts/ci/ops/ops.py --all --generator ninja`（Qt→ImGui→Android→Harmony）验证编译；
   本地全绿后才提交 push 触发 CI。不要拿 CI 当第一道验证。
2. **CI 验证环境差异**：本地无法覆盖的环境（iOS clang/arm64、Android 设备、视觉回归、
   SafeCombine 静态库合并等）靠 GitLab CI 兜底，用本 skill 闭环验证。
3. **CI 卡住判断**：monitor 若长时间无输出，先 `status` 查流水线实际状态，不要干等；
   流水线终态（failed/success）后 monitor 应立即退出，若未退出说明脚本或网络问题。

## 场景

本机是 Windows，很多问题无法本地复现（iOS clang/arm64、Android 设备、视觉回归测试等），
只能靠 GitLab CI 的 MR 流水线验证。本 skill 把「读 CI 结果」完全自动化，配合 agent 完成
「监控 → 分析 → 修复 → 提交 → 再监控」的闭环，不再需要手动拷日志。

## Git 操作纪律（强制，2026-08-17 事故教训）

1. **写操作分工（2026-08-19 用户确认调整）**：
   - agent 可做：创建 MR（需 `api` scope PAT，由用户提供）；创建 MR 后**监控构建是否开始，
     未开始就主动触发**——流水线状态为 `manual`（如 GritMobile 的 Build_Windows 在
     merge_request_event 下 `when: manual`）时 play 对应 job
     （`POST /projects/:id/jobs/:job_id/play`），无流水线时新建
     （`POST /projects/:id/merge_requests/:iid/pipelines`）；Job 失败时取回日志、调查根因、
     修复并 push 开发分支，再监控新流水线。
   - agent 禁做：**最终合并（merge）操作**。合并 MR 永远由用户本人点击；agent 只负责把
     流水线跑到全绿并报告结果。严禁 push develop 等受保护分支（见 #2）。
   - 读操作（status/jobs/log/errors/watch/monitor）用 `read_api` scope 即可。
   - 教训：曾因 agent 用本地 git 权限直接 push develop 合并分支内容，绕过 MR 评审流程。
2. **严禁 push develop 等受保护分支**：任何情况下不得直接向 develop/master push 或
   force-push。代码改动只允许 push 到 `liuguoyuan/jira/PAI-XXX` 这类开发分支。
3. **新建 MR 必须使用 squash 选项**：所有分支上的多个 commit 在合并时合并为单个
   commit（GitLab MR 页勾选 "Squash commits" / API 传 `squash=true`），保持 develop 历史干净。
4. revert 用 `git revert`（不 reset 已推送历史）；分支重建需 force 时只用
   `--force-with-lease`，且必须经用户确认。

## 前置：GitLab Token（一次性）

脚本读取 PAT（读操作 `read_api` scope 即可；创建 MR / 触发流水线需用户提供 `api` scope token，见「写操作分工」）：
1. 命令行参数 `--token <PAT>`
2. 环境变量 `GITLAB_TOKEN`
3. 本地配置文件 `~/.config/gwci/config.json`（推荐，参考 atlassian MCP 方式，见同目录 README.md）

创建：`https://git-rd.office.gritworld.cn/-/profile/personal_access_tokens`（勾选 read_api 即可）

## 工具：ci_monitor.py

```bash
PY=python   # 或你的 Python 解释器路径
S=path/to/ci_monitor.py

$PY $S status                         # 当前 MR 流水线概览 + 各 Job 状态
$PY $S jobs                           # 列出流水线 Job id/name/status
$PY $S log --job <名字> --out x.log   # 下载指定 Job 日志（默认 Build_iOS）
$PY $S errors x.log                   # 从日志提取并分类错误（编译/测试/环境/API）
$PY $S watch --job <名字>             # 等单个 Job 结束，抓日志+摘要（--sha 匹配 commit）
$PY $S monitor [--exclude <名,名>]    # 监控全流水线，任一 Job 失败即立即处理
                                     # 默认排除 Code_Review（特殊 Job 不监控），可用 --exclude "" 关闭
```

## 全流水线闭环工作流（agent 执行）

0. **（开 MR 后）确认流水线已开始**：先查当前 MR 流水线；若状态为 `manual` 或无流水线，
   按「写操作分工」主动触发构建（play manual job / 新建流水线），再进入第 1 步。
   注意 GritMobile（git-prod）的 `.gitlab-ci.yml` 中 merge_request_event 触发的
   `Build_Windows` 是 `when: manual`，不 play 就不会真正开始 build。
1. **监控全流水线**：`monitor --sha <commit>`（后台跑）。它会打印每个 Job 的状态流转，
   直到流水线终态，然后输出：`total/success/failed(blocking/allowed)`，并把每个**阻塞失败**
   Job 的日志存到 `ci_failures/`、用 `errors` 分类。退出码 0=全绿、2=有阻塞失败。
2. **逐个分析失败**：读 monitor 输出的分类结果 + 对应日志。区分：
   - 编译/链接类（compile/linker/undefined-symbol/vtable）→ 改代码；
   - 测试崩溃/断言（test-crash/test-fail）→ 查代码或判 flaky；
   - 环境类（env-device 设备掉线、robocopy、Editor 建工程失败）→ 不阻塞代码，报给对应 owner；
   - API/凭据类（api 403）→ 报管理员，allow_failure 的忽略。
3. **修复代码问题**：最小化修改 → `git add -A && git commit -m "fix(ci): <描述>" && git push`。
   分支常是 `<author>/jira/GME-XXXX`，已关联 MR 到 develop，**push 即自动触发新 MR 流水线**。
4. **回到第 1 步**：再 `monitor --sha <新commit>` 等新结果，循环直到全绿。
5. **收尾**：成功后清理 TEMP-DIAG 等调试代码并单独提交。

## 已知坑

- GritMobile（git-prod.office.gritworld.cn，项目 gm/GritMobile）：MR 流水线的
  `Build_Windows` 在 `merge_request_event` 下是 `when: manual`（pipeline 状态显示 manual），
  `Export_Android` 用 `needs` 等它完成后自动执行——不 play 就不会 build（2026-08-19 实测
  pipeline #28122）。
- 日志噪音多：`DVTPortal`、`DVTDownloadable`、`ld: warning`、`section_start/end` 已被 `errors`
  过滤。分类：job-fail / test-crash / test-fail / env-device / api / env / compile / linker 等。
- **iOS 独有根因（已确诊）**：`scripts/Apple/Developer/IOS/SafeCombineLibraries.py` 合并静态库时，
  多个第三方库 `.o` 重名（`Mesh.o`/`allocator.o`），macOS 大小写不敏感 FS 下 `ar x` 互踩丢符号 →
  `undefined symbol / missing vtable`。**解法 = 把被 GWRenderEngine 内联的 external OBJECT 库
  改成 STATIC**（已改：draco、meshoptimizer；仍 OBJECT 待排查：edtaa3/etc1/iqa/libsquish/
  poly_ftgl/pvrtc/tinyexr）。
- `monitor` 默认把 `Code_Review` 排除在监控外（它无 script 定义，会把流水线卡在 running 数小时）；
  判定「完成」的标准是**所有非排除 Job 到终态**，而非 pipeline 状态。可 `--exclude ""` 恢复监控、
  或 `--exclude A,B` 自定义。超时仍会列出非排除的 still-pending Job。
- bx 源码重复（`external/bx/src/` 与 `Render/GWRenderEngine/source/private/deviceManager/core/bx/`），
  后者仍在被编译进引擎；真正迁移成 STATIC 后再删副本。
- 子模块推送：external 在 `git@git-rd.office.gritworld.cn:AndroidEngine/thirdparty/gwcp3rdparty.git`
  （分支 `<author>/jira/GME-XXXX`）。本地 HEAD/branch 可能被 TortoiseGit/其他工具弄成 detached，
  `git push <branch>` 报 "src refspec does not match any" 时改用
  `git push origin <sha>:refs/heads/<branch>`；主仓库更新子模块指针用
  `git update-index --cacheinfo 160000,<sha>,external`。

## 参考

- CI 配置：仓库根 `.gitlab-ci.yml`；`Build_iOS` 走 `scripts/Apple/CI/BuildExportIOS.zsh -t IOS`。
- 合并脚本：`scripts/Apple/Developer/IOS/SafeCombineLibraries.py`。
