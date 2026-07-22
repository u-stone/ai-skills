# oh-my-openagent-config

Create, review, or upgrade `oh-my-openagent.json` routing configurations.
Model upgrades are catalog-first: discover current provider offerings online,
choose a verified target, then edit and validate the route.

## When to use

- Setting up a new oh-my-openagent.json from scratch
- Upgrading model versions (Claude, GPT, Gemini, DeepSeek)
- Adding/modifying routes for specific work types
- Auditing fallback chains for cost and availability

## When NOT to use

- Editing application code, prompts, LSP settings, or credentials
- Modifying files outside `oh-my-openagent.json` / `opencode.json`
- General configuration questions not related to oh-my-openagent

## Quick start

### Lite (single route change)

```
1. Read both configs
2. Apply targeted edit
3. Validate: parse JSON + terminal fallback invariant
```

### Upgrade (model discovery + version upgrade)

```
1. Read + inventory models
2. Query OpenCode/provider catalogs online
3. Select stable, capability-compatible target
4. Upgrade consistently
5. Full validation + decision manifest
```

### Critical (full audit)

```
Standard + structured review manifest + optional Momus review
```

## Key rules

| Rule | Summary |
|---|---|
| Terminal fallback | Every chain ends with `gwai/deepseek-*` |
| No paid after DeepSeek | Paid models before DeepSeek, never after |
| Visual primary = Gemini | DeepSeek is cost fallback, not visual substitute |
| Exact model IDs | Never invent or abbreviate; verify every ID |
| Catalog-first upgrades | No online evidence, no new-model decision |
| Lifecycle-aware | Prefer stable/GA; document preview/deprecated exceptions |
| No config scope creep | Don't touch credentials, LSP, or prompts |

## Validation pass criteria

- JSON parses
- All model IDs verified
- Discovery source and retrieval time recorded
- Upgrade target is stable/GA and capability-compatible, or exception documented
- Terminal fallback invariant holds
- No paid model after DeepSeek
- Visual primaries use Gemini
- Old model IDs absent (replacements verified)
- Custom DeepSeek entries have no unsupported variants

## Recovery

- Retry budget: 2 per catalog read, 1 per edit, 1 per validation
- 3 failures → hard stop, revert, report
- Missing catalog → use logical labels, never invent IDs

## Output

`EvidenceRecord` + structured `ReviewManifest` for every completed task.

## Runtime deployment

This repository is a selectable skill collection. It is the source of truth,
not an automatically loaded runtime directory. To enable this skill, manually
copy this directory to the runtime skill location, for example:

```powershell
Copy-Item -Recurse -Force `
  "D:\MyGitHub\ai-skills\skills\oh-my-openagent-config" `
  "C:\Users\<user>\.config\opencode\skills\oh-my-openagent-config"
```

After copying, restart the runtime or reload skills. Verify the loaded skill's
frontmatter name is `oh-my-openagent-config` and its description mentions
catalog-first online model discovery. Do not use a junction or automatic sync.
