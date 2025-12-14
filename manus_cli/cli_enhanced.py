"""
Enhanced CLI application with streaming, roles, and conversation history
"""

import sys
import uuid
import typer
from typing import Optional
from datetime import datetime
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.live import Live
from rich.table import Table
from rich import print as rprint

from .api_enhanced import ManusClient, ManusAPIError, RateLimitError
from .roles import get_role, list_roles, get_system_prompt
from . import __version__

app = typer.Typer(
    name="manus",
    help="Manus AI - Enhanced command-line interface for interacting with Manus AI",
    add_completion=True,
)

console = Console()


def version_callback(value: bool):
    """Display version information"""
    if value:
        console.print(f"[bold blue]Manus CLI[/bold blue] version [green]{__version__}[/green]")
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
    Manus CLI - Interact with Manus AI from your terminal
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
    )
):
    """
    Configure Manus CLI settings
    
    Example:
        manus configure --api-key sk-your-api-key --role developer --stream
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
    )
):
    """
    Send a message to Manus AI and get a response
    
    Examples:
        manus chat "Hello, how are you?"
        manus chat "Write a Python function" --role developer --stream
        manus chat --interactive  # Start interactive session
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
    
    if interactive or not message:
        _interactive_chat(client, mode, role, stream)
    else:
        _single_message(client, message, mode, role, stream)


def _single_message(client: ManusClient, message: str, mode: str, role: str, stream: bool):
    """Send a single message and display response"""
    console.print(f"\n[bold cyan]You:[/bold cyan] {message}\n")
    
    system_prompt = get_system_prompt(role)
    
    try:
        if stream:
            console.print("[bold magenta]Manus:[/bold magenta] ", end="")
            
            for chunk in client.stream_task(message, mode=mode, system_prompt=system_prompt):
                console.print(chunk, end="")
            
            console.print()  # New line after streaming
        else:
            with console.status("[bold green]Manus is thinking...", spinner="dots"):
                response = client.create_task(message, mode=mode, system_prompt=system_prompt)
            
            console.print("[bold magenta]Manus:[/bold magenta]")
            
            # Display task information
            task_id = response.get('task_id', 'N/A')
            status = response.get('status', 'N/A')
            
            console.print(Panel(
                f"[dim]Task ID: {task_id}\nStatus: {status}[/dim]",
                border_style="blue"
            ))
            
            # Display the full response
            console.print("\n[bold]Response:[/bold]")
            console.print_json(data=response)
            
    except RateLimitError as e:
        console.print(f"\n[red]Rate Limit Error:[/red] {e}")
        console.print("[yellow]Please wait a moment before trying again.[/yellow]")
        raise typer.Exit(1)
    except ManusAPIError as e:
        console.print(f"\n[red]Error:[/red] {e}")
        raise typer.Exit(1)


def _interactive_chat(client: ManusClient, mode: str, role: str, stream: bool):
    """Start an interactive chat session with conversation history"""
    conversation_id = str(uuid.uuid4())
    messages = []
    current_mode = mode
    current_role = role
    current_stream = stream
    
    role_info = get_role(current_role)
    
    console.print(Panel(
        f"[bold cyan]Manus AI - Interactive Chat[/bold cyan]\n\n"
        f"[bold]Current Role:[/bold] {role_info['name']}\n"
        f"[bold]Mode:[/bold] {current_mode}\n"
        f"[bold]Streaming:[/bold] {'Enabled' if current_stream else 'Disabled'}\n\n"
        "[bold]Commands:[/bold]\n"
        "  /quit or /exit - Exit the chat\n"
        "  /clear - Clear the screen\n"
        "  /mode <mode> - Change execution mode\n"
        "  /role <role> - Change role/persona\n"
        "  /stream - Toggle streaming\n"
        "  /save - Save conversation\n"
        "  /history - Show conversation history\n"
        "  /roles - List available roles\n"
        "  /help - Show this help\n",
        border_style="blue"
    ))
    
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
                
                elif command == '/clear':
                    console.clear()
                    continue
                
                elif command.startswith('/mode '):
                    new_mode = command.split(' ', 1)[1].strip()
                    current_mode = new_mode
                    console.print(f"[green]Mode changed to: {current_mode}[/green]")
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
                
                elif command == '/save':
                    client.save_conversation(conversation_id, messages)
                    console.print(f"[green]Conversation saved: {conversation_id}[/green]")
                    continue
                
                elif command == '/history':
                    console.print(f"\n[bold]Conversation History ({len(messages)} messages):[/bold]")
                    for i, msg in enumerate(messages, 1):
                        role_label = "You" if msg["role"] == "user" else "Manus"
                        console.print(f"\n[cyan]{i}. {role_label}:[/cyan] {msg['content'][:100]}...")
                    continue
                
                elif command == '/roles':
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("Key", style="cyan")
                    table.add_column("Name", style="green")
                    
                    for r in list_roles():
                        table.add_row(r["key"], r["name"])
                    
                    console.print(table)
                    continue
                
                elif command == '/help':
                    console.print(Panel(
                        "[bold]Available Commands:[/bold]\n"
                        "  /quit, /exit - Exit the chat\n"
                        "  /clear - Clear the screen\n"
                        "  /mode <mode> - Change execution mode\n"
                        "  /role <role> - Change role/persona\n"
                        "  /stream - Toggle streaming\n"
                        "  /save - Save conversation\n"
                        "  /history - Show conversation history\n"
                        "  /roles - List available roles\n"
                        "  /help - Show this help\n",
                        border_style="blue"
                    ))
                    continue
                
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    console.print("[dim]Type /help for available commands[/dim]")
                    continue
            
            # Add user message to history
            messages.append({"role": "user", "content": message})
            
            # Get system prompt for current role
            system_prompt = get_system_prompt(current_role)
            
            # Send message to API
            try:
                if current_stream:
                    console.print("\n[bold magenta]Manus:[/bold magenta] ", end="")
                    
                    response_text = ""
                    for chunk in client.stream_task(message, mode=current_mode, system_prompt=system_prompt):
                        console.print(chunk, end="")
                        response_text += chunk
                    
                    console.print()  # New line after streaming
                    
                    # Add assistant response to history
                    messages.append({"role": "assistant", "content": response_text})
                else:
                    with console.status("[bold green]Manus is thinking...", spinner="dots"):
                        response = client.create_task(message, mode=current_mode, system_prompt=system_prompt)
                    
                    console.print("\n[bold magenta]Manus:[/bold magenta]")
                    
                    # Display task information
                    task_id = response.get('task_id', 'N/A')
                    status = response.get('status', 'N/A')
                    
                    console.print(f"[dim]Task ID: {task_id} | Status: {status}[/dim]")
                    console.print_json(data=response)
                    
                    # Add assistant response to history
                    messages.append({"role": "assistant", "content": str(response)})
                    
            except RateLimitError as e:
                console.print(f"\n[red]Rate Limit Error:[/red] {e}")
                console.print("[yellow]Please wait before sending another message.[/yellow]")
            except ManusAPIError as e:
                console.print(f"\n[red]Error:[/red] {e}")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Chat interrupted. Type /quit to exit or continue chatting.[/yellow]")
            continue
        except EOFError:
            console.print("\n[yellow]Goodbye![/yellow]")
            break


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
    )
):
    """
    Create a new task and get the task ID
    
    Example:
        manus task "Analyze this data" --role data-scientist
    """
    try:
        client = ManusClient()
        config = ManusClient.load_config()
        
        if mode is None:
            mode = config.get("default_mode", "speed")
        
        if role is None:
            role = config.get("default_role", "assistant")
        
        system_prompt = get_system_prompt(role)
        
        with console.status("[bold green]Creating task...", spinner="dots"):
            response = client.create_task(prompt, mode=mode, system_prompt=system_prompt)
        
        task_id = response.get('task_id')
        status = response.get('status')
        
        console.print(f"\n[green]✓[/green] Task created successfully!")
        console.print(f"[bold]Task ID:[/bold] {task_id}")
        console.print(f"[bold]Status:[/bold] {status}")
        console.print(f"\n[dim]Full response:[/dim]")
        console.print_json(data=response)
        
    except ManusAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def status(
    task_id: str = typer.Argument(..., help="Task ID to check")
):
    """
    Check the status of a task
    
    Example:
        manus status abc123def456
    """
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
    """
    List saved conversation history
    
    Example:
        manus history
    """
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
