"""
Main CLI application using Typer
"""

import sys
import typer
from typing import Optional
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.live import Live
from rich.spinner import Spinner
from rich import print as rprint

from .api import ManusClient, ManusAPIError
from . import __version__

app = typer.Typer(
    name="manus",
    help="Manus AI - Command-line interface for interacting with Manus AI",
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
    )
):
    """
    Configure Manus CLI with your API key
    
    Example:
        manus configure --api-key sk-your-api-key
        manus configure  # Interactive mode
    """
    if not api_key:
        console.print("[bold yellow]Configure Manus CLI[/bold yellow]\n")
        api_key = Prompt.ask(
            "[cyan]Enter your Manus API key[/cyan]",
            password=True
        )
    
    if not api_key or not api_key.strip():
        console.print("[red]Error: API key cannot be empty[/red]")
        raise typer.Exit(1)
    
    try:
        ManusClient.save_api_key(api_key.strip())
        console.print("\n[green]✓[/green] API key saved successfully!")
        console.print(f"[dim]Configuration stored in: {ManusClient.CONFIG_FILE}[/dim]")
    except Exception as e:
        console.print(f"[red]Error saving configuration: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def chat(
    message: Optional[str] = typer.Argument(
        None,
        help="Message to send to Manus AI"
    ),
    mode: str = typer.Option(
        "speed",
        "--mode",
        "-m",
        help="Execution mode (speed, quality, etc.)"
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
        manus chat "Write a Python function to sort a list" --mode quality
        manus chat --interactive  # Start interactive session
    """
    try:
        client = ManusClient()
    except ManusAPIError as e:
        console.print(f"[red]Error: {e}[/red]")
        console.print("\n[yellow]Tip:[/yellow] Run 'manus configure' to set up your API key")
        raise typer.Exit(1)
    
    if interactive or not message:
        _interactive_chat(client, mode)
    else:
        _single_message(client, message, mode)


def _single_message(client: ManusClient, message: str, mode: str):
    """Send a single message and display response"""
    console.print(f"\n[bold cyan]You:[/bold cyan] {message}\n")
    
    with console.status("[bold green]Manus is thinking...", spinner="dots"):
        try:
            response = client.create_task(message, mode=mode)
            
            console.print("[bold magenta]Manus:[/bold magenta]")
            
            # Display task information
            task_id = response.get('task_id', 'N/A')
            status = response.get('status', 'N/A')
            
            console.print(Panel(
                f"[dim]Task ID: {task_id}\nStatus: {status}[/dim]",
                border_style="blue"
            ))
            
            # Display the full response
            console.print("\n[bold]Full Response:[/bold]")
            console.print_json(data=response)
            
        except ManusAPIError as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(1)


def _interactive_chat(client: ManusClient, mode: str):
    """Start an interactive chat session"""
    console.print(Panel(
        "[bold cyan]Manus AI - Interactive Chat[/bold cyan]\n\n"
        "Type your messages and press Enter to send.\n"
        "Commands:\n"
        "  /quit or /exit - Exit the chat\n"
        "  /clear - Clear the screen\n"
        "  /mode <mode> - Change execution mode\n",
        border_style="blue"
    ))
    
    current_mode = mode
    
    while True:
        try:
            message = Prompt.ask("\n[bold cyan]You[/bold cyan]")
            
            if not message.strip():
                continue
            
            # Handle commands
            if message.startswith('/'):
                command = message.lower().strip()
                
                if command in ['/quit', '/exit']:
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
                
                else:
                    console.print(f"[red]Unknown command: {command}[/red]")
                    continue
            
            # Send message to API
            with console.status("[bold green]Manus is thinking...", spinner="dots"):
                try:
                    response = client.create_task(message, mode=current_mode)
                    
                    console.print("\n[bold magenta]Manus:[/bold magenta]")
                    
                    # Display task information
                    task_id = response.get('task_id', 'N/A')
                    status = response.get('status', 'N/A')
                    
                    console.print(f"[dim]Task ID: {task_id} | Status: {status}[/dim]")
                    console.print_json(data=response)
                    
                except ManusAPIError as e:
                    console.print(f"[red]Error: {e}[/red]")
        
        except KeyboardInterrupt:
            console.print("\n[yellow]Chat interrupted. Type /quit to exit.[/yellow]")
            continue
        except EOFError:
            console.print("\n[yellow]Goodbye![/yellow]")
            break


@app.command()
def task(
    prompt: str = typer.Argument(..., help="Task prompt to send"),
    mode: str = typer.Option(
        "speed",
        "--mode",
        "-m",
        help="Execution mode"
    )
):
    """
    Create a new task and get the task ID
    
    Example:
        manus task "Analyze this data and create a report"
    """
    try:
        client = ManusClient()
        
        with console.status("[bold green]Creating task...", spinner="dots"):
            response = client.create_task(prompt, mode=mode)
        
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


def run():
    """Entry point for the CLI"""
    app()


if __name__ == "__main__":
    run()
