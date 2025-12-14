"""Performance Monitoring Dashboard for Manus CLI v5.2"""
import time
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

@dataclass
class PerformanceMetric:
    operation: str
    duration: float
    tokens_used: int
    timestamp: str
    success: bool
    error: Optional[str] = None

class PerformanceMonitor:
    """Monitors and tracks CLI performance metrics."""
    
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.metrics_dir = Path.home() / ".manus" / "metrics"
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.current_operation = None
        self.start_time = None
    
    def start_operation(self, operation: str):
        """Starts tracking an operation."""
        self.current_operation = operation
        self.start_time = time.time()
    
    def end_operation(self, tokens_used: int = 0, success: bool = True, error: Optional[str] = None):
        """Ends tracking and records metric."""
        if not self.current_operation:
            return
        
        duration = time.time() - self.start_time
        metric = PerformanceMetric(
            operation=self.current_operation,
            duration=duration,
            tokens_used=tokens_used,
            timestamp=datetime.now().isoformat(),
            success=success,
            error=error
        )
        
        self.metrics.append(metric)
        self.save_metric(metric)
        
        self.current_operation = None
        self.start_time = None
    
    def save_metric(self, metric: PerformanceMetric):
        """Saves metric to disk."""
        date_str = datetime.now().strftime("%Y%m%d")
        file_path = self.metrics_dir / f"metrics_{date_str}.jsonl"
        with open(file_path, "a") as f:
            f.write(json.dumps(asdict(metric)) + "\n")
    
    def load_metrics(self, days: int = 7) -> List[PerformanceMetric]:
        """Loads metrics from last N days."""
        all_metrics = []
        for file in sorted(self.metrics_dir.glob("metrics_*.jsonl"), reverse=True)[:days]:
            with open(file) as f:
                for line in f:
                    all_metrics.append(PerformanceMetric(**json.loads(line)))
        return all_metrics
    
    def get_stats(self) -> Dict[str, Any]:
        """Computes performance statistics."""
        if not self.metrics:
            self.metrics = self.load_metrics()
        
        if not self.metrics:
            return {}
        
        total_ops = len(self.metrics)
        successful_ops = sum(1 for m in self.metrics if m.success)
        total_duration = sum(m.duration for m in self.metrics)
        total_tokens = sum(m.tokens_used for m in self.metrics)
        
        return {
            "total_operations": total_ops,
            "successful_operations": successful_ops,
            "success_rate": successful_ops / total_ops * 100,
            "avg_duration": total_duration / total_ops,
            "total_tokens": total_tokens,
            "avg_tokens_per_op": total_tokens / total_ops if total_ops > 0 else 0
        }
    
    def display_dashboard(self):
        """Displays performance dashboard."""
        stats = self.get_stats()
        
        if not stats:
            console.print("[yellow]No metrics available yet[/yellow]")
            return
        
        # Stats panel
        stats_text = f"""
**Total Operations:** {stats['total_operations']}
**Success Rate:** {stats['success_rate']:.1f}%
**Avg Duration:** {stats['avg_duration']:.2f}s
**Total Tokens:** {stats['total_tokens']:,}
**Avg Tokens/Op:** {stats['avg_tokens_per_op']:.0f}
"""
        
        console.print(Panel(
            stats_text,
            title="[bold cyan]Performance Dashboard[/bold cyan]",
            border_style="cyan"
        ))
        
        # Recent operations table
        table = Table(title="Recent Operations")
        table.add_column("Operation", style="cyan")
        table.add_column("Duration", style="yellow")
        table.add_column("Tokens", style="green")
        table.add_column("Status", style="white")
        
        for metric in self.metrics[-10:]:
            status = "✅" if metric.success else "❌"
            table.add_row(
                metric.operation,
                f"{metric.duration:.2f}s",
                str(metric.tokens_used),
                status
            )
        
        console.print(table)
