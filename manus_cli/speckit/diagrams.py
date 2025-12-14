"""
Diagram Generation: Mermaid and D2
Generates visual diagrams from specifications and plans
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()


class DiagramGenerator:
    """Generates diagrams from specifications using Mermaid and D2"""
    
    def __init__(self, spec_dir: Path):
        self.spec_dir = spec_dir
        self.diagrams_dir = spec_dir / "diagrams"
        self.diagrams_dir.mkdir(exist_ok=True)
    
    def generate_all(self, plan_content: str, spec_content: str) -> List[Path]:
        """
        Generate all relevant diagrams
        
        Returns:
            List of generated diagram file paths
        """
        console.print(Panel(
            "[bold cyan]Generating Diagrams[/bold cyan]\n"
            "Creating visual representations...",
            border_style="cyan"
        ))
        
        generated = []
        
        # Generate architecture diagram
        arch_diagram = self.generate_architecture_diagram(plan_content)
        if arch_diagram:
            generated.append(arch_diagram)
            console.print(f"✓ Architecture diagram: [cyan]{arch_diagram.name}[/cyan]")
        
        # Generate data flow diagram
        flow_diagram = self.generate_data_flow_diagram(plan_content)
        if flow_diagram:
            generated.append(flow_diagram)
            console.print(f"✓ Data flow diagram: [cyan]{flow_diagram.name}[/cyan]")
        
        # Generate user journey diagram
        journey_diagram = self.generate_user_journey(spec_content)
        if journey_diagram:
            generated.append(journey_diagram)
            console.print(f"✓ User journey diagram: [cyan]{journey_diagram.name}[/cyan]")
        
        # Generate sequence diagram
        sequence_diagram = self.generate_sequence_diagram(plan_content)
        if sequence_diagram:
            generated.append(sequence_diagram)
            console.print(f"✓ Sequence diagram: [cyan]{sequence_diagram.name}[/cyan]")
        
        if not generated:
            console.print("[yellow]No diagrams generated. Add more details to plan/spec.[/yellow]")
        
        return generated
    
    def generate_architecture_diagram(self, plan_content: str) -> Optional[Path]:
        """Generate architecture diagram using Mermaid"""
        
        # Extract architecture info from plan
        components = self._extract_components(plan_content)
        
        if not components:
            return None
        
        # Generate Mermaid syntax
        mermaid_code = "graph TD\n"
        mermaid_code += "    %% Architecture Diagram\n\n"
        
        # Add components
        for i, component in enumerate(components, 1):
            node_id = f"C{i}"
            mermaid_code += f"    {node_id}[{component}]\n"
        
        # Add connections (simple linear flow for now)
        for i in range(len(components) - 1):
            mermaid_code += f"    C{i+1} --> C{i+2}\n"
        
        # Add styling
        mermaid_code += "\n    classDef default fill:#f9f,stroke:#333,stroke-width:2px\n"
        
        # Save Mermaid file
        mermaid_file = self.diagrams_dir / "architecture.mmd"
        mermaid_file.write_text(mermaid_code)
        
        # Try to render to PNG (if manus-render-diagram is available)
        png_file = self.diagrams_dir / "architecture.png"
        try:
            result = subprocess.run(
                ["manus-render-diagram", str(mermaid_file), str(png_file)],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                return png_file
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return mermaid_file
    
    def generate_data_flow_diagram(self, plan_content: str) -> Optional[Path]:
        """Generate data flow diagram using D2"""
        
        # Extract data flows from plan
        flows = self._extract_data_flows(plan_content)
        
        if not flows:
            return None
        
        # Generate D2 syntax
        d2_code = "# Data Flow Diagram\n\n"
        d2_code += "direction: right\n\n"
        
        # Add nodes and connections
        for i, flow in enumerate(flows, 1):
            source = flow.get("source", f"Source{i}")
            target = flow.get("target", f"Target{i}")
            label = flow.get("label", "data")
            
            d2_code += f"{source} -> {target}: {label}\n"
        
        # Add styling
        d2_code += "\nstyle: {\n"
        d2_code += "  fill: \"#e1f5ff\"\n"
        d2_code += "  stroke: \"#0288d1\"\n"
        d2_code += "}\n"
        
        # Save D2 file
        d2_file = self.diagrams_dir / "dataflow.d2"
        d2_file.write_text(d2_code)
        
        # Try to render to PNG
        png_file = self.diagrams_dir / "dataflow.png"
        try:
            result = subprocess.run(
                ["manus-render-diagram", str(d2_file), str(png_file)],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                return png_file
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return d2_file
    
    def generate_user_journey(self, spec_content: str) -> Optional[Path]:
        """Generate user journey diagram using Mermaid"""
        
        # Extract user stories
        stories = self._extract_user_stories(spec_content)
        
        if not stories:
            return None
        
        # Generate Mermaid journey diagram
        mermaid_code = "journey\n"
        mermaid_code += "    title User Journey\n"
        
        for story in stories[:5]:  # Limit to 5 stories
            # Extract action from story
            action = story.split("I want to")[-1].strip() if "I want to" in story else story
            action = action.split("so that")[0].strip()
            
            mermaid_code += f"    section {action[:30]}\n"
            mermaid_code += f"      Start: 5: User\n"
            mermaid_code += f"      Action: 3: User, System\n"
            mermaid_code += f"      Complete: 5: User\n"
        
        # Save Mermaid file
        mermaid_file = self.diagrams_dir / "user-journey.mmd"
        mermaid_file.write_text(mermaid_code)
        
        # Try to render
        png_file = self.diagrams_dir / "user-journey.png"
        try:
            result = subprocess.run(
                ["manus-render-diagram", str(mermaid_file), str(png_file)],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                return png_file
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return mermaid_file
    
    def generate_sequence_diagram(self, plan_content: str) -> Optional[Path]:
        """Generate sequence diagram using Mermaid"""
        
        # Extract interactions from plan
        interactions = self._extract_interactions(plan_content)
        
        if not interactions:
            return None
        
        # Generate Mermaid sequence diagram
        mermaid_code = "sequenceDiagram\n"
        mermaid_code += "    participant User\n"
        mermaid_code += "    participant Frontend\n"
        mermaid_code += "    participant Backend\n"
        mermaid_code += "    participant Database\n\n"
        
        # Add interactions
        for interaction in interactions[:10]:  # Limit to 10
            mermaid_code += f"    User->>Frontend: {interaction}\n"
            mermaid_code += f"    Frontend->>Backend: Process request\n"
            mermaid_code += f"    Backend->>Database: Query data\n"
            mermaid_code += f"    Database-->>Backend: Return data\n"
            mermaid_code += f"    Backend-->>Frontend: Response\n"
            mermaid_code += f"    Frontend-->>User: Display result\n\n"
        
        # Save Mermaid file
        mermaid_file = self.diagrams_dir / "sequence.mmd"
        mermaid_file.write_text(mermaid_code)
        
        # Try to render
        png_file = self.diagrams_dir / "sequence.png"
        try:
            result = subprocess.run(
                ["manus-render-diagram", str(mermaid_file), str(png_file)],
                capture_output=True,
                timeout=10
            )
            if result.returncode == 0:
                return png_file
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return mermaid_file
    
    def _extract_components(self, plan_content: str) -> List[str]:
        """Extract architecture components from plan"""
        components = []
        
        # Look for component lists
        lines = plan_content.split("\n")
        in_components = False
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ["component", "layer", "module", "service"]):
                in_components = True
                continue
            
            if in_components and line.startswith("##"):
                break
            
            if in_components and (line.strip().startswith("-") or line.strip().startswith("*")):
                component = line.strip().lstrip("-*").strip()
                if component and len(component) < 50:
                    components.append(component.split(":")[0].strip())
        
        # Default components if none found
        if not components:
            components = ["Frontend", "API", "Backend", "Database"]
        
        return components[:8]  # Limit to 8 components
    
    def _extract_data_flows(self, plan_content: str) -> List[Dict[str, str]]:
        """Extract data flows from plan"""
        flows = []
        
        # Look for data flow descriptions
        lines = plan_content.split("\n")
        
        for line in lines:
            if "->" in line or "→" in line or "to" in line.lower():
                parts = line.replace("->", "→").split("→")
                if len(parts) >= 2:
                    source = parts[0].strip().lstrip("-*").strip()
                    target = parts[1].strip()
                    
                    if source and target:
                        flows.append({
                            "source": source[:30],
                            "target": target[:30],
                            "label": "data"
                        })
        
        # Default flows if none found
        if not flows:
            flows = [
                {"source": "User", "target": "Frontend", "label": "request"},
                {"source": "Frontend", "target": "API", "label": "call"},
                {"source": "API", "target": "Database", "label": "query"}
            ]
        
        return flows[:10]  # Limit to 10 flows
    
    def _extract_user_stories(self, spec_content: str) -> List[str]:
        """Extract user stories from spec"""
        stories = []
        
        lines = spec_content.split("\n")
        for line in lines:
            if "as a" in line.lower() or "i want to" in line.lower():
                story = line.strip().lstrip("-*0123456789.").strip()
                if story:
                    stories.append(story)
        
        return stories
    
    def _extract_interactions(self, plan_content: str) -> List[str]:
        """Extract user interactions from plan"""
        interactions = []
        
        # Look for action verbs
        action_verbs = ["create", "read", "update", "delete", "submit", "view", "edit", "search"]
        
        lines = plan_content.split("\n")
        for line in lines:
            for verb in action_verbs:
                if verb in line.lower():
                    interaction = line.strip().lstrip("-*").strip()
                    if interaction and len(interaction) < 50:
                        interactions.append(interaction[:40])
                        break
        
        # Default interactions
        if not interactions:
            interactions = ["Create item", "View list", "Update item", "Delete item"]
        
        return interactions
