"""
Splash screen and interactive start for Manus CLI.
"""

import time
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.align import Align

console = Console()


def show_splash_screen():
    """
    Display the Manus CLI splash screen with 'AND AFTER YOU' prompt.
    
    This creates an inviting, interactive experience that signals to users
    they can start interacting with the CLI.
    """
    
    # Main ASCII art banner - MANUS (original beautiful design)
    banner = """
███╗   ███╗ █████╗ ███╗   ██╗██╗   ██╗███████╗
████╗ ████║██╔══██╗████╗  ██║██║   ██║██╔════╝
██╔████╔██║███████║██╔██╗ ██║██║   ██║███████╗
██║╚██╔╝██║██╔══██║██║╚██╗██║██║   ██║╚════██║
██║ ╚═╝ ██║██║  ██║██║ ╚████║╚██████╔╝███████║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝
    """
    
    # Create the main panel - let Rich auto-size to content
    console.print()
    
    # Center the entire panel
    from rich.align import Align as RichAlign
    
    panel = Panel(
        Align.center(
            f"[bold cyan]{banner}[/bold cyan]\n\n"
            f"[bold white]AI-POWERED COMMAND LINE INTERFACE[/bold white]\n"
            f"[dim]Professional • Intelligent • Spec-Driven[/dim]"
        ),
        border_style="cyan",
        padding=(1, 2)
    )
    
    console.print(RichAlign.center(panel))
    
    # Animated "AND AFTER YOU" prompt
    console.print()
    
    # Create a stylized prompt message
    prompt_text = Text()
    prompt_text.append("✨ ", style="yellow")
    prompt_text.append("AND AFTER YOU", style="bold magenta")
    prompt_text.append(" ✨", style="yellow")
    
    console.print(Align.center(prompt_text))
    console.print()
    
    # Show quick stats
    stats_panel = Panel(
        "[cyan]Available Commands:[/cyan]\n"
        "  • [green]chat[/green]      - Talk to Manus AI\n"
        "  • [green]roles[/green]     - View 12 professional roles\n"
        "  • [green]configure[/green] - Setup your API key\n"
        "  • [green]update[/green]    - Update to latest version\n"
        "  • [green]help[/green]      - Show all commands\n\n"
        "[cyan]Quick Start:[/cyan]\n"
        "  [dim]manus chat \"Hello, world!\"[/dim]\n"
        "  [dim]manus chat \"Create a web app\" --role developer[/dim]",
        title="[bold]Ready to Assist[/bold]",
        border_style="green",
        padding=(1, 2)
    )
    
    console.print(Align.center(stats_panel))
    console.print()


def show_interactive_splash():
    """
    Show splash screen and enter interactive mode.
    
    This provides a welcoming experience where users can immediately
    start chatting after seeing the splash screen.
    """
    from . import __version__
    
    # Show the splash
    show_splash_screen()
    
    # Show version and timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    console.print(f"[dim]Manus CLI v{__version__} • {timestamp}[/dim]")
    console.print()
    
    # Interactive prompt message
    console.print("[bold cyan]💬 Interactive Mode[/bold cyan]")
    console.print("[dim]Type your message and press Enter. Type 'exit' or 'quit' to leave.[/dim]")
    console.print()
    
    return True


def show_mini_splash(role: str = "assistant", mode: str = "balanced"):
    """
    Show a minimal splash screen for quick interactions.
    
    Args:
        role: The AI role being used
        mode: The execution mode (speed/balanced/quality)
    """
    
    console.print()
    console.print(Panel(
        f"[bold cyan]MANUS AI[/bold cyan] • [green]{role.upper()}[/green] • [yellow]{mode.upper()}[/yellow]",
        border_style="cyan",
        padding=(0, 2)
    ))
    console.print()


def show_welcome_message():
    """Show a simple welcome message without full splash."""
    
    console.print()
    console.print("[bold cyan]👋 Welcome to Manus CLI[/bold cyan]")
    console.print("[dim]Type 'manus start' for interactive mode or 'manus --help' for commands.[/dim]")
    console.print()
