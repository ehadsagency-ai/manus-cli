"""
Enhanced Streaming module for Manus CLI v5.0

Implements streaming responses with rich UI, progress indicators,
and token counting.

Based on Claude documentation analysis.
"""

from rich.live import Live
from rich.spinner import Spinner
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
import time
from typing import Generator, Optional


console = Console()


class StreamingHandler:
    """Handles streaming responses with rich UI."""
    
    def __init__(self, show_thinking: bool = False, show_stats: bool = False):
        """
        Initialize streaming handler.
        
        Args:
            show_thinking: Whether to display thinking process
            show_stats: Whether to show token statistics
        """
        self.show_thinking = show_thinking
        self.show_stats = show_stats
        self.buffer = ""
        self.thinking_buffer = ""
        self.in_thinking = False
        self.token_count = 0
        self.start_time = None
    
    def stream_response(self, response_generator: Generator[str, None, None]):
        """
        Streams response with live updates.
        
        Args:
            response_generator: Generator yielding chunks of text
        """
        self.start_time = time.time()
        
        with Live(
            Spinner("dots", text="[cyan]Connecting...[/cyan]"),
            console=console,
            refresh_per_second=10
        ) as live:
            for chunk in response_generator:
                self._process_chunk(chunk, live)
        
        # Final output
        self._display_final_output()
    
    def _process_chunk(self, chunk: str, live: Live):
        """Processes a single chunk of streamed text."""
        # Detect thinking tags
        if "<thinking>" in chunk:
            self.in_thinking = True
            if self.show_thinking:
                live.update(Spinner("dots", text="[cyan]💭 Analyzing...[/cyan]"))
            return
        
        if "</thinking>" in chunk:
            self.in_thinking = False
            live.update(Spinner("dots", text="[green]✍️  Generating answer...[/green]"))
            return
        
        # Buffer content
        if self.in_thinking:
            if self.show_thinking:
                self.thinking_buffer += chunk
                live.update(Panel(
                    self.thinking_buffer,
                    title="[cyan]💭 Thinking Process[/cyan]",
                    border_style="cyan"
                ))
        else:
            self.buffer += chunk
            self.token_count += len(chunk.split())  # Rough estimate
            
            # Update live display
            if self.show_stats:
                elapsed = time.time() - self.start_time
                tokens_per_sec = self.token_count / elapsed if elapsed > 0 else 0
                status = f"[cyan]Tokens: {self.token_count} | Speed: {tokens_per_sec:.1f} tok/s[/cyan]"
                
                live.update(Panel(
                    Markdown(self.buffer),
                    title=status,
                    border_style="green"
                ))
            else:
                live.update(Markdown(self.buffer))
    
    def _display_final_output(self):
        """Displays the final output after streaming completes."""
        # Display thinking if requested
        if self.show_thinking and self.thinking_buffer:
            console.print(Panel(
                self.thinking_buffer,
                title="[cyan]💭 Thinking Process[/cyan]",
                border_style="cyan",
                padding=(1, 2)
            ))
        
        # Display answer
        console.print(Panel(
            Markdown(self.buffer),
            title="[green]✅ Answer[/green]",
            border_style="green",
            padding=(1, 2)
        ))
        
        # Display stats if requested
        if self.show_stats and self.start_time:
            elapsed = time.time() - self.start_time
            tokens_per_sec = self.token_count / elapsed if elapsed > 0 else 0
            
            stats = f"""
**Statistics:**
- Tokens: {self.token_count}
- Time: {elapsed:.2f}s
- Speed: {tokens_per_sec:.1f} tokens/sec
"""
            console.print(Panel(
                stats,
                title="[blue]📊 Statistics[/blue]",
                border_style="blue"
            ))


class ProgressStreamingHandler:
    """Streaming handler with progress bar for long operations."""
    
    def __init__(self, total_steps: Optional[int] = None):
        """
        Initialize progress streaming handler.
        
        Args:
            total_steps: Total number of steps (if known)
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.buffer = ""
    
    def stream_with_progress(
        self,
        response_generator: Generator[str, None, None],
        task_description: str = "Processing"
    ):
        """
        Streams response with progress bar.
        
        Args:
            response_generator: Generator yielding chunks
            task_description: Description of the task
        """
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task(
                task_description,
                total=self.total_steps if self.total_steps else 100
            )
            
            for chunk in response_generator:
                self.buffer += chunk
                self.current_step += 1
                
                if self.total_steps:
                    progress.update(task, completed=self.current_step)
                else:
                    # Indeterminate progress
                    progress.update(task, advance=1)
        
        # Display final result
        console.print(Panel(
            Markdown(self.buffer),
            title="[green]✅ Complete[/green]",
            border_style="green"
        ))


class MultiPhaseStreamingHandler:
    """Streaming handler for multi-phase operations (spec-driven workflow)."""
    
    def __init__(self, phases: list[str]):
        """
        Initialize multi-phase streaming handler.
        
        Args:
            phases: List of phase names
        """
        self.phases = phases
        self.current_phase_index = 0
        self.phase_outputs = {}
    
    def stream_phase(
        self,
        phase_name: str,
        response_generator: Generator[str, None, None]
    ):
        """
        Streams a single phase with phase indicator.
        
        Args:
            phase_name: Name of the current phase
            response_generator: Generator yielding chunks
        """
        buffer = ""
        
        phase_num = self.current_phase_index + 1
        total_phases = len(self.phases)
        
        with Live(
            Spinner("dots", text=f"[cyan]Phase {phase_num}/{total_phases}: {phase_name}...[/cyan]"),
            console=console,
            refresh_per_second=10
        ) as live:
            for chunk in response_generator:
                buffer += chunk
                live.update(Panel(
                    Markdown(buffer),
                    title=f"[cyan]Phase {phase_num}/{total_phases}: {phase_name}[/cyan]",
                    border_style="cyan"
                ))
        
        # Store phase output
        self.phase_outputs[phase_name] = buffer
        
        # Display completion
        console.print(Panel(
            Markdown(buffer),
            title=f"[green]✅ Phase {phase_num}/{total_phases}: {phase_name} Complete[/green]",
            border_style="green"
        ))
        
        self.current_phase_index += 1
    
    def get_phase_output(self, phase_name: str) -> Optional[str]:
        """Gets the output of a specific phase."""
        return self.phase_outputs.get(phase_name)
    
    def get_all_outputs(self) -> dict[str, str]:
        """Gets all phase outputs."""
        return self.phase_outputs.copy()


# Example usage
if __name__ == "__main__":
    import time
    
    # Simulate streaming response
    def simulate_stream():
        """Simulates a streaming API response."""
        text = """
<thinking>
Let me think through this problem step by step:
1. First, I need to understand the requirements
2. Then, I'll design the architecture
3. Finally, I'll provide the implementation plan
</thinking>

<answer>
# Microservices Architecture

## Overview
A microservices architecture consists of small, independent services that communicate via APIs.

## Key Components
1. **API Gateway** - Entry point for all requests
2. **Service Registry** - Service discovery
3. **Load Balancer** - Distributes traffic
4. **Message Queue** - Asynchronous communication

## Benefits
- Scalability
- Flexibility
- Fault isolation
- Technology diversity
</answer>
"""
        
        for char in text:
            yield char
            time.sleep(0.01)  # Simulate network delay
    
    # Test basic streaming
    print("Test 1: Basic Streaming")
    print("="*80)
    handler1 = StreamingHandler(show_thinking=False, show_stats=False)
    handler1.stream_response(simulate_stream())
    
    print("\n\nTest 2: Streaming with Thinking and Stats")
    print("="*80)
    handler2 = StreamingHandler(show_thinking=True, show_stats=True)
    handler2.stream_response(simulate_stream())
    
    print("\n\nTest 3: Multi-Phase Streaming")
    print("="*80)
    phases = ["Constitution", "Specify", "Plan"]
    handler3 = MultiPhaseStreamingHandler(phases)
    
    for phase in phases:
        handler3.stream_phase(phase, simulate_stream())
        time.sleep(0.5)  # Pause between phases
