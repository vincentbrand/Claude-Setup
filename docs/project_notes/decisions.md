# Architectural Decision Records (ADRs)

This file tracks significant architectural and design decisions made during the project.

## Format

```markdown
### ADR-XXX: Decision Title (YYYY-MM-DD)

**Context:**
- Why the decision was needed
- What problem it solves

**Decision:**
- What was chosen

**Alternatives Considered:**
- Option 1 -> Why rejected
- Option 2 -> Why rejected

**Consequences:**
- Benefits
- Trade-offs
```

## Guidelines

- Number ADRs sequentially (ADR-001, ADR-002, etc.)
- Keep decisions focused on architecture, not implementation details
- Document the "why" not just the "what"
- Include enough context that future developers understand the reasoning
- Don't delete old ADRs - they provide historical context
- If a decision changes, add a revision date and note rather than deleting

---

## Decision Records

<!-- Add decision records below this line -->

### ADR-001: Adopt Structured Project Memory System (2026-02-03)

**Context:**
- Claude Code skills and development practices need to persist across sessions
- Recurring bugs and architectural decisions were being rediscovered repeatedly
- Multiple AI tools (Claude Code, Cursor, Codex) used in development require consistent knowledge access
- Need institutional knowledge that survives team member changes and tool switches

**Decision:**
- Implement structured project memory in `docs/project_notes/` with four files: bugs.md, decisions.md, key_facts.md, issues.md
- Configure CLAUDE.md and AGENTS.md with Memory-Aware Protocols for automatic memory checking
- Use progressive disclosure pattern (templates in skill references, actual memory in docs/)
- Follow ADR format for architectural decisions, bug log format for issues

**Alternatives Considered:**
- Wiki or Notion -> Requires separate tool, not version controlled with code
- Code comments only -> Scattered, hard to search, not accessible to AI tools
- No formal system -> Status quo of rediscovering solutions, rejected due to inefficiency
- AI-specific hidden directory -> Rejected because visible docs/ encourages team adoption

**Consequences:**
- Benefits:
  - Automatic memory-aware behavior through CLAUDE.md protocols
  - Cross-platform support (Claude Code, Cursor, Codex, Gemini, etc.)
  - Version controlled with code in git
  - Visible location encourages human maintenance
  - Reduces time spent rediscovering solutions
- Trade-offs:
  - Requires manual entry of bugs/decisions (not fully automated)
  - Needs periodic cleanup to avoid bloat
  - Team must learn and follow memory file formats
