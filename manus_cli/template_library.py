"""
Template Library
Manage and customize spec templates
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()


class TemplateLibrary:
    """Template library for spec-driven development"""
    
    def __init__(self, templates_dir: Path):
        self.templates_dir = templates_dir
        self.templates_dir.mkdir(parents=True, exist_ok=True)
        self.catalog_file = templates_dir / "catalog.json"
        self.load_catalog()
    
    def load_catalog(self):
        """Load template catalog"""
        if self.catalog_file.exists():
            self.catalog = json.loads(self.catalog_file.read_text())
        else:
            self.catalog = {
                "templates": {},
                "categories": ["web", "api", "mobile", "data", "ml", "general"]
            }
            self.save_catalog()
    
    def save_catalog(self):
        """Save template catalog"""
        self.catalog_file.write_text(json.dumps(self.catalog, indent=2))
    
    def list_templates(self, category: Optional[str] = None):
        """List available templates"""
        console.print(Panel(
            "[bold cyan]Template Library[/bold cyan]\n"
            "Available spec templates",
            border_style="cyan"
        ))
        
        # Filter by category if specified
        templates = self.catalog["templates"]
        if category:
            templates = {
                k: v for k, v in templates.items()
                if v.get("category") == category
            }
        
        if not templates:
            console.print("[yellow]No templates found.[/yellow]")
            return
        
        # Display templates
        table = Table()
        table.add_column("Name", style="cyan")
        table.add_column("Category", style="yellow")
        table.add_column("Description", style="white")
        
        for name, template in templates.items():
            table.add_row(
                name,
                template.get("category", "general"),
                template.get("description", "")
            )
        
        console.print(table)
    
    def add_template(self, name: str, category: str, description: str, files: Dict[str, str]):
        """Add a new template"""
        console.print(Panel(
            f"[bold cyan]Adding Template: {name}[/bold cyan]",
            border_style="cyan"
        ))
        
        # Create template directory
        template_dir = self.templates_dir / name
        template_dir.mkdir(exist_ok=True)
        
        # Save template files
        for filename, content in files.items():
            file_path = template_dir / filename
            file_path.write_text(content)
        
        # Update catalog
        self.catalog["templates"][name] = {
            "category": category,
            "description": description,
            "files": list(files.keys()),
            "created": str(Path.ctime(template_dir))
        }
        self.save_catalog()
        
        console.print(f"✓ Template '{name}' added successfully")
    
    def get_template(self, name: str) -> Optional[Dict[str, str]]:
        """Get template files"""
        if name not in self.catalog["templates"]:
            console.print(f"[red]Template '{name}' not found.[/red]")
            return None
        
        template_dir = self.templates_dir / name
        if not template_dir.exists():
            console.print(f"[red]Template directory not found: {template_dir}[/red]")
            return None
        
        # Load template files
        template_info = self.catalog["templates"][name]
        files = {}
        
        for filename in template_info["files"]:
            file_path = template_dir / filename
            if file_path.exists():
                files[filename] = file_path.read_text()
        
        return files
    
    def customize_template(self, name: str):
        """Interactive template customization"""
        console.print(Panel(
            f"[bold cyan]Customizing Template: {name}[/bold cyan]",
            border_style="cyan"
        ))
        
        # Get template
        files = self.get_template(name)
        if not files:
            return
        
        console.print("\n[bold]Available files:[/bold]")
        for i, filename in enumerate(files.keys(), 1):
            console.print(f"  {i}. {filename}")
        
        # Select file to customize
        file_choice = Prompt.ask("\nSelect file to customize (number)", default="1")
        try:
            file_index = int(file_choice) - 1
            filename = list(files.keys())[file_index]
        except (ValueError, IndexError):
            console.print("[red]Invalid selection.[/red]")
            return
        
        # Show current content
        console.print(f"\n[bold]Current content of {filename}:[/bold]")
        console.print(files[filename][:500] + "..." if len(files[filename]) > 500 else files[filename])
        
        # Ask for customization
        if Confirm.ask("\nEdit this file?"):
            console.print("\n[yellow]Note: Open the file in your editor:[/yellow]")
            template_path = self.templates_dir / name / filename
            console.print(f"  {template_path}")
            console.print("\nPress Enter when done editing...")
            input()
            
            # Reload template
            files[filename] = template_path.read_text()
            console.print("✓ Template updated")
    
    def create_preset_templates(self):
        """Create preset templates"""
        console.print("Creating preset templates...")
        
        # Web App Template
        self.add_template(
            "web-app",
            "web",
            "Full-stack web application",
            {
                "constitution-template.md": self._get_web_constitution(),
                "spec-template.md": self._get_web_spec(),
                "plan-template.md": self._get_web_plan()
            }
        )
        
        # API Template
        self.add_template(
            "rest-api",
            "api",
            "RESTful API service",
            {
                "constitution-template.md": self._get_api_constitution(),
                "spec-template.md": self._get_api_spec(),
                "plan-template.md": self._get_api_plan()
            }
        )
        
        # Data Pipeline Template
        self.add_template(
            "data-pipeline",
            "data",
            "Data processing pipeline",
            {
                "constitution-template.md": self._get_data_constitution(),
                "spec-template.md": self._get_data_spec(),
                "plan-template.md": self._get_data_plan()
            }
        )
        
        console.print("✓ Preset templates created")
    
    def _get_web_constitution(self) -> str:
        return """# Web Application Constitution

**Version**: 1.0.0

## Principles

1. **User-First Design**: Prioritize user experience
2. **Responsive**: Work on all devices
3. **Performance**: Fast load times (<3s)
4. **Accessibility**: WCAG 2.1 AA compliance
5. **Security**: HTTPS, input validation, auth

## Tech Stack Preferences

- Frontend: React/Vue/Angular
- Backend: Node.js/Python/Java
- Database: PostgreSQL/MongoDB
- Hosting: Cloud platform (AWS/GCP/Azure)
"""
    
    def _get_web_spec(self) -> str:
        return """# [FEATURE_NAME]

## Overview

[DESCRIPTION]

## User Stories

- As a [USER_TYPE], I want to [ACTION] so that [BENEFIT]

## Requirements

### Functional
- [REQUIREMENT_1]

### Non-Functional
- Performance: [METRIC]
- Security: [REQUIREMENT]

## Success Criteria

- [ ] [CRITERION_1]
"""
    
    def _get_web_plan(self) -> str:
        return """# Technical Plan: [FEATURE_NAME]

## Architecture

### Frontend
- Framework: [FRAMEWORK]
- State Management: [SOLUTION]

### Backend
- Framework: [FRAMEWORK]
- API: REST/GraphQL

### Database
- Type: [DATABASE]
- Schema: [DESCRIPTION]

## Implementation Phases

1. Setup & Configuration
2. Backend API Development
3. Frontend Development
4. Integration & Testing
"""
    
    def _get_api_constitution(self) -> str:
        return """# API Constitution

**Version**: 1.0.0

## Principles

1. **RESTful Design**: Follow REST principles
2. **Versioning**: API versioning from v1
3. **Documentation**: OpenAPI/Swagger docs
4. **Security**: Authentication & rate limiting
5. **Monitoring**: Logging & metrics
"""
    
    def _get_api_spec(self) -> str:
        return """# API Specification: [API_NAME]

## Endpoints

### GET /[RESOURCE]
- **Description**: [DESCRIPTION]
- **Auth**: Required/Optional
- **Response**: [SCHEMA]

### POST /[RESOURCE]
- **Description**: [DESCRIPTION]
- **Body**: [SCHEMA]
- **Response**: [SCHEMA]

## Data Models

### [MODEL_NAME]
```json
{
  "field": "type"
}
```
"""
    
    def _get_api_plan(self) -> str:
        return """# API Implementation Plan

## Tech Stack
- Framework: [FRAMEWORK]
- Database: [DATABASE]
- Auth: [METHOD]

## Endpoints Implementation

1. Setup project structure
2. Implement data models
3. Create API endpoints
4. Add authentication
5. Write tests
6. Deploy
"""
    
    def _get_data_constitution(self) -> str:
        return """# Data Pipeline Constitution

**Version**: 1.0.0

## Principles

1. **Data Quality**: Validation at every step
2. **Scalability**: Handle growing data volumes
3. **Reliability**: Error handling & retries
4. **Monitoring**: Track pipeline health
5. **Documentation**: Clear data lineage
"""
    
    def _get_data_spec(self) -> str:
        return """# Data Pipeline Specification

## Data Sources
- Source 1: [DESCRIPTION]
- Source 2: [DESCRIPTION]

## Transformations
1. [TRANSFORMATION_1]
2. [TRANSFORMATION_2]

## Output
- Destination: [LOCATION]
- Format: [FORMAT]
- Schedule: [FREQUENCY]
"""
    
    def _get_data_plan(self) -> str:
        return """# Data Pipeline Implementation Plan

## Architecture
- Orchestration: [TOOL]
- Processing: [FRAMEWORK]
- Storage: [DATABASE]

## Implementation Steps
1. Setup infrastructure
2. Implement data ingestion
3. Build transformations
4. Setup scheduling
5. Add monitoring
"""
