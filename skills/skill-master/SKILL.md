---
name: skill-master
description: A meta-skill for managing, auditing, and optimizing the Gemini CLI skill ecosystem. Use this skill when creating new skills, updating existing ones, or auditing the skill library. It ensures the `skills_map.md` registry is kept in sync.
---

# Skill Master: The Guardian of Skills

This skill empowers you to act as the architect of the Gemini CLI skill library. 
Its primary directive is to ensure high quality, consistency, and discoverability across all skills.

## Core Workflows

### 1. Creating a New Skill (Registration)
**Trigger**: "Create a new skill for X"
**Process**:
1.  **Analyze**: Determine if the skill is necessary (vs. generic prompt).
2.  **Scaffold**: Use `skill-creator` instructions to build the directory.
3.  **Register**: **MANDATORY**. You MUST append a new entry to `~/.gemini/skills_map.md`.
    *   Initialize Version at `0.1.0`.
    *   Set Status to `Active` or `Experimental`.

### 2. Updating a Skill (Maintenance)
**Trigger**: "Update the X skill" or "Fix a bug in X skill"
**Process**:
1.  **Edit**: Modify the `SKILL.md` or resources.
2.  **Bump Version**: Increment the version in `skills_map.md` (Patch for fixes, Minor for features).
3.  **Update Date**: Set `Last Updated` to today's date.
4.  **Log Limitations**: If the update introduces or reveals a limitation, record it in the map.

### 3. Auditing (Optimization)
**Trigger**: "Audit my skills" or "Check for obsolete skills"
**Process**:
1.  **Read Map**: Read `~/.gemini/skills_map.md`.
2.  **Verify**: Check if listed skills actually exist in `~/.gemini/skills/`.
3.  **Review**: For each skill, ask:
    *   Is the `description` strictly under 100 words?
    *   Does it follow the "Progressive Disclosure" principle?
    *   Are the examples still valid?
4.  **Report**: Generate a Markdown report of issues found.

## The Skills Map Schema

Location: `~/.gemini/skills_map.md`

| Column | Description |
| :--- | :--- |
| **Skill Name** | Exact folder name (kebab-case). |
| **Version** | SemVer (e.g., 1.2.0). |
| **Last Updated**| YYYY-MM-DD. |
| **Status** | `Active`, `Deprecated`, `Experimental`. |
| **Known Limitations** | Concise warning about what the skill CANNOT do. |

## Best Practices for Skill Design
*   **Single Responsibility**: A skill should do one thing well.
*   **Reference Over Context**: Move long texts to `references/` files.
*   **Atomic Scripts**: Scripts should be self-contained and assume standard environments.