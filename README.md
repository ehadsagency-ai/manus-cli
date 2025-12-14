# 🌱 Manus CLI v3.0

**A command-line interface for Manus AI with Spec-Driven Development for rigorous thinking and project creation**

[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/ehadsagency-ai/manus-cli/releases)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## ✨ What's New in v3.0

### 🎯 Spec-Driven Development

Manus CLI now integrates **Spec-Driven Development** methodology inspired by [GitHub Spec-Kit](https://github.com/github/spec-kit). Instead of "vibe coding", the CLI guides you through a structured 6-step process for rigorous thinking and predictable outcomes.

**When you say "Create a web app", Manus CLI now:**

1. 📜 **Establishes principles** - Defines code quality, testing standards, UX guidelines
2. 📋 **Clarifies requirements** - Captures WHAT you want and WHY
3. 🏗️ **Plans technically** - Determines HOW with tech stack and architecture
4. ✅ **Breaks down tasks** - Generates actionable, ordered task list
5. 🚀 **Implements** - Executes according to the structured plan
6. ✨ **Summarizes** - Reviews deliverables and next steps

All specifications are saved as markdown files in `.manus/` for version control and team collaboration.

---

## 📋 Table of Contents

- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Spec-Driven Development](#-spec-driven-development-guide)
- [Commands](#-commands)
- [Roles](#-roles)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎁 Features

### Core Features (v1.0)
- ✅ **Chat with Manus AI** - Send messages and get intelligent responses
- ✅ **Task creation** - Create and track tasks
- ✅ **API key management** - Secure configuration storage
- ✅ **Interactive mode** - Persistent chat sessions

### Enhanced Features (v2.0)
- ✅ **12 Professional Roles** - Specialized AI personas (developer, data-scientist, writer, etc.)
- ✅ **Streaming Responses** - Real-time response generation
- ✅ **Conversation History** - Save, load, and manage conversations
- ✅ **Enhanced Error Handling** - Retry logic with exponential backoff
- ✅ **Advanced Configuration** - Customize defaults for mode, role, streaming

### Spec-Driven Features (v3.0)
- 🎯 **Automatic Trigger Detection** - Keywords like "create", "build", "develop" activate spec-driven mode
- 🎯 **Complexity Analysis** - Determines if full process is needed
- 🎯 **6-Step Guided Process** - Constitution → Spec → Plan → Tasks → Implement → Summary
- 🎯 **ASCII Art Splash Screen** - Beautiful visual feedback with context info
- 🎯 **Structured Files** - Markdown files in `.manus/` directory
- 🎯 **Role Integration** - Works with all 12 professional roles
- 🎯 **Flexible Activation** - Auto-detect, manual, or always-on

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Install from GitHub

```bash
pip install git+https://github.com/ehadsagency-ai/manus-cli.git
```

### Install in Development Mode

```bash
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli
pip install -e .
```

### Verify Installation

```bash
manus --version
# Output: Manus CLI version 3.0.0
#         With Spec-Driven Development support
```

---

## 🚀 Quick Start

### 1. Configure Your API Key

```bash
manus configure --api-key sk-your-api-key-here
```

Or configure interactively:

```bash
manus configure
```

### 2. Send Your First Message

```bash
manus chat "Hello, how are you?"
```

### 3. Try Spec-Driven Development

```bash
manus chat "Create a todo application with React" --spec-driven
```

You'll be guided through 6 structured steps!

### 4. Start Interactive Mode

```bash
manus chat -i
```

---

## 🎯 Spec-Driven Development Guide

### What is Spec-Driven Development?

**Spec-Driven Development flips the script** on traditional coding. Instead of writing code first and documenting later, specifications become executable and directly drive implementation.

### When Does It Activate?

Spec-driven mode activates automatically when you use keywords like:

- **English**: `create`, `build`, `develop`, `design`, `construct`
- **French**: `créer`, `construire`, `développer`, `concevoir`
- **Reflection**: `réflexion`, `reflexion`, `think`, `reflect`

### The 6-Step Process

#### Step 1: Constitution 📜

**Purpose**: Establish governing principles and development guidelines

**What happens**:
- Define code quality standards
- Set testing requirements
- Establish UX principles
- Define performance requirements
- Set security considerations

**Output**: `constitution.md`

**Example**:
```markdown
# Project Constitution

## Code Quality
- Follow PEP 8 for Python code
- Maximum function length: 50 lines
- Minimum test coverage: 80%

## Testing Standards
- Unit tests for all business logic
- Integration tests for API endpoints
- E2E tests for critical user flows
```

---

#### Step 2: Specification 📋

**Purpose**: Define WHAT to build and WHY

**What happens**:
- Clarify requirements
- Define user stories
- Identify success criteria
- Document constraints

**Output**: `spec.md`

**Example**:
```markdown
# Project Specification

## User Stories

1. As a user, I want to create todo items so that I can track my tasks
2. As a user, I want to mark items as complete so that I can see my progress
3. As a user, I want to filter by status so that I can focus on active tasks

## Success Criteria

- Users can create, read, update, delete todos
- Todos persist across sessions
- Interface is responsive on mobile and desktop
```

---

#### Step 3: Technical Plan 🏗️

**Purpose**: Define HOW to implement

**What happens**:
- Choose tech stack
- Design architecture
- Define data models
- Plan API structure

**Output**: `plan.md`

**Example**:
```markdown
# Technical Implementation Plan

## Technology Stack

- **Frontend**: React 18 + TypeScript + TailwindCSS
- **Backend**: Node.js + Express + TypeScript
- **Database**: PostgreSQL
- **Deployment**: Docker + Docker Compose

## Architecture

- REST API with JSON responses
- JWT authentication
- PostgreSQL for data persistence
- React SPA for frontend
```

---

#### Step 4: Task Breakdown ✅

**Purpose**: Generate actionable task list

**What happens**:
- Break plan into specific tasks
- Order tasks by dependencies
- Estimate effort
- Identify milestones

**Output**: `tasks.md`

**Example**:
```markdown
# Task Breakdown

## Phase 1: Foundation
- [ ] Set up project structure
- [ ] Configure TypeScript and ESLint
- [ ] Set up PostgreSQL database
- [ ] Create database schema

## Phase 2: Backend API
- [ ] Implement todo CRUD endpoints
- [ ] Add authentication middleware
- [ ] Write API tests

## Phase 3: Frontend
- [ ] Create React components
- [ ] Implement state management
- [ ] Connect to API
- [ ] Add responsive styling
```

---

#### Step 5: Implementation 🚀

**Purpose**: Execute tasks according to plan

**What happens**:
- AI executes tasks systematically
- Progress is logged
- Issues are documented
- Deliverables are created

**Output**: `implementation.md` + actual code/files

---

#### Step 6: Summary ✨

**Purpose**: Review and next steps

**What happens**:
- Summary of completed work
- List of deliverables
- Suggestions for next steps
- Documentation links

---

### Using Spec-Driven Mode

#### Auto-Detection (Recommended)

```bash
# Automatically activates for creation tasks
manus chat "Create a blog platform with Django"
manus chat "Build a REST API for user management"
manus chat "Develop a mobile app with React Native"
```

#### Manual Activation

```bash
# Force spec-driven mode
manus chat "Write a simple script" --spec-driven

# Disable spec-driven mode
manus chat "Create a hello world" --no-spec-driven
```

#### In Interactive Mode

```bash
manus chat -i

# In chat:
You: /spec
# Next message will use spec-driven mode

You: Create a task management system
# Guided through 6 steps
```

#### With Specific Working Directory

```bash
# Spec files will be created in /path/to/project/.manus/
manus chat "Build a web scraper" --spec-driven --dir /path/to/project
```

---

## 📚 Commands

### `manus configure`

Configure CLI settings

**Options**:
- `--api-key`, `-k` - Your Manus API key
- `--mode`, `-m` - Default execution mode (speed, quality)
- `--role`, `-r` - Default role/persona
- `--stream` / `--no-stream` - Enable/disable streaming
- `--spec-driven` / `--no-spec-driven` - Enable/disable spec-driven by default

**Examples**:
```bash
# Basic configuration
manus configure --api-key sk-your-key

# Full configuration
manus configure \
  --api-key sk-your-key \
  --mode quality \
  --role developer \
  --stream \
  --spec-driven

# View current config
manus configure
```

---

### `manus chat`

Send messages to Manus AI

**Arguments**:
- `message` - Message to send (optional, omit for interactive mode)

**Options**:
- `--mode`, `-m` - Execution mode
- `--role`, `-r` - Role/persona to use
- `--stream` / `--no-stream` - Enable/disable streaming
- `--interactive`, `-i` - Start interactive session
- `--spec-driven` / `--no-spec-driven` - Force spec-driven mode
- `--dir`, `-d` - Working directory for spec files

**Examples**:
```bash
# Simple message
manus chat "Hello, how are you?"

# With role and streaming
manus chat "Write a Python function" --role developer --stream

# Spec-driven project creation
manus chat "Create a todo app" --spec-driven

# Interactive mode
manus chat -i
```

---

### `manus task`

Create a new task (alias for `chat`)

**Examples**:
```bash
manus task "Build a web scraper" --spec-driven --role developer
```

---

### `manus roles`

List available roles/personas

**Output**:
```
Available Roles

┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Key           ┃ Name                ┃ Description                            ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ assistant     │ Helpful Assistant   │ General-purpose helpful assistant      │
│ developer     │ Software Developer  │ Expert in software development         │
│ data-scientist│ Data Scientist      │ Specialized in data analysis           │
│ writer        │ Content Writer      │ Professional content creator           │
│ ...           │ ...                 │ ...                                    │
└───────────────┴─────────────────────┴────────────────────────────────────────┘
```

---

### `manus status`

Check task status

**Arguments**:
- `task_id` - Task ID to check

**Example**:
```bash
manus status abc123def456
```

---

### `manus history`

List saved conversations

**Example**:
```bash
manus history
```

---

## 🎭 Roles

Manus CLI includes 12 professional roles with specialized system prompts:

| Key | Name | Best For |
|-----|------|----------|
| `assistant` | Helpful Assistant | General questions and tasks |
| `developer` | Software Developer | Writing code, debugging, architecture |
| `data-scientist` | Data Scientist | Data analysis, ML, statistics |
| `writer` | Content Writer | Articles, documentation, copywriting |
| `teacher` | Patient Teacher | Explaining concepts, tutorials |
| `analyst` | Business Analyst | Requirements, business logic |
| `researcher` | Research Assistant | Research, fact-checking, citations |
| `debugger` | Code Debugger | Finding and fixing bugs |
| `architect` | Software Architect | System design, architecture patterns |
| `copywriter` | Marketing Copywriter | Marketing copy, ads, landing pages |
| `consultant` | Technical Consultant | Technical advice, best practices |
| `reviewer` | Code Reviewer | Code review, quality assessment |

**Usage**:
```bash
# Use specific role
manus chat "Design a microservices architecture" --role architect

# Change role in interactive mode
You: /role data-scientist
```

---

## ⚙️ Configuration

### Configuration File

Location: `~/.config/manus/config.json`

**Example**:
```json
{
  "api_key": "sk-your-api-key",
  "default_mode": "quality",
  "default_role": "developer",
  "stream": true,
  "spec_driven": false
}
```

### Environment Variables

You can also use environment variables:

```bash
export MANUS_API_KEY="sk-your-api-key"
export MANUS_DEFAULT_MODE="quality"
export MANUS_DEFAULT_ROLE="developer"
```

---

## 💡 Examples

### Example 1: Simple Chat

```bash
$ manus chat "What is Python?"

You: What is Python?

Manus: Python is a high-level, interpreted programming language...
```

---

### Example 2: Spec-Driven Project Creation

```bash
$ manus chat "Create a blog platform with Django" --spec-driven

╭─────────────────────────── Manus Spec-Driven Mode ───────────────────────────╮
│                                                                              │
│ ███████╗██████╗ ███████╗ ██████╗    ██████╗ ██████╗ ██╗██╗   ██╗███████╗███╗│
│ ██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔══██╗██║██║   ██║██╔════╝████│
│ ███████╗██████╔╝█████╗  ██║         ██║  ██║██████╔╝██║██║   ██║█████╗  ██╔█│
│ ╚════██║██╔═══╝ ██╔══╝  ██║         ██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██║╚│
│ ███████║██║     ███████╗╚██████╗    ██████╔╝██║  ██║██║ ╚████╔╝ ███████╗██║ │
│ ╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝ │
│                                                                              │
│ Structured Thinking Process Activated                                        │
│ Inspired by GitHub Spec-Kit Methodology                                      │
│                                                                              │
│ Mode: QUALITY                                                                │
│ Role: Developer                                                              │
│ Complexity: HIGH                                                             │
│ Working Dir: /home/user/projects/blog                                        │
│ Spec Dir: /home/user/projects/blog/.manus                                    │
│                                                                              │
│ ⚡ Preparing to guide you through 6 structured steps...                      │
╰──────────────────────────────────────────────────────────────────────────────╯

[Guided through 6 steps...]

✓ Constitution saved to: .manus/constitution.md
✓ Specification saved to: .manus/spec.md
✓ Technical plan saved to: .manus/plan.md
✓ Task list saved to: .manus/tasks.md
✓ Implementation log created: .manus/implementation.md

[AI implements the project...]
```

---

### Example 3: Interactive Mode with Roles

```bash
$ manus chat -i

╭─────────────────────────── Manus AI - Interactive Chat v3.0 ──────────────────╮
│                                                                               │
│ Current Role: Helpful Assistant                                               │
│ Mode: speed                                                                   │
│ Streaming: Enabled                                                            │
│ Working Dir: /home/user                                                       │
│                                                                               │
│ ✨ Spec-Driven Development: Enabled                                           │
│ Use keywords like 'create', 'build', 'develop' to trigger structured thinking│
│                                                                               │
│ Commands:                                                                     │
│   /quit or /exit - Exit the chat                                             │
│   /spec - Force spec-driven mode for next message                            │
│   /role <role> - Change role/persona                                         │
│   /stream - Toggle streaming                                                 │
│   /help - Show all commands                                                  │
╰───────────────────────────────────────────────────────────────────────────────╯

You: /role developer
✓ Role changed to: Software Developer

You: Create a REST API for user management
[Spec-driven process activates automatically...]

You: /quit
Goodbye!
```

---

## 📁 Project Structure

### CLI Structure

```
manus-cli/
├── manus_cli/
│   ├── __init__.py           # Package initialization
│   ├── api.py                # Original API client (v1.0)
│   ├── api_enhanced.py       # Enhanced API client (v2.0)
│   ├── cli.py                # Original CLI (v1.0)
│   ├── cli_enhanced.py       # Enhanced CLI (v2.0)
│   ├── cli_v3.py             # Spec-driven CLI (v3.0) ⭐
│   ├── roles.py              # Role definitions (v2.0)
│   ├── spec_driven.py        # Spec-driven engine (v3.0) ⭐
│   ├── __main__.py           # Entry point v1.0
│   ├── __main_enhanced__.py  # Entry point v2.0
│   └── __main_v3__.py        # Entry point v3.0
├── setup.py                  # Package setup
├── pyproject.toml            # Modern Python packaging
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── CHANGELOG.md              # Version history
├── LICENSE                   # MIT License
├── INSTALLATION.md           # Installation guide
└── EXAMPLES.md               # Usage examples
```

### Generated `.manus/` Structure

When using spec-driven mode:

```
your-project/
└── .manus/
    ├── constitution.md       # Project principles
    ├── spec.md              # Requirements & user stories
    ├── plan.md              # Technical implementation plan
    ├── tasks.md             # Actionable task breakdown
    └── implementation.md    # Implementation log
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli

# Install in development mode
pip install -e .

# Run tests
pytest

# Format code
black manus_cli/
```

### Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Write clear commit messages

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **GitHub Spec-Kit** - Inspiration for spec-driven development methodology
- **Claude & OpenAI** - Best practices for AI CLI tools
- **Typer** - Excellent CLI framework
- **Rich** - Beautiful terminal formatting

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/ehadsagency-ai/manus-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/ehadsagency-ai/manus-cli/discussions)
- **Documentation**: [GitHub Wiki](https://github.com/ehadsagency-ai/manus-cli/wiki)

---

## 🗺️ Roadmap

### v3.1 (Planned)
- Template library for common project types
- Spec validation and consistency checking
- Git integration for automatic versioning

### v3.2 (Planned)
- Team collaboration features
- Export to PDF/HTML
- AI-powered spec refinement

### v4.0 (Future)
- Voice input support
- Web dashboard
- Multi-agent collaboration

---

**Made with ❤️ by the Manus CLI Team**

**Star ⭐ this repo if you find it useful!**
