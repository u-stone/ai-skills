---
name: engineering-master
description: Implements high-rigor industrial software engineering workflows (Plan-Align-Execute-Commit-Review cycle). Use when managing complex, long-term projects that require atomic iterations, strict SSOT alignment, and mandatory manual code reviews.
---

# Engineering Master

## Overview

Engineering Master enforces a high-rigor "Plan-Align-Execute-Commit-Review" implementation cycle to ensure architectural integrity and code quality in complex C++ or other large-scale software projects.

## Core Principles

1.  **Identity & Context First**: Every action begins by consulting the project's Single Source of Truth (SSOT).
2.  **Atomic Iteration**: Break large tasks into the smallest possible functional units.
3.  **Mandatory Review Loop**: Git commit after every atomic unit and pause for user approval.
4.  **Surgical Precision**: Minimal-change updates to existing code and documentation.

## The Engineering Workflow

Follow these steps for EVERY task implementation:

### Step 1: Context Alignment
Before modifying or creating any file:
- Read `plan.md` to identify the current Phase and task.
- Read `naming_convention.md` (SSOT) to ensure all class names, methods, and terms match perfectly.
- Read `coding_standards.md` to align with the project's style (e.g., Google C++ Style, private member suffixes).

### Step 2: Atomic Planning
Decompose the current task into atomic sub-tasks.
- An atomic unit is typically a single method implementation, a single class structure, or a specific logic block.
- Communicate the plan for the next atomic unit to the user.

### Step 3: Precise Execution
Execute the implementation with surgical precision:
- **Code**: English comments, English naming (per SSOT), Google Style.
- **Docs**: Chinese content (per project mandate), detailed technical explanation, minimal structural changes.
- Ensure no line exceeds 100 characters.

### Step 4: Atomic Commit & Pause
Once the atomic unit is verified (compiles/tests pass):
1.  **Git Commit**: Commit only the changes for this specific unit.
    - Format: `[Phase X] Implement/Fix: <brief description>`
2.  **Review Request**: Summarize the changes and request a Code Review.
3.  **MANDATORY PAUSE**: Stop all activities. Wait for the user to provide an "Approved" or "Proceed" command. Do NOT move to the next sub-task automatically.

## Rules of Engagement

- **No Speculative Implementation**: Never implement features not explicitly defined in the plan or approved during review.
- **Glossary Enforcement**: If a term is not in `naming_convention.md`, ask for clarification or propose an addition before using it.
- **Language Segregation**: 
    - Code Comments: English.
    - Technical Documentation: Chinese.
    - Commit Messages: English (Phase tag + description).

## Handling Architectural Conflicts

If you encounter a conflict between the current implementation and the documentation:
1.  Stop implementation.
2.  Report the conflict to the user.
3.  Propose a surgical fix for the documentation before proceeding.

## Essential Project Files

This Skill relies on the following documents as the "Source of Truth" for logical control.

### 1. Roadmap & Tasks (`plan.md`)
*   **Role**: Defines macro phases and micro-task checklists.
*   **Format**: Markdown task lists.
*   **Guideline**: Locate current task before coding; check upon completion.

### 2. Single Source of Truth (`naming_convention.md`)
*   **Role**: Enforces alignment of namespaces, classes, methods, enums, and tokens.
*   **Format**: Categorized table (Term | Type | Description).
*   **Guideline**: Prohibit names not defined in or conflicting with this table.

### 3. Coding Standards (`coding_standards.md`)
*   **Role**: Mandates code style (Google Style), ownership principles, and concurrency strategies.
*   **Format**: Rule-based statements.
*   **Guideline**: Enforce underscore suffix `_`, disable exceptions, and English-only comments.

### 4. Project Mandates (`GEMINI.md`)
*   **Role**: Defines collaboration rhythm (Atomic Commit + Pause) and AI behavioral boundaries.
*   **Format**: High-priority mandates.
*   **Guideline**: The supreme directive for this project, overriding general system settings.

### 5. Architecture Whitepapers (`docs/architecture/*.md`)
*   **Role**: Records deep design motives, state machines, domain models, and scenarios.
*   **Format**: Technical docs including Mermaid diagrams.
*   **Guideline**: Implementation must strictly match the logic loops (e.g., state triggers) defined here.
