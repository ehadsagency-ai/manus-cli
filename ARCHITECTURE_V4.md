# Manus CLI v4.0 - Complete Spec-Kit Integration Architecture

## Overview

Manus CLI v4.0 integrates the **complete GitHub Spec-Kit methodology** as a built-in thinking and creation process. This is NOT an optional feature but a core part of how the CLI operates when users request to "create", "build", or engage in "reflexion/thinking".

## Design Principles

1. **Built-In Process**: Spec-driven development is the default workflow, not an option
2. **Guided Experience**: Interactive step-by-step guidance through all 6 phases
3. **File-Based Artifacts**: All outputs saved to `.manus/` directory with full traceability
4. **Quality Gates**: Validation at every phase with max 3 iterations
5. **Role Integration**: All 12 roles work with spec-driven methodology
6. **Flexibility**: Adapts to task complexity (simple vs complex)

## Architecture Components

### 1. Core Modules

```
manus_cli/
├── __init__.py                  # v4.0.0
├── api_enhanced.py              # API client (from v2.0)
├── roles.py                     # 12 professional roles (from v2.0)
├── cli_v4.py                    # Main CLI with full Spec-Kit integration
├── speckit/
│   ├── __init__.py
│   ├── core.py                  # Core Spec-Kit engine
│   ├── phases.py                # 6-phase implementation
│   ├── templates.py             # Template management
│   ├── validation.py            # Quality gates & checklists
│   ├── constitution.py          # Phase 1: Constitution
│   ├── specify.py               # Phase 2: Specification
│   ├── clarify.py               # Phase 3: Clarification (optional)
│   ├── plan.py                  # Phase 4: Planning
│   ├── tasks.py                 # Phase 5: Task Breakdown
│   ├── implement.py             # Phase 6: Implementation
│   ├── analyze.py               # Enhancement: Consistency check
│   ├── checklist.py             # Enhancement: Quality checklists
│   └── utils.py                 # Utilities (versioning, file ops)
├── templates/
│   ├── constitution-template.md
│   ├── spec-template.md
│   ├── clarifications-template.md
│   ├── plan-template.md
│   ├── tasks-template.md
│   ├── implementation-template.md
│   ├── checklist-requirements.md
│   ├── checklist-technical.md
│   └── checklist-security.md
└── __main_v4__.py               # Entry point
```

### 2. Workflow Detection

```python
# Trigger keywords for Spec-Driven mode
SPEC_DRIVEN_KEYWORDS = [
    "créer", "create", "construire", "build",
    "réflexion", "reflexion", "thinking", "penser",
    "projet", "project", "application", "app",
    "développer", "develop", "coder", "code"
]

def should_use_spec_driven(message: str) -> tuple[bool, str]:
    """
    Detect if message requires spec-driven process.
    Returns: (should_use, complexity_level)
    complexity_level: "simple" | "moderate" | "complex"
    """
    # Check for trigger keywords
    has_trigger = any(kw in message.lower() for kw in SPEC_DRIVEN_KEYWORDS)
    
    if not has_trigger:
        return False, "none"
    
    # Assess complexity
    word_count = len(message.split())
    has_multiple_features = any(word in message.lower() for word in ["et", "and", "avec", "with", "plus"])
    
    if word_count < 10 and not has_multiple_features:
        return True, "simple"
    elif word_count < 30:
        return True, "moderate"
    else:
        return True, "complex"
```

### 3. Phase Implementation

#### Phase 1: Constitution
```python
class ConstitutionPhase:
    """
    Establishes project principles and governance.
    Output: .manus/memory/constitution.md
    """
    
    def execute(self, project_context: dict) -> ConstitutionResult:
        # 1. Check if constitution exists
        # 2. If not, create from template
        # 3. Fill placeholders with project-specific values
        # 4. Apply semantic versioning
        # 5. Generate Sync Impact Report
        # 6. Save to .manus/memory/constitution.md
        pass
    
    def validate(self, constitution: str) -> ValidationResult:
        # Check: No unexplained placeholders
        # Check: Valid semantic version
        # Check: ISO date format
        # Check: Declarative principles
        # Check: Proper formatting
        pass
```

#### Phase 2: Specification
```python
class SpecificationPhase:
    """
    Defines WHAT users need and WHY (not HOW).
    Output: .manus/specs/feature-NNN-short-name/spec.md
    """
    
    def execute(self, user_request: str, constitution: Constitution) -> SpecResult:
        # 1. Generate branch name (action-noun format)
        # 2. Calculate feature number (find highest N + 1)
        # 3. Create feature directory
        # 4. Fill spec template (WHAT/WHY only, no HOW)
        # 5. Document assumptions
        # 6. Add [NEEDS CLARIFICATION] markers (max 3)
        # 7. Generate requirements checklist
        # 8. Validate (max 3 iterations)
        pass
    
    def validate(self, spec: str) -> ValidationResult:
        # Check: Business-focused (no technical details)
        # Check: Testable functional requirements
        # Check: User Scenarios & Testing present
        # Check: Measurable success criteria
        # Check: Max 3 clarification markers
        pass
```

#### Phase 3: Clarification (Optional)
```python
class ClarificationPhase:
    """
    De-risk ambiguous areas before planning.
    Output: .manus/specs/feature-NNN/clarifications.md
    """
    
    def should_run(self, spec: Specification) -> bool:
        # Run if:
        # - Spec has [NEEDS CLARIFICATION] markers
        # - User explicitly requests clarification
        # - Complexity level is "complex"
        pass
    
    def execute(self, spec: Specification) -> ClarificationResult:
        # 1. Extract clarification markers from spec
        # 2. Generate structured questions
        # 3. Present options to user (interactive)
        # 4. Document decisions and rationale
        # 5. Update spec with clarifications
        # 6. Remove clarification markers
        pass
```

#### Phase 4: Planning
```python
class PlanningPhase:
    """
    Defines HOW to build (tech stack, architecture).
    Output: .manus/specs/feature-NNN/plan.md
    """
    
    def execute(self, spec: Specification, role: Role) -> PlanResult:
        # 1. Select tech stack (justified)
        # 2. Design architecture
        # 3. Generate diagrams (Mermaid/D2)
        # 4. Define file structure
        # 5. Assess risks & mitigation
        # 6. Document rollback strategies
        # 7. Consider performance/scalability
        pass
    
    def validate(self, plan: str, spec: Specification) -> ValidationResult:
        # Check: All spec requirements addressed
        # Check: Technology choices justified
        # Check: Architecture diagram present
        # Check: Risk assessment completed
        # Check: Rollback strategy documented
        pass
```

#### Phase 5: Task Breakdown
```python
class TasksPhase:
    """
    Breaks down into actionable tasks.
    Output: .manus/specs/feature-NNN/tasks.md
    """
    
    def execute(self, plan: Plan) -> TasksResult:
        # 1. Extract components from plan
        # 2. Create task categories (Setup, Core, Testing, Docs, Deploy)
        # 3. Define dependencies between tasks
        # 4. Estimate effort (hours/days)
        # 5. Add acceptance criteria per task
        # 6. Include verification steps
        pass
    
    def validate(self, tasks: str, plan: Plan) -> ValidationResult:
        # Check: All plan components covered
        # Check: Tasks independently testable
        # Check: Dependencies explicitly mapped
        # Check: Effort estimates provided
        # Check: Acceptance criteria present
        pass
```

#### Phase 6: Implementation
```python
class ImplementationPhase:
    """
    Executes according to plan.
    Output: Code + .manus/specs/feature-NNN/implementation.md
    """
    
    def execute(self, tasks: Tasks, api_client: ManusAPI) -> ImplementationResult:
        # 1. Show splash screen with context
        # 2. Execute tasks one by one
        # 3. Track progress in implementation.md
        # 4. Document deviations with rationale
        # 5. Generate code via Manus API
        # 6. Run verification steps
        # 7. Prepare PR description
        pass
    
    def track_progress(self, task_id: str, status: str, notes: str):
        # Update implementation.md with:
        # - Task status (TODO, IN_PROGRESS, DONE, BLOCKED)
        # - Completion timestamp
        # - Issues/blockers
        # - Deviations from plan
        pass
```

### 4. Enhancement Commands

#### Analyze Command
```python
class AnalyzeCommand:
    """
    Cross-artifact consistency validation.
    Run after tasks, before implementation.
    """
    
    def execute(self, feature_dir: Path) -> AnalysisReport:
        # 1. Load spec, plan, tasks
        # 2. Check spec requirements → plan components mapping
        # 3. Check plan components → tasks mapping
        # 4. Validate success criteria coverage
        # 5. Check risk mitigation completeness
        # 6. Generate inconsistency report
        pass
```

#### Checklist Command
```python
class ChecklistCommand:
    """
    Generate quality checklists.
    Run after plan.
    """
    
    def execute(self, feature_dir: Path) -> ChecklistResult:
        # Generate checklists:
        # - requirements.md: Requirements completeness
        # - technical.md: Technical feasibility
        # - security.md: Security/privacy compliance
        # - performance.md: Performance/scalability
        pass
```

### 5. User Interface Flow

```
User: "manus chat 'Create a todo app with user authentication'"

CLI: 🎯 Spec-Driven Development Mode Activated
     Complexity: MODERATE
     
     ╔══════════════════════════════════════════════════════╗
     ║  SPEC-DRIVEN PROCESS                                 ║
     ║  Structured Thinking & Creation                      ║
     ╠══════════════════════════════════════════════════════╣
     ║  Mode: QUALITY | Role: Developer                     ║
     ║  Token Budget: 50,000 | Context: 0 KB                ║
     ╚══════════════════════════════════════════════════════╝
     
     Phase 1/6: Constitution
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ✓ Loading project principles...
     ✓ Constitution v1.0.0 found
     
     Phase 2/6: Specification
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     ✓ Feature: add-todo-auth
     ✓ Branch: feature-001-add-todo-auth
     ✓ Spec created: .manus/specs/feature-001-add-todo-auth/spec.md
     
     📋 Clarifications Needed (2/3):
     
     1. Authentication Method
        Options:
        A) Email/Password (traditional)
        B) OAuth (Google, GitHub)
        C) Magic Link (passwordless)
        
        Your choice (A/B/C): _
```

### 6. File Structure

```
project/
├── .manus/
│   ├── memory/
│   │   └── constitution.md              # v1.0.0 - Project principles
│   ├── specs/
│   │   └── feature-001-add-todo-auth/
│   │       ├── spec.md                  # WHAT & WHY
│   │       ├── clarifications.md        # Q&A decisions
│   │       ├── plan.md                  # HOW (tech stack)
│   │       ├── tasks.md                 # Actionable breakdown
│   │       ├── implementation.md        # Progress tracking
│   │       └── checklists/
│   │           ├── requirements.md
│   │           ├── technical.md
│   │           └── security.md
│   ├── config.json                      # CLI configuration
│   └── history.json                     # Conversation history
└── [project files...]
```

### 7. Configuration

```json
{
  "api_key": "sk-...",
  "default_mode": "quality",
  "default_role": "developer",
  "streaming": true,
  "spec_driven": {
    "enabled": true,
    "auto_detect": true,
    "complexity_threshold": "moderate",
    "skip_clarification_for_simple": true,
    "max_clarifications": 3,
    "validation_iterations": 3,
    "generate_diagrams": true,
    "create_github_issues": false
  }
}
```

### 8. Integration with Existing Features

- **Roles**: All 12 roles work with spec-driven process
- **Streaming**: Real-time updates during each phase
- **History**: All phases saved to conversation history
- **Error Handling**: Retry logic with exponential backoff
- **Interactive Mode**: Slash commands for phase navigation

### 9. Slash Commands (Interactive Mode)

```
/constitution  - View/update project constitution
/spec         - Create new specification
/clarify      - Add clarifications to current spec
/plan         - Generate implementation plan
/tasks        - Break down into tasks
/implement    - Start implementation
/analyze      - Run consistency analysis
/checklist    - Generate quality checklists
/status       - Show current phase and progress
/skip         - Skip optional phase (clarify only)
/restart      - Restart from beginning
```

## Implementation Priority

### Phase 1 (MVP - v4.0.0)
- ✅ Core Spec-Kit engine
- ✅ 6 phases (constitution, specify, plan, tasks, implement)
- ✅ Template system
- ✅ Basic validation
- ✅ File-based artifacts
- ✅ Splash screen with ASCII art

### Phase 2 (v4.1.0)
- ⏳ Clarification phase (optional)
- ⏳ Enhancement commands (analyze, checklist)
- ⏳ Advanced validation with checklists
- ⏳ Diagram generation (Mermaid)

### Phase 3 (v4.2.0)
- ⏳ GitHub integration (issues, PRs)
- ⏳ Team collaboration features
- ⏳ CI/CD integration
- ⏳ Analytics dashboard

## Success Criteria

1. ✅ Spec-driven process activates automatically for "create/build" requests
2. ✅ All 6 phases implemented with validation
3. ✅ File artifacts saved to `.manus/` directory
4. ✅ Quality gates enforce max 3 iterations
5. ✅ Splash screen shows context and progress
6. ✅ Works with all 12 professional roles
7. ✅ Adapts to task complexity (simple/moderate/complex)
8. ✅ Complete traceability from requirements to code

## Conclusion

Manus CLI v4.0 transforms from a simple chat interface into a **rigorous, spec-driven development tool** that guides users through structured thinking and creation processes, ensuring quality, consistency, and traceability at every step.
