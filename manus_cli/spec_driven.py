"""
Spec-Driven Development module for Manus CLI
Inspired by GitHub Spec-Kit methodology
"""

import os
import re
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.table import Table

console = Console()


class SpecDrivenProcess:
    """Manages the Spec-Driven Development process"""
    
    # Keywords that trigger spec-driven process
    TRIGGER_KEYWORDS = [
        'créer', 'creer', 'create', 
        'construire', 'build',
        'réflexion', 'reflexion', 'reflect', 'think',
        'développer', 'developper', 'develop',
        'concevoir', 'design'
    ]
    
    # Complexity indicators for full process
    COMPLEXITY_INDICATORS = [
        'app', 'application', 'système', 'system',
        'plateforme', 'platform', 'projet', 'project',
        'architecture', 'infrastructure', 'api',
        'database', 'backend', 'frontend', 'fullstack'
    ]
    
    def __init__(self, working_dir: Path = Path.cwd()):
        """Initialize spec-driven process"""
        self.working_dir = working_dir
        self.manus_dir = working_dir / ".manus"
        self.manus_dir.mkdir(exist_ok=True)
        
        # Spec files
        self.constitution_file = self.manus_dir / "constitution.md"
        self.spec_file = self.manus_dir / "spec.md"
        self.plan_file = self.manus_dir / "plan.md"
        self.tasks_file = self.manus_dir / "tasks.md"
        self.implementation_file = self.manus_dir / "implementation.md"
        self.context_file = self.manus_dir / "context.json"
    
    @staticmethod
    def should_trigger(prompt: str) -> bool:
        """Check if prompt should trigger spec-driven process"""
        prompt_lower = prompt.lower()
        return any(keyword in prompt_lower for keyword in SpecDrivenProcess.TRIGGER_KEYWORDS)
    
    @staticmethod
    def is_complex_task(prompt: str) -> bool:
        """Determine if task is complex enough for full spec-driven process"""
        prompt_lower = prompt.lower()
        
        # Check for complexity indicators
        complexity_score = sum(1 for indicator in SpecDrivenProcess.COMPLEXITY_INDICATORS 
                              if indicator in prompt_lower)
        
        # Check for length (longer prompts tend to be more complex)
        word_count = len(prompt.split())
        
        # Complex if: multiple complexity indicators OR long prompt
        return complexity_score >= 2 or word_count > 30
    
    def show_splash_screen(self, prompt: str, role: str, mode: str):
        """Show ASCII art splash screen with context info"""
        
        # ASCII art banner (using ANSI Shadow style)
        banner = """
███████╗██████╗ ███████╗ ██████╗    ██████╗ ██████╗ ██╗██╗   ██╗███████╗███╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔══██╗██║██║   ██║██╔════╝████╗  ██║
███████╗██████╔╝█████╗  ██║         ██║  ██║██████╔╝██║██║   ██║█████╗  ██╔██╗ ██║
╚════██║██╔═══╝ ██╔══╝  ██║         ██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║
███████║██║     ███████╗╚██████╗    ██████╔╝██║  ██║██║ ╚████╔╝ ███████╗██║ ╚████║
╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝
        """
        
        # Calculate context stats
        prompt_tokens = len(prompt.split()) * 1.3  # Rough estimate
        is_complex = self.is_complex_task(prompt)
        
        # Create info text
        info_text = f"""[cyan]Mode:[/cyan] [green]{mode.upper()}[/green]
[cyan]Role:[/cyan] [green]{role.title()}[/green]
[cyan]Complexity:[/cyan] [green]{'HIGH' if is_complex else 'STANDARD'}[/green]
[cyan]Est. Tokens:[/cyan] [green]~{int(prompt_tokens)}[/green]
[cyan]Working Dir:[/cyan] [green]{self.working_dir}[/green]
[cyan]Spec Dir:[/cyan] [green]{self.manus_dir}[/green]"""
        
        # Display splash
        console.print(Panel(
            f"[bold magenta]{banner}[/bold magenta]\n\n"
            f"[bold cyan]Structured Thinking Process Activated[/bold cyan]\n"
            f"[dim]Inspired by GitHub Spec-Kit Methodology[/dim]\n\n"
            f"{info_text}\n\n"
            f"[yellow]⚡ Preparing to guide you through 6 structured steps...[/yellow]",
            border_style="magenta",
            title="[bold]Manus Spec-Driven Mode[/bold]",
            subtitle=f"[dim]{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]"
        ))
        
        console.print()
    
    def step_1_constitution(self, role: str) -> str:
        """Step 1: Establish project principles (constitution)"""
        console.print(Panel(
            "[bold cyan]Step 1/6: Constitution[/bold cyan]\n\n"
            "Define the governing principles and development guidelines for this project.\n"
            "These principles will guide all subsequent development decisions.\n\n"
            "[yellow]Think about:[/yellow]\n"
            "• Code quality standards\n"
            "• Testing requirements\n"
            "• User experience principles\n"
            "• Performance requirements\n"
            "• Security considerations",
            border_style="cyan",
            title="📜 Project Constitution"
        ))
        
        if self.constitution_file.exists():
            console.print(f"[yellow]Found existing constitution:[/yellow] {self.constitution_file}")
            use_existing = Confirm.ask("Use existing constitution?")
            if use_existing:
                return self.constitution_file.read_text()
        
        console.print(f"\n[bold]Current Role:[/bold] {role}")
        console.print("[dim]The AI will suggest principles based on your role and project context.[/dim]\n")
        
        # User can provide custom principles or let AI suggest
        custom = Confirm.ask("Do you want to provide custom principles? (No = AI will suggest)")
        
        if custom:
            console.print("\n[cyan]Enter your project principles (press Ctrl+D or Ctrl+Z when done):[/cyan]")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            constitution = "\n".join(lines)
        else:
            constitution = f"[AI will suggest principles based on {role} role and project context]"
        
        # Save constitution
        self.constitution_file.write_text(f"""# Project Constitution

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Role**: {role}

## Governing Principles

{constitution}

---
*This constitution guides all development decisions for this project.*
""")
        
        console.print(f"\n[green]✓[/green] Constitution saved to: {self.constitution_file}")
        return constitution
    
    def step_2_specify(self, prompt: str) -> str:
        """Step 2: Define what to build (requirements and user stories)"""
        console.print(Panel(
            "[bold cyan]Step 2/6: Specification[/bold cyan]\n\n"
            "Define WHAT you want to build and WHY.\n"
            "Focus on requirements, user stories, and outcomes.\n\n"
            "[yellow]Avoid:[/yellow] Technical implementation details\n"
            "[green]Focus on:[/green] User needs, business value, desired outcomes",
            border_style="cyan",
            title="📋 Requirements Specification"
        ))
        
        console.print(f"\n[bold]Initial Prompt:[/bold]\n{prompt}\n")
        
        # Ask for clarification
        needs_clarification = Confirm.ask("Do you want to add more details or clarify requirements?")
        
        additional_details = ""
        if needs_clarification:
            console.print("\n[cyan]Additional requirements or clarifications:[/cyan]")
            additional_details = Prompt.ask("Details")
        
        spec_content = f"""# Project Specification

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Initial Request

{prompt}

## Additional Requirements

{additional_details if additional_details else "_No additional requirements specified._"}

## User Stories

[AI will generate user stories based on requirements]

## Success Criteria

[AI will define success criteria]

## Constraints

[AI will identify constraints]

---
*This specification defines WHAT to build, not HOW to build it.*
"""
        
        self.spec_file.write_text(spec_content)
        console.print(f"\n[green]✓[/green] Specification saved to: {self.spec_file}")
        
        return spec_content
    
    def step_3_plan(self, role: str, mode: str) -> str:
        """Step 3: Create technical implementation plan"""
        console.print(Panel(
            "[bold cyan]Step 3/6: Technical Plan[/bold cyan]\n\n"
            "Define HOW to implement the specification.\n"
            "Choose tech stack, architecture, and technical approach.\n\n"
            "[yellow]Consider:[/yellow]\n"
            "• Technology stack\n"
            "• Architecture patterns\n"
            "• Data models\n"
            "• API design\n"
            "• Infrastructure needs",
            border_style="cyan",
            title="🏗️ Implementation Plan"
        ))
        
        console.print(f"\n[bold]Role:[/bold] {role}")
        console.print(f"[bold]Mode:[/bold] {mode}\n")
        
        # Ask for tech stack preferences
        has_preferences = Confirm.ask("Do you have specific tech stack preferences?")
        
        tech_preferences = ""
        if has_preferences:
            console.print("\n[cyan]Tech stack preferences (e.g., 'Python + FastAPI + PostgreSQL'):[/cyan]")
            tech_preferences = Prompt.ask("Tech stack")
        
        plan_content = f"""# Technical Implementation Plan

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Role**: {role}
**Mode**: {mode}

## Technology Stack

{tech_preferences if tech_preferences else "[AI will suggest optimal tech stack based on requirements]"}

## Architecture

[AI will design system architecture]

## Data Models

[AI will define data structures]

## API Design

[AI will design API endpoints and contracts]

## Implementation Approach

[AI will outline implementation strategy]

## Technical Constraints

[AI will identify technical constraints]

---
*This plan defines HOW to build the specification.*
"""
        
        self.plan_file.write_text(plan_content)
        console.print(f"\n[green]✓[/green] Technical plan saved to: {self.plan_file}")
        
        return plan_content
    
    def step_4_tasks(self) -> str:
        """Step 4: Break down into actionable tasks"""
        console.print(Panel(
            "[bold cyan]Step 4/6: Task Breakdown[/bold cyan]\n\n"
            "Generate actionable task list from the implementation plan.\n"
            "Each task should be clear, specific, and achievable.\n\n"
            "[green]Good tasks are:[/green]\n"
            "• Specific and actionable\n"
            "• Properly ordered\n"
            "• Testable\n"
            "• Reasonably sized",
            border_style="cyan",
            title="✅ Task List"
        ))
        
        tasks_content = f"""# Task Breakdown

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Tasks

[AI will generate ordered, actionable task list]

### Phase 1: Foundation
- [ ] Task 1
- [ ] Task 2

### Phase 2: Core Features
- [ ] Task 3
- [ ] Task 4

### Phase 3: Polish & Testing
- [ ] Task 5
- [ ] Task 6

## Task Dependencies

[AI will identify task dependencies]

## Estimated Effort

[AI will provide effort estimates]

---
*These tasks will be executed in the implementation phase.*
"""
        
        self.tasks_file.write_text(tasks_content)
        console.print(f"\n[green]✓[/green] Task list saved to: {self.tasks_file}")
        
        return tasks_content
    
    def step_5_implement(self) -> str:
        """Step 5: Execute implementation"""
        console.print(Panel(
            "[bold cyan]Step 5/6: Implementation[/bold cyan]\n\n"
            "Execute all tasks according to the plan.\n"
            "The AI will now build your project following the structured approach.\n\n"
            "[yellow]⚡ Starting implementation...[/yellow]",
            border_style="cyan",
            title="🚀 Implementation"
        ))
        
        # This will be handled by the actual Manus API call
        # We just prepare the context
        
        implementation_content = f"""# Implementation Log

**Started**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Implementation Progress

[AI will execute tasks and log progress here]

## Completed Tasks

- [ ] Tasks will be marked as completed during implementation

## Issues & Solutions

[AI will document any issues encountered and solutions]

## Final Deliverables

[AI will list all created files and artifacts]

---
*This log tracks the implementation process.*
"""
        
        self.implementation_file.write_text(implementation_content)
        console.print(f"\n[green]✓[/green] Implementation log created: {self.implementation_file}")
        
        return implementation_content
    
    def step_6_summary(self):
        """Step 6: Show summary and next steps"""
        console.print(Panel(
            "[bold cyan]Step 6/6: Summary[/bold cyan]\n\n"
            "[green]✓ Spec-Driven Process Complete![/green]\n\n"
            "All specification files have been created in:\n"
            f"[yellow]{self.manus_dir}[/yellow]\n\n"
            "[bold]Created Files:[/bold]\n"
            f"• {self.constitution_file.name}\n"
            f"• {self.spec_file.name}\n"
            f"• {self.plan_file.name}\n"
            f"• {self.tasks_file.name}\n"
            f"• {self.implementation_file.name}\n\n"
            "[dim]The AI will now process your request with this structured context...[/dim]",
            border_style="green",
            title="✨ Process Complete"
        ))
    
    def run_full_process(self, prompt: str, role: str, mode: str) -> Dict[str, str]:
        """Run the complete spec-driven process"""
        
        # Show splash screen
        self.show_splash_screen(prompt, role, mode)
        
        console.print("\n[bold magenta]Starting Spec-Driven Development Process...[/bold magenta]\n")
        
        # Run all steps
        constitution = self.step_1_constitution(role)
        console.print()
        
        spec = self.step_2_specify(prompt)
        console.print()
        
        plan = self.step_3_plan(role, mode)
        console.print()
        
        tasks = self.step_4_tasks()
        console.print()
        
        implementation = self.step_5_implement()
        console.print()
        
        self.step_6_summary()
        console.print()
        
        return {
            "constitution": constitution,
            "spec": spec,
            "plan": plan,
            "tasks": tasks,
            "implementation": implementation,
            "working_dir": str(self.working_dir),
            "manus_dir": str(self.manus_dir)
        }
    
    def get_context_for_api(self) -> str:
        """Get formatted context to send to Manus API"""
        context_parts = []
        
        if self.constitution_file.exists():
            context_parts.append(f"## Constitution\n\n{self.constitution_file.read_text()}")
        
        if self.spec_file.exists():
            context_parts.append(f"## Specification\n\n{self.spec_file.read_text()}")
        
        if self.plan_file.exists():
            context_parts.append(f"## Technical Plan\n\n{self.plan_file.read_text()}")
        
        if self.tasks_file.exists():
            context_parts.append(f"## Tasks\n\n{self.tasks_file.read_text()}")
        
        return "\n\n---\n\n".join(context_parts)


def create_enhanced_prompt(original_prompt: str, spec_context: str, role: str) -> str:
    """Create enhanced prompt with spec-driven context"""
    
    enhanced = f"""# Spec-Driven Development Request

You are working in **Spec-Driven Development** mode as a **{role}**.

## Original Request
{original_prompt}

## Structured Context

{spec_context}

## Instructions

Please implement this request following the structured approach defined above:

1. **Follow the Constitution**: Adhere to the project principles and guidelines
2. **Meet the Specification**: Ensure all requirements and user stories are addressed
3. **Execute the Plan**: Implement according to the technical plan
4. **Complete the Tasks**: Work through the task list systematically
5. **Document Progress**: Update the implementation log as you work

Provide a complete, production-ready implementation that follows best practices and the defined guidelines.
"""
    
    return enhanced
