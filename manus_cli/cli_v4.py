"""
Manus CLI v4.0 - Complete Spec-Kit Integration
Professional CLI with GitHub Spec-Kit methodology
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt, Confirm

# Import from existing modules
from .api_enhanced import ManusClient
from .roles import ROLES, get_system_prompt
from .speckit import (
    SpecKitEngine,
    should_use_spec_driven,
    assess_complexity,
    ConstitutionPhase,
    SpecificationPhase,
    PlanningPhase,
)
from .updater import check_for_updates

app = typer.Typer(help="Manus CLI v5.3 - Spec-Driven Development")
console = Console()

# Version
from . import __version__

def version_callback(value: bool):
    """Callback for --version flag."""
    if value:
        console.print(f"[bold green]Manus CLI v{__version__}[/bold green]")
        raise typer.Exit()

@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version", "-v",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit"
        )
    ] = None,
):
    """Manus CLI - Professional AI Agent Command-Line Interface with Spec-Driven Development."""
    # Check for updates (non-blocking, once per day)
    try:
        check_for_updates(silent=False)
    except Exception:
        # Silently ignore update check failures
        pass

# Configuration
CONFIG_DIR = Path.home() / ".config" / "manus"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.json"
TEMPLATES_DIR = Path(__file__).parent / "templates"


def load_config() -> dict:
    """Load configuration from file."""
    if not CONFIG_FILE.exists():
        return {}
    
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def save_config(config: dict):
    """Save configuration to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


def get_api_client() -> Optional[ManusClient]:
    """Get configured API client with CLI session ID."""
    from .session import get_cli_session_id
    
    config = load_config()
    api_key = config.get("api_key")
    
    if not api_key:
        console.print("[red]Error:[/red] API key not configured. Run [cyan]manus configure[/cyan] first.")
        return None
    
    # Get or create CLI session ID (separate from Web)
    session_id = get_cli_session_id()
    
    return ManusClient(api_key=api_key, session_id=session_id)


@app.command()
def configure(
    api_key: str = typer.Option(None, "--api-key", help="Manus API key"),
    mode: str = typer.Option(None, "--mode", help="Default mode (speed/balanced/quality)"),
    role: str = typer.Option(None, "--role", help="Default role"),
    streaming: bool = typer.Option(None, "--streaming/--no-streaming", help="Enable streaming"),
    show: bool = typer.Option(False, "--show", help="Show current configuration"),
):
    """
    Configure Manus CLI settings.
    
    Examples:
        manus configure --api-key YOUR_KEY
        manus configure --mode quality --role developer
        manus configure --show
    """
    config = load_config()
    
    # If --show flag, just display config and exit
    if show:
        if not config:
            console.print("[yellow]No configuration found. Run 'manus configure --api-key YOUR_KEY' to get started.[/yellow]")
            return
        
        table = Table(title="Current Configuration")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("API Key", "***" + config.get("api_key", "")[-8:] if config.get("api_key") else "Not set")
        table.add_row("Default Mode", config.get("default_mode", "quality"))
        table.add_row("Default Role", config.get("default_role", "assistant"))
        table.add_row("Streaming", str(config.get("streaming", True)))
        table.add_row("Spec-Driven", str(config.get("spec_driven", {}).get("enabled", True)))
        
        console.print(table)
        return
    
    # If no options provided, show help
    if not any([api_key, mode, role, streaming is not None]):
        console.print("[yellow]No options provided. Use --help to see available options or --show to view current config.[/yellow]")
        return
    
    # Update config
    if api_key:
        config["api_key"] = api_key
        console.print("[green]✓[/green] API key configured")
    
    if mode:
        if mode not in ["speed", "balanced", "quality"]:
            console.print("[red]Error:[/red] Mode must be one of: speed, balanced, quality")
            raise typer.Exit(1)
        config["default_mode"] = mode
        console.print(f"[green]✓[/green] Default mode set to {mode}")
    
    if role:
        if role not in ROLES:
            console.print(f"[red]Error:[/red] Invalid role. Run 'manus roles' to see available roles.")
            raise typer.Exit(1)
        config["default_role"] = role
        console.print(f"[green]✓[/green] Default role set to {role}")
    
    if streaming is not None:
        config["streaming"] = streaming
        console.print(f"[green]✓[/green] Streaming {'enabled' if streaming else 'disabled'}")
    
    # Spec-Driven defaults
    if "spec_driven" not in config:
        config["spec_driven"] = {
            "enabled": True,
            "auto_detect": True,
            "complexity_threshold": "moderate",
            "skip_clarification_for_simple": True,
            "max_clarifications": 3,
            "validation_iterations": 3,
        }
    
    save_config(config)
    console.print("[green]✓[/green] Configuration saved")
    
    # Show updated config
    console.print()
    table = Table(title="Updated Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("API Key", "***" + config.get("api_key", "")[-8:] if config.get("api_key") else "Not set")
    table.add_row("Default Mode", config.get("default_mode", "quality"))
    table.add_row("Default Role", config.get("default_role", "assistant"))
    table.add_row("Streaming", str(config.get("streaming", True)))
    table.add_row("Spec-Driven", str(config.get("spec_driven", {}).get("enabled", True)))
    
    console.print(table)


@app.command()
def roles():
    """
    List all available roles.
    """
    table = Table(title="Available Roles")
    table.add_column("Role", style="cyan")
    table.add_column("Description", style="white")
    
    for role_key, role_info in ROLES.items():
        table.add_row(role_key, role_info["name"])
    
    console.print(table)


@app.command()
def chat(
    message: str = typer.Argument(None, help="Message to send (optional in interactive mode)"),
    role: str = typer.Option(None, "--role", "-r", help="Role to use"),
    mode: str = typer.Option(None, "--mode", "-m", help="Mode (speed/balanced/quality)"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Start interactive mode"),
    no_spec_driven: bool = typer.Option(False, "--no-spec-driven", help="Disable spec-driven mode"),
):
    """
    Send a message to Manus AI.
    
    Examples:
        manus chat "Hello, how are you?"
        manus chat "Create a todo app" --role developer
        manus chat "Build a REST API" --mode quality
        manus chat -i  # Interactive mode
    """
    # Get API client
    client = get_api_client()
    if not client:
        raise typer.Exit(1)
    
    # Load config
    config = load_config()
    
    # Determine role and mode
    role = role or config.get("default_role", "assistant")
    mode = mode or config.get("default_mode", "quality")
    
    # Handle interactive mode
    if interactive or message is None:
        run_interactive_chat(client, role, mode, config, no_spec_driven)
        return
    
    # Validate message for non-interactive mode
    if not message:
        console.print("[red]Error:[/red] MESSAGE is required (or use -i for interactive mode)")
        raise typer.Exit(1)
    
    # Check if spec-driven mode should be used
    spec_driven_config = config.get("spec_driven", {})
    use_spec_driven = (
        spec_driven_config.get("enabled", True) and
        spec_driven_config.get("auto_detect", True) and
        not no_spec_driven
    )
    
    if use_spec_driven:
        should_use, complexity = should_use_spec_driven(message)
        
        if should_use:
            # Run spec-driven workflow
            run_spec_driven_workflow(message, role, mode, complexity, client)
            return
    
    # Regular chat mode
    system_prompt = get_system_prompt(role)
    
    try:
        if config.get("streaming", True):
            console.print(f"[bold cyan]{role.title()}:[/bold cyan]", end=" ")
            for chunk in client.stream_task(message, system_prompt=system_prompt, mode=mode):
                console.print(chunk, end="")
            console.print()  # New line after streaming
        else:
            response_text = client.chat(message, system_prompt=system_prompt, mode=mode)
            console.print(f"[bold cyan]{role.title()}:[/bold cyan] {response_text}")
    
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


def run_interactive_chat(
    client: ManusClient,
    role: str,
    mode: str,
    config: dict,
    no_spec_driven: bool
):
    """
    Run interactive chat session.
    
    Args:
        client: API client
        role: User's role
        mode: Execution mode
        config: Configuration dict
        no_spec_driven: Whether to disable spec-driven mode
    """
    from .splash import show_interactive_splash
    
    # Show splash screen
    show_interactive_splash()
    
    # Get system prompt
    system_prompt = get_system_prompt(role)
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_input = Prompt.ask("[bold green]You[/bold green]")
            
            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "q", "bye"]:
                console.print("\n[cyan]👋 Goodbye![/cyan]\n")
                break
            
            # Skip empty input
            if not user_input.strip():
                continue
            
            # Check if spec-driven mode should be used
            spec_driven_config = config.get("spec_driven", {})
            use_spec_driven = (
                spec_driven_config.get("enabled", True) and
                spec_driven_config.get("auto_detect", True) and
                not no_spec_driven
            )
            
            if use_spec_driven:
                should_use, complexity = should_use_spec_driven(user_input)
                
                if should_use:
                    # Run spec-driven workflow
                    run_spec_driven_workflow(user_input, role, mode, complexity, client)
                    continue
            
            # Regular chat
            console.print()
            if config.get("streaming", True):
                console.print(f"[bold cyan]{role.title()}:[/bold cyan] ", end="")
                for chunk in client.stream_task(user_input, system_prompt=system_prompt, mode=mode):
                    console.print(chunk, end="")
                console.print("\n")  # New line after streaming
            else:
                response_text = client.chat(user_input, system_prompt=system_prompt, mode=mode)
                console.print(f"[bold cyan]{role.title()}:[/bold cyan] {response_text}\n")
        
        except KeyboardInterrupt:
            console.print("\n\n[cyan]👋 Goodbye![/cyan]\n")
            break
        except Exception as e:
            console.print(f"\n[red]Error:[/red] {e}\n")
            continue


def run_spec_driven_workflow(
    message: str,
    role: str,
    mode: str,
    complexity: str,
    client: ManusClient
):
    """
    Run the complete spec-driven workflow.
    
    Args:
        message: User's message/request
        role: User's role
        mode: Execution mode
        complexity: Complexity level (simple/moderate/complex)
        client: API client
    """
    # Initialize Spec-Kit engine
    engine = SpecKitEngine()
    
    # Show splash screen
    engine.show_splash_screen(mode, role, complexity)
    
    # Extract project info from message
    project_name = Prompt.ask("[cyan]Project name[/cyan]", default="my-project")
    
    # Phase 1: Constitution
    engine.show_phase_header(1, "Constitution", total_phases=3)
    
    constitution_phase = ConstitutionPhase(
        memory_dir=engine.memory_dir,
        templates_dir=TEMPLATES_DIR
    )
    
    success, constitution_path = constitution_phase.execute(
        project_name=project_name,
        project_description=message
    )
    
    if not success:
        console.print("[red]✗[/red] Constitution phase failed")
        raise typer.Exit(1)
    
    # Validate constitution
    is_valid, errors = constitution_phase.validate(constitution_path)
    if not is_valid:
        console.print("[yellow]⚠[/yellow] Constitution validation warnings:")
        for error in errors:
            console.print(f"  • {error}")
    
    # Phase 2: Specification
    engine.show_phase_header(2, "Specification", total_phases=3)
    
    # Generate branch name and feature number
    feature_number = engine.get_next_feature_number()
    short_name = engine.generate_branch_name(message)
    
    specification_phase = SpecificationPhase(
        specs_dir=engine.specs_dir,
        templates_dir=TEMPLATES_DIR
    )
    
    success, feature_dir, metadata = specification_phase.execute(
        feature_number=feature_number,
        short_name=short_name,
        description=message,
        role=role
    )
    
    if not success:
        console.print("[red]✗[/red] Specification phase failed")
        raise typer.Exit(1)
    
    # Save metadata
    engine.save_metadata(feature_dir, metadata)
    
    # Validate specification
    spec_file = feature_dir / "spec.md"
    is_valid, errors = specification_phase.validate(spec_file)
    if not is_valid:
        console.print("[yellow]⚠[/yellow] Specification validation warnings:")
        for error in errors:
            console.print(f"  • {error}")
    
    # Phase 3: Planning
    engine.show_phase_header(3, "Planning", total_phases=3)
    
    planning_phase = PlanningPhase(templates_dir=TEMPLATES_DIR)
    
    success, plan_file = planning_phase.execute(
        feature_dir=feature_dir,
        spec_file=spec_file,
        role=role,
        metadata=metadata
    )
    
    if not success:
        console.print("[red]✗[/red] Planning phase failed")
        raise typer.Exit(1)
    
    # Validate plan
    is_valid, errors = planning_phase.validate(plan_file, spec_file)
    if not is_valid:
        console.print("[yellow]⚠[/yellow] Plan validation warnings:")
        for error in errors:
            console.print(f"  • {error}")
    
    # Summary
    console.print()
    console.print("[bold green]✓ Spec-Driven Workflow Complete![/bold green]")
    console.print()
    
    summary_table = Table(title="Generated Artifacts")
    summary_table.add_column("Artifact", style="cyan")
    summary_table.add_column("Location", style="white")
    
    summary_table.add_row("Constitution", str(constitution_path))
    summary_table.add_row("Specification", str(spec_file))
    summary_table.add_row("Plan", str(plan_file))
    
    console.print(summary_table)
    console.print()
    console.print("[dim]Next steps:[/dim]")
    console.print("  1. Review the generated artifacts")
    console.print("  2. Make any necessary adjustments")
    console.print("  3. Run [cyan]manus task[/cyan] to break down into tasks (coming in v4.1)")
    console.print("  4. Run [cyan]manus implement[/cyan] to start implementation (coming in v4.1)")


@app.command()
def task(
    message: str = typer.Argument(..., help="Task description"),
    mode: str = typer.Option(None, "--mode", "-m", help="Mode (speed/balanced/quality)"),
):
    """
    Create a task (uses spec-driven workflow if applicable).
    
    This is a simplified version for v4.0 MVP.
    Full task breakdown will be available in v4.1.
    """
    console.print("[yellow]Note:[/yellow] Full task breakdown coming in v4.1")
    console.print("[dim]For now, using regular chat mode...[/dim]")
    console.print()
    
    # Fallback to chat
    chat(message=message, mode=mode, interactive=False, no_spec_driven=True)


@app.command()
def history(
    limit: int = typer.Option(10, "--limit", "-n", help="Number of entries to show"),
    clear: bool = typer.Option(False, "--clear", help="Clear history"),
):
    """
    View or clear conversation history.
    """
    if clear:
        if HISTORY_FILE.exists():
            HISTORY_FILE.unlink()
            console.print("[green]✓[/green] History cleared")
        else:
            console.print("[yellow]No history to clear[/yellow]")
        return
    
    if not HISTORY_FILE.exists():
        console.print("[yellow]No history found[/yellow]")
        return
    
    with open(HISTORY_FILE, "r") as f:
        history_data = json.load(f)
    
    entries = history_data.get("entries", [])[-limit:]
    
    if not entries:
        console.print("[yellow]No history entries[/yellow]")
        return
    
    console.print(f"[bold]Last {len(entries)} entries:[/bold]")
    console.print()
    
    for entry in entries:
        timestamp = entry.get("timestamp", "unknown")
        role = entry.get("role", "unknown")
        message = entry.get("message", "")
        
        console.print(f"[dim]{timestamp}[/dim] [cyan]{role}:[/cyan] {message[:100]}...")


@app.command()
def session(
    clear: bool = typer.Option(False, "--clear", help="Clear current session"),
    new: bool = typer.Option(False, "--new", help="Create new session"),
):
    """
    Manage CLI session (separate from Web interface).
    
    Examples:
        manus session          # Show current session info
        manus session --new    # Start a new session
        manus session --clear  # Clear current session
    """
    from .session import session_manager
    
    if clear:
        session_manager.clear_session()
        console.print("[green]✓[/green] Session cleared")
        return
    
    if new:
        session_id = session_manager.create_new_session()
        console.print(f"[green]✓[/green] New session created: [cyan]{session_id}[/cyan]")
        return
    
    # Show session info
    info = session_manager.get_session_info()
    if not info:
        console.print("[yellow]No active session[/yellow]")
        return
    
    table = Table(title="CLI Session Info")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="white")
    
    table.add_row("Session ID", info.get("session_id", "N/A"))
    table.add_row("Created At", info.get("created_at", "N/A"))
    table.add_row("Source", info.get("source", "N/A"))
    
    console.print(table)
    console.print("\n[dim]Note: CLI sessions are separate from Web interface sessions[/dim]")


@app.command()
def version():
    """
    Show version information.
    """
    from . import __version__
    
    table = Table(title="Manus CLI")
    table.add_column("Component", style="cyan")
    table.add_column("Version", style="white")
    
    table.add_row("CLI", __version__)
    table.add_row("Spec-Kit", "1.0.0")
    table.add_row("Python", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    console.print(table)


@app.command()
def start(
    role: str = typer.Option(None, "--role", "-r", help="Role to use"),
    mode: str = typer.Option(None, "--mode", "-m", help="Mode (speed/balanced/quality)"),
):
    """
    Start Manus CLI with interactive splash screen.
    
    This command displays the beautiful 'AND AFTER YOU' splash screen
    and enters interactive mode, making it clear that you can start chatting.
    """
    # Get API client
    client = get_api_client()
    if not client:
        raise typer.Exit(1)
    
    # Load config
    config = load_config()
    
    # Determine role and mode
    role = role or config.get("default_role", "assistant")
    mode = mode or config.get("default_mode", "quality")
    
    # Run interactive chat with splash
    run_interactive_chat(client, role, mode, config, no_spec_driven=False)


@app.command()
def update():
    """
    Update Manus CLI to the latest version from GitHub.
    """
    from .updater import update_cli
    
    try:
        update_cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]Update cancelled by user.[/yellow]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Update failed: {e}[/red]")
        raise typer.Exit(1)


def main():
    """Main entry point."""
    app()


if __name__ == "__main__":
    main()
