"""
Phase 4: Task Breakdown
Breaks down the plan into actionable, ordered tasks
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class TaskBreakdownPhase:
    """Handles Phase 4: Task Breakdown"""
    
    def __init__(self, spec_dir: Path):
        self.spec_dir = spec_dir
        self.tasks_file = spec_dir / "tasks.md"
        self.metadata_file = spec_dir / "metadata.json"
    
    def execute(self, plan_content: str, spec_content: str, project_name: str) -> Tuple[bool, str]:
        """
        Execute task breakdown phase
        
        Returns:
            Tuple of (success, tasks_content)
        """
        console.print(Panel(
            "[bold cyan]Phase 4/6: Task Breakdown[/bold cyan]\n"
            "Breaking down plan into actionable tasks...",
            border_style="cyan"
        ))
        
        # Load template
        template = self._load_template()
        
        # Generate tasks from plan
        tasks_content = self._generate_tasks(template, plan_content, spec_content, project_name)
        
        # Save tasks file
        self._save_tasks(tasks_content)
        
        # Validate tasks
        warnings = self._validate_tasks(tasks_content, plan_content)
        
        # Display results
        console.print(f"✓ Tasks created: [cyan]{self.tasks_file}[/cyan]")
        
        if warnings:
            console.print("⚠ Task breakdown validation warnings:")
            for warning in warnings:
                console.print(f"  • {warning}")
        
        return True, tasks_content
    
    def _load_template(self) -> str:
        """Load tasks template"""
        template_path = Path(__file__).parent.parent / "templates" / "tasks-template.md"
        if template_path.exists():
            return template_path.read_text()
        
        # Fallback template
        return """# Task Breakdown

**Feature**: [FEATURE_NAME]
**Date**: [DATE]
**Status**: Not Started

## Overview

[OVERVIEW]

## Task List

### Phase 1: [PHASE_NAME]

- [ ] **Task 1.1**: [TASK_DESCRIPTION]
  - **Effort**: [EFFORT]
  - **Dependencies**: [DEPENDENCIES]
  - **Acceptance Criteria**: [CRITERIA]

### Phase 2: [PHASE_NAME]

- [ ] **Task 2.1**: [TASK_DESCRIPTION]
  - **Effort**: [EFFORT]
  - **Dependencies**: [DEPENDENCIES]
  - **Acceptance Criteria**: [CRITERIA]

## Milestones

- [ ] **Milestone 1**: [MILESTONE_NAME] - [DATE]
- [ ] **Milestone 2**: [MILESTONE_NAME] - [DATE]

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| [RISK] | [STRATEGY] |

## Notes

[NOTES]
"""
    
    def _generate_tasks(self, template: str, plan_content: str, spec_content: str, project_name: str) -> str:
        """Generate tasks content from template and plan"""
        
        # Extract feature name from spec
        feature_name = self._extract_feature_name(spec_content)
        
        # Fill template placeholders
        tasks_content = template
        tasks_content = tasks_content.replace("[FEATURE_NAME]", feature_name)
        tasks_content = tasks_content.replace("[DATE]", datetime.now().strftime("%Y-%m-%d"))
        tasks_content = tasks_content.replace("[PROJECT_NAME]", project_name)
        
        # Generate overview from plan
        overview = self._generate_overview(plan_content)
        tasks_content = tasks_content.replace("[OVERVIEW]", overview)
        
        # Generate task phases from plan
        phases = self._extract_phases_from_plan(plan_content)
        if phases:
            task_sections = self._generate_task_sections(phases)
            # Replace first phase section
            tasks_content = tasks_content.replace(
                "### Phase 1: [PHASE_NAME]",
                task_sections,
                1
            )
            # Remove second phase template
            lines = tasks_content.split("\n")
            filtered_lines = []
            skip_until_milestone = False
            for line in lines:
                if "### Phase 2:" in line:
                    skip_until_milestone = True
                    continue
                if skip_until_milestone and line.startswith("##"):
                    skip_until_milestone = False
                if not skip_until_milestone:
                    filtered_lines.append(line)
            tasks_content = "\n".join(filtered_lines)
        
        # Generate milestones
        milestones = self._generate_milestones(phases)
        tasks_content = tasks_content.replace(
            "- [ ] **Milestone 1**: [MILESTONE_NAME] - [DATE]",
            milestones
        )
        # Remove milestone 2 template
        tasks_content = tasks_content.replace(
            "\n- [ ] **Milestone 2**: [MILESTONE_NAME] - [DATE]",
            ""
        )
        
        # Extract risks from plan
        risks = self._extract_risks_from_plan(plan_content)
        if risks:
            risk_table = self._generate_risk_table(risks)
            tasks_content = tasks_content.replace(
                "| [RISK] | [STRATEGY] |",
                risk_table
            )
        
        # Add notes
        notes = f"Tasks generated from plan on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        tasks_content = tasks_content.replace("[NOTES]", notes)
        
        return tasks_content
    
    def _extract_feature_name(self, spec_content: str) -> str:
        """Extract feature name from spec"""
        for line in spec_content.split("\n"):
            if line.startswith("# "):
                return line.replace("# ", "").strip()
        return "Unknown Feature"
    
    def _generate_overview(self, plan_content: str) -> str:
        """Generate overview from plan"""
        lines = plan_content.split("\n")
        overview_lines = []
        in_overview = False
        
        for line in lines:
            if "## Overview" in line or "## Summary" in line:
                in_overview = True
                continue
            if in_overview and line.startswith("##"):
                break
            if in_overview and line.strip():
                overview_lines.append(line.strip())
        
        if overview_lines:
            return " ".join(overview_lines)
        
        return "Break down the technical plan into actionable, ordered tasks."
    
    def _extract_phases_from_plan(self, plan_content: str) -> List[Dict[str, str]]:
        """Extract implementation phases from plan"""
        phases = []
        lines = plan_content.split("\n")
        current_phase = None
        
        for line in lines:
            if "### Phase" in line or "### Step" in line:
                if current_phase:
                    phases.append(current_phase)
                phase_name = line.replace("###", "").strip()
                current_phase = {"name": phase_name, "description": ""}
            elif current_phase and line.strip() and not line.startswith("#"):
                current_phase["description"] += line.strip() + " "
        
        if current_phase:
            phases.append(current_phase)
        
        # If no phases found, create default phases
        if not phases:
            phases = [
                {"name": "Phase 1: Foundation", "description": "Set up project structure and dependencies"},
                {"name": "Phase 2: Core Implementation", "description": "Implement main features"},
                {"name": "Phase 3: Testing & Polish", "description": "Add tests and refine"}
            ]
        
        return phases
    
    def _generate_task_sections(self, phases: List[Dict[str, str]]) -> str:
        """Generate task sections from phases"""
        sections = []
        
        for i, phase in enumerate(phases, 1):
            section = f"### {phase['name']}\n\n"
            
            # Generate 3-5 tasks per phase
            task_count = min(5, max(3, len(phase['description'].split('.')) // 2))
            
            for j in range(1, task_count + 1):
                section += f"- [ ] **Task {i}.{j}**: [Implement specific component]\n"
                section += f"  - **Effort**: [S/M/L]\n"
                section += f"  - **Dependencies**: [Previous tasks]\n"
                section += f"  - **Acceptance Criteria**: [Specific criteria]\n\n"
            
            sections.append(section)
        
        return "\n".join(sections)
    
    def _generate_milestones(self, phases: List[Dict[str, str]]) -> str:
        """Generate milestones from phases"""
        milestones = []
        
        from datetime import datetime, timedelta
        base_date = datetime.now()
        
        for i, phase in enumerate(phases, 1):
            milestone_name = phase['name'].split(':')[-1].strip() if ':' in phase['name'] else phase['name']
            # Estimate milestone date (1 week per milestone)
            milestone_date = (base_date + timedelta(weeks=i)).strftime("%Y-%m-%d")
            milestones.append(f"- [ ] **Milestone {i}**: {milestone_name} Complete - {milestone_date}")
        
        return "\n".join(milestones)
    
    def _extract_risks_from_plan(self, plan_content: str) -> List[Dict[str, str]]:
        """Extract risks from plan"""
        risks = []
        lines = plan_content.split("\n")
        in_risks = False
        
        for line in lines:
            if "## Risk" in line or "## Risks" in line:
                in_risks = True
                continue
            if in_risks and line.startswith("##"):
                break
            if in_risks and line.strip().startswith("-") or line.strip().startswith("*"):
                risk_text = line.strip().lstrip("-*").strip()
                if risk_text:
                    risks.append({"risk": risk_text, "mitigation": "To be defined"})
        
        if not risks:
            risks = [
                {"risk": "Technical complexity", "mitigation": "Incremental development and testing"},
                {"risk": "Timeline constraints", "mitigation": "Prioritize MVP features"}
            ]
        
        return risks
    
    def _generate_risk_table(self, risks: List[Dict[str, str]]) -> str:
        """Generate risk mitigation table"""
        rows = []
        for risk in risks:
            rows.append(f"| {risk['risk']} | {risk['mitigation']} |")
        return "\n".join(rows)
    
    def _save_tasks(self, tasks_content: str):
        """Save tasks to file"""
        self.tasks_file.write_text(tasks_content)
        
        # Update metadata
        if self.metadata_file.exists():
            metadata = json.loads(self.metadata_file.read_text())
        else:
            metadata = {}
        
        metadata["tasks_created"] = datetime.now().isoformat()
        metadata["tasks_file"] = str(self.tasks_file)
        
        self.metadata_file.write_text(json.dumps(metadata, indent=2))
    
    def _validate_tasks(self, tasks_content: str, plan_content: str) -> List[str]:
        """Validate tasks against plan"""
        warnings = []
        
        # Check for placeholders
        placeholders = []
        for line in tasks_content.split("\n"):
            if "[" in line and "]" in line:
                start = line.index("[")
                end = line.index("]", start)
                placeholder = line[start+1:end]
                if placeholder.isupper() and placeholder not in ["S/M/L", "DATE"]:
                    placeholders.append(placeholder)
        
        if placeholders:
            warnings.append(f"Unexplained placeholders found: {', '.join(set(placeholders))}")
        
        # Check for task structure
        if "- [ ]" not in tasks_content:
            warnings.append("No checkboxes found. Tasks should use checkbox format.")
        
        # Check for effort estimation
        if "Effort" not in tasks_content:
            warnings.append("Missing effort estimation for tasks.")
        
        # Check for acceptance criteria
        if "Acceptance Criteria" not in tasks_content:
            warnings.append("Missing acceptance criteria for tasks.")
        
        return warnings
