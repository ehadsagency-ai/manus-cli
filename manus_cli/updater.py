"""
Auto-update checker for Manus CLI.

Checks GitHub for new versions and provides update functionality.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, Tuple
from datetime import datetime, timedelta

import requests
from rich.console import Console
from rich.panel import Panel

from . import __version__

console = Console()

# GitHub repository info
GITHUB_REPO = "ehadsagency-ai/manus-cli"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"
CHECK_INTERVAL_HOURS = 24  # Check once per day

# Cache file location
CACHE_DIR = Path.home() / ".config" / "manus"
UPDATE_CACHE_FILE = CACHE_DIR / "update_check.json"


def get_latest_version() -> Optional[str]:
    """
    Fetch the latest version from GitHub releases.
    
    Returns:
        Latest version string (e.g., "5.4.0") or None if fetch fails
    """
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Get tag name and remove 'v' prefix if present
        tag_name = data.get("tag_name", "")
        if tag_name.startswith("v"):
            tag_name = tag_name[1:]
        
        return tag_name
    except Exception:
        # Silently fail - don't interrupt user workflow
        return None


def parse_version(version: str) -> Tuple[int, int, int]:
    """
    Parse version string into tuple of integers.
    
    Args:
        version: Version string like "5.3.0"
    
    Returns:
        Tuple of (major, minor, patch)
    """
    try:
        parts = version.split(".")
        return (int(parts[0]), int(parts[1]), int(parts[2]))
    except (ValueError, IndexError):
        return (0, 0, 0)


def is_newer_version(latest: str, current: str) -> bool:
    """
    Check if latest version is newer than current version.
    
    Args:
        latest: Latest version string
        current: Current version string
    
    Returns:
        True if latest is newer than current
    """
    latest_tuple = parse_version(latest)
    current_tuple = parse_version(current)
    return latest_tuple > current_tuple


def should_check_update() -> bool:
    """
    Check if enough time has passed since last update check.
    
    Returns:
        True if should check for updates
    """
    if not UPDATE_CACHE_FILE.exists():
        return True
    
    try:
        with open(UPDATE_CACHE_FILE, "r") as f:
            cache = json.load(f)
        
        last_check = datetime.fromisoformat(cache.get("last_check", ""))
        now = datetime.now()
        
        # Check if more than CHECK_INTERVAL_HOURS have passed
        return (now - last_check) > timedelta(hours=CHECK_INTERVAL_HOURS)
    except Exception:
        return True


def save_check_timestamp():
    """Save the current timestamp as last update check time."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    cache = {
        "last_check": datetime.now().isoformat(),
        "current_version": __version__
    }
    
    with open(UPDATE_CACHE_FILE, "w") as f:
        json.dump(cache, f)


def check_for_updates(silent: bool = False) -> Optional[str]:
    """
    Check if a new version is available.
    
    Args:
        silent: If True, don't show any output
    
    Returns:
        Latest version if update available, None otherwise
    """
    if not should_check_update():
        return None
    
    latest_version = get_latest_version()
    save_check_timestamp()
    
    if not latest_version:
        return None
    
    if is_newer_version(latest_version, __version__):
        if not silent:
            show_update_notification(latest_version)
        return latest_version
    
    return None


def show_update_notification(latest_version: str):
    """
    Display update notification to user.
    
    Args:
        latest_version: The latest available version
    """
    message = f"""
[yellow]⚠️  New version available![/yellow]

Current version: [red]{__version__}[/red]
Latest version:  [green]{latest_version}[/green]

Run [cyan]manus update[/cyan] to upgrade
Or: [dim]pip3 install --upgrade git+https://github.com/{GITHUB_REPO}.git[/dim]
    """.strip()
    
    console.print(Panel(message, border_style="yellow", padding=(1, 2)))
    console.print()


def update_cli():
    """
    Main update function called by the CLI command.
    
    Checks for updates and performs the update if available.
    """
    # First check if update is available
    console.print("[cyan]Checking for updates...[/cyan]\n")
    
    latest_version = get_latest_version()
    
    if not latest_version:
        console.print("[yellow]⚠️  Could not check for updates.[/yellow]")
        console.print("[dim]Please check your internet connection.[/dim]")
        return
    
    if not is_newer_version(latest_version, __version__):
        console.print(f"[green]✅ You already have the latest version ({__version__})[/green]")
        return
    
    # Show what will be updated
    console.print(f"[yellow]Update available:[/yellow]")
    console.print(f"  Current: [red]{__version__}[/red]")
    console.print(f"  Latest:  [green]{latest_version}[/green]\n")
    
    # Perform the update
    perform_update()


def perform_update() -> bool:
    """
    Perform the update using pip.
    
    Returns:
        True if update successful, False otherwise
    """
    console.print("[cyan]🔄 Updating Manus CLI...[/cyan]\n")
    
    try:
        # Use pip3 to upgrade from GitHub
        cmd = [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--upgrade",
            "--force-reinstall",
            f"git+https://github.com/{GITHUB_REPO}.git"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            console.print("[green]✅ Update successful![/green]")
            console.print("\n[dim]Please restart your terminal or run:[/dim]")
            console.print("[cyan]manus --version[/cyan]")
            return True
        else:
            console.print(f"[red]❌ Update failed:[/red]\n{result.stderr}")
            return False
            
    except Exception as e:
        console.print(f"[red]❌ Update failed: {str(e)}[/red]")
        return False
