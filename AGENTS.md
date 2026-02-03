# Claude-Setup Repository

## Project Overview

This repository provides a comprehensive development environment setup for Claude Code with pre-configured skills and best practices for multiple technology stacks. It serves as a kickstart template for AI-powered development workflows.

### Purpose

- Provide production-ready skills for .NET, Vue 3, DevOps, and Python development
- Establish clean architecture patterns and coding standards
- Enable seamless integration with Claude Code through optimized skill structure
- Maintain institutional knowledge through structured project memory

### Repository Structure

```
Claude-Setup/
├── .claude/
│   └── skills/              # Claude Code skills
│       ├── devops/          # Docker, docker-compose, CI/CD standards
│       ├── dotnet-dev/      # .NET 8+ with clean architecture
│       ├── vue3-dev/        # Vue 3 Composition API patterns
│       ├── python-dev/      # Python development standards
│       ├── skill-creator/   # Meta-skill for creating new skills
│       └── project-memory/  # Project memory system
├── docs/
│   └── project_notes/       # Project memory files
├── README.md               # Comprehensive documentation
├── LICENSE                 # MIT License
└── .gitignore             # Comprehensive ignore rules
```

### Technology Stack

- **Claude Code**: AI-powered development CLI
- **Skills System**: Modular, self-contained capability packages
- **Multiple Tech Stacks**: .NET 8+, Vue 3, Python, DevOps
- **Clean Architecture**: Domain-driven design patterns

### Development Workflow

1. Copy skills from this repository to global (`~/.claude/skills/`) or project-specific (`.claude/skills/`) locations
2. Skills automatically trigger based on file types, keywords, or explicit invocation
3. Project memory maintains institutional knowledge across sessions
4. Cross-platform support through AGENTS.md configuration

## Project Memory System

This project maintains institutional knowledge in `docs/project_notes/` for consistency across sessions.

### Memory Files

- **bugs.md** - Bug log with dates, solutions, and prevention notes
- **decisions.md** - Architectural Decision Records (ADRs) with context and trade-offs
- **key_facts.md** - Project configuration, credentials, ports, important URLs
- **issues.md** - Work log with ticket IDs, descriptions, and URLs

### Memory-Aware Protocols

**Before proposing architectural changes:**
- Check `docs/project_notes/decisions.md` for existing decisions
- Verify the proposed approach doesn't conflict with past choices
- If it does conflict, acknowledge the existing decision and explain why a change is warranted

**When encountering errors or bugs:**
- Search `docs/project_notes/bugs.md` for similar issues
- Apply known solutions if found
- Document new bugs and solutions when resolved

**When looking up project configuration:**
- Check `docs/project_notes/key_facts.md` for credentials, ports, URLs, service accounts
- Prefer documented facts over assumptions

**When completing work on tickets:**
- Log completed work in `docs/project_notes/issues.md`
- Include ticket ID, date, brief description, and URL

**When user requests memory updates:**
- Update the appropriate memory file (bugs, decisions, key_facts, or issues)
- Follow the established format and style (bullet lists, dates, concise entries)

### Style Guidelines for Memory Files

- **Prefer bullet lists over tables** for simplicity and ease of editing
- **Keep entries concise** (1-3 lines for descriptions)
- **Always include dates** for temporal context
- **Include URLs** for tickets, documentation, monitoring dashboards
- **Manual cleanup** of old entries is expected (not automated)

## Skills Overview

### DevOps Skill
- Docker and docker-compose best practices
- Modular Makefile architecture
- Container registry management (Scaleway)
- Bruno API testing workflows
- Service orchestration patterns

### .NET Development Skill
- .NET 8+ with modern C# features
- Clean Architecture structure
- ASP.NET Core Web APIs (Minimal & Controller-based)
- Entity Framework Core patterns
- CQRS with MediatR
- JWT authentication and FluentValidation
- xUnit testing standards

### Vue 3 Development Skill
- Composition API with `<script setup>`
- Tailwind CSS + Scoped SCSS
- Pinia state management
- Vue Router patterns
- Playwright testing
- Clean, minimal design aesthetic

### Python Development Skill
- FastAPI applications
- Type hints and modern Python
- Testing patterns
- Virtual environment management

### Skill Creator
- Meta-skill for creating custom skills
- Skill creation workflows and best practices
- Validation and packaging tools
- Progressive disclosure patterns

### Project Memory
- Structured memory system in `docs/project_notes/`
- Bug solutions, architectural decisions, key facts, work history
- Automatic memory-aware behavior
- Cross-platform support (Claude Code, Cursor, Codex, etc.)

## Contributing Guidelines

When contributing to this repository:

1. **Skills**: Follow existing skill structure with YAML frontmatter + markdown body
2. **Documentation**: Update README.md and relevant memory files
3. **Testing**: Test skills with real-world scenarios before submitting
4. **Format**: Use imperative/infinitive form in skill documentation
5. **Memory**: Log architectural decisions in `docs/project_notes/decisions.md`

## Installation & Usage

See [README.md](README.md) for comprehensive installation instructions, plugin setup, and usage examples.

## License

MIT License - see [LICENSE](LICENSE) file for details.
