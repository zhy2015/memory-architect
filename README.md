# Memory Master (zhy2015/memory-master)

A unified memory management skill for OpenClaw agents. This skill consolidates the functionalities of memory archiving, deduplication, distillation, and project context delegation into a single, efficient tool.

## Features & Mechanisms

### 1. The "Three-Tier Memory Dam" (三级记忆水坝)
This skill enforces a strict lifecycle for all agent memory to prevent context bloating and hallucination:
- **Short-term Memory**: `memory/daily/*.md` — Raw, chronological daily conversation logs.
- **Long-term Memory**: `MEMORY.md` / `USER.md` — Highly distilled, generalized rules, facts, and user preferences.
- **Cold Archive**: `memory/distilled/` & `memory/archive/` — Old daily logs that have been processed and moved out of the active context window.

### 2. Daily Journal Distillation
*(See `scripts/daily_distillation_workflow.md`)*
Triggered via system Heartbeats, the agent autonomously scans `memory/daily/` for non-current-day logs, extracts "golden" rules/patterns into `MEMORY.md`, and then moves the original logs to `memory/distilled/` to keep the active daily directory clean.

### 3. Project Context Delegation (项目级记忆下放)
To prevent the global `MEMORY.md` from becoming bloated with specific code deployment steps or debugging logs, the agent is trained to **delegate** project-specific memory. It cuts these details out of the main memory and writes them into a `DEPLOY_MANUAL.md` or `PROJECT_MEMORY.md` directly inside the target project's repository, committing them via Git. The global memory only retains a pointer.

### 4. Skill Auto-Consolidation (上下文收敛)
*(See `scripts/skill_registry_workflow.md`)*
To prevent the `<available_skills>` prompt from overflowing, this tool periodically audits registered skills. High-overlap skills are merged, and atomic tools are symlinked under Task Facades (e.g., `Code-Ops-Node`) rather than exposed globally.

## Usage

This skill is designed to be invoked autonomously by the agent via Heartbeat triggers or when the user explicitly requests maintenance.

**Manual Triggers:**
- "清理记忆" (Clean up memory / Archive)
- "去重记忆" (Deduplicate memory)
- "蒸馏记忆" (Distill memory)
- "分类项目记忆" (Delegate project memory)

By managing these mechanisms, `memory-master` ensures the agent remains lightweight, responsive, and free from the "fabrication gradient" caused by overgrown context windows.
