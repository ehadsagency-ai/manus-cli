"""
Phase 5: Implementation
Executes tasks according to the plan and tracks progress
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn

console = Console()


class ImplementationPhase:
    """Handles Phase 5: Implementation"""
    
    def __init__(self, spec_dir: Path):
        self.spec_dir = spec_dir
        self.implementation_file = spec_dir / "implementation.md"
        self.metadata_file = spec_dir / "metadata.json"
    
    def execute(self, tasks_content: str, plan_content: str, project_name: str) -> Tuple[bool, str]:
        """
        Execute implementation phase
        
        Returns:
            Tuple of (success, implementation_content)
        """
        console.print(Panel(
            "[bold cyan]Phase 5/6: Implementation[/bold cyan]\n"
            "Executing tasks according to plan...",
            border_style="cyan"
        ))
        
        # Load template
        template = self._load_template()
        
        # Generate implementation log
        impl_content = self._generate_implementation_log(
            template, tasks_content, plan_content, project_name
        )
        
        # Save implementation file
        self._save_implementation(impl_content)
        
        # Display results
        console.print(f"✓ Implementation log created: [cyan]{self.implementation_file}[/cyan]")
        console.print("\n[yellow]Note:[/yellow] Actual code implementation requires API integration.")
        console.print("       This phase creates the implementation tracking document.")
        
        return True, impl_content
    
    def _load_template(self) -> str:
        """Load implementation template"""
        # Simple implementation log template
        return """# Implementation Log

**Feature**: [FEATURE_NAME]
**Started**: [START_DATE]
**Status**: [STATUS]

## Overview

[OVERVIEW]

## Implementation Progress

### Completed Tasks

[COMPLETED_TASKS]

### In Progress

[IN_PROGRESS_TASKS]

### Pending

[PENDING_TASKS]

## Deliverables

[DELIVERABLES]

## Issues Encountered

[ISSUES]

## Next Steps

[NEXT_STEPS]

## Notes

[NOTES]
"""
    
    def _generate_implementation_log(
        self, template: str, tasks_content: str, plan_content: str, project_name: str
    ) -> str:
        """Generate implementation log from template"""
        
        # Extract feature name
        feature_name = self._extract_feature_name(tasks_content)
        
        # Fill template
        impl_content = template
        impl_content = impl_content.replace("[FEATURE_NAME]", feature_name)
        impl_content = impl_content.replace("[START_DATE]", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        impl_content = impl_content.replace("[STATUS]", "In Progress")
        impl_content = impl_content.replace("[PROJECT_NAME]", project_name)
        
        # Generate overview
        overview = f"Implementation of {feature_name} according to the technical plan."
        impl_content = impl_content.replace("[OVERVIEW]", overview)
        
        # Extract tasks
        tasks = self._extract_tasks(tasks_content)
        
        # Categorize tasks (for MVP, all are pending)
        completed = "None yet - implementation requires API integration"
        in_progress = "Awaiting implementation"
        pending = self._format_task_list(tasks)
        
        impl_content = impl_content.replace("[COMPLETED_TASKS]", completed)
        impl_content = impl_content.replace("[IN_PROGRESS_TASKS]", in_progress)
        impl_content = impl_content.replace("[PENDING_TASKS]", pending)
        
        # Generate deliverables from plan
        deliverables = self._extract_deliverables(plan_content)
        impl_content = impl_content.replace("[DELIVERABLES]", deliverables)
        
        # Issues (none yet)
        issues = "No issues encountered yet."
        impl_content = impl_content.replace("[ISSUES]", issues)
        
        # Next steps
        next_steps = self._generate_next_steps(tasks)
        impl_content = impl_content.replace("[NEXT_STEPS]", next_steps)
        
        # Notes
        notes = f"Implementation log created on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n"
        notes += "This document will be updated as tasks are completed."
        impl_content = impl_content.replace("[NOTES]", notes)
        
        return impl_content
    
    def _extract_feature_name(self, tasks_content: str) -> str:
        """Extract feature name from tasks"""
        for line in tasks_content.split("\n"):
            if "**Feature**:" in line:
                return line.split("**Feature**:")[-1].strip()
            if line.startswith("# "):
                return line.replace("# ", "").strip()
        return "Unknown Feature"
    
    def _extract_tasks(self, tasks_content: str) -> List[str]:
        """Extract task list from tasks content"""
        tasks = []
        for line in tasks_content.split("\n"):
            if line.strip().startswith("- [ ]"):
                task = line.strip().replace("- [ ]", "").strip()
                if task and not task.startswith("**Milestone"):
                    tasks.append(task)
        return tasks
    
    def _format_task_list(self, tasks: List[str]) -> str:
        """Format task list for display"""
        if not tasks:
            return "No tasks defined"
        
        formatted = []
        for i, task in enumerate(tasks[:10], 1):  # Limit to first 10
            formatted.append(f"{i}. {task}")
        
        if len(tasks) > 10:
            formatted.append(f"... and {len(tasks) - 10} more tasks")
        
        return "\n".join(formatted)
    
    def _extract_deliverables(self, plan_content: str) -> str:
        """Extract deliverables from plan"""
        deliverables = []
        
        # Look for common deliverable sections
        lines = plan_content.split("\n")
        in_deliverables = False
        
        for line in lines:
            if "## Deliverable" in line or "## Output" in line:
                in_deliverables = True
                continue
            if in_deliverables and line.startswith("##"):
                break
            if in_deliverables and line.strip().startswith("-"):
                deliverables.append(line.strip())
        
        if deliverables:
            return "\n".join(deliverables)
        
        # Default deliverables
        return """- Fully functional implementation
- Unit tests with >80% coverage
- Integration tests for key flows
- Documentation (README, API docs)
- Deployment configuration"""
    
    def _generate_next_steps(self, tasks: List[str]) -> str:
        """Generate next steps from tasks"""
        if not tasks:
            return "1. Define tasks\n2. Begin implementation"
        
        next_steps = []
        for i, task in enumerate(tasks[:3], 1):
            next_steps.append(f"{i}. {task}")
        
        if len(tasks) > 3:
            next_steps.append(f"{len(tasks) - 3} more tasks to follow...")
        
        return "\n".join(next_steps)
    
    def _save_implementation(self, impl_content: str):
        """Save implementation log to file"""
        self.implementation_file.write_text(impl_content)
        
        # Update metadata
        if self.metadata_file.exists():
            metadata = json.loads(self.metadata_file.read_text())
        else:
            metadata = {}
        
        metadata["implementation_started"] = datetime.now().isoformat()
        metadata["implementation_file"] = str(self.implementation_file)
        metadata["status"] = "in_progress"
        
        self.metadata_file.write_text(json.dumps(metadata, indent=2))
