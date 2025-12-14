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
