# AI skill auditing workflow

This repository maintains reusable AI agent skills.

OpenCode loads this file as the project rule file. The detailed skill-auditor prompt is loaded through `opencode.json`:

```json
{
  "instructions": ["skills/requirement.md"]
}
```

When working in an agent that does not support `opencode.json`, read `skills/requirement.md` before auditing, optimizing, or refactoring any skill.
