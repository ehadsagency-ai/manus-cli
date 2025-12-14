# Manus CLI v4.0 🚀

**Professional CLI for Manus AI with complete GitHub Spec-Kit methodology**

[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](https://github.com/ehadsagency-ai/manus-cli)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## ✨ What's New in v4.0

**Complete Spec-Kit Integration** - Rigorous, spec-driven development built into the CLI

🎯 **Automatic Detection** - Triggers on "create", "build", "develop" keywords  
📋 **3-Phase Workflow** - Constitution → Specification → Planning  
📁 **File Artifacts** - Structured outputs in `.manus/` directory  
✅ **Quality Validation** - Checks at every phase  
🎨 **Professional UI** - ASCII art splash screen  
🎭 **12 Roles** - Developer, Architect, Data Scientist, etc.

---

## 🚀 Quick Start

```bash
# Install
pip install git+https://github.com/ehadsagency-ai/manus-cli.git

# Configure
manus configure --api-key YOUR_KEY

# Create a project (auto-triggers spec-driven mode)
manus chat "Create a todo app"
```

---

## 📚 Commands

```bash
manus chat "message"              # Chat with Manus AI
manus chat "Create X"             # Spec-driven mode (auto)
manus chat "message" --role dev   # Use specific role
manus roles                       # List all roles
manus configure                   # Configure settings
manus version                     # Show version
```

---

## 🏗️ Spec-Kit Workflow

When you say **"Create a web app"**, the CLI:

### Phase 1: Constitution 📜
- Establishes project principles
- Defines governance rules
- Output: `.manus/memory/constitution.md`

### Phase 2: Specification 📋
- Defines WHAT to build (not HOW)
- Business requirements only
- User scenarios & success criteria
- Output: `.manus/specs/feature-001-name/spec.md`

### Phase 3: Planning 🏗️
- Defines HOW to build
- Tech stack & architecture
- Risk assessment
- Output: `.manus/specs/feature-001-name/plan.md`

---

## 📁 Generated Structure

```
.manus/
├── memory/
│   └── constitution.md
└── specs/
    └── feature-001-short-name/
        ├── spec.md
        ├── plan.md
        └── metadata.json
```

---

## 🎭 Professional Roles

| Role | Description |
|------|-------------|
| `assistant` | Helpful Assistant |
| `developer` | Software Developer |
| `architect` | Software Architect |
| `data-scientist` | Data Scientist |
| `writer` | Content Writer |
| `debugger` | Code Debugger |
| `analyst` | Business Analyst |
| `researcher` | Research Assistant |
| `teacher` | Patient Teacher |
| `copywriter` | Marketing Copywriter |
| `consultant` | Technical Consultant |
| `reviewer` | Code Reviewer |

---

## ⚙️ Configuration

Config file: `~/.config/manus/config.json`

```json
{
  "api_key": "sk-...",
  "default_mode": "quality",
  "default_role": "assistant",
  "streaming": true,
  "spec_driven": {
    "enabled": true,
    "auto_detect": true
  }
}
```

---

## 📖 Examples

### Simple Todo App
```bash
manus chat "Create a todo list application"
# → Guides through 3 phases
# → Generates constitution, spec, plan
```

### REST API with Role
```bash
manus chat "Build a REST API" --role developer
# → Developer-focused spec and plan
```

### Disable Spec-Driven
```bash
manus chat "What is Python?" --no-spec-driven
# → Regular chat mode
```

---

## 🗺️ Roadmap

### v4.0.0 (Current) ✅
- [x] Complete Spec-Kit engine
- [x] 3-phase workflow
- [x] Quality validation
- [x] Professional UI

### v4.1.0 (Next)
- [ ] Phase 4: Task Breakdown
- [ ] Phase 5: Implementation
- [ ] Phase 6: Clarification
- [ ] Diagram generation (Mermaid)

### v4.2.0 (Future)
- [ ] GitHub integration
- [ ] Team collaboration
- [ ] Template library

---

## 📄 License

MIT License - see [LICENSE](LICENSE)

---

## 🙏 Acknowledgments

- Inspired by [GitHub Spec-Kit](https://github.com/github/spec-kit)
- Built with [Typer](https://typer.tiangolo.com/) & [Rich](https://rich.readthedocs.io/)
- Powered by [Manus AI](https://manus.app)

---

**Made with ❤️ by the Manus Team**
