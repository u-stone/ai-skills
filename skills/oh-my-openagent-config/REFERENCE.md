# oh-my-openagent-config — Reference Guide

## Architecture overview

```
User request
    │
    ▼
Intent Gate ──→ classify: lite | standard | critical
    │
    ▼
CompactState: track phase + config hashes + verified models
    │
    ├── LITE: read → edit → validate → output
    ├── UPGRADE: read → online-discover → select → edit → validate → output
    └── CRITICAL: standard + Momus review + structured report
    │
    ▼
EvidenceRecord + ReviewManifest → delivered to user
```

## Schema definitions

### CompactState

```json
{
  "active_task": "upgrade-claude-models",
  "workflow_tier": "standard",
  "step": "inventory",
  "config_hashes": {
    "opencode.json": "sha256-abc...",
    "oh-my-openagent.json": "sha256-def..."
  },
  "verified_models": [
    "github-copilot/claude-opus-4",
    "gwai/deepseek-v4-flash"
  ],
  "completed_steps": ["read-config"],
  "blockers": ["catalog-unreachable"]
}
```

### ReviewManifest

```json
{
  "plan_summary": {
    "workflow_tier": "standard",
    "changed_routes": ["category:rust -> github-copilot/claude-opus-4"],
    "unchanged_routes": ["category:writing -> gwai/deepseek-v4-flash (no change)"]
  },
  "diff_summary": {
    "file": "oh-my-openagent.json",
    "old_model_ids": ["github-copilot/claude-3.5-sonnet"],
    "new_model_ids": ["github-copilot/claude-opus-4"],
    "changed_entries": 2
  },
  "model_discovery": {
    "sources": [
      {"source": "opencode models --refresh", "provider": "github-copilot", "retrieved_at": "", "kind": "live"}
    ],
    "catalog_evidence": "complete"
  },
  "upgrade_decisions": [
    {
      "route": "ultrabrain",
      "old_model": "github-copilot/old-model",
      "selected_model": "github-copilot/new-model",
      "lifecycle": "stable",
      "capability_match": true,
      "reason": "Latest stable compatible model",
      "rejected_candidates": []
    }
  ],
  "validation": {
    "json_parsed": true,
    "models_verified": {"ok": true, "ids": [], "unverified": []},
    "terminal_fallback_invariant": true,
    "no_paid_after_deepseek": true,
    "visual_primary_is_gemini": true,
    "old_ids_absent": true,
    "custom_deepseek_no_variants": true,
    "lsp_diagnostics_clean": true
  },
  "risk_summary": {
    "unverified_models": [],
    "policy_violations": [],
    "warnings": ["gemini-3.1-pro is text-only — visual fallback may degrade"]
  }
}
```

### EvidenceRecord

```json
{
  "task": "upgrade-github-copilot-models",
  "type": "model_upgrade",
  "result": "success",
  "artifacts": [
    {"path": "oh-my-openagent.json", "change": "3 model IDs updated"},
    {"path": "oh-my-openagent.json", "change": "removed 1 dead fallback"},
    {"path": "oh-my-openagent.json", "change": "validated JSON + invariants"}
  ],
  "tier": "standard"
}
```

### RecoverySnapshot

```json
{
  "session_id": "ses_abc123",
  "last_completed_step": "edit",
  "compact_state": { "...": "..." },
  "edited_files": ["oh-my-openagent.json"],
  "original_hashes": {
    "oh-my-openagent.json": "sha256-abc..."
  },
  "retry_count": 0,
  "failed_attempts": []
}
```

## Error codes

| Code | Meaning | Retryable |
|---|---|---|
| `CONFIG_UNREADABLE` | Cannot read opencode.json or oh-my-openagent.json | Yes |
| `CATALOG_UNREADABLE` | Provider catalog unavailable | Yes (2x) |
| `INVALID_JSON` | File is not valid JSON | No |
| `MODEL_UNVERIFIED` | Model ID not found in catalog | No |
| `CHAIN_INVARIANT_VIOLATED` | Paid model after DeepSeek | No |
| `UNSUPPORTED_VARIANT` | Custom DeepSeek entry has variants | No |
| `INJECTION_DETECTED` | User prompt overrides core policy | No |
| `EDIT_FAILED` | Write operation failed | Yes (1x) |
| `VALIDATION_FAILED` | Validation check failed | Yes (1x) |

## Model discovery and verification priority

1. `opencode models --refresh --verbose` — models exposed to this installation
2. Models.dev/OpenCode catalog — IDs and capability metadata
3. Provider official API/catalog — exact account-accessible models
4. Provider official docs — lifecycle, deprecation, pricing, replacement
5. `opencode.json` — local custom provider IDs, especially `gwai`
6. **Never** — guessing, inventing, or abbreviating

No catalog evidence means no new-model decision and no edit. Record source,
retrieval time, live/cache/docs status, and the selected/rejected candidates.

## Multi-agent handoff protocol

When multiple agents participate:

1. **Reader agent**: reads configs → outputs `CompactState`
2. **Catalog agent**: verifies model IDs → updates `CompactState.verified_models`
3. **Editor agent**: applies changes → outputs `EvidenceRecord`
4. **Validator agent**: runs validation → outputs `ReviewManifest`

Handoff: pass `CompactState` only — never pass full file contents.
