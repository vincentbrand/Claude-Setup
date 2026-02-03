# 🚀 Claude Code Development Setup

> **Kickstart your AI-powered development workflow with pre-configured skills and plugins for Claude Code**

A comprehensive setup repository for [Claude Code](https://github.com/anthropics/claude-code) that provides production-ready skills for various development stacks, helping you leverage AI-assisted coding with best practices and clean architecture patterns from day one.

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Skills Overview](#-skills-overview)
- [Project Memory System](#-project-memory-system)
- [Plugin Installation](#-plugin-installation)
- [Usage Examples](#-usage-examples)
- [Customization](#-customization)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 🎯 **Pre-configured Skills** - Ready-to-use development skills for multiple tech stacks
- 🏗️ **Clean Architecture** - Best practices for .NET, Vue, Python, and DevOps
- 🔧 **Production-Ready** - Battle-tested patterns and standards
- 📦 **Easy Integration** - Simple copy-paste setup into your projects
- 🛠️ **Plugin Support** - Includes setup for essential Claude Code plugins
- 🔄 **Extensible** - Create your own custom skills using the included skill-creator
- 🧠 **Project Memory System** - Automatic memory-aware behavior that persists knowledge across sessions

---

## 🚀 Quick Start

### Prerequisites

- [Claude Code](https://github.com/anthropics/claude-code) installed (`brew install --cask claude-code`)
- Git installed on your system

### Installation

1. **Clone this repository:**

```bash
git clone https://github.com/yourusername/claude-setup.git
cd claude-setup
```

2. **Copy skills to your Claude Code directory:**

```bash
# Copy all skills to Claude Code's global skills directory
cp -r .claude/skills/* ~/.claude/skills/

# OR copy to a specific project
cp -r .claude/skills/* /path/to/your/project/.claude/skills/
```

3. **Restart Claude Code** to load the new skills:

```bash
# Close any running Claude Code sessions and restart
```

4. **Verify installation:**

```bash
# In Claude Code, type:
/skills
```

You should see the installed skills listed.

---

## 🎓 Skills Overview

This repository includes the following development skills:

### 🐳 DevOps

**Trigger:** Docker, docker-compose, Makefiles, CI/CD pipelines

Comprehensive DevOps standards including:
- Docker and docker-compose best practices
- Modular Makefile architecture
- Container registry management (Scaleway)
- Bruno API testing workflows
- Service orchestration patterns

[View DevOps Skill](.claude/skills/devops/SKILL.md)

---

### 💻 .NET Development

**Trigger:** C# projects, ASP.NET Core, Entity Framework Core

Modern .NET development with clean architecture:
- ASP.NET Core Web APIs (Minimal & Controller-based)
- Entity Framework Core patterns
- CQRS with MediatR
- Clean Architecture structure
- JWT authentication
- FluentValidation
- xUnit testing
- .NET 8+ features (primary constructors, file-scoped namespaces)

[View .NET Skill](.claude/skills/dotnet-dev/SKILL.md)

---

### 🎨 Vue 3 Development

**Trigger:** Vue 3 components, frontend work

Modern Vue 3 frontend development:
- Composition API with `<script setup>`
- Tailwind CSS + Scoped SCSS
- Pinia state management
- Vue Router patterns
- Playwright testing
- Clean, minimal design aesthetic

[View Vue 3 Skill](.claude/skills/vue3-dev/SKILL.md)

---

### 🐍 Python Development

**Trigger:** Python projects (if included)

Python development best practices:
- FastAPI applications
- Type hints and modern Python
- Testing patterns
- Virtual environment management

[View Python Skill](.claude/skills/python-dev/SKILL.md) _(if available)_

---

### 🛠️ Skill Creator

**Trigger:** Creating new skills

Meta-skill for creating custom skills:
- Skill creation workflows
- Best practices for skill design
- Validation and packaging tools
- Progressive disclosure patterns

[View Skill Creator](.claude/skills/skill-creator/SKILL.md)

---

## 🧠 Project Memory System

The project memory system maintains institutional knowledge across development sessions, ensuring that bug solutions, architectural decisions, and project facts persist over time. This creates a "memory" that survives tool switches, team member changes, and session boundaries.

### What Makes It Automatic

The key to the memory system is **CLAUDE.md** at the repository root. This file contains "Memory-Aware Protocols" that configure Claude to automatically:

- ✅ Check `docs/project_notes/decisions.md` before proposing architectural changes
- ✅ Search `docs/project_notes/bugs.md` when encountering errors
- ✅ Reference `docs/project_notes/key_facts.md` for project configuration
- ✅ Log completed work in `docs/project_notes/issues.md`

**Without CLAUDE.md, memory checking is manual.** With it, Claude proactively consults project memory before making suggestions.

### Memory Files Structure

```
docs/
└── project_notes/
    ├── bugs.md         # Bug log with solutions and prevention strategies
    ├── decisions.md    # Architectural Decision Records (ADRs)
    ├── key_facts.md    # Project configuration, ports, URLs, service accounts
    └── issues.md       # Work log with ticket IDs and completion status
```

### How It Works

1. **Automatic Checks**: When you encounter an error, Claude searches `bugs.md` for known solutions
2. **Consistent Decisions**: Before proposing changes, Claude checks `decisions.md` for existing architectural choices
3. **Configuration Lookup**: Claude references `key_facts.md` for database ports, API endpoints, and project IDs
4. **Work Tracking**: Completed tickets are logged in `issues.md` for project history

### Cross-Platform Support

The repository includes both **CLAUDE.md** and **AGENTS.md** with identical memory protocols. This ensures memory awareness works across:

- Claude Code
- Cursor
- GitHub Copilot
- Codex
- Gemini
- Any AI coding tool that reads project context

### Security Note

The `key_facts.md` file is designed for **non-sensitive configuration only**:

**Store:** Hostnames, ports, project IDs, service account names, API endpoints
**Never store:** Passwords, API keys, private keys, OAuth secrets, credentials

Use proper secret management (environment variables, vaults) for sensitive data.

### Example: Bug Memory in Action

```
# Scenario: Database connection error
User: "I'm getting 'connection refused' from the database"

# Claude automatically:
1. Searches docs/project_notes/bugs.md for "connection"
2. Finds previous solution: "Use AlloyDB Auth Proxy on port 5432"
3. Applies the known fix immediately
4. No need to rediscover the solution
```

### Getting Started with Project Memory

The memory system is **already configured** in this repository with:

- ✅ CLAUDE.md with Memory-Aware Protocols
- ✅ AGENTS.md for cross-platform support
- ✅ docs/project_notes/ with template files
- ✅ ADR-001 documenting the memory system adoption

To use in your own projects:

```bash
# Copy memory configuration to your project
cp CLAUDE.md /path/to/your/project/
cp AGENTS.md /path/to/your/project/
cp -r docs/project_notes /path/to/your/project/docs/

# Or invoke the project-memory skill
/project-memory
```

### Benefits

- **Compound Interest Effect**: Memory becomes more valuable as knowledge accumulates over time
- **Team Consistency**: All team members and AI tools share the same institutional knowledge
- **Faster Debugging**: Known bug solutions are applied immediately without rediscovery
- **Architectural Alignment**: Decisions remain consistent with past choices
- **Session Continuity**: Knowledge persists across coding sessions and context windows

[View Project Memory Skill](.claude/skills/project-memory/SKILL.md)
[View CLAUDE.md](CLAUDE.md)
[View Memory Files](docs/project_notes/)

---

## 🔌 Plugin Installation

Claude Code supports plugins to extend functionality. Here's how to install essential plugins:

### 1️⃣ Code Simplifier Plugin

The `code-simplifier` plugin helps refine and simplify code while preserving functionality.

```bash
# Install code-simplifier plugin
/plugin install code-simplifier
```

**What it does:**
- ✅ Simplifies complex code
- ✅ Improves code clarity and consistency
- ✅ Maintains all functionality
- ✅ Focuses on recently modified code

**Usage:**
```bash
# In Claude Code
/simplify
```

---

### 2️⃣ GitHub Plugin

The `github` plugin enables seamless GitHub integration for issues, PRs, and repository management.

```bash
# Install GitHub plugin
/plugin install github
```

**What it does:**
- 🔗 Creates pull requests from Claude Code
- 📋 Manages GitHub issues
- ✅ Checks PR status and CI/CD runs
- 📦 Interacts with releases

**Usage:**
```bash
# Create a pull request
/gh pr create

# View issues
/gh issue list

# Check PR status
/gh pr status
```

**Authentication:**

After installing the GitHub plugin, you may need to authenticate:

```bash
# Follow the authentication prompts
gh auth login
```

---

### 📦 Managing Plugins

```bash
# List installed plugins
/plugin

# Update a plugin
/plugin update code-simplifier

# Uninstall a plugin
/plugin uninstall plugin-name
```

---

## 💡 Usage Examples

### Example 1: Building a .NET Web API

```bash
# In your project directory with Claude Code
You: "Create a new ASP.NET Core Web API with clean architecture for a user management system"

# Claude will automatically use the dotnet-dev skill and:
# - Set up clean architecture structure
# - Create entities, DTOs, commands, queries
# - Implement MediatR handlers
# - Add FluentValidation
# - Set up Entity Framework Core
# - Configure dependency injection
```

### Example 2: Dockerizing an Application

```bash
You: "Create a Dockerfile and docker-compose.yml for my FastAPI backend with PostgreSQL"

# Claude will automatically use the devops skill and:
# - Create optimized Dockerfile with best practices
# - Set up docker-compose with proper networking
# - Add health checks
# - Configure environment variables
# - Create a Makefile for common operations
```

### Example 3: Building Vue Components

```bash
You: "Create a user profile component with Pinia state management"

# Claude will automatically use the vue3-dev skill and:
# - Use Composition API with <script setup>
# - Implement Pinia store
# - Apply Tailwind CSS styling
# - Follow component best practices
```

---

## 🎨 Customization

### Creating Your Own Skills

Use the included `skill-creator` skill to build custom skills:

```bash
# Invoke the skill creator
/skill-creator

# Or create manually
python .claude/skills/skill-creator/scripts/init_skill.py my-custom-skill --path .claude/skills
```

**Skill Structure:**
```
my-custom-skill/
├── SKILL.md              # Main skill documentation (required)
├── scripts/              # Executable scripts (optional)
├── references/           # Reference documentation (optional)
└── assets/              # Templates and assets (optional)
```

### Modifying Existing Skills

1. Navigate to `.claude/skills/<skill-name>/`
2. Edit `SKILL.md` to update guidelines
3. Add or modify resources in `scripts/`, `references/`, or `assets/`
4. Restart Claude Code to reload changes

### Packaging Skills for Distribution

```bash
# Package a skill into a zip file
python .claude/skills/skill-creator/scripts/package_skill.py .claude/skills/my-custom-skill

# This creates: my-custom-skill.zip
```

---

## 📂 Repository Structure

```
claude-setup/
├── .claude/
│   └── skills/
│       ├── devops/          # DevOps & Docker standards
│       ├── dotnet-dev/      # .NET development best practices
│       ├── vue3-dev/        # Vue 3 frontend patterns
│       ├── python-dev/      # Python development (if included)
│       └── skill-creator/   # Skill creation meta-skill
├── dotnet-dev.zip          # Packaged .NET skill
└── README.md               # This file
```

---

## 🔧 Advanced Configuration

### Global vs Project Skills

**Global Skills** (apply to all projects):
```bash
~/.claude/skills/
```

**Project Skills** (apply to specific project):
```bash
/your/project/.claude/skills/
```

Project skills take precedence over global skills if they have the same name.

### Skill Invocation

Skills are triggered automatically based on:
- File types you're working with
- Keywords in your prompts
- Explicitly invoking with `/skill-name`

**Explicit invocation:**
```bash
/dotnet-dev
/devops
/vue3-dev
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-skill`)
3. **Add or improve skills** in `.claude/skills/`
4. **Test your changes** with Claude Code
5. **Commit your changes** (`git commit -m 'Add amazing skill'`)
6. **Push to the branch** (`git push origin feature/amazing-skill`)
7. **Open a Pull Request**

### Contribution Guidelines

- Follow existing skill structure and formatting
- Include comprehensive documentation in `SKILL.md`
- Add concrete examples and code samples
- Test skills with real-world scenarios
- Use clear, imperative language (not second-person)

---

## 📚 Resources

- [Claude Code Documentation](https://github.com/anthropics/claude-code)
- [Claude API Documentation](https://docs.anthropic.com/)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)
- [Claude Code Skill Guide](https://github.com/anthropics/claude-code/blob/main/SKILLS.md)

---

## 🆘 Troubleshooting

### Skills not loading?

1. Verify skills are in correct directory:
   ```bash
   ls ~/.claude/skills/
   ```

2. Check skill structure (must have `SKILL.md` with proper frontmatter)

3. Restart Claude Code completely

4. Check for validation errors:
   ```bash
   python .claude/skills/skill-creator/scripts/package_skill.py .claude/skills/skill-name
   ```

### Plugins not working?

1. Ensure you're running the latest Claude Code version:
   ```bash
   brew upgrade claude-code
   ```

2. Verify plugin installation:
   ```bash
   /plugin
   ```

3. Re-install the plugin:
   ```bash
   /plugin uninstall plugin-name
   /plugin install plugin-name
   ```

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for creating Claude and Claude Code
- The open-source community for best practices and patterns
- All contributors who help improve these skills

---

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/claude-setup/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/claude-setup/discussions)
- **Claude Code Issues:** [Claude Code GitHub](https://github.com/anthropics/claude-code/issues)

---

<div align="center">

**Made with ❤️ for the Claude Code community**

⭐ **Star this repo** if you find it helpful!

</div>
