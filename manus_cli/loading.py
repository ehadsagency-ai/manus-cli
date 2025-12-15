"""
Loading animations and progress indicators for Manus CLI
"""

import time
from contextlib import contextmanager
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()


@contextmanager
def loading_spinner(message: str, success_message: str = None):
    """
    Context manager for showing a loading spinner.
    
    Args:
        message: Message to display while loading
        success_message: Message to display on success (optional)
    
    Usage:
        with loading_spinner("Processing..."):
            # Do work
            pass
    """
    spinner = Spinner("dots", text=f"[cyan]{message}[/cyan]")
    
    with Live(spinner, console=console, refresh_per_second=10):
        try:
            yield
            # Success
            if success_message:
                console.print(f"[green]✓[/green] {success_message}")
        except Exception as e:
            # Error
            console.print(f"[red]✗[/red] Error: {str(e)}")
            raise


@contextmanager
def progress_bar(total: int, description: str = "Processing"):
    """
    Context manager for showing a progress bar.
    
    Args:
        total: Total number of items
        description: Description of the task
    
    Usage:
        with progress_bar(100, "Processing items") as update:
            for i in range(100):
                # Do work
                update(1)  # Increment by 1
    """
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    )
    
    with progress:
        task_id = progress.add_task(description, total=total)
        
        def update(advance: int = 1):
            progress.update(task_id, advance=advance)
        
        yield update


def show_phase_header(phase_number: int, total_phases: int, phase_name: str):
    """
    Show a phase header with progress.
    
    Args:
        phase_number: Current phase number (1-indexed)
        total_phases: Total number of phases
        phase_name: Name of the current phase
    """
    from rich.panel import Panel
    from rich.text import Text
    
    # Create progress bar
    progress_text = "━" * 60
    filled = int((phase_number / total_phases) * 60)
    progress_bar_text = f"[green]{'━' * filled}[/green][dim]{'━' * (60 - filled)}[/dim]"
    
    header = Text()
    header.append(f"Phase {phase_number}/{total_phases}: ", style="bold cyan")
    header.append(phase_name, style="bold white")
    
    console.print()
    console.print(header)
    console.print(progress_bar_text)


def show_step(message: str, status: str = "working"):
    """
    Show a step in the process.
    
    Args:
        message: Step message
        status: Status ("working", "success", "warning", "error")
    """
    icons = {
        "working": "[cyan]→[/cyan]",
        "success": "[green]✓[/green]",
        "warning": "[yellow]⚠[/yellow]",
        "error": "[red]✗[/red]",
    }
    
    icon = icons.get(status, "→")
    console.print(f"{icon} {message}")


def show_ai_thinking(message: str = "AI is thinking"):
    """
    Show an animated "AI is thinking" indicator.
    
    Args:
        message: Message to display
    
    Returns:
        Context manager for the spinner
    """
    return loading_spinner(f"🤖 {message}...", f"{message} complete")


# Example usage
if __name__ == "__main__":
    # Test spinner
    with loading_spinner("Testing spinner", "Spinner test complete"):
        time.sleep(2)
    
    # Test progress bar
    with progress_bar(100, "Testing progress") as update:
        for i in range(100):
            time.sleep(0.02)
            update(1)
    
    # Test phase header
    show_phase_header(1, 3, "Constitution")
    show_step("Checking for existing constitution...", "success")
    show_step("Creating new constitution...", "working")
    
    # Test AI thinking
    with show_ai_thinking("Generating specification"):
        time.sleep(2)
