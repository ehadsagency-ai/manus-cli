"""
Constitution Phase - Establish project principles and governance
"""

import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple
from rich.console import Console
from rich.prompt import Prompt, Confirm

console = Console()


class ConstitutionPhase:
    """
    Phase 1: Constitution
    Establishes project principles and governance.
    Output: .manus/memory/constitution.md
    """
    
    def __init__(self, memory_dir: Path, templates_dir: Path):
        """
        Initialize Constitution phase.
        
        Args:
            memory_dir: Memory directory path
            templates_dir: Templates directory path
        """
        self.memory_dir = memory_dir
        self.templates_dir = templates_dir
        self.constitution_file = memory_dir / "constitution.md"
        self.template_file = templates_dir / "constitution-template.md"
    
    def execute(self, project_name: str, project_description: str) -> Tuple[bool, str]:
        """
        Execute the constitution phase.
        
        Args:
            project_name: Name of the project
            project_description: Description of the project
            
        Returns:
            (success, constitution_path)
        """
        console.print("[cyan]✓[/cyan] Checking for existing constitution...")
        
        # Check if constitution already exists
        if self.constitution_file.exists():
            console.print(f"[green]✓[/green] Constitution found: {self.constitution_file}")
            version = self._extract_version(self.constitution_file)
            console.print(f"[dim]  Version: {version}[/dim]")
            return True, str(self.constitution_file)
        
        # Create new constitution
        from ..loading import loading_spinner
        
        with loading_spinner("Creating new constitution", "Constitution created"):
            # Load template
            if not self.template_file.exists():
                console.print(f"[red]✗[/red] Template not found: {self.template_file}")
                return False, ""
            
            with open(self.template_file, "r") as f:
                template = f.read()
            
            # Fill placeholders
            constitution = self._fill_template(
                template,
                project_name=project_name,
                project_description=project_description
            )
            
            # Save constitution
            with open(self.constitution_file, "w") as f:
                f.write(constitution)
        
        console.print(f"[dim]  Location: {self.constitution_file}[/dim]")
        console.print(f"[dim]  Version: 1.0.0[/dim]")
        
        return True, str(self.constitution_file)
    
    def _extract_version(self, constitution_file: Path) -> str:
        """
        Extract version from constitution file.
        
        Args:
            constitution_file: Constitution file path
            
        Returns:
            Version string (e.g., "1.0.0")
        """
        with open(constitution_file, "r") as f:
            content = f.read()
        
        # Look for version pattern
        match = re.search(r"Version:\s*(\d+\.\d+\.\d+)", content)
        if match:
            return match.group(1)
        
        return "unknown"
    
    def _fill_template(self, template: str, project_name: str, project_description: str) -> str:
        """
        Fill template placeholders with actual values.
        
        Args:
            template: Template content
            project_name: Project name
            project_description: Project description
            
        Returns:
            Filled template
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Basic replacements
        replacements = {
            "[PROJECT_NAME]": project_name,
            "[PROJECT_DESCRIPTION]": project_description,
            "[CONSTITUTION_VERSION]": "1.0.0",
            "[RATIFICATION_DATE]": today,
            "[LAST_AMENDED_DATE]": today,
        }
        
        result = template
        for placeholder, value in replacements.items():
            result = result.replace(placeholder, value)
        
        return result
    
    def validate(self, constitution_path: str) -> Tuple[bool, list]:
        """
        Validate constitution file.
        
        Args:
            constitution_path: Path to constitution file
            
        Returns:
            (is_valid, errors)
        """
        errors = []
        
        if not Path(constitution_path).exists():
            errors.append("Constitution file does not exist")
            return False, errors
        
        with open(constitution_path, "r") as f:
            content = f.read()
        
        # Check for unexplained placeholders
        placeholders = re.findall(r"\[([A-Z_]+)\]", content)
        if placeholders:
            errors.append(f"Unexplained placeholders found: {', '.join(placeholders)}")
        
        # Check for version
        if not re.search(r"Version:\s*\d+\.\d+\.\d+", content):
            errors.append("Version not found or invalid format")
        
        # Check for dates in ISO format
        if not re.search(r"\d{4}-\d{2}-\d{2}", content):
            errors.append("Dates not in ISO format (YYYY-MM-DD)")
        
        return len(errors) == 0, errors
