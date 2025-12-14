"""
Enhancement Commands: analyze, checklist
Additional quality assurance and analysis tools
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


class EnhancementCommands:
    """Enhancement commands for quality assurance"""
    
    def __init__(self, spec_dir: Path):
        self.spec_dir = spec_dir
        self.metadata_file = spec_dir / "metadata.json"
    
    def analyze(self) -> Dict[str, any]:
        """
        Analyze all artifacts for quality and consistency
        
        Returns:
            Analysis results dictionary
        """
        console.print(Panel(
            "[bold cyan]Analyzing Artifacts[/bold cyan]\n"
            "Checking quality and consistency...",
            border_style="cyan"
        ))
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "artifacts": {},
            "consistency": {},
            "quality_score": 0,
            "recommendations": []
        }
        
        # Analyze each artifact
        artifacts = {
            "constitution": self.spec_dir.parent.parent / "memory" / "constitution.md",
            "spec": self.spec_dir / "spec.md",
            "plan": self.spec_dir / "plan.md",
            "tasks": self.spec_dir / "tasks.md",
            "implementation": self.spec_dir / "implementation.md"
        }
        
        for name, path in artifacts.items():
            if path.exists():
                content = path.read_text()
                analysis = self._analyze_artifact(name, content)
                results["artifacts"][name] = analysis
        
        # Check consistency across artifacts
        results["consistency"] = self._check_consistency(artifacts)
        
        # Calculate quality score
        results["quality_score"] = self._calculate_quality_score(results)
        
        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)
        
        # Display results
        self._display_analysis_results(results)
        
        # Save analysis
        analysis_file = self.spec_dir / "analysis.json"
        analysis_file.write_text(json.dumps(results, indent=2))
        
        console.print(f"\n✓ Analysis saved: [cyan]{analysis_file}[/cyan]")
        
        return results
    
    def checklist(self) -> Dict[str, bool]:
        """
        Run quality checklist on all artifacts
        
        Returns:
            Checklist results dictionary
        """
        console.print(Panel(
            "[bold cyan]Quality Checklist[/bold cyan]\n"
            "Running comprehensive quality checks...",
            border_style="cyan"
        ))
        
        # Load checklist template
        checklist_items = self._load_checklist()
        
        # Run checks
        results = {}
        for category, items in checklist_items.items():
            console.print(f"\n[bold]{category}[/bold]")
            results[category] = {}
            
            for item in items:
                passed = self._check_item(item)
                results[category][item["name"]] = passed
                
                status = "✓" if passed else "✗"
                color = "green" if passed else "red"
                console.print(f"  [{color}]{status}[/{color}] {item['name']}")
        
        # Calculate pass rate
        total = sum(len(items) for items in results.values())
        passed = sum(
            1 for category in results.values()
            for passed in category.values()
            if passed
        )
        pass_rate = (passed / total * 100) if total > 0 else 0
        
        console.print(f"\n[bold]Pass Rate:[/bold] {pass_rate:.1f}% ({passed}/{total})")
        
        # Save checklist results
        checklist_file = self.spec_dir / "checklist-results.json"
        checklist_file.write_text(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "results": results,
            "pass_rate": pass_rate,
            "passed": passed,
            "total": total
        }, indent=2))
        
        console.print(f"✓ Checklist results saved: [cyan]{checklist_file}[/cyan]")
        
        return results
    
    def _analyze_artifact(self, name: str, content: str) -> Dict[str, any]:
        """Analyze a single artifact"""
        analysis = {
            "length": len(content),
            "lines": len(content.split("\n")),
            "sections": content.count("##"),
            "placeholders": self._count_placeholders(content),
            "completeness": 0,
            "issues": []
        }
        
        # Check for placeholders
        if analysis["placeholders"] > 0:
            analysis["issues"].append(f"{analysis['placeholders']} placeholders remaining")
        
        # Check for minimum content
        if analysis["length"] < 500:
            analysis["issues"].append("Content may be too brief")
        
        # Check for structure
        if analysis["sections"] < 3:
            analysis["issues"].append("May need more sections for clarity")
        
        # Calculate completeness
        max_issues = 3
        completeness = max(0, 100 - (len(analysis["issues"]) / max_issues * 100))
        analysis["completeness"] = round(completeness, 1)
        
        return analysis
    
    def _count_placeholders(self, content: str) -> int:
        """Count remaining placeholders in content"""
        count = 0
        for line in content.split("\n"):
            if "[" in line and "]" in line:
                start = line.index("[")
                end = line.index("]", start)
                placeholder = line[start+1:end]
                if placeholder.isupper():
                    count += 1
        return count
    
    def _check_consistency(self, artifacts: Dict[str, Path]) -> Dict[str, any]:
        """Check consistency across artifacts"""
        consistency = {
            "feature_name": True,
            "dates": True,
            "terminology": True,
            "issues": []
        }
        
        # Check feature name consistency
        feature_names = set()
        for name, path in artifacts.items():
            if path.exists():
                content = path.read_text()
                for line in content.split("\n"):
                    if "**Feature**:" in line:
                        feature_names.add(line.split("**Feature**:")[-1].strip())
        
        if len(feature_names) > 1:
            consistency["feature_name"] = False
            consistency["issues"].append("Inconsistent feature names across artifacts")
        
        return consistency
    
    def _calculate_quality_score(self, results: Dict[str, any]) -> float:
        """Calculate overall quality score"""
        if not results["artifacts"]:
            return 0.0
        
        # Average completeness across artifacts
        completeness_scores = [
            art["completeness"]
            for art in results["artifacts"].values()
        ]
        
        avg_completeness = sum(completeness_scores) / len(completeness_scores)
        
        # Consistency bonus
        consistency_score = 100 if not results["consistency"]["issues"] else 80
        
        # Weighted average
        quality_score = (avg_completeness * 0.7) + (consistency_score * 0.3)
        
        return round(quality_score, 1)
    
    def _generate_recommendations(self, results: Dict[str, any]) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        # Check quality score
        if results["quality_score"] < 70:
            recommendations.append("Overall quality is below target. Review all artifacts.")
        
        # Check individual artifacts
        for name, analysis in results["artifacts"].items():
            if analysis["placeholders"] > 0:
                recommendations.append(f"Fill remaining placeholders in {name}")
            
            if analysis["completeness"] < 80:
                recommendations.append(f"Improve completeness of {name}")
        
        # Check consistency
        if results["consistency"]["issues"]:
            for issue in results["consistency"]["issues"]:
                recommendations.append(f"Fix consistency: {issue}")
        
        if not recommendations:
            recommendations.append("All artifacts meet quality standards!")
        
        return recommendations
    
    def _display_analysis_results(self, results: Dict[str, any]):
        """Display analysis results in a table"""
        console.print("\n[bold]Analysis Results[/bold]\n")
        
        # Artifacts table
        table = Table(title="Artifact Analysis")
        table.add_column("Artifact", style="cyan")
        table.add_column("Completeness", style="green")
        table.add_column("Issues", style="yellow")
        
        for name, analysis in results["artifacts"].items():
            issues_str = f"{len(analysis['issues'])} issues" if analysis['issues'] else "None"
            table.add_row(
                name.title(),
                f"{analysis['completeness']}%",
                issues_str
            )
        
        console.print(table)
        
        # Quality score
        score = results["quality_score"]
        color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
        console.print(f"\n[bold]Quality Score:[/bold] [{color}]{score}%[/{color}]")
        
        # Recommendations
        if results["recommendations"]:
            console.print("\n[bold]Recommendations:[/bold]")
            for rec in results["recommendations"]:
                console.print(f"  • {rec}")
    
    def _load_checklist(self) -> Dict[str, List[Dict[str, str]]]:
        """Load quality checklist"""
        return {
            "Constitution": [
                {"name": "Principles defined", "check": "constitution_exists"},
                {"name": "Version specified", "check": "version_format"},
                {"name": "Governance rules clear", "check": "governance_section"}
            ],
            "Specification": [
                {"name": "Requirements documented", "check": "requirements_section"},
                {"name": "User stories present", "check": "user_stories"},
                {"name": "Success criteria defined", "check": "success_criteria"},
                {"name": "No technical details (HOW)", "check": "no_how_in_spec"}
            ],
            "Planning": [
                {"name": "Tech stack specified", "check": "tech_stack_section"},
                {"name": "Architecture documented", "check": "architecture_section"},
                {"name": "Risks identified", "check": "risks_section"},
                {"name": "File structure defined", "check": "file_structure"}
            ],
            "Tasks": [
                {"name": "Tasks broken down", "check": "task_list"},
                {"name": "Effort estimated", "check": "effort_estimates"},
                {"name": "Dependencies identified", "check": "dependencies"},
                {"name": "Acceptance criteria set", "check": "acceptance_criteria"}
            ]
        }
    
    def _check_item(self, item: Dict[str, str]) -> bool:
        """Check a single checklist item"""
        check_name = item["check"]
        
        # Simple checks based on file existence and content
        if check_name == "constitution_exists":
            const_file = self.spec_dir.parent.parent / "memory" / "constitution.md"
            return const_file.exists()
        
        if check_name == "version_format":
            const_file = self.spec_dir.parent.parent / "memory" / "constitution.md"
            if const_file.exists():
                content = const_file.read_text()
                return "Version:" in content or "**Version**:" in content
            return False
        
        if check_name in ["governance_section", "requirements_section", "user_stories",
                          "success_criteria", "tech_stack_section", "architecture_section",
                          "risks_section", "file_structure"]:
            # Check for section headers
            spec_file = self.spec_dir / "spec.md"
            plan_file = self.spec_dir / "plan.md"
            
            section_map = {
                "governance_section": ("constitution.md", "Governance"),
                "requirements_section": ("spec.md", "Requirements"),
                "user_stories": ("spec.md", "User Stories"),
                "success_criteria": ("spec.md", "Success Criteria"),
                "tech_stack_section": ("plan.md", "Tech Stack"),
                "architecture_section": ("plan.md", "Architecture"),
                "risks_section": ("plan.md", "Risk"),
                "file_structure": ("plan.md", "File Structure")
            }
            
            if check_name in section_map:
                filename, section = section_map[check_name]
                if filename == "constitution.md":
                    file_path = self.spec_dir.parent.parent / "memory" / filename
                else:
                    file_path = self.spec_dir / filename
                
                if file_path.exists():
                    content = file_path.read_text()
                    return section in content
            
            return False
        
        if check_name == "no_how_in_spec":
            spec_file = self.spec_dir / "spec.md"
            if spec_file.exists():
                content = spec_file.read_text().lower()
                technical_terms = ["implementation", "code", "function", "class", "method"]
                return not any(term in content for term in technical_terms)
            return True
        
        if check_name in ["task_list", "effort_estimates", "dependencies", "acceptance_criteria"]:
            tasks_file = self.spec_dir / "tasks.md"
            if tasks_file.exists():
                content = tasks_file.read_text()
                checks = {
                    "task_list": "- [ ]",
                    "effort_estimates": "Effort",
                    "dependencies": "Dependencies",
                    "acceptance_criteria": "Acceptance Criteria"
                }
                return checks[check_name] in content
            return False
        
        # Default: pass
        return True
