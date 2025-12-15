## [5.5.3] - 2024-12-15

### 🎨 Perfect Centering

This release updates the splash screen to use **"AI CLI"** for perfect centering and visual balance.

### Changed
- **Splash screen text**: Changed from "AI CLI DRIVEN" to "AI CLI" for better fit
- **Perfect centering**: All elements now perfectly centered in the panel
- **Compact design**: Cleaner, more professional appearance
- **Visual balance**: Panel auto-sizes to content for optimal display

### Technical Details
- Reduced ASCII art width from 84 to 34 characters
- Used `Align.center()` for perfect text centering
- Panel uses `expand=False` for auto-sizing
- All commands tested and verified

---

## [5.5.2] - 2024-12-15

### 🎨 Splash Screen Update

This release updates the splash screen ASCII art to display "AI CLI DRIVEN" instead of "MANUS".

### Changed
- **Splash screen branding**: Updated ASCII art from "MANUS" to "AI CLI DRIVEN"
- **Layout**: Split into two lines (AI CLI / DRIVEN) for better readability
- **Visual consistency**: Maintains the beautiful "AND AFTER YOU" prompt

### Technical Details
- Updated `splash.py` with new ASCII art
- Optimized panel width for proper display
- All commands tested and verified

---

## [5.5.1] - 2024-12-15

### 🐛 Hotfix Release

This hotfix release fixes critical packaging issues and adds missing features.

### Fixed
- **pyproject.toml version mismatch**: Updated from 5.3.0 to 5.5.1
- **Missing subpackages**: Changed `packages = ["manus_cli"]` to `packages = {find = {}}` to include all subpackages (speckit, etc.)
- **Package installation**: pip now correctly installs version 5.5.1 with all modules

### Added
- **`--show` flag for configure command**: Display current configuration without making changes
- **Input validation**: Mode and role validation in configure command
- **Better error messages**: Clear feedback for invalid mode or role values

### Changed
- Configure command now requires at least one option (or --show)
- Mode and role are now optional in configure (only update if provided)
- Improved configure command help text with examples

### Technical Details
- Fixed pyproject.toml to use `find_packages` equivalent
- All version files synchronized (5.5.1)
- Comprehensive testing performed

---

## [5.5.0] - 2024-12-15

### ✨ Interactive Splash Screen & Fixed Interactive Mode

This release adds a beautiful interactive splash screen with "AND AFTER YOU" prompt and fixes the interactive chat mode.

### Added

#### Interactive Features
- **`manus start` command**: New command that displays splash screen and enters interactive mode
- **"AND AFTER YOU" splash screen**: Beautiful ASCII art with welcoming prompt
- **Interactive mode fix**: `manus chat -i` now works without requiring MESSAGE argument
- **Quick command reference**: Splash screen shows available commands and examples
- **Exit commands**: Support for exit, quit, q, bye to leave interactive mode
- **Keyboard interrupt handling**: Clean Ctrl+C exit

### Changed
- Version bumped from 5.4.0 to 5.5.0
- `manus chat` MESSAGE argument now optional (for interactive mode)
- README updated with `manus start` documentation
- Interactive mode now shows splash screen automatically

### Fixed
- **Interactive mode error**: Fixed "Missing argument 'MESSAGE'" error when using `manus chat -i`
- **Better UX**: Users now immediately understand they can interact after seeing splash screen

### New Commands
```bash
manus start           # Show splash screen and enter interactive mode
manus start --role developer  # Interactive mode with specific role
manus chat -i         # Alternative way to start interactive mode
```

### Splash Screen Preview
```
███╗   ███╗ █████╗ ███╗   ██╗██╗   ██╗███████╗
████╗ ████║██╔══██╗████╗  ██║██║   ██║██╔════╝
██╔████╔██║███████║██╔██╗ ██║██║   ██║███████╗
██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║╚════██║
██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝███████║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

✨ AND AFTER YOU ✨
```

---

## [5.4.0] - 2024-12-15

### 🔄 Auto-Update System

This release adds a complete auto-update system that keeps Manus CLI up-to-date automatically.

### Added

#### Auto-Update Features
- **Automatic update checking**: CLI checks GitHub for new versions once per day
- **Update notification**: Beautiful panel notification when new version is available
- **`manus update` command**: One-command update from GitHub
- **Update checker module** (`manus_cli/updater.py`): Handles all update logic
- **Update cache**: Stores last check timestamp in `~/.config/manus/update_check.json`
- **Configurable**: Can disable via `check_updates: false` in config.json

### Changed
- Version bumped from 5.3.0 to 5.4.0
- README updated with auto-update documentation and examples
- CLI startup now includes non-blocking update check

### Technical Details
- Uses GitHub Releases API to fetch latest version
- Graceful error handling for network failures
- Silent fallback if update check fails (doesn't interrupt workflow)
- 24-hour check interval to avoid excessive API calls
- Semantic version comparison (major.minor.patch)

### New Command
```bash
manus update  # Check for updates and install if available
```

### Auto-Update Notification Example
```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ⚠️  New version available!                                 │
│                                                             │
│  Current version: 5.3.0                                     │
│  Latest version:  5.4.0                                     │
│                                                             │
│  Run manus update to upgrade                                │
│  Or: pip3 install --upgrade git+https://github.com/...     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## [4.2.0] - 2025-01-15

### 🚀 Major Release: Complete Spec-Kit Implementation

This release completes the full GitHub Spec-Kit methodology with all 6 phases, enhancement commands, diagram generation, GitHub integration, CI/CD automation, analytics, and template library.

### Added

#### All 6 Phases Implemented
- ✅ **Phase 4: Task Breakdown** - Break down plan into actionable, ordered tasks
- ✅ **Phase 5: Implementation** - Execute tasks and track progress
- ✅ **Phase 6: Clarification** - Identify and resolve ambiguities (optional)

#### Enhancement Commands
- `manus analyze` - Comprehensive artifact quality analysis
- `manus checklist` - Run quality checklist validation
- Automatic quality scoring (0-100%)
- Consistency checking across artifacts
- Actionable recommendations

#### Diagram Generation
- **Architecture diagrams** (Mermaid) - Component relationships
- **Data flow diagrams** (D2) - Data movement visualization
- **User journey diagrams** (Mermaid) - User experience flows
- **Sequence diagrams** (Mermaid) - Interaction sequences
- Auto-rendering to PNG using `manus-render-diagram`
- Saved in `.manus/specs/*/diagrams/`

#### GitHub Integration
- `manus github sync` - Commit and push specs to GitHub
- `manus github issues` - Create GitHub issues from tasks
- `manus github branch <name>` - Create feature branches
- `manus github pr` - Create pull requests
- Automatic git initialization
- Label management (spec-driven, effort-*)

#### CI/CD Integration
- Auto-generate **GitHub Actions** workflows
- Support for Python, Node.js, Java, Go
- **Docker Compose** configuration generation
- Database service templates (Postgres, MySQL, MongoDB, Redis)
- Test and build automation
- Deployment pipeline scaffolding

#### Analytics Dashboard
- Track project metrics and progress
- Quality score trends over time
- Task completion rates
- Timeline visualization
- `manus analytics` command
- JSON-based storage in `.manus/analytics.json`

#### Template Library
- **Preset templates**: web-app, rest-api, data-pipeline
- Custom template creation and management
- Template customization interface
- Category-based organization (web, api, mobile, data, ml)
- `manus templates list [category]`
- `manus templates add <name>`
- `manus templates customize <name>`

### Changed
- Workflow now executes all 6 phases (previously 3)
- Enhanced splash screen with full statistics
- Improved error handling and recovery
- Better validation with specific quality gates
- Metadata tracking for all artifacts

### Technical Improvements
- Modular architecture (`speckit/`, `integrations/`)
- Comprehensive metadata in `metadata.json`
- Rich CLI output with tables, panels, progress bars
- Extensible plugin system foundation
- JSON-based analytics and configuration

### File Structure (Updated)
```
.manus/
├── memory/
│   └── constitution.md
├── specs/
│   └── feature-NNN-short-name/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── implementation.md
│       ├── clarifications.md (optional)
│       ├── analysis.json
│       ├── checklist-results.json
│       ├── metadata.json
│       └── diagrams/
│           ├── architecture.mmd (or .png)
│           ├── dataflow.d2 (or .png)
│           ├── user-journey.mmd (or .png)
│           └── sequence.mmd (or .png)
├── analytics.json
└── templates/
    └── catalog.json
```

### New Commands Summary
```bash
# Enhancement commands
manus analyze                    # Quality analysis
manus checklist                  # Quality checklist

# GitHub integration
manus github sync                # Sync to GitHub
manus github issues              # Create issues
manus github branch <name>       # Create branch
manus github pr                  # Create PR

# Analytics
manus analytics                  # Show dashboard

# Templates
manus templates list             # List templates
manus templates add <name>       # Add template
manus templates customize <name> # Customize template
```

### Breaking Changes
None. Fully backward compatible with v4.0.0.

### Migration from v4.0.0
No migration needed. All new features are additive.

**To use new features:**
1. Update: `pip install --upgrade git+https://github.com/ehadsagency-ai/manus-cli.git`
2. Run workflow: `manus chat "Create a todo app"`
3. All 6 phases execute automatically
4. Use new commands as needed

### Performance
- Phase execution: ~5-10 seconds per phase
- Diagram generation: ~2-5 seconds
- Quality analysis: ~1-2 seconds
- GitHub operations: depends on network

### Known Issues
- Diagram rendering requires `manus-render-diagram` utility
- GitHub operations require `gh` CLI to be installed and authenticated
- Clarification phase is interactive (can be skipped)

### Roadmap (v4.3+)
- Real-time collaboration
- Web dashboard for visualization
- Advanced template marketplace
- More CI/CD platform integrations
- Enhanced AI-powered generation

---

# Changelog

All notable changes to Manus CLI will be documented in this file.

## [4.0.0] - 2024-12-14

### 🎉 Major Release: Complete Spec-Kit Integration (MVP)

This release implements the **complete GitHub Spec-Kit methodology** as a core feature of Manus CLI, transforming it into a rigorous spec-driven development tool.

### Added

#### Complete Spec-Kit Engine
- **Automatic keyword detection** for "create", "build", "develop", "réflexion" triggers
- **Complexity assessment** (simple/moderate/complex)
- **3-phase workflow** (Constitution → Specification → Planning)
- **File-based artifacts** in `.manus/` directory
- **Quality validation** at each phase
- **Professional ASCII art splash screen**

#### Phase Implementations
1. **Constitution Phase**: Project principles and governance
2. **Specification Phase**: WHAT users need and WHY (not HOW)
3. **Planning Phase**: HOW to build (tech stack, architecture)

#### Templates System
- `constitution-template.md`
- `spec-template.md`
- `plan-template.md`
- `tasks-template.md` (for v4.1)
- `checklist-template.md` (for v4.1)

#### File Structure
```
.manus/
├── memory/
│   └── constitution.md
└── specs/
    └── feature-NNN-short-name/
        ├── spec.md
        ├── plan.md
        └── metadata.json
```

### Changed
- CLI entry point: `cli_v4.py`
- Version: 4.0.0
- Spec-driven mode activates automatically

### Roadmap (v4.1+)
- Phase 4: Task Breakdown
- Phase 5: Implementation
- Phase 6: Clarification (optional)
- Enhancement commands (analyze, checklist)
- Diagram generation (Mermaid)
- GitHub integration

---

## [3.0.0] - 2024-12-14
### Added
- Spec-Driven Development prototype
- Basic splash screen
- 6-step guided process

---

## [2.0.0] - 2024-12-14
### Added
- 12 professional roles
- Streaming responses
- Conversation history

---

## [1.0.0] - 2024-12-13
### Added
- Initial release
- Basic chat functionality

[4.0.0]: https://github.com/ehadsagency-ai/manus-cli/releases/tag/v4.0.0
