"""
Specification Phase - Define WHAT users need and WHY (not HOW)
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, List
from rich.console import Console
from rich.prompt import Prompt

console = Console()


class SpecificationPhase:
    """
    Phase 2: Specification
    Defines WHAT users need and WHY (not HOW).
    Output: .manus/specs/feature-NNN-short-name/spec.md
    """
    
    def __init__(self, specs_dir: Path, templates_dir: Path):
        """
        Initialize Specification phase.
        
        Args:
            specs_dir: Specs directory path
            templates_dir: Templates directory path
        """
        self.specs_dir = specs_dir
        self.templates_dir = templates_dir
        self.template_file = templates_dir / "spec-template.md"
    
    def execute(
        self,
        feature_number: int,
        short_name: str,
        description: str,
        role: str
    ) -> Tuple[bool, Path, Dict]:
        """
        Execute the specification phase.
        
        Args:
            feature_number: Feature number (e.g., 1, 2, 3)
            short_name: Short name for the feature (e.g., "add-user-auth")
            description: Feature description from user
            role: User's role (affects spec style)
            
        Returns:
            (success, feature_dir, metadata)
        """
        # Create feature directory
        feature_name = f"feature-{feature_number:03d}-{short_name}"
        feature_dir = self.specs_dir / feature_name
        feature_dir.mkdir(parents=True, exist_ok=True)
        
        console.print(f"[cyan]→[/cyan] Feature: {feature_name}")
        
        from ..loading import loading_spinner
        
        with loading_spinner("Creating specification", "Specification created"):
            # Load template
            if not self.template_file.exists():
                console.print(f"[red]✗[/red] Template not found: {self.template_file}")
                return False, feature_dir, {}
            
            with open(self.template_file, "r") as f:
                template = f.read()
            
            # Generate spec content
            spec_content = self._generate_spec(
                template=template,
                feature_name=feature_name,
                description=description,
                role=role
            )
            
            # Save spec file
            spec_file = feature_dir / "spec.md"
            with open(spec_file, "w") as f:
                f.write(spec_content)
        
        console.print(f"[dim]  Location: {spec_file}[/dim]")
        
        # Create metadata
        metadata = {
            "feature_number": feature_number,
            "short_name": short_name,
            "feature_name": feature_name,
            "description": description,
            "role": role,
            "created_at": datetime.now().isoformat(),
            "phase": "specification",
            "status": "in_progress"
        }
        
        return True, feature_dir, metadata
    
    def _generate_spec(
        self,
        template: str,
        feature_name: str,
        description: str,
        role: str
    ) -> str:
        """
        Generate specification content from template.
        
        Args:
            template: Template content
            feature_name: Feature name
            description: Feature description
            role: User's role
            
        Returns:
            Filled specification
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Extract feature title from description (first sentence or first 10 words)
        words = description.split()
        feature_title = " ".join(words[:10])
        if len(words) > 10:
            feature_title += "..."
        
        # Basic replacements
        replacements = {
            "[FEATURE_NAME]": feature_name,
            "[FEATURE_TITLE]": feature_title,
            "[DESCRIPTION]": description,
            "[CREATED_DATE]": today,
            "[AUTHOR_ROLE]": role.title(),
            "[VERSION]": "1.0.0",
        }
        
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)
        
        # Add AI-generated sections placeholder
        result = self._add_generated_sections(result, description)
        
        return result
    
    def _add_generated_sections(self, spec: str, description: str) -> str:
        """
        Add AI-generated sections to the spec.
        
        Args:
            spec: Spec content with template
            description: Feature description
            
        Returns:
            Spec with generated sections
        """
        # This is a simplified version
        # In a real implementation, this would call the Manus API to generate:
        # - User Scenarios & Testing
        # - Functional Requirements
        # - Success Criteria
        # - Assumptions
        # - Key Entities (if applicable)
        
        # For MVP, we'll add placeholders that indicate AI generation is needed
        sections_to_generate = [
            ("## User Scenarios & Testing", "<!-- AI will generate user scenarios based on description -->"),
            ("## Functional Requirements", "<!-- AI will generate testable requirements -->"),
            ("## Success Criteria", "<!-- AI will generate measurable success criteria -->"),
            ("## Assumptions", f"<!-- Based on description: {description} -->"),
        ]
        
        for section_header, placeholder in sections_to_generate:
            if section_header in spec:
                # Replace empty section with placeholder
                spec = re.sub(
                    f"{re.escape(section_header)}\\s*\\n\\s*\\n",
                    f"{section_header}\\n\\n{placeholder}\\n\\n",
                    spec
                )
        
        return spec
    
    def validate(self, spec_file: Path) -> Tuple[bool, List[str]]:
        """
        Validate specification file.
        
        Args:
            spec_file: Path to spec file
            
        Returns:
            (is_valid, errors)
        """
        errors = []
        
        if not spec_file.exists():
            errors.append("Specification file does not exist")
            return False, errors
        
        with open(spec_file, "r") as f:
            content = f.read()
        
        # Check for required sections
        required_sections = [
            "## User Scenarios & Testing",
            "## Functional Requirements",
            "## Success Criteria",
        ]
        
        for section in required_sections:
            if section not in content:
                errors.append(f"Missing required section: {section}")
        
        # Check for unexplained placeholders (except AI generation markers)
        placeholders = re.findall(r"\[([A-Z_]+)\]", content)
        # Filter out known placeholders
        known_placeholders = ["NEEDS CLARIFICATION"]
        unknown_placeholders = [p for p in placeholders if p not in known_placeholders]
        
        if unknown_placeholders:
            errors.append(f"Unexplained placeholders found: {', '.join(unknown_placeholders)}")
        
        # Check for clarification markers (max 3)
        clarification_markers = re.findall(r"\[NEEDS CLARIFICATION:([^\]]+)\]", content)
        if len(clarification_markers) > 3:
            errors.append(f"Too many clarification markers: {len(clarification_markers)} (max 3)")
        
        # Check for technical details (HOW instead of WHAT)
        technical_keywords = [
            "database", "api", "endpoint", "schema", "table", "query",
            "function", "class", "method", "algorithm", "implementation"
        ]
        content_lower = content.lower()
        found_technical = [kw for kw in technical_keywords if kw in content_lower]
        
        if found_technical:
            errors.append(
                f"Specification contains technical details (HOW): {', '.join(found_technical)}. "
                "Focus on WHAT and WHY only."
            )
        
        return len(errors) == 0, errors
