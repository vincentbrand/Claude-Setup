# Project Key Facts

This file contains important project configuration, URLs, service accounts, and other key information.

## Security Guidelines

**WHAT TO STORE:**
- Service account names (not credentials)
- Database hostnames and ports (not passwords)
- Project IDs and resource names
- API endpoints and URLs
- Port numbers and protocols
- Configuration file locations

**WHAT NOT TO STORE (SECURITY RISK):**
- Passwords or API keys
- Private keys or certificates
- OAuth secrets
- Database credentials
- Any sensitive authentication tokens

Store credentials in proper secret management systems (environment variables, vaults, etc.).

---

## Repository Structure

- **Skills Location**: `.claude/skills/`
- **Memory System**: `docs/project_notes/`
- **Main Documentation**: `README.md`
- **Configuration**: `CLAUDE.md`, `AGENTS.md`

## Development Environment

- **Claude Code Version**: 2.1.29+
- **Primary Technologies**: .NET 8+, Vue 3, Python, Docker
- **License**: MIT

## Skills Available

- `devops` - Docker, docker-compose, CI/CD standards
- `dotnet-dev` - .NET 8+ with clean architecture
- `vue3-dev` - Vue 3 Composition API patterns
- `python-dev` - Python development standards
- `skill-creator` - Meta-skill for creating new skills
- `project-memory` - Structured memory system

## Installation Locations

- **Global Skills**: `~/.claude/skills/`
- **Project Skills**: `/path/to/project/.claude/skills/`

Project skills take precedence over global skills if they have the same name.

## Important URLs

- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Claude API Documentation](https://docs.anthropic.com/)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

---

## Additional Configuration

<!-- Add project-specific configuration below this line -->
