"""
Planning Phase - Define HOW to build (tech stack, architecture)
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, List
from rich.console import Console

console = Console()


class PlanningPhase:
    """
    Phase 3: Planning
    Defines HOW to build (tech stack, architecture).
    Output: .manus/specs/feature-NNN/plan.md
    """
    
    def __init__(self, templates_dir: Path):
        """
        Initialize Planning phase.
        
        Args:
            templates_dir: Templates directory path
        """
        self.templates_dir = templates_dir
        self.template_file = templates_dir / "plan-template.md"
    
    def execute(
        self,
        feature_dir: Path,
        spec_file: Path,
        role: str,
        metadata: Dict
    ) -> Tuple[bool, Path]:
        """
        Execute the planning phase.
        
        Args:
            feature_dir: Feature directory path
            spec_file: Specification file path
            role: User's role
            metadata: Feature metadata
            
        Returns:
            (success, plan_file_path)
        """
        console.print(f"[cyan]→[/cyan] Creating implementation plan...")
        
        # Load template
        if not self.template_file.exists():
            console.print(f"[red]✗[/red] Template not found: {self.template_file}")
            return False, Path()
        
        with open(self.template_file, "r") as f:
            template = f.read()
        
        # Load spec to extract requirements
        with open(spec_file, "r") as f:
            spec_content = f.read()
        
        # Generate plan content
        plan_content = self._generate_plan(
            template=template,
            spec_content=spec_content,
            feature_name=metadata.get("feature_name", ""),
            role=role
        )
        
        # Save plan file
        plan_file = feature_dir / "plan.md"
        with open(plan_file, "w") as f:
            f.write(plan_content)
        
        console.print(f"[green]✓[/green] Plan created: {plan_file}")
        
        return True, plan_file
    
    def _generate_plan(
        self,
        template: str,
        spec_content: str,
        feature_name: str,
        role: str
    ) -> str:
        """
        Generate plan content from template.
        
        Args:
            template: Template content
            spec_content: Specification content
            feature_name: Feature name
            role: User's role
            
        Returns:
            Filled plan
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Basic replacements
        replacements = {
            "[FEATURE_NAME]": feature_name,
            "[CREATED_DATE]": today,
            "[AUTHOR_ROLE]": role.title(),
            "[VERSION]": "1.0.0",
        }
        
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)
        
        # Add AI-generated sections placeholder
        result = self._add_generated_sections(result, spec_content, role)
        
        return result
    
    def _add_generated_sections(self, plan: str, spec_content: str, role: str) -> str:
        """
        Add AI-generated sections to the plan.
        
        Args:
            plan: Plan content with template
            spec_content: Specification content
            role: User's role
            
        Returns:
            Plan with generated sections
        """
        # This is a simplified version
        # In a real implementation, this would call the Manus API to generate:
        # - Tech Stack (justified choices)
        # - Architecture (with diagrams)
        # - File Structure
        # - Component Breakdown
        # - Risk Assessment
        # - Performance Considerations
        
        # For MVP, we'll add placeholders that indicate AI generation is needed
        sections_to_generate = [
            ("## Tech Stack", f"<!-- AI will suggest tech stack based on {role} role and spec requirements -->"),
            ("## Architecture", "<!-- AI will design architecture with Mermaid diagram -->"),
            ("## File Structure", "<!-- AI will define file/folder structure -->"),
            ("## Component Breakdown", "<!-- AI will break down into components -->"),
            ("## Risk Assessment", "<!-- AI will identify risks and mitigation strategies -->"),
        ]
        
        for section_header, placeholder in sections_to_generate:
            if section_header in plan:
                # Replace empty section with placeholder
                plan = re.sub(
                    f"{re.escape(section_header)}\\s*\\n\\s*\\n",
                    f"{section_header}\\n\\n{placeholder}\\n\\n",
                    plan
                )
        
        return plan
    
    def validate(self, plan_file: Path, spec_file: Path) -> Tuple[bool, List[str]]:
        """
        Validate plan file.
        
        Args:
            plan_file: Path to plan file
            spec_file: Path to spec file
            
        Returns:
            (is_valid, errors)
        """
        errors = []
        
        if not plan_file.exists():
            errors.append("Plan file does not exist")
            return False, errors
        
        with open(plan_file, "r") as f:
            plan_content = f.read()
        
        # Check for required sections
        required_sections = [
            "## Tech Stack",
            "## Architecture",
            "## File Structure",
        ]
        
        for section in required_sections:
            if section not in plan_content:
                errors.append(f"Missing required section: {section}")
        
        # Check for unexplained placeholders
        placeholders = re.findall(r"\[([A-Z_]+)\]", plan_content)
        if placeholders:
            errors.append(f"Unexplained placeholders found: {', '.join(placeholders)}")
        
        # Check that plan addresses spec requirements
        # (Simplified check - in real implementation, would do semantic analysis)
        with open(spec_file, "r") as f:
            spec_content = f.read()
        
        # Extract requirements from spec
        requirements_section = re.search(
            r"## Functional Requirements\s*\n(.*?)(?=\n##|\Z)",
            spec_content,
            re.DOTALL
        )
        
        if requirements_section:
            requirements_text = requirements_section.group(1)
            # Check if plan mentions key terms from requirements
            # (Very basic check for MVP)
            key_terms = re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b", requirements_text)
            mentioned_terms = [term for term in key_terms if term.lower() in plan_content.lower()]
            
            if len(mentioned_terms) < len(key_terms) * 0.5:  # At least 50% coverage
                errors.append(
                    "Plan does not adequately address spec requirements. "
                    f"Only {len(mentioned_terms)}/{len(key_terms)} key terms mentioned."
                )
        
        return len(errors) == 0, errors
