"""
GitHub Integration
Sync specs to GitHub, create issues, and manage PRs
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

console = Console()


class GitHubIntegration:
    """GitHub integration for spec-driven development"""
    
    def __init__(self, spec_dir: Path):
        self.spec_dir = spec_dir
        self.metadata_file = spec_dir / "metadata.json"
        self.git_initialized = self._check_git()
    
    def _check_git(self) -> bool:
        """Check if git is initialized"""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                cwd=self.spec_dir,
                timeout=5
            )
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return False
    
    def sync_to_github(self, commit_message: Optional[str] = None) -> bool:
        """
        Sync all spec artifacts to GitHub
        
        Returns:
            Success status
        """
        console.print(Panel(
            "[bold cyan]Syncing to GitHub[/bold cyan]\n"
            "Committing and pushing spec artifacts...",
            border_style="cyan"
        ))
        
        if not self.git_initialized:
            console.print("[yellow]Git not initialized. Initialize? (y/n)[/yellow]")
            if Confirm.ask("Initialize git repository?"):
                self._init_git()
            else:
                console.print("[red]Sync cancelled.[/red]")
                return False
        
        # Add all spec files
        try:
            subprocess.run(
                ["git", "add", ".manus/"],
                cwd=self.spec_dir.parent.parent,
                check=True,
                timeout=10
            )
            
            # Commit
            if not commit_message:
                commit_message = f"Update specs: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            
            subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.spec_dir.parent.parent,
                check=True,
                timeout=10
            )
            
            # Push
            subprocess.run(
                ["git", "push"],
                cwd=self.spec_dir.parent.parent,
                check=True,
                timeout=30
            )
            
            console.print("✓ Successfully synced to GitHub")
            return True
            
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error syncing to GitHub: {e}[/red]")
            return False
        except subprocess.TimeoutExpired:
            console.print("[red]Timeout while syncing to GitHub[/red]")
            return False
    
    def create_issues_from_tasks(self, tasks_content: str) -> List[str]:
        """
        Create GitHub issues from task list
        
        Returns:
            List of created issue URLs
        """
        console.print(Panel(
            "[bold cyan]Creating GitHub Issues[/bold cyan]\n"
            "Converting tasks to issues...",
            border_style="cyan"
        ))
        
        # Extract tasks
        tasks = self._extract_tasks(tasks_content)
        
        if not tasks:
            console.print("[yellow]No tasks found to create issues.[/yellow]")
            return []
        
        console.print(f"Found {len(tasks)} tasks. Create issues? (y/n)")
        if not Confirm.ask("Create GitHub issues?"):
            return []
        
        # Create issues using gh CLI
        issue_urls = []
        
        for i, task in enumerate(tasks, 1):
            try:
                # Extract task details
                title = task.get("title", f"Task {i}")
                body = task.get("description", "")
                labels = task.get("labels", ["spec-driven", "task"])
                
                # Create issue
                result = subprocess.run(
                    [
                        "gh", "issue", "create",
                        "--title", title,
                        "--body", body,
                        "--label", ",".join(labels)
                    ],
                    capture_output=True,
                    text=True,
                    cwd=self.spec_dir.parent.parent,
                    timeout=15
                )
                
                if result.returncode == 0:
                    issue_url = result.stdout.strip()
                    issue_urls.append(issue_url)
                    console.print(f"✓ Created issue {i}/{len(tasks)}: {title}")
                else:
                    console.print(f"✗ Failed to create issue: {title}")
                    
            except (FileNotFoundError, subprocess.TimeoutExpired) as e:
                console.print(f"[red]Error creating issue: {e}[/red]")
                break
        
        console.print(f"\n✓ Created {len(issue_urls)} issues")
        return issue_urls
    
    def create_feature_branch(self, feature_name: str) -> bool:
        """
        Create a feature branch for implementation
        
        Returns:
            Success status
        """
        console.print(Panel(
            f"[bold cyan]Creating Feature Branch[/bold cyan]\n"
            f"Branch: {feature_name}",
            border_style="cyan"
        ))
        
        try:
            # Create and checkout branch
            subprocess.run(
                ["git", "checkout", "-b", feature_name],
                cwd=self.spec_dir.parent.parent,
                check=True,
                timeout=10
            )
            
            console.print(f"✓ Created and switched to branch: {feature_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error creating branch: {e}[/red]")
            return False
    
    def create_pull_request(self, title: str, description: str) -> Optional[str]:
        """
        Create a pull request
        
        Returns:
            PR URL if successful
        """
        console.print(Panel(
            "[bold cyan]Creating Pull Request[/bold cyan]\n"
            f"Title: {title}",
            border_style="cyan"
        ))
        
        try:
            result = subprocess.run(
                [
                    "gh", "pr", "create",
                    "--title", title,
                    "--body", description,
                    "--label", "spec-driven"
                ],
                capture_output=True,
                text=True,
                cwd=self.spec_dir.parent.parent,
                timeout=15
            )
            
            if result.returncode == 0:
                pr_url = result.stdout.strip()
                console.print(f"✓ Created PR: {pr_url}")
                return pr_url
            else:
                console.print(f"[red]Failed to create PR: {result.stderr}[/red]")
                return None
                
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            console.print(f"[red]Error creating PR: {e}[/red]")
            return None
    
    def _init_git(self):
        """Initialize git repository"""
        try:
            subprocess.run(
                ["git", "init"],
                cwd=self.spec_dir.parent.parent,
                check=True,
                timeout=10
            )
            console.print("✓ Git repository initialized")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error initializing git: {e}[/red]")
    
    def _extract_tasks(self, tasks_content: str) -> List[Dict[str, any]]:
        """Extract tasks from tasks content"""
        tasks = []
        current_task = None
        
        lines = tasks_content.split("\n")
        for line in lines:
            if line.strip().startswith("- [ ]"):
                # Save previous task
                if current_task:
                    tasks.append(current_task)
                
                # Start new task
                task_text = line.strip().replace("- [ ]", "").strip()
                if "**" in task_text:
                    # Extract title from bold text
                    start = task_text.index("**") + 2
                    end = task_text.index("**", start)
                    title = task_text[start:end]
                    description = task_text[end+2:].strip().lstrip(":").strip()
                else:
                    title = task_text
                    description = ""
                
                current_task = {
                    "title": title,
                    "description": description,
                    "labels": ["spec-driven", "task"]
                }
            
            elif current_task and line.strip().startswith("- **"):
                # Add details to current task
                if "Effort" in line:
                    current_task["labels"].append("effort-" + line.split(":")[-1].strip().lower())
                elif "Dependencies" in line:
                    deps = line.split(":")[-1].strip()
                    if deps and deps != "[Previous tasks]":
                        current_task["description"] += f"\n\nDependencies: {deps}"
                elif "Acceptance Criteria" in line:
                    criteria = line.split(":")[-1].strip()
                    if criteria and criteria != "[Specific criteria]":
                        current_task["description"] += f"\n\nAcceptance Criteria: {criteria}"
        
        # Save last task
        if current_task:
            tasks.append(current_task)
        
        return tasks
