"""
Analytics and Metrics
Track spec-driven development metrics and progress
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


class Analytics:
    """Analytics for spec-driven development"""
    
    def __init__(self, manus_dir: Path):
        self.manus_dir = manus_dir
        self.analytics_file = manus_dir / "analytics.json"
        self.load_analytics()
    
    def load_analytics(self):
        """Load analytics data"""
        if self.analytics_file.exists():
            self.data = json.loads(self.analytics_file.read_text())
        else:
            self.data = {
                "projects": {},
                "total_specs": 0,
                "total_tasks": 0,
                "completed_tasks": 0,
                "quality_scores": [],
                "timeline": []
            }
    
    def save_analytics(self):
        """Save analytics data"""
        self.analytics_file.write_text(json.dumps(self.data, indent=2))
    
    def track_project(self, project_name: str, spec_dir: Path):
        """Track a new project"""
        project_data = {
            "name": project_name,
            "created": datetime.now().isoformat(),
            "spec_dir": str(spec_dir),
            "phases_completed": [],
            "quality_score": 0,
            "tasks_total": 0,
            "tasks_completed": 0
        }
        
        self.data["projects"][project_name] = project_data
        self.data["total_specs"] += 1
        
        self.data["timeline"].append({
            "timestamp": datetime.now().isoformat(),
            "event": "project_created",
            "project": project_name
        })
        
        self.save_analytics()
    
    def track_phase_completion(self, project_name: str, phase: str):
        """Track phase completion"""
        if project_name in self.data["projects"]:
            project = self.data["projects"][project_name]
            if phase not in project["phases_completed"]:
                project["phases_completed"].append(phase)
                
                self.data["timeline"].append({
                    "timestamp": datetime.now().isoformat(),
                    "event": "phase_completed",
                    "project": project_name,
                    "phase": phase
                })
                
                self.save_analytics()
    
    def track_quality_score(self, project_name: str, score: float):
        """Track quality score"""
        if project_name in self.data["projects"]:
            self.data["projects"][project_name]["quality_score"] = score
            self.data["quality_scores"].append({
                "project": project_name,
                "score": score,
                "timestamp": datetime.now().isoformat()
            })
            self.save_analytics()
    
    def track_tasks(self, project_name: str, total: int, completed: int):
        """Track task progress"""
        if project_name in self.data["projects"]:
            project = self.data["projects"][project_name]
            old_total = project["tasks_total"]
            old_completed = project["tasks_completed"]
            
            project["tasks_total"] = total
            project["tasks_completed"] = completed
            
            self.data["total_tasks"] += (total - old_total)
            self.data["completed_tasks"] += (completed - old_completed)
            
            self.save_analytics()
    
    def display_dashboard(self):
        """Display analytics dashboard"""
        console.print(Panel(
            "[bold cyan]Analytics Dashboard[/bold cyan]\n"
            "Spec-Driven Development Metrics",
            border_style="cyan"
        ))
        
        # Overall stats
        console.print("\n[bold]Overall Statistics[/bold]")
        stats_table = Table()
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")
        
        stats_table.add_row("Total Projects", str(self.data["total_specs"]))
        stats_table.add_row("Total Tasks", str(self.data["total_tasks"]))
        stats_table.add_row("Completed Tasks", str(self.data["completed_tasks"]))
        
        completion_rate = 0
        if self.data["total_tasks"] > 0:
            completion_rate = (self.data["completed_tasks"] / self.data["total_tasks"]) * 100
        stats_table.add_row("Completion Rate", f"{completion_rate:.1f}%")
        
        avg_quality = 0
        if self.data["quality_scores"]:
            avg_quality = sum(s["score"] for s in self.data["quality_scores"]) / len(self.data["quality_scores"])
        stats_table.add_row("Avg Quality Score", f"{avg_quality:.1f}%")
        
        console.print(stats_table)
        
        # Recent projects
        console.print("\n[bold]Recent Projects[/bold]")
        projects_table = Table()
        projects_table.add_column("Project", style="cyan")
        projects_table.add_column("Phases", style="yellow")
        projects_table.add_column("Quality", style="green")
        projects_table.add_column("Tasks", style="blue")
        
        recent_projects = sorted(
            self.data["projects"].items(),
            key=lambda x: x[1].get("created", ""),
            reverse=True
        )[:5]
        
        for name, project in recent_projects:
            phases = len(project.get("phases_completed", []))
            quality = project.get("quality_score", 0)
            tasks = f"{project.get('tasks_completed', 0)}/{project.get('tasks_total', 0)}"
            
            projects_table.add_row(name, f"{phases}/6", f"{quality:.1f}%", tasks)
        
        console.print(projects_table)
        
        # Timeline
        console.print("\n[bold]Recent Activity[/bold]")
        recent_events = self.data["timeline"][-10:]
        
        for event in reversed(recent_events):
            timestamp = datetime.fromisoformat(event["timestamp"])
            time_str = timestamp.strftime("%Y-%m-%d %H:%M")
            event_type = event["event"].replace("_", " ").title()
            project = event.get("project", "")
            phase = event.get("phase", "")
            
            if phase:
                console.print(f"  [{time_str}] {event_type}: {project} - {phase}")
            else:
                console.print(f"  [{time_str}] {event_type}: {project}")
    
    def generate_report(self) -> str:
        """Generate analytics report"""
        report = "# Spec-Driven Development Analytics Report\n\n"
        report += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Overall metrics
        report += "## Overall Metrics\n\n"
        report += f"- **Total Projects**: {self.data['total_specs']}\n"
        report += f"- **Total Tasks**: {self.data['total_tasks']}\n"
        report += f"- **Completed Tasks**: {self.data['completed_tasks']}\n"
        
        completion_rate = 0
        if self.data["total_tasks"] > 0:
            completion_rate = (self.data["completed_tasks"] / self.data["total_tasks"]) * 100
        report += f"- **Completion Rate**: {completion_rate:.1f}%\n"
        
        avg_quality = 0
        if self.data["quality_scores"]:
            avg_quality = sum(s["score"] for s in self.data["quality_scores"]) / len(self.data["quality_scores"])
        report += f"- **Average Quality Score**: {avg_quality:.1f}%\n\n"
        
        # Project details
        report += "## Projects\n\n"
        
        for name, project in self.data["projects"].items():
            report += f"### {name}\n\n"
            report += f"- **Created**: {project.get('created', 'Unknown')}\n"
            report += f"- **Phases Completed**: {len(project.get('phases_completed', []))}/6\n"
            report += f"- **Quality Score**: {project.get('quality_score', 0):.1f}%\n"
            report += f"- **Tasks**: {project.get('tasks_completed', 0)}/{project.get('tasks_total', 0)}\n\n"
        
        # Trends
        report += "## Trends\n\n"
        
        if len(self.data["quality_scores"]) >= 2:
            recent_scores = [s["score"] for s in self.data["quality_scores"][-5:]]
            trend = "improving" if recent_scores[-1] > recent_scores[0] else "declining"
            report += f"- Quality trend: {trend}\n"
        
        report += f"- Total activity events: {len(self.data['timeline'])}\n"
        
        return report
