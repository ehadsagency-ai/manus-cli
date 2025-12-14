"""
Phase 6: Clarification (Optional)
Identifies and resolves ambiguities in specifications
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()


class ClarificationPhase:
    """Handles Phase 6: Clarification (Optional)"""
    
    def __init__(self, spec_dir: Path):
        self.spec_dir = spec_dir
        self.clarifications_file = spec_dir / "clarifications.md"
        self.metadata_file = spec_dir / "metadata.json"
        self.max_clarifications = 3
    
    def execute(self, spec_content: str, plan_content: str, tasks_content: str) -> Tuple[bool, str]:
        """
        Execute clarification phase
        
        Returns:
            Tuple of (success, clarifications_content)
        """
        console.print(Panel(
            "[bold cyan]Phase 6/6: Clarification (Optional)[/bold cyan]\n"
            "Identifying ambiguities and assumptions...",
            border_style="cyan"
        ))
        
        # Identify ambiguities
        ambiguities = self._identify_ambiguities(spec_content, plan_content, tasks_content)
        
        if not ambiguities:
            console.print("✓ No significant ambiguities found. Specifications are clear.")
            return True, ""
        
        console.print(f"\n[yellow]Found {len(ambiguities)} items needing clarification:[/yellow]")
        for i, amb in enumerate(ambiguities[:5], 1):
            console.print(f"  {i}. {amb['question']}")
        
        # Ask if user wants to clarify now
        if len(ambiguities) > 5:
            console.print(f"  ... and {len(ambiguities) - 5} more")
        
        clarify_now = Confirm.ask("\nWould you like to address these clarifications now?", default=False)
        
        if not clarify_now:
            console.print("[yellow]Skipping clarifications.[/yellow] You can address them later.")
            return True, ""
        
        # Interactive clarification
        clarifications = self._interactive_clarification(ambiguities)
        
        # Generate clarifications document
        clarifications_content = self._generate_clarifications_doc(clarifications)
        
        # Save clarifications
        self._save_clarifications(clarifications_content)
        
        console.print(f"✓ Clarifications saved: [cyan]{self.clarifications_file}[/cyan]")
        
        return True, clarifications_content
    
    def _identify_ambiguities(
        self, spec_content: str, plan_content: str, tasks_content: str
    ) -> List[Dict[str, str]]:
        """Identify ambiguities and assumptions in specifications"""
        ambiguities = []
        
        # Check for [NEEDS CLARIFICATION] markers
        for content, source in [
            (spec_content, "specification"),
            (plan_content, "plan"),
            (tasks_content, "tasks")
        ]:
            for line in content.split("\n"):
                if "[NEEDS CLARIFICATION]" in line:
                    question = line.replace("[NEEDS CLARIFICATION]", "").strip()
                    ambiguities.append({
                        "source": source,
                        "question": question,
                        "answer": ""
                    })
        
        # Check for vague terms in spec
        vague_terms = ["maybe", "possibly", "probably", "should", "could", "might"]
        for line in spec_content.split("\n"):
            for term in vague_terms:
                if term in line.lower():
                    ambiguities.append({
                        "source": "specification",
                        "question": f"Clarify: {line.strip()}",
                        "answer": ""
                    })
                    break
        
        # Check for missing details in plan
        if "TBD" in plan_content or "TODO" in plan_content:
            ambiguities.append({
                "source": "plan",
                "question": "Complete TBD/TODO items in technical plan",
                "answer": ""
            })
        
        # Limit to max clarifications
        return ambiguities[:self.max_clarifications]
    
    def _interactive_clarification(self, ambiguities: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Interactive clarification process"""
        clarifications = []
        
        console.print("\n[bold]Clarification Process[/bold]")
        console.print("Please provide answers to the following questions:\n")
        
        for i, amb in enumerate(ambiguities, 1):
            console.print(f"[cyan]Question {i}/{len(ambiguities)}[/cyan] ({amb['source']})")
            console.print(f"  {amb['question']}")
            
            answer = Prompt.ask("  Your answer", default="Skip")
            
            if answer.lower() != "skip":
                clarifications.append({
                    "source": amb['source'],
                    "question": amb['question'],
                    "answer": answer,
                    "timestamp": datetime.now().isoformat()
                })
            
            console.print()
        
        return clarifications
    
    def _generate_clarifications_doc(self, clarifications: List[Dict[str, str]]) -> str:
        """Generate clarifications document"""
        doc = "# Clarifications\n\n"
        doc += f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        doc += f"**Total Clarifications**: {len(clarifications)}\n\n"
        doc += "## Questions and Answers\n\n"
        
        for i, clar in enumerate(clarifications, 1):
            doc += f"### {i}. {clar['source'].title()}\n\n"
            doc += f"**Question**: {clar['question']}\n\n"
            doc += f"**Answer**: {clar['answer']}\n\n"
            doc += f"**Timestamp**: {clar['timestamp']}\n\n"
            doc += "---\n\n"
        
        doc += "## Impact Analysis\n\n"
        doc += "These clarifications may require updates to:\n\n"
        
        sources = set(c['source'] for c in clarifications)
        for source in sources:
            doc += f"- {source.title()}\n"
        
        doc += "\n## Next Steps\n\n"
        doc += "1. Review clarifications\n"
        doc += "2. Update affected documents\n"
        doc += "3. Validate consistency across all artifacts\n"
        
        return doc
    
    def _save_clarifications(self, clarifications_content: str):
        """Save clarifications to file"""
        self.clarifications_file.write_text(clarifications_content)
        
        # Update metadata
        if self.metadata_file.exists():
            metadata = json.loads(self.metadata_file.read_text())
        else:
            metadata = {}
        
        metadata["clarifications_completed"] = datetime.now().isoformat()
        metadata["clarifications_file"] = str(self.clarifications_file)
        
        self.metadata_file.write_text(json.dumps(metadata, indent=2))
