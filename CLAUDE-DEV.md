# Claude Code — Full Arsenal Configuration

> Drop-in CLAUDE.md to unlock the full potential of Claude Code skills, workflows, and quality gates. Language-agnostic. Copy to any project as `CLAUDE.md`.

## Core Principle: Skills First

Before responding to ANY request, check if a skill applies. Even a 1% chance means invoke it. Skills are loaded via the `Skill` tool — never read skill files directly.

**Priority order when multiple skills apply:**
1. Process skills first (brainstorming, systematic-debugging) — they determine HOW to approach
2. Implementation skills second (frontend-design, mcp-builder, dotnet-dev, etc.) — they guide execution

## Development Workflow

All non-trivial work follows this chain. Do not skip steps.

```
brainstorming → writing-plans → [executing-plans | subagent-driven-development] → finishing-a-development-branch
```

- **Before creating features, components, or modifying behavior**: invoke `brainstorming`. Get design approval before writing code.
- **Before writing code**: invoke `writing-plans`. Break work into bite-sized tasks (2-5 min each). Save plan to `docs/plans/`.
- **To execute**: choose `executing-plans` (batched with human review checkpoints) or `subagent-driven-development` (faster, same session, agent review).
- **When done**: invoke `finishing-a-development-branch` to verify tests and present merge/PR/keep/discard options.

**Slash commands** for the workflow:
- `/brainstorm` — explore requirements and design before implementation
- `/write-plan` — create detailed implementation plan
- `/execute-plan` — execute plan in batches with review checkpoints

## Quality Gates

These are non-negotiable. They use "Iron Law" enforcement — no exceptions.

### Test-Driven Development
Invoke `test-driven-development` when implementing any feature or bugfix. Write a failing test FIRST, then implement minimally, then verify. Red-Green-Refactor.

### Systematic Debugging
Invoke `systematic-debugging` when encountering any bug, test failure, or unexpected behavior. Find root cause BEFORE proposing fixes. If 3+ fixes fail, question the architecture.

### Verification Before Completion
Invoke `verification-before-completion` before claiming ANY work is complete, fixed, or passing. Run the actual verification command, read the output, THEN make the claim. Evidence before assertions.

### Code Review
- Invoke `requesting-code-review` after completing major features or before merging — dispatches a code-reviewer subagent.
- Invoke `code-reviewer` when a major project step needs review against the plan.
- Invoke `receiving-code-review` when processing feedback — verify technically before implementing, push back when wrong.

## Parallel Work

Invoke `dispatching-parallel-agents` when facing 2+ independent tasks (different test files, different subsystems, different bugs). One agent per problem domain, running concurrently.

## Git Workflow

- Invoke `using-git-worktrees` when starting feature work that needs isolation from the current workspace.
- Invoke `finishing-a-development-branch` when implementation is complete and tests pass.
- Never force-push, skip hooks, or take destructive git actions without explicit user confirmation.

## Language & Stack Skills

Invoke the matching skill when working in that technology. These provide architecture patterns, conventions, and best practices specific to each stack:

| Skill | Trigger |
|-------|---------|
| `dotnet-dev` | C#, .NET, ASP.NET Core, Entity Framework |
| `vue3-dev` | Vue 3, Composition API, Pinia |
| `python-dev` | Python, FastAPI, Celery |
| `devops` | Docker, docker-compose, Makefiles, CI/CD |
| `frontend-design` | Web UI, components, pages, landing pages, dashboards |
| `mcp-builder` | Building MCP (Model Context Protocol) servers |
| `webapp-testing` | Testing web applications with Playwright |
| `web-artifacts-builder` | Multi-component HTML artifacts with React/Tailwind/shadcn |

These are not exhaustive — for languages without a dedicated skill, apply clean architecture principles, idiomatic patterns, and the project's existing conventions.

## Document & File Processing

Invoke the matching skill whenever the file type is involved — as input, output, or both:

| Skill | Trigger |
|-------|---------|
| `pdf` | Any .pdf operation (read, create, merge, split, OCR, forms) |
| `pptx` | Any .pptx / slides / deck / presentation |
| `docx` | Any .docx / Word document |
| `xlsx` | Any .xlsx, .xlsm, .csv, .tsv spreadsheet |

## Creative & Design Skills

| Skill | Trigger |
|-------|---------|
| `canvas-design` | Posters, visual art, static design (.png, .pdf) |
| `algorithmic-art` | Generative/algorithmic art with p5.js |
| `theme-factory` | Styling artifacts with themes (10 presets + custom) |
| `brand-guidelines` | Anthropic brand colors and typography |
| `slack-gif-creator` | Animated GIFs optimized for Slack |

## Communication & Documentation

| Skill | Trigger |
|-------|---------|
| `internal-comms` | Status reports, newsletters, FAQs, incident reports |
| `doc-coauthoring` | Co-authoring documentation, proposals, specs |

## Meta Skills

| Skill | Trigger |
|-------|---------|
| `skill-creator` | Creating or updating skills |
| `writing-skills` | Writing and verifying skills before deployment |
| `project-memory` | Setting up structured project memory in `docs/project_notes/` |

## Project Memory

Maintain institutional knowledge in `docs/project_notes/`. Check these BEFORE making assumptions:

- **bugs.md** — search before debugging; log new bugs with solutions when resolved
- **decisions.md** — check before proposing architectural changes; log new ADRs
- **key_facts.md** — check for project config, ports, URLs before assuming
- **issues.md** — log completed work with ticket IDs and dates

## Principles

- **YAGNI** — only build what's needed now. Three similar lines > premature abstraction.
- **DRY** — but don't abstract prematurely. Duplication is cheaper than the wrong abstraction.
- **Evidence over claims** — run verification, read output, then speak.
- **Skills over intuition** — if a skill exists for the task, use it.
- **Parallel when possible** — use parallel tool calls and parallel agents for independent work.
- **Ask, don't guess** — when blocked or uncertain, ask the user.
