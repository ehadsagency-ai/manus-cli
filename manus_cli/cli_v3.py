"""
Manus CLI v3.0 with Spec-Driven Development integration
"""

import sys
import uuid
import typer
from typing import Optional
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.table import Table
from rich import print as rprint

from .api_enhanced import ManusClient, ManusAPIError, RateLimitError
from .roles import get_role, list_roles, get_system_prompt
from .spec_driven import SpecDrivenProcess, create_enhanced_prompt
from . import __version__

app = typer.Typer(
    name="manus",
    help="Manus AI - CLI with Spec-Driven Development for rigorous thinking and project creation",
    add_completion=True,
)

console = Console()


def version_callback(value: bool):
    """Display version information"""
    if value:
        console.print(f"[bold blue]Manus CLI[/bold blue] version [green]{__version__}[/green]")
        console.print(f"[dim]With Spec-Driven Development support[/dim]")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit"
    )
):
    """
    Manus CLI v3.0 - Interact with Manus AI with structured thinking
    """
    pass


@app.command()
def configure(
    api_key: Optional[str] = typer.Option(
        None,
        "--api-key",
        "-k",
        help="Your Manus API key"
    ),
    default_mode: Optional[str] = typer.Option(
        None,
        "--mode",
        "-m",
        help="Default execution mode (speed, quality)"
    ),
    default_role: Optional[str] = typer.Option(
        None,
        "--role",
        "-r",
        help="Default role/persona"
    ),
    stream: Optional[bool] = typer.Option(
        None,
        "--stream/--no-stream",
        help="Enable/disable streaming by default"
    ),
    spec_driven: Optional[bool] = typer.Option(
        None,
        "--spec-driven/--no-spec-driven",
        help="Enable/disable spec-driven mode by default"
    )
):
    """
    Configure Manus CLI settings including Spec-Driven Development
    
    Example:
        manus configure --api-key sk-your-api-key --role developer --spec-driven
    """
    config = ManusClient.load_config()
    
    if not api_key and not config.get("api_key"):
        console.print("[bold yellow]Configure Manus CLI[/bold yellow]\n")
        api_key = Prompt.ask(
            "[cyan]Enter your Manus API key[/cyan]",
            password=True
        )
    
    if api_key:
        config["api_key"] = api_key.strip()
    
    if default_mode:
        config["default_mode"] = default_mode
    
    if default_role:
        config["default_role"] = default_role
    
    if stream is not None:
        config["stream"] = stream
    
    if spec_driven is not None:
        config["spec_driven"] = spec_driven
    
    if config:
        ManusClient.save_config(config)
        console.print("\n[green]✓[/green] Configuration saved successfully!")
        console.print(f"[dim]Configuration stored in: {ManusClient.CONFIG_FILE}[/dim]")
        
        # Show current config
        console.print("\n[bold]Current Configuration:[/bold]")
        for key, value in config.items():
            if key == "api_key":
                console.print(f"  {key}: {'*' * 20}")
            else:
                console.print(f"  {key}: {value}")
    else:
        console.print("[red]No configuration changes made[/red]")


@app.command()
def roles():
    """
    List available roles/personas
    
    Example:
        manus roles
    """
    console.print("[bold cyan]Available Roles[/bold cyan]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Key", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Description", style="white")
    
    for role in list_roles():
        table.add_row(
            role["key"],
            role["name"],
            role["description"]
        )
    
    console.print(table)
    console.print("\n[dim]Use '/role <key>' in interactive mode or '--role <key>' in commands[/dim]")


@app.command()
def chat(
    message: Optional[str] = typer.Argument(
        None,
        help="Message to send to Manus AI"
    ),
    mode: Optional[str] = typer.Option(
        None,
        "--mode",
        "-m",
        help="Execution mode (speed, quality, etc.)"
    ),
    role: Optional[str] = typer.Option(
        None,
        "--role",
        "-r",
        help="Role/persona to use"
    ),
    stream: Optional[bool] = typer.Option(
        None,
        "--stream/--no-stream",
        help="Enable/disable streaming"
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Start interactive chat session"
    ),
    spec_driven: Optional[bool] = typer.Option(
        None,
        "--spec-driven/--no-spec-driven",
        help="Force enable/disable spec-driven mode"
    ),
    working_dir: Optional[str] = typer.Option(
        None,
        "--dir",
        "-d",
        help="Working directory for spec files"
    )
):
    """
    Send a message to Manus AI with optional Spec-Driven Development
    
    Examples:
        manus chat "Hello, how are you?"
        manus chat "Create a todo app" --spec-driven
        manus chat "Build a REST API" --role developer
        manus chat --interactive
    """
    try:
        client = ManusClient()
    except ManusAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("\n[yellow]Tip:[/yellow] Run 'manus configure' to set up your API key")
        raise typer.Exit(1)
    
    # Load config for defaults
    config = ManusClient.load_config()
    
    # Use config defaults if not specified
    if mode is None:
        mode = config.get("default_mode", "speed")
    
    if role is None:
        role = config.get("default_role", "assistant")
    
    if stream is None:
        stream = config.get("stream", False)
    
    # Determine working directory
    work_dir = Path(working_dir) if working_dir else Path.cwd()
    
    if interactive or not message:
        _interactive_chat_v3(client, mode, role, stream, work_dir, config)
    else:
        _single_message_v3(client, message, mode, role, stream, spec_driven, work_dir, config)


def _single_message_v3(
    client: ManusClient, 
    message: str, 
    mode: str, 
    role: str, 
    stream: bool,
    spec_driven: Optional[bool],
    working_dir: Path,
    config: dict
):
    """Send a single message with optional spec-driven process"""
    
    # Determine if spec-driven should be used
    use_spec_driven = False
    
    if spec_driven is True:
        # Explicitly requested
        use_spec_driven = True
    elif spec_driven is False:
        # Explicitly disabled
        use_spec_driven = False
    else:
        # Auto-detect based on keywords and config
        if SpecDrivenProcess.should_trigger(message):
            # Check if complex enough
            if SpecDrivenProcess.is_complex_task(message):
                use_spec_driven = True
            else:
                # Ask user for simple tasks
                use_spec_driven = Confirm.ask(
                    "\n[yellow]This looks like a creation task. Use Spec-Driven Development for structured thinking?[/yellow]"
                )
    
    # If spec-driven, run the process
    if use_spec_driven:
        spec_process = SpecDrivenProcess(working_dir)
        
        try:
            # Run full spec-driven process
            spec_context_dict = spec_process.run_full_process(message, role, mode)
            
            # Get formatted context
            spec_context = spec_process.get_context_for_api()
            
            # Create enhanced prompt
            enhanced_prompt = create_enhanced_prompt(message, spec_context, role)
            
            console.print("[bold green]Sending enhanced request to Manus AI...[/bold green]\n")
            
            # Send to API with enhanced context
            system_prompt = get_system_prompt(role)
            
            if stream:
                console.print("[bold magenta]Manus:[/bold magenta] ", end="")
                
                for chunk in client.stream_task(enhanced_prompt, mode=mode, system_prompt=system_prompt):
                    console.print(chunk, end="")
                
                console.print()
            else:
                with console.status("[bold green]Manus is thinking with structured approach...", spinner="dots"):
                    response = client.create_task(enhanced_prompt, mode=mode, system_prompt=system_prompt)
                
                console.print("[bold magenta]Manus:[/bold magenta]")
                
                task_id = response.get('task_id', 'N/A')
                status = response.get('status', 'N/A')
                
                console.print(Panel(
                    f"[dim]Task ID: {task_id}\nStatus: {status}\nSpec Dir: {spec_process.manus_dir}[/dim]",
                    border_style="blue"
                ))
                
                console.print("\n[bold]Response:[/bold]")
                console.print_json(data=response)
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Spec-driven process interrupted[/yellow]")
            raise typer.Exit(0)
    
    else:
        # Standard message without spec-driven
        console.print(f"\n[bold cyan]You:[/bold cyan] {message}\n")
        
        system_prompt = get_system_prompt(role)
        
        try:
            if stream:
                console.print("[bold magenta]Manus:[/bold magenta] ", end="")
                
                for chunk in client.stream_task(message, mode=mode, system_prompt=system_prompt):
                    console.print(chunk, end="")
                
                console.print()
            else:
                with console.status("[bold green]Manus is thinking...", spinner="dots"):
                    response = client.create_task(message, mode=mode, system_prompt=system_prompt)
                
                console.print("[bold magenta]Manus:[/bold magenta]")
                
                task_id = response.get('task_id', 'N/A')
                status = response.get('status', 'N/A')
                
                console.print(Panel(
                    f"[dim]Task ID: {task_id}\nStatus: {status}[/dim]",
                    border_style="blue"
                ))
                
                console.print("\n[bold]Response:[/bold]")
                console.print_json(data=response)
                
        except RateLimitError as e:
            console.print(f"\n[red]Rate Limit Error:[/red] {e}")
            console.print("[yellow]Please wait a moment before trying again.[/yellow]")
            raise typer.Exit(1)
        except ManusAPIError as e:
            console.print(f"\n[red]Error:[/red] {e}")
            raise typer.Exit(1)


def _interactive_chat_v3(
    client: ManusClient,
    mode: str,
    role: str,
    stream: bool,
    working_dir: Path,
    config: dict
):
    """Interactive chat with spec-driven support"""
    conversation_id = str(uuid.uuid4())
    messages = []
    current_mode = mode
    current_role = role
    current_stream = stream
    
    role_info = get_role(current_role)
    
    console.print(Panel(
        f"[bold cyan]Manus AI - Interactive Chat v3.0[/bold cyan]\n\n"
        f"[bold]Current Role:[/bold] {role_info['name']}\n"
        f"[bold]Mode:[/bold] {current_mode}\n"
        f"[bold]Streaming:[/bold] {'Enabled' if current_stream else 'Disabled'}\n"
        f"[bold]Working Dir:[/bold] {working_dir}\n\n"
        f"[bold magenta]✨ Spec-Driven Development:[/bold magenta] Enabled\n"
        f"[dim]Use keywords like 'create', 'build', 'develop' to trigger structured thinking[/dim]\n\n"
        "[bold]Commands:[/bold]\n"
        "  /quit or /exit - Exit the chat\n"
        "  /spec - Force spec-driven mode for next message\n"
        "  /role <role> - Change role/persona\n"
        "  /stream - Toggle streaming\n"
        "  /help - Show all commands\n",
        border_style="blue"
    ))
    
    force_spec_next = False
    
    while True:
        try:
            message = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            if not message.strip():
                continue
            
            # Handle commands
            if message.startswith('/'):
                command = message.lower().strip()
                
                if command in ['/quit', '/exit']:
                    if messages:
                        save = Confirm.ask("Save conversation before exiting?")
                        if save:
                            client.save_conversation(conversation_id, messages)
                            console.print(f"[green]Conversation saved: {conversation_id}[/green]")
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                elif command == '/spec':
                    force_spec_next = True
                    console.print("[green]Spec-driven mode will be used for your next message[/green]")
                    continue
                
                elif command.startswith('/role '):
                    new_role = command.split(' ', 1)[1].strip()
                    role_info = get_role(new_role)
                    current_role = new_role
                    console.print(f"[green]Role changed to: {role_info['name']}[/green]")
                    continue
                
                elif command == '/stream':
                    current_stream = not current_stream
                    console.print(f"[green]Streaming {'enabled' if current_stream else 'disabled'}[/green]")
                    continue
                
                elif command == '/help':
                    console.print(Panel(
                        "[bold]Available Commands:[/bold]\n"
                        "  /quit, /exit - Exit the chat\n"
                        "  /spec - Force spec-driven mode for next message\n"
                        "  /role <role> - Change role/persona\n"
                        "  /stream - Toggle streaming\n"
                        "  /save - Save conversation\n"
                        "  /history - Show conversation history\n"
                        "  /help - Show this help\n",
                        border_style="blue"
                    ))
                    continue
                
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    continue
            
            # Check if spec-driven should be used
            use_spec = force_spec_next or (
                SpecDrivenProcess.should_trigger(message) and 
                SpecDrivenProcess.is_complex_task(message)
            )
            
            force_spec_next = False  # Reset flag
            
            # Process message
            if use_spec:
                _single_message_v3(
                    client, message, current_mode, current_role, 
                    current_stream, True, working_dir, config
                )
            else:
                # Standard chat
                messages.append({"role": "user", "content": message})
                
                system_prompt = get_system_prompt(current_role)
                
                try:
                    if current_stream:
                        console.print("\n[bold magenta]Manus:[/bold magenta] ", end="")
                        
                        response_text = ""
                        for chunk in client.stream_task(message, mode=current_mode, system_prompt=system_prompt):
                            console.print(chunk, end="")
                            response_text += chunk
                        
                        console.print()
                        messages.append({"role": "assistant", "content": response_text})
                    else:
                        with console.status("[bold green]Manus is thinking...", spinner="dots"):
                            response = client.create_task(message, mode=current_mode, system_prompt=system_prompt)
                        
                        console.print("\n[bold magenta]Manus:[/bold magenta]")
                        console.print_json(data=response)
                        
                        messages.append({"role": "assistant", "content": str(response)})
                        
                except RateLimitError as e:
                    console.print(f"\n[red]Rate Limit Error:[/red] {e}")
                except ManusAPIError as e:
                    console.print(f"\n[red]Error:[/red] {e}")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Chat interrupted. Type /quit to exit or continue chatting.[/yellow]")
            continue
        except EOFError:
            console.print("\n[yellow]Goodbye![/yellow]")
            break


# Keep other commands from v2
@app.command()
def task(
    prompt: str = typer.Argument(..., help="Task prompt to send"),
    mode: Optional[str] = typer.Option(
        None,
        "--mode",
        "-m",
        help="Execution mode"
    ),
    role: Optional[str] = typer.Option(
        None,
        "--role",
        "-r",
        help="Role/persona to use"
    ),
    spec_driven: bool = typer.Option(
        False,
        "--spec-driven",
        help="Use spec-driven development"
    )
):
    """
    Create a new task with optional spec-driven process
    
    Example:
        manus task "Build a web scraper" --spec-driven --role developer
    """
    # Redirect to chat command
    chat(message=prompt, mode=mode, role=role, spec_driven=spec_driven)


@app.command()
def status(
    task_id: str = typer.Argument(..., help="Task ID to check")
):
    """Check the status of a task"""
    try:
        client = ManusClient()
        
        with console.status("[bold green]Fetching task status...", spinner="dots"):
            response = client.get_task_status(task_id)
        
        console.print(f"\n[bold]Task Status:[/bold]")
        console.print_json(data=response)
        
    except ManusAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def history():
    """List saved conversation history"""
    try:
        client = ManusClient()
        conversations = client.list_conversations()
        
        if not conversations:
            console.print("[yellow]No saved conversations found[/yellow]")
            return
        
        console.print("[bold cyan]Saved Conversations[/bold cyan]\n")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan")
        table.add_column("Date", style="green")
        table.add_column("Messages", style="white")
        
        for conv in conversations:
            timestamp = datetime.fromtimestamp(conv["timestamp"])
            table.add_row(
                conv["id"][:16] + "...",
                timestamp.strftime("%Y-%m-%d %H:%M"),
                str(conv["message_count"])
            )
        
        console.print(table)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


def run():
    """Entry point for the CLI"""
    app()


if __name__ == "__main__":
    run()
