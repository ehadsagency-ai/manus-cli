# Changelog

All notable changes to Manus CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2024-12-14

### 🎯 Major Feature: Spec-Driven Development Integration

This release introduces **Spec-Driven Development** methodology inspired by GitHub Spec-Kit, bringing structured thinking and rigorous project creation to Manus CLI.

### Added

#### Spec-Driven Development System
- **Automatic trigger detection** for creation/building keywords (`create`, `build`, `develop`, `construire`, `créer`, `réflexion`)
- **Complexity analysis** to determine if full spec-driven process is needed
- **6-step guided process**:
  1. **Constitution** - Establish project principles and guidelines
  2. **Specification** - Define WHAT to build (requirements, user stories)
  3. **Technical Plan** - Define HOW to build (tech stack, architecture)
  4. **Task Breakdown** - Generate actionable task list
  5. **Implementation** - Execute tasks according to plan
  6. **Summary** - Review and next steps

#### Visual Enhancements
- **ASCII art splash screen** with project context information
- **Token usage estimation** display
- **Working directory** and spec file location display
- **Complexity indicator** (STANDARD vs HIGH)
- Beautiful **step-by-step panels** guiding through the process

#### File Management
- **Automatic `.manus/` directory** creation in working directory
- **Structured markdown files** for each phase:
  - `constitution.md` - Project principles
  - `spec.md` - Requirements and specifications
  - `plan.md` - Technical implementation plan
  - `tasks.md` - Actionable task breakdown
  - `implementation.md` - Implementation log
- **Context preservation** across CLI sessions

#### CLI Commands & Options
- `--spec-driven` / `--no-spec-driven` flag for chat and task commands
- `--dir` option to specify working directory for spec files
- `/spec` command in interactive mode to force spec-driven for next message
- Enhanced help text with spec-driven examples

#### Integration Features
- **Works with all existing roles** (developer, data-scientist, writer, etc.)
- **Flexible activation**: Auto-detect, manual trigger, or always-on
- **Role-aware system prompts** in spec-driven context
- **Enhanced API prompts** with full spec context

### Changed

- **Version bumped to 3.0.0** across all files
- **CLI description updated** to highlight spec-driven capabilities
- **Entry point changed** to `cli_v3.py`
- **Interactive mode enhanced** with spec-driven awareness
- **Help messages improved** with spec-driven examples

### Technical Details

#### New Modules
- `spec_driven.py` - Core spec-driven development engine
  - `SpecDrivenProcess` class managing the 6-step workflow
  - Trigger keyword detection
  - Complexity analysis
  - File management and context generation
  - Enhanced prompt creation

#### Architecture
```
User Input
    ↓
Trigger Detection (keywords: create, build, etc.)
    ↓
Complexity Analysis (simple vs complex task)
    ↓
[If Spec-Driven Triggered]
    ↓
Splash Screen (ASCII art + context)
    ↓
6-Step Guided Process
    ├─ 1. Constitution
    ├─ 2. Specification
    ├─ 3. Technical Plan
    ├─ 4. Task Breakdown
    ├─ 5. Implementation
    └─ 6. Summary
    ↓
Enhanced Prompt → Manus API
    ↓
Structured Response
```

### Backward Compatibility

- **All v2.0 features preserved**:
  - 12 professional roles
  - Streaming responses
  - Conversation history
  - Enhanced error handling
  - Configuration management
  - Interactive mode

- **v1.0 and v2.0 commands still work** without spec-driven mode
- **Spec-driven is opt-in** by default (auto-detected or manual)
- **No breaking changes** to existing workflows

### Examples

#### Basic Usage
```bash
# Auto-detect spec-driven mode
manus chat "Create a todo application"

# Force spec-driven mode
manus chat "Build a simple calculator" --spec-driven

# Disable spec-driven mode
manus chat "Create a hello world" --no-spec-driven

# Specify working directory
manus chat "Build a REST API" --spec-driven --dir /path/to/project
```

#### Interactive Mode
```bash
manus chat -i

# In interactive mode:
You: /spec
# Next message will use spec-driven mode

You: Create a blog platform
# Guided through 6 steps automatically
```

#### With Roles
```bash
# Spec-driven with developer role
manus chat "Build a microservices architecture" --role developer --spec-driven

# Spec-driven with architect role
manus task "Design a scalable system" --role architect --spec-driven
```

### Files Created in `.manus/` Directory

When spec-driven mode is activated, the following structure is created:

```
.manus/
├── constitution.md      # Project principles and guidelines
├── spec.md             # Requirements and user stories
├── plan.md             # Technical implementation plan
├── tasks.md            # Actionable task breakdown
└── implementation.md   # Implementation log and progress
```

### Philosophy

The spec-driven approach follows these principles:

1. **Specifications become executable** - Not just documentation
2. **Separation of concerns** - WHAT vs HOW
3. **Structured thinking** - Step-by-step methodology
4. **Quality gates** - Multiple checkpoints for validation
5. **Predictable outcomes** - Focus on scenarios, not "vibe coding"

### Inspiration

This feature is inspired by [GitHub Spec-Kit](https://github.com/github/spec-kit), an open-source toolkit for Spec-Driven Development that emphasizes:

- Product scenarios over implementation details
- Executable specifications
- Structured development phases
- Quality-first approach

### Migration Guide

#### From v2.0 to v3.0

No migration needed! All v2.0 features work exactly as before.

**To start using spec-driven mode:**

1. Update to v3.0:
   ```bash
   pip install --upgrade git+https://github.com/ehadsagency-ai/manus-cli.git
   ```

2. Use creation keywords or `--spec-driven` flag:
   ```bash
   manus chat "Create a web app" --spec-driven
   ```

3. Follow the guided 6-step process

4. Find your spec files in `.manus/` directory

**Optional configuration:**
```bash
# Enable spec-driven by default
manus configure --spec-driven

# Disable spec-driven by default
manus configure --no-spec-driven
```

### Known Limitations

- Spec-driven process requires user interaction (not fully automated)
- `.manus/` files are created locally (not synced to cloud by default)
- Complexity detection is heuristic-based (may need manual override)

### Future Enhancements (Planned for v3.1+)

- **Template library** for common project types
- **Spec validation** and consistency checking
- **Git integration** for automatic spec versioning
- **Team collaboration** features
- **Export to other formats** (PDF, HTML)
- **AI-powered spec refinement** suggestions

---

## [2.0.0] - 2024-12-14

### Added
- 12 professional roles with system prompts
- Real-time streaming responses
- Conversation history management
- Enhanced error handling with retry logic
- Advanced configuration system
- Interactive mode improvements

### Changed
- Improved CLI interface
- Better documentation

---

## [1.0.0] - 2024-12-13

### Added
- Initial release
- Basic chat functionality
- Task creation
- API key configuration
- Simple interactive mode

---

[3.0.0]: https://github.com/ehadsagency-ai/manus-cli/releases/tag/v3.0.0
[2.0.0]: https://github.com/ehadsagency-ai/manus-cli/releases/tag/v2.0.0
[1.0.0]: https://github.com/ehadsagency-ai/manus-cli/releases/tag/v1.0.0
