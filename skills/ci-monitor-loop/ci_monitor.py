#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitLab CI monitor & auto-fix loop helper for GWCPEngine.

Purpose
-------
On Windows many issues cannot be reproduced locally (iOS clang/arm64 compile/link,
Android device tests, visual regression, ...). The only way to verify is: push ->
CI MR pipeline -> read the job logs. This script automates the "read the CI
result" half of that loop for the WHOLE pipeline:

    status   show the latest pipeline + its jobs for the current branch
    jobs     list jobs of a pipeline (default: latest on current branch)
    log      download a job's trace to a local file (default: Build_iOS -> error.log)
    errors   extract and classify error lines from a downloaded log
    watch    poll the pipeline until the target job finishes, then download the
             log and print an error summary (blocks)
    monitor  wait for the whole pipeline (all non-excluded jobs) to finish, then
             fetch every blocking-failed job's log + classify its errors; this is
             the core of the monitor -> analyze -> fix -> push -> monitor loop

Auth
----
Reads a GitLab Personal Access Token (scope: read_api is enough; api if you
also want to trigger pipelines) from, in order:
    1. --token command-line argument
    2. environment variable GITLAB_TOKEN
    3. local JSON config file ~/.config/gwci/config.json  ("gitlab_token"
       field; see CONFIG below) -- recommended, never commit this file

CONFIG
------
Optional JSON config at ~/.config/gwci/config.json (override with --config).
The file lives OUTSIDE the git repo; never commit it.

Multi-server format (recommended; pick one with --server NAME):

    {
      "default": "git-rd",
      "servers": {
        "git-rd": {
          "gitlab_host": "https://git-rd.office.gritworld.cn",
          "gitlab_project": "AndroidEngine/GWCPEngine",
          "gitlab_token": "<PAT>"
        },
        "git-prod": {
          "gitlab_host": "https://git-prod.office.gritworld.cn",
          "gitlab_project": "gm/GritMobile",
          "gitlab_token": "<PAT>"
        }
      }
    }

Legacy single-server format (still supported):

    {
      "gitlab_host": "https://git-rd.office.gritworld.cn",
      "gitlab_project": "AndroidEngine/GWCPEngine",
      "gitlab_token": "<PAT>"
    }

Create the token at:
    https://git-rd.office.gritworld.cn/-/profile/personal_access_tokens

Usage examples
--------------
    python ci_monitor.py status                          # default server
    python ci_monitor.py --server git-prod status        # named server
    python ci_monitor.py jobs
    python ci_monitor.py log --job Build_iOS --out error.log
    python ci_monitor.py errors error.log
    python ci_monitor.py watch --job Build_iOS --interval 30 --timeout 3600
    python ci_monitor.py monitor --sha <commit>     # whole-pipeline monitor
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

DEFAULT_HOST = "https://git-rd.office.gritworld.cn"
DEFAULT_PROJECT = "AndroidEngine/GWCPEngine"
DEFAULT_JOB = "Build_iOS"

# ---------------------------------------------------------------------------
# config / auth
# ---------------------------------------------------------------------------

def _config_path():
    p = os.environ.get("GWCI_CONFIG")
    if p:
        return p
    return os.path.join(os.path.expanduser("~"), ".config", "gwci", "config.json")


def load_config(path=None):
    """Read the optional local JSON config (host/project/token). Returns {} if
    missing or unreadable. The file lives outside the git repo (never commit it)."""
    path = path or _config_path()
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, dict):
            return {}
        return data
    except Exception as e:
        print("WARNING: cannot read config {}: {}".format(path, e), file=sys.stderr)
        return {}


def select_server(config, name=None):
    """Resolve one server entry from config. Supports two formats:

    1. multi-server (new, recommended):
       {"default": "git-rd",
        "servers": {"git-rd": {"gitlab_host": ..., "gitlab_project": ...,
                               "gitlab_token": ...},
                    "git-prod": {...}}}
    2. legacy single-server (old): top-level gitlab_host/project/token keys.

    Selection order: --server name > config["default"] > the only server if
    exactly one. Returns a flat dict (host/project/token), or {} when nothing
    matches; an unmatched explicit name logs a warning listing available keys."""
    config = config or {}
    servers = config.get("servers")
    if isinstance(servers, dict) and servers:
        if not name:
            name = config.get("default")
        if not name:
            keys = list(servers.keys())
            if len(keys) == 1:
                name = keys[0]
        if name and name in servers:
            return dict(servers[name])
        print("WARNING: server '{}' not in config (available: {}).".format(
            name or "", ", ".join(sorted(servers.keys()))), file=sys.stderr)
        return {}
    # legacy flat single-server config
    return config


def resolve_token(args_token=None, config=None):
    config = config or {}
    tok = (args_token or "").strip()
    if tok:
        return tok
    tok = os.environ.get("GITLAB_TOKEN", "").strip()
    if tok:
        return tok
    tok = str(config.get("gitlab_token", "") or "").strip()
    if tok:
        return tok
    return None


def api_request(host, token, path, params=None):
    url = host.rstrip("/") + "/api/v4" + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url)
    if token:
        req.add_header("PRIVATE-TOKEN", token)
    req.add_header("User-Agent", "gw-ios-ci-loop")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:500]
        return e.code, {"error": body}


def project_id(project):
    return urllib.parse.quote(project, safe="")


def current_branch():
    # read branch from the git repo in cwd
    try:
        import subprocess
        out = subprocess.check_output(
            ["git", "branch", "--show-current"], stderr=subprocess.DEVNULL
        ).decode("utf-8", "replace").strip()
        return out or None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# api helpers
# ---------------------------------------------------------------------------

def latest_pipeline(host, token, project, ref):
    pid = project_id(project)
    status, data = api_request(
        host, token, "/projects/{}/pipelines".format(pid),
        {"ref": ref, "order_by": "id", "sort": "desc", "per_page": 1},
    )
    if status != 200:
        print("ERROR fetching pipelines:", data, file=sys.stderr)
        return None
    if not data:
        return None
    return data[0]


def ci_lint(host, token, project, ref):
    """Validate the CI YAML (with includes resolved) for a ref via GitLab's
    CI Lint API. Returns (valid, errors, warnings):
      - valid:   None when the API call itself failed (unreachable/HTTP error),
                 True when config is valid, False when yaml_errors exist
      - errors:  list of yaml_errors strings (empty when valid)
      - warnings: list of lint warnings
    Catches config problems that make pipelines fail at creation with 0 jobs
    (e.g. rules rejecting all jobs, hooks nesting too deep), reporting the
    precise GitLab error message."""
    pid = project_id(project)
    status, data = api_request(
        host, token, "/projects/{}/ci/lint".format(pid),
        {"content_ref": ref, "include_merged_yaml": "true"},
    )
    if status != 200:
        return None, ["lint API HTTP {}: {}".format(status, data)], []
    errors = data.get("errors") or []
    warnings = data.get("warnings") or []
    return bool(data.get("valid")) and not errors, errors, warnings


def find_mr(host, token, project, source_branch):
    """Return the full MR object (incl. head_pipeline) for the first open MR
    whose source branch is source_branch, or None. The list endpoint omits
    head_pipeline, so we re-fetch the single MR by iid."""
    pid = project_id(project)
    status, data = api_request(
        host, token, "/projects/{}/merge_requests".format(pid),
        {"source_branch": source_branch, "state": "opened", "per_page": 1},
    )
    if status != 200 or not data:
        return None
    iid = data[0].get("iid")
    status2, full = api_request(
        host, token, "/projects/{}/merge_requests/{}".format(pid, iid),
    )
    if status2 == 200 and full:
        return full
    return data[0]


def git_head_sha():
    try:
        import subprocess
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode("utf-8", "replace").strip()
        return out or None
    except Exception:
        return None


def _sha_matches(candidate, expected):
    if expected is None:
        return True
    return (candidate or "").lower().startswith(expected.lower())


def active_pipeline(host, token, project, ref, expected_sha=None):
    """Return the pipeline that actually runs Build_iOS for this branch.

    Build_iOS only runs in the merge-request pipeline (ref
    'refs/merge-requests/<iid>/head'), NOT in the push/branch pipeline. So we
    prefer the open MR's head_pipeline; fall back to the latest branch pipeline.
    If expected_sha is given, only return a pipeline whose sha matches (so we
    never watch a stale pre-push pipeline)."""
    mr = find_mr(host, token, project, ref)
    if mr:
        hp = mr.get("head_pipeline") or {}
        if hp.get("id") and _sha_matches(hp.get("sha"), expected_sha):
            return hp
    pl = latest_pipeline(host, token, project, ref)
    if pl and _sha_matches(pl.get("sha"), expected_sha):
        return pl
    return None


def pipeline_jobs(host, token, project, pipeline_id):
    pid = project_id(project)
    status, data = api_request(
        host, token,
        "/projects/{}/pipelines/{}/jobs".format(pid, pipeline_id),
        {"per_page": 100},
    )
    if status != 200:
        print("ERROR fetching jobs:", data, file=sys.stderr)
        return []
    return data


def find_job(host, token, project, pipeline_id, job_name):
    for j in pipeline_jobs(host, token, project, pipeline_id):
        if j.get("name") == job_name:
            return j
    return None


def job_trace(host, token, project, job_id):
    pid = project_id(project)
    url = host.rstrip("/") + "/api/v4/projects/{}/jobs/{}/trace".format(pid, job_id)
    req = urllib.request.Request(url)
    if token:
        req.add_header("PRIVATE-TOKEN", token)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return "[trace error {}]".format(e.code)


# ---------------------------------------------------------------------------
# error extraction
# ---------------------------------------------------------------------------

NOISE_PATTERNS = [
    r"ld: warning",
    r"DVTPortal",
    r"DVTDownloadable",
    r"section_start",
    r"section_end",
    r"Resolving secrets",
    r"Preparing the",
    r"Running with gitlab-runner",
    r"Getting source from",
    r"Removing ",
    r"note: ",
    r"warning: ",
    r"collapsed multi-line command",
]

SIGNAL_PATTERNS = [
    # compile / link
    (r"fatal error", "fatal"),
    (r"Undefined symbol|undefined symbol", "undefined-symbol"),
    (r"symbol\(s\) not found", "linker"),
    (r"missing vtable", "vtable"),
    (r"\*\* BUILD FAILED \*\*", "build-fail"),
    (r"linker command failed", "linker"),
    (r"TEMP-DIAG.*(MISSING|LOST|!!)", "diag"),
    (r"no member named|undeclared|use of undeclared", "compile-error"),
    (r"clang: error|: error|error C[0-9]+", "compile-error"),
    (r"Script .* build failed", "script"),
    # universal / runtime / test / environment / api
    (r"(?i)job failed|exit status", "job-fail"),
    (r"(?i)exited with code|did not exit cleanly|process.*exited", "test-crash"),
    (r"(?i)access violation|0xc0000005|segmentation fault|stack overflow", "crash"),
    (r"(?i)tests? failed|result\.xml not found|new baselines", "test-fail"),
    (r"(?i)adb devices|findstr.*Device_ID|device.*(offline|not found)", "env-device"),
    (r"(?i)llm.*(fail|失败)|http 40[0-9]|普通用户不支持|forbidden|unauthorized", "api"),
    (r"(?i)robocopy.*(fail|return code)|not available or failed", "env"),
    (r"(?i)error:", "error"),
]


def extract_errors(text):
    """Return a list of (kind, line) for the interesting lines."""
    noise = [re.compile(p) for p in NOISE_PATTERNS]
    signals = [(re.compile(p), k) for p, k in SIGNAL_PATTERNS]
    out = []
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if any(n.search(line) for n in noise):
            continue
        for rx, kind in signals:
            if rx.search(line):
                out.append((kind, line))
                break
    return out


def summarize_errors(text, max_lines=60):
    errs = extract_errors(text)
    if not errs:
        tail = [l.rstrip() for l in text.splitlines() if l.strip()][-15:]
        return "No signature matched; last 15 log lines:\n" + "\n".join(tail)
    lines = []
    for kind, line in errs[:max_lines]:
        lines.append("[{}] {}".format(kind, line))
    if len(errs) > max_lines:
        lines.append("... (+{} more)".format(len(errs) - max_lines))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def cmd_status(args, host, token):
    ref = args.ref or current_branch()
    if not ref:
        print("Cannot determine branch; pass --ref.", file=sys.stderr)
        return 1
    pl = active_pipeline(host, token, args.project, ref)
    if not pl:
        print("No pipeline found for ref '{}'.".format(ref))
        return 1
    print("Pipeline #{id}  status={status}  ref={ref}  sha={sha}".format(
        id=pl.get("id"), status=pl.get("status"), ref=pl.get("ref"),
        sha=(pl.get("sha") or "")[:8]))
    print("URL: {}/-/pipelines/{}".format(host.rstrip("/"), pl.get("id")))
    print("-" * 60)
    jobs = pipeline_jobs(host, token, args.project, pl.get("id"))
    for j in jobs:
        print("{name:<28} {stage:<12} {status}".format(
            name=j.get("name", ""), stage=j.get("stage", ""),
            status=j.get("status", "")))
    return 0


def cmd_jobs(args, host, token):
    ref = args.ref or current_branch()
    pl = active_pipeline(host, token, args.project, ref)
    if not pl:
        print("No pipeline found.", file=sys.stderr)
        return 1
    jobs = pipeline_jobs(host, token, args.project, pl.get("id"))
    for j in jobs:
        print("{id}\t{name}\t{stage}\t{status}".format(
            id=j.get("id"), name=j.get("name", ""),
            stage=j.get("stage", ""), status=j.get("status", "")))
    return 0


def cmd_log(args, host, token):
    ref = args.ref or current_branch()
    pl = active_pipeline(host, token, args.project, ref)
    if not pl:
        print("No pipeline found.", file=sys.stderr)
        return 1
    job = find_job(host, token, args.project, pl.get("id"), args.job)
    if not job:
        print("Job '{}' not found in pipeline #{}.".format(args.job, pl.get("id")),
              file=sys.stderr)
        return 1
    print("Job '{}' id={} status={}".format(job.get("name"), job.get("id"),
                                             job.get("status")))
    trace = job_trace(host, token, args.project, job.get("id"))
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(trace)
    print("Saved {} bytes -> {}".format(len(trace), args.out))
    return 0


def cmd_errors(args, host, token):
    with open(args.log, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    print(summarize_errors(text, args.max_lines))
    return 0


def _wait_for(desc, fetch, poll_interval=10, wait_timeout=180):
    """Retry fetch() until it returns a truthy value or wait_timeout passes.
    Returns the value or None. Used to ride out the post-push window where the
    pipeline/job has not been created yet."""
    start = time.time()
    last = None
    while time.time() - start < wait_timeout:
        last = fetch()
        if last:
            return last
        print("[{}] waiting for {} to appear ...".format(
            time.strftime("%H:%M:%S"), desc))
        time.sleep(poll_interval)
    return last


def cmd_lint(args, host, token):
    """Validate the CI YAML (with includes resolved) for a ref via GitLab's
    CI Lint API. Catches config errors (rules rejecting all jobs, hooks
    nesting too deep, ...) that make pipelines fail at creation with 0 jobs,
    reporting the precise GitLab error message BEFORE pushing/waiting."""
    ref = args.ref or current_branch()
    if not ref:
        print("Cannot determine branch; pass --ref.", file=sys.stderr)
        return 1
    valid, errors, warnings = ci_lint(host, token, args.project, ref)
    if valid is None:
        print("LINT API unavailable: {}".format(errors))
        return 1
    print("lint {} (ref={})".format("VALID" if valid else "INVALID", ref))
    for w in warnings:
        print("  warning: {}".format(w))
    for e in errors:
        print("  error:   {}".format(e))
    return 0 if valid else 2


def cmd_watch(args, host, token):
    ref = args.ref or current_branch()
    if not ref:
        print("Cannot determine branch; pass --ref.", file=sys.stderr)
        return 1
    expected_sha = args.sha or git_head_sha()

    # 1) wait for the pipeline for THIS commit to appear (push -> MR pipeline
    #    has a few seconds of lag; match on sha so we never watch a stale one).
    pl = _wait_for(
        "pipeline for sha {} (MR '{}')".format(
            (expected_sha or "?")[:8], ref),
        lambda: active_pipeline(host, token, args.project, ref, expected_sha),
        poll_interval=10, wait_timeout=180,
    )
    if not pl:
        print("No pipeline for sha {} appeared on '{}' within 180s.".format(
            (expected_sha or "?")[:8], ref), file=sys.stderr)
        return 1
    print("Watching pipeline #{} (source={} ref={} sha={}) for job '{}' ...".format(
        pl.get("id"), pl.get("source"), pl.get("ref"),
        (pl.get("sha") or "")[:8], args.job))

    # 2) wait for the job to be listed (jobs are created shortly after the
    #    pipeline); the Build stage may also be delayed by needs/dependencies.
    job = _wait_for(
        "job '{}' in pipeline #{}".format(args.job, pl.get("id")),
        lambda: find_job(host, token, args.project, pl.get("id"), args.job),
        poll_interval=10, wait_timeout=300,
    )
    if not job:
        print("Job '{}' not found in pipeline #{} within 300s.".format(
            args.job, pl.get("id")), file=sys.stderr)
        return 1

    terminal = {"success", "failed", "canceled", "skipped", "manual"}
    start = time.time()
    deadline = start + args.timeout
    last_status = None
    while time.time() < deadline:
        status, data = api_request(
            host, token,
            "/projects/{}/jobs/{}".format(project_id(args.project), job.get("id")),
        )
        st = (data or {}).get("status") if status == 200 else job.get("status")
        if st != last_status:
            print("[{}] job status -> {}".format(
                time.strftime("%H:%M:%S"), st))
            last_status = st
        if st in terminal:
            break
        time.sleep(args.interval)

    trace = job_trace(host, token, args.project, job.get("id"))
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(trace)
    print("=" * 60)
    print("Job '{}' finished with status: {}".format(args.job, last_status))
    print("Log saved -> {} ({} bytes)".format(args.out, len(trace)))
    print("=" * 60)
    print(summarize_errors(trace, args.max_lines))
    return 0 if last_status == "success" else 2


TERMINAL_PIPELINE = {"success", "failed", "canceled", "skipped"}
TERMINAL_JOB = {"success", "failed", "canceled", "skipped", "manual"}
DEFAULT_EXCLUDED_JOBS = "Code_Review"


def _ts():
    return time.strftime("%H:%M:%S")


def _print_lint_diag(host, token, project, ref):
    """Best-effort: lint the branch config and print the precise GitLab
    yaml_errors when a pipeline fails to produce jobs (CONFIG-FAIL)."""
    try:
        ok, errs, warns = ci_lint(host, token, project, ref)
    except Exception as e:  # noqa: BLE001 - diagnostic path, never crash the loop
        print("    (lint diag unavailable: {})".format(e))
        return
    if ok is False:
        print("    CI YAML INVALID on '{}':".format(ref))
        for e in errs:
            print("      error: {}".format(e))
    elif ok is None:
        print("    (lint diag unavailable: {})".format(errs))
    elif warns:
        print("    lint warnings on '{}':".format(ref))
        for w in warns:
            print("      warning: {}".format(w))


def cmd_monitor(args, host, token):
    """Monitor ALL jobs of the active pipeline until it finishes, then fetch
    every blocking-failed job's log and summarize its errors.

    This is the 'watch the whole CI' half of the loop:
      monitor -> analyze failures -> fix code -> push -> monitor again."""
    ref = args.ref or current_branch()
    if not ref:
        print("Cannot determine branch; pass --ref.", file=sys.stderr)
        return 1
    expected_sha = args.sha or git_head_sha()

    if args.pipeline:
        st, pdata = api_request(
            host, token,
            "/projects/{}/pipelines/{}".format(project_id(args.project), args.pipeline),
        )
        pl = pdata if st == 200 else None
        if not pl:
            print("Pipeline #{} not found.".format(args.pipeline), file=sys.stderr)
            return 1
    else:
        pl = _wait_for(
            "pipeline for sha {}".format((expected_sha or "?")[:8]),
            lambda: active_pipeline(host, token, args.project, ref, expected_sha),
            poll_interval=10, wait_timeout=180,
        )
        if not pl:
            print("No pipeline appeared for sha {} on '{}'.".format(
                (expected_sha or "?")[:8], ref), file=sys.stderr)
            return 1
    pid = pl.get("id")
    print("[{}] Monitoring pipeline #{} (source={} ref={} sha={})".format(
        _ts(), pid, pl.get("source"), pl.get("ref"), (pl.get("sha") or "")[:8]))

    # Pre-flight: validate the CI config (includes resolved) for this branch.
    # Catches yaml_errors that make pipelines fail at creation with 0 jobs
    # (e.g. rules rejecting all jobs, hooks nesting too deep) and reports the
    # precise GitLab error instead of timing out waiting for jobs that never
    # appear. `--pipeline` monitors an already-created pipeline, so linting
    # then is informational only.
    if not args.pipeline:
        lint_ok, lint_errs, lint_warns = ci_lint(host, token, args.project, ref)
        if lint_ok is False:
            print("[{}] CONFIG-FAIL: CI YAML INVALID on '{}' -> fix before monitoring:".format(
                _ts(), ref))
            for e in lint_errs:
                print("    error: {}".format(e))
            return 2
        for w in lint_warns:
            print("[{}] lint warning: {}".format(_ts(), w))
        if lint_ok is None:
            print("[{}] lint pre-check skipped (API error): {}".format(_ts(), lint_errs))

    excluded = {n.strip() for n in (args.exclude or "").split(",") if n.strip()}
    if excluded:
        print("[{}] excluded from monitor: {}".format(_ts(), ", ".join(sorted(excluded))))

    def relevant(j):
        return j.get("name") not in excluded

    # poll jobs until all non-excluded jobs reach a terminal state, OR any
    # non-excluded job FAILS (fail-fast: stop waiting and start handling the
    # failure immediately, so a slow / stuck sibling job no longer blocks us).
    start = time.time()
    deadline = start + args.timeout
    pst = None
    last_jobs = {}
    done = False
    early_fail = False
    empty_poll_count = 0  # 连续检测到"流水线无 job"的轮询次数（配置失败信号）
    while time.time() < deadline:
        st, pdata = api_request(
            host, token,
            "/projects/{}/pipelines/{}".format(project_id(args.project), pid),
        )
        new_pst = pdata.get("status") if st == 200 else None
        if new_pst != pst:
            print("[{}] pipeline -> {}".format(_ts(), new_pst))
            pst = new_pst
        jobs = pipeline_jobs(host, token, args.project, pid)
        rel = [j for j in jobs if relevant(j)]
        for j in rel:
            jid = j.get("id")
            jst = j.get("status")
            prev = last_jobs.get(jid)
            if prev is not None and prev != jst:
                print("[{}]   job {:<28} -> {} (id={})".format(_ts(), j.get("name"), jst, jid))
            last_jobs[jid] = jst
        if any(j.get("status") == "failed" and not j.get("allow_failure") for j in rel):
            print("[{}] FAIL-FAST: a blocking job failed -> stop waiting, handle now".format(_ts()))
            done = True
            early_fail = True
            break
        if rel and all(j.get("status") in TERMINAL_JOB for j in rel):
            done = True
            break
        # 配置失败检测: 流水线已终态但没有任何(相关) job, 或连续多轮 job 列表为空。
        # 常见原因: .gitlab-ci.yml 的 rules 阻止了所有 job (0 秒创建即 failed),
        # 或 pipeline 被跳过。此时轮询永远等不到 job 终态, 必须主动识别。
        if pst in TERMINAL_PIPELINE and not rel:
            print("[{}] CONFIG-FAIL: pipeline #{} is {} but has NO (relevant) jobs "
                  "-> CI config (rules/include) likely rejected all jobs".format(
                      _ts(), pid, pst))
            _print_lint_diag(host, token, args.project, ref)
            return 2
        if not rel:
            empty_poll_count += 1
            if empty_poll_count >= 3:
                print("[{}] CONFIG-FAIL: pipeline #{} returned no jobs for {} consecutive polls "
                      "-> CI config may be broken (0 jobs created)".format(
                          _ts(), pid, empty_poll_count))
                _print_lint_diag(host, token, args.project, ref)
                return 2
        else:
            empty_poll_count = 0
        time.sleep(args.interval)
    if not done:
        print("[{}] Timed out; still waiting on jobs in progress.".format(_ts()))
        pending = [j for j in pipeline_jobs(host, token, args.project, pid)
                   if relevant(j) and j.get("status") in ("running", "pending", "created")]
        for j in pending:
            print("  still pending: {} (id={}, status={}, started={})".format(
                j.get("name"), j.get("id"), j.get("status"), j.get("started_at")))
        if not pending and pst in TERMINAL_PIPELINE:
            print("  -> pipeline #{} ended {} but no relevant jobs tracked; "
                  "likely CI config rejected all jobs (rules/include)".format(pid, pst))
        return 1

    jobs = pipeline_jobs(host, token, args.project, pid)
    rel = [j for j in jobs if relevant(j)]
    failed = [j for j in rel if j.get("status") == "failed"]
    blocking = [j for j in failed if not j.get("allow_failure")]
    allowed = [j for j in failed if j.get("allow_failure")]
    n_success = sum(1 for j in rel if j.get("status") == "success")

    print("=" * 66)
    print("Pipeline #{} monitor-complete (pipeline status: {}{})".format(
        pid, pst, " [early-fail: still more jobs running]" if early_fail else ""))
    print("jobs: total={} success={} failed={} (blocking={} allowed={}) excluded={}".format(
        len(jobs), n_success, len(failed), len(blocking), len(allowed), len(jobs) - len(rel)))
    for j in jobs:
        if not relevant(j):
            print("  [excluded] {} -> {} (id={})".format(j.get("name"), j.get("status"), j.get("id")))
    if early_fail:
        still_running = [j for j in rel if j.get("status") in ("running", "pending", "created")]
        for j in still_running:
            print("  [still-running] {} (id={}, status={})".format(
                j.get("name"), j.get("id"), j.get("status")))
    print("=" * 66)

    try:
        os.makedirs(args.out_dir, exist_ok=True)
    except OSError:
        pass

    for j in blocking:
        name, jid = j.get("name"), j.get("id")
        print("\n--- FAILED(blocking): {} (job {}) ---".format(name, jid))
        trace = job_trace(host, token, args.project, jid)
        out_path = os.path.join(args.out_dir, "{}_{}.log".format(jid, name))
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(trace)
        print("  log -> {}".format(out_path))
        print(summarize_errors(trace, args.max_lines))

    for j in allowed:
        print("\n--- FAILED(allowed, 不阻塞): {} (job {}) ---".format(
            j.get("name"), j.get("id")))

    print("=" * 66)
    if blocking:
        print("{} blocking job(s) failed -> 定位修复后重新提交，再 monitor。".format(len(blocking)))
        return 2
    print("All jobs passed (allowed failures ignored).")
    return 0


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(description="GWCPEngine CI monitor & auto-fix loop helper")
    p.add_argument("--host", default=None, help="GitLab host (default: config file or %s)" % DEFAULT_HOST)
    p.add_argument("--project", default=None, help="GitLab project (default: config file or %s)" % DEFAULT_PROJECT)
    p.add_argument("--server", default=None,
                   help="named server entry in multi-server config (config['servers'] key)")
    p.add_argument("--config", default=None,
                   help="JSON config file (default: ~/.config/gwci/config.json)")
    p.add_argument("--token", default=None, help="GitLab PAT (overrides config/env/file)")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="show latest pipeline + jobs")
    s.add_argument("--ref", default=None)

    j = sub.add_parser("jobs", help="list jobs of latest pipeline")
    j.add_argument("--ref", default=None)

    l = sub.add_parser("log", help="download job trace")
    l.add_argument("--ref", default=None)
    l.add_argument("--job", default=DEFAULT_JOB)
    l.add_argument("--out", default="error.log")

    e = sub.add_parser("errors", help="extract errors from a log file")
    e.add_argument("log")
    e.add_argument("--max-lines", type=int, default=60)

    li = sub.add_parser("lint", help="validate CI YAML (includes resolved) for a ref")
    li.add_argument("--ref", default=None)

    w = sub.add_parser("watch", help="poll job until done, then fetch log")
    w.add_argument("--ref", default=None)
    w.add_argument("--sha", default=None, help="commit sha to match (overrides git rev-parse HEAD)")
    w.add_argument("--job", default=DEFAULT_JOB)
    w.add_argument("--out", default="error.log")
    w.add_argument("--interval", type=int, default=30)
    w.add_argument("--timeout", type=int, default=3600)
    w.add_argument("--max-lines", type=int, default=60)

    m = sub.add_parser("monitor",
                       help="watch ALL jobs until pipeline finishes, fetch failed logs")
    m.add_argument("--ref", default=None)
    m.add_argument("--sha", default=None, help="commit sha to match (overrides git rev-parse HEAD)")
    m.add_argument("--pipeline", type=int, default=None,
                   help="target a specific pipeline id (overrides sha matching)")
    m.add_argument("--exclude", default=DEFAULT_EXCLUDED_JOBS,
                   help="comma-separated job names to ignore (default: Code_Review)")
    m.add_argument("--out-dir", default="ci_failures",
                   help="directory to save failed job logs")
    m.add_argument("--interval", type=int, default=30)
    m.add_argument("--timeout", type=int, default=7200)
    m.add_argument("--max-lines", type=int, default=60)
    return p


def main():
    # Windows console defaults to GBK; CI logs contain emoji / non-GBK chars,
    # so re-encode stdout/stderr as UTF-8 with lossy fallback instead of crashing.
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    args = build_parser().parse_args()

    # errors only reads a local file; no network/token needed.
    if args.cmd == "errors":
        return cmd_errors(args, args.host or DEFAULT_HOST, None)

    config = load_config(args.config)
    cfg = select_server(config, args.server)
    host = args.host or cfg.get("gitlab_host") or DEFAULT_HOST
    project = args.project or cfg.get("gitlab_project") or DEFAULT_PROJECT
    args.project = project

    token = resolve_token(args_token=args.token, config=cfg)
    if not token:
        print("No GitLab token found.", file=sys.stderr)
        print("Set GITLAB_TOKEN, or write {} with a 'gitlab_token' field.".format(
            _config_path()), file=sys.stderr)
        return 1
    return {
        "status": cmd_status,
        "jobs": cmd_jobs,
        "log": cmd_log,
        "lint": cmd_lint,
        "watch": cmd_watch,
        "monitor": cmd_monitor,
    }[args.cmd](args, host, token)


if __name__ == "__main__":
    sys.exit(main())
