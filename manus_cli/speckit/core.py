"""
Spec-Kit Core Engine
Orchestrates the spec-driven development workflow
"""

import os
import json
from pathlib import Path
from typing import Optional, Tuple, Dict, Any
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

console = Console()

# Trigger keywords for Spec-Driven mode
SPEC_DRIVEN_KEYWORDS = [
    # French
    "créer", "creer", "construire", "développer", "developper",
    "réflexion", "reflexion", "penser", "projet", "application",
    "coder", "programmer", "implémenter", "implementer",
    # English
    "create", "build", "develop", "thinking", "think",
    "project", "app", "application", "code", "program",
    "implement", "design", "architect",
]


def should_use_spec_driven(message: str) -> Tuple[bool, str]:
    """
    Detect if message requires spec-driven process.
    
    Returns:
        (should_use, complexity_level)
        complexity_level: "simple" | "moderate" | "complex"
    """
    message_lower = message.lower()
    
    # Check for trigger keywords
    has_trigger = any(kw in message_lower for kw in SPEC_DRIVEN_KEYWORDS)
    
    if not has_trigger:
        return False, "none"
    
    # Assess complexity
    complexity = assess_complexity(message)
    
    return True, complexity


def assess_complexity(message: str) -> str:
    """
    Assess the complexity of the request.
    
    Returns: "simple" | "moderate" | "complex"
    """
    word_count = len(message.split())
    
    # Check for multiple features
    multiple_indicators = ["et", "and", "avec", "with", "plus", "also", "également"]
    has_multiple = any(word in message.lower() for word in multiple_indicators)
    
    # Check for technical terms
    technical_terms = [
        "api", "database", "auth", "authentication", "backend", "frontend",
        "microservice", "docker", "kubernetes", "ci/cd", "deployment"
    ]
    has_technical = any(term in message.lower() for term in technical_terms)
    
    # Complexity scoring
    if word_count < 10 and not has_multiple and not has_technical:
        return "simple"
    elif word_count < 30 and not (has_multiple and has_technical):
        return "moderate"
    else:
        return "complex"


class SpecKitEngine:
    """
    Main Spec-Kit engine that orchestrates the workflow.
    """
    
    def __init__(self, project_dir: Path = None):
        """
        Initialize the Spec-Kit engine.
        
        Args:
            project_dir: Project directory (defaults to current directory)
        """
        self.project_dir = project_dir or Path.cwd()
        self.manus_dir = self.project_dir / ".manus"
        self.memory_dir = self.manus_dir / "memory"
        self.specs_dir = self.manus_dir / "specs"
        
        # Ensure directories exist
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.specs_dir.mkdir(parents=True, exist_ok=True)
    
    def show_splash_screen(self, mode: str, role: str, complexity: str):
        """
        Display the Spec-Driven splash screen with ASCII art.
        """
        # ASCII art banner
        banner = """
 █████╗ ██╗      ██████╗██╗     ██╗    ██████╗ ██████╗ ██╗██╗   ██╗███████╗███╗   ██╗
██╔══██╗██║     ██╔════╝██║     ██║    ██╔══██╗██╔══██╗██║██║   ██║██╔════╝████╗  ██║
███████║██║     ██║     ██║     ██║    ██║  ██║██████╔╝██║██║   ██║█████╗  ██╔██╗ ██║
██╔══██║██║     ██║     ██║     ██║    ██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║
██║  ██║██║     ╚██████╗███████╗██║    ██████╔╝██║  ██║██║ ╚████╔╝ ███████╗██║ ╚████║
╚═╝  ╚═╝╚═╝      ╚═════╝╚══════╝╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝
        """
        
        console.print(f"[bold cyan]{banner}[/bold cyan]")
        console.print("[bold]Structured Thinking Process Activated[/bold]")
        console.print()
        
        # Info table
        info_table = Table(show_header=False, box=None, padding=(0, 2))
        info_table.add_column("Key", style="cyan", justify="right")
        info_table.add_column("Value", style="white")
        
        info_table.add_row("Mode", mode.upper())
        info_table.add_row("Role", role.title())
        info_table.add_row("Complexity", complexity.upper())
        info_table.add_row("Methodology", "GitHub Spec-Kit")
        info_table.add_row("Version", "4.0.0")
        
        panel = Panel(
            info_table,
            title="[bold cyan]AI-CLI Driven Development[/bold cyan]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(panel)
        console.print()
    
    def get_next_feature_number(self) -> int:
        """
        Get the next feature number by finding the highest existing number.
        
        Returns:
            Next feature number (N+1)
        """
        max_num = 0
        
        # Check existing spec directories
        if self.specs_dir.exists():
            for item in self.specs_dir.iterdir():
                if item.is_dir() and item.name.startswith("feature-"):
                    try:
                        # Extract number from "feature-NNN-short-name"
                        parts = item.name.split("-")
                        if len(parts) >= 2:
                            num = int(parts[1])
                            max_num = max(max_num, num)
                    except (ValueError, IndexError):
                        continue
        
        return max_num + 1
    
    def generate_branch_name(self, description: str) -> str:
        """
        Generate a concise branch name from description.
        
        Format: action-noun (e.g., "add-user-auth")
        
        Args:
            description: Feature description
            
        Returns:
            Short branch name (2-4 words)
        """
        # Simple implementation: take first few meaningful words
        words = description.lower().split()
        
        # Filter out common words
        stop_words = {"a", "an", "the", "with", "for", "to", "in", "on", "at", "of", "and", "or"}
        meaningful_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Take first 3-4 words
        short_name = "-".join(meaningful_words[:4])
        
        # Clean up
        short_name = "".join(c if c.isalnum() or c == "-" else "-" for c in short_name)
        short_name = "-".join(filter(None, short_name.split("-")))  # Remove empty parts
        
        return short_name[:50]  # Limit length
    
    def save_metadata(self, feature_dir: Path, metadata: Dict[str, Any]):
        """
        Save feature metadata to JSON file.
        
        Args:
            feature_dir: Feature directory
            metadata: Metadata dictionary
        """
        metadata_file = feature_dir / "metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(metadata, f, indent=2, default=str)
    
    def load_metadata(self, feature_dir: Path) -> Optional[Dict[str, Any]]:
        """
        Load feature metadata from JSON file.
        
        Args:
            feature_dir: Feature directory
            
        Returns:
            Metadata dictionary or None if not found
        """
        metadata_file = feature_dir / "metadata.json"
        if not metadata_file.exists():
            return None
        
        with open(metadata_file, "r") as f:
            return json.load(f)
    
    def show_phase_header(self, phase_num: int, phase_name: str, total_phases: int = 6):
        """
        Display a phase header.
        
        Args:
            phase_num: Current phase number
            phase_name: Phase name
            total_phases: Total number of phases
        """
        console.print()
        console.print(f"[bold cyan]Phase {phase_num}/{total_phases}: {phase_name}[/bold cyan]")
        console.print("━" * 60)
    
    def run_full_workflow(
        self,
        user_request: str,
        role: str = "developer",
        project_name: str = "project",
        skip_clarification: bool = False
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Run complete spec-driven workflow (all 6 phases)
        
        Returns:
            Tuple of (success, results_dict)
        """
        from .constitution import ConstitutionPhase
        from .specify import SpecificationPhase
        from .plan import PlanningPhase
        from .tasks import TaskBreakdownPhase
        from .implement import ImplementationPhase
        from .clarify import ClarificationPhase
        from .enhancements import EnhancementCommands
        from .diagrams import DiagramGenerator
        
        results = {
            "success": False,
            "phases": {},
            "artifacts": {},
            "errors": []
        }
        
        try:
            # Phase 1: Constitution
            self.show_phase_header(1, "Constitution")
            constitution_phase = ConstitutionPhase(self.memory_dir)
            success, constitution_content = constitution_phase.execute(project_name, role)
            results["phases"]["constitution"] = success
            results["artifacts"]["constitution"] = str(constitution_phase.constitution_file)
            
            if not success:
                results["errors"].append("Constitution phase failed")
                return False, results
            
            # Phase 2: Specification
            self.show_phase_header(2, "Specification")
            feature_name = self._generate_feature_name(user_request)
            feature_dir = self._create_feature_dir(feature_name)
            
            spec_phase = SpecificationPhase(feature_dir)
            success, spec_content = spec_phase.execute(user_request, project_name, role)
            results["phases"]["specification"] = success
            results["artifacts"]["specification"] = str(spec_phase.spec_file)
            
            if not success:
                results["errors"].append("Specification phase failed")
                return False, results
            
            # Phase 3: Planning
            self.show_phase_header(3, "Planning")
            plan_phase = PlanningPhase(feature_dir)
            success, plan_content = plan_phase.execute(spec_content, project_name, role)
            results["phases"]["planning"] = success
            results["artifacts"]["plan"] = str(plan_phase.plan_file)
            
            if not success:
                results["errors"].append("Planning phase failed")
                return False, results
            
            # Phase 4: Task Breakdown
            self.show_phase_header(4, "Task Breakdown")
            tasks_phase = TaskBreakdownPhase(feature_dir)
            success, tasks_content = tasks_phase.execute(plan_content, spec_content, project_name)
            results["phases"]["tasks"] = success
            results["artifacts"]["tasks"] = str(tasks_phase.tasks_file)
            
            if not success:
                results["errors"].append("Task breakdown phase failed")
                return False, results
            
            # Phase 5: Implementation
            self.show_phase_header(5, "Implementation")
            impl_phase = ImplementationPhase(feature_dir)
            success, impl_content = impl_phase.execute(tasks_content, plan_content, project_name)
            results["phases"]["implementation"] = success
            results["artifacts"]["implementation"] = str(impl_phase.implementation_file)
            
            if not success:
                results["errors"].append("Implementation phase failed")
                return False, results
            
            # Phase 6: Clarification (optional)
            if not skip_clarification:
                self.show_phase_header(6, "Clarification (Optional)")
                clarify_phase = ClarificationPhase(feature_dir)
                success, clarify_content = clarify_phase.execute(spec_content, plan_content, tasks_content)
                results["phases"]["clarification"] = success
                if clarify_content:
                    results["artifacts"]["clarification"] = str(clarify_phase.clarifications_file)
            
            # Generate diagrams
            console.print("\n[cyan]Generating diagrams...[/cyan]")
            diagram_gen = DiagramGenerator(feature_dir)
            diagrams = diagram_gen.generate_all(plan_content, spec_content)
            results["artifacts"]["diagrams"] = [str(d) for d in diagrams]
            
            # Run quality analysis
            console.print("\n[cyan]Running quality analysis...[/cyan]")
            enhancements = EnhancementCommands(feature_dir)
            analysis = enhancements.analyze()
            results["quality_analysis"] = analysis
            
            results["success"] = True
            
            # Display summary
            self._display_summary(results)
            
            return True, results
            
        except Exception as e:
            console.print(f"[red]Error in workflow: {e}[/red]")
            results["errors"].append(str(e))
            return False, results
    
    def _generate_feature_name(self, user_request: str) -> str:
        """Generate feature name from user request"""
        branch_name = self.generate_branch_name(user_request)
        feature_num = self.get_next_feature_number()
        return f"feature-{feature_num:03d}-{branch_name}"
    
    def _create_feature_dir(self, feature_name: str) -> Path:
        """Create feature directory"""
        feature_dir = self.specs_dir / feature_name
        feature_dir.mkdir(exist_ok=True)
        return feature_dir
    
    def _display_summary(self, results: Dict[str, Any]):
        """Display workflow summary"""
        console.print("\n" + "="*60)
        console.print(Panel(
            "[bold green]Spec-Driven Workflow Complete![/bold green]\n"
            "All phases executed successfully",
            border_style="green"
        ))
        
        # Phases summary
        console.print("\n[bold]Phases Completed:[/bold]")
        for phase, success in results["phases"].items():
            status = "✓" if success else "✗"
            color = "green" if success else "red"
            console.print(f"  [{color}]{status}[/{color}] {phase.title()}")
        
        # Artifacts summary
        console.print("\n[bold]Generated Artifacts:[/bold]")
        for artifact_type, path in results["artifacts"].items():
            if isinstance(path, list):
                console.print(f"  • {artifact_type.title()}: {len(path)} files")
            else:
                console.print(f"  • {artifact_type.title()}")
        
        # Quality score
        if "quality_analysis" in results:
            score = results["quality_analysis"].get("quality_score", 0)
            color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
            console.print(f"\n[bold]Quality Score:[/bold] [{color}]{score}%[/{color}]")
        
        # Next steps
        console.print("\n[bold]Next Steps:[/bold]")
        console.print("  1. Review generated specifications")
        console.print("  2. Run: manus analyze  (for detailed analysis)")
        console.print("  3. Run: manus checklist  (for quality checks)")
        console.print("  4. Run: manus github sync  (to push to GitHub)")
        console.print("  5. Run: manus github issues  (to create GitHub issues)")
