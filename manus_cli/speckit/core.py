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
███████╗██████╗ ███████╗ ██████╗    ██████╗ ██████╗ ██╗██╗   ██╗███████╗███╗   ██╗
██╔════╝██╔══██╗██╔════╝██╔════╝    ██╔══██╗██╔══██╗██║██║   ██║██╔════╝████╗  ██║
███████╗██████╔╝█████╗  ██║         ██║  ██║██████╔╝██║██║   ██║█████╗  ██╔██╗ ██║
╚════██║██╔═══╝ ██╔══╝  ██║         ██║  ██║██╔══██╗██║╚██╗ ██╔╝██╔══╝  ██║╚██╗██║
███████║██║     ███████╗╚██████╗    ██████╔╝██║  ██║██║ ╚████╔╝ ███████╗██║ ╚████║
╚══════╝╚═╝     ╚══════╝ ╚═════╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝
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
            title="[bold cyan]Spec-Driven Development[/bold cyan]",
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
    
    def show_phase_header(self, phase_num: int, phase_name: str, total_phases: int = 3):
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
