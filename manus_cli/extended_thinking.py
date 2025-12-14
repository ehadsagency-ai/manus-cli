"""
Extended Thinking module for Manus CLI v5.1

Implements Claude's Extended Thinking feature for deep reasoning on complex tasks.
Based on Claude documentation analysis.
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()


@dataclass
class ThinkingConfig:
    """Configuration for extended thinking mode."""
    enabled: bool = False
    show_thinking: bool = False
    thinking_budget: int = 10000  # tokens
    min_complexity_score: float = 0.7  # 0-1 scale


class ExtendedThinking:
    """
    Implements extended thinking for complex reasoning tasks.
    
    Extended thinking allows the model to "think" longer before responding,
    improving accuracy on complex tasks like math, coding, and analysis.
    """
    
    def __init__(self, config: Optional[ThinkingConfig] = None):
        """
        Initialize extended thinking.
        
        Args:
            config: Configuration for thinking behavior
        """
        self.config = config or ThinkingConfig()
    
    def should_use_extended_thinking(self, task: str, complexity_score: Optional[float] = None) -> bool:
        """
        Determines if extended thinking should be used.
        
        Args:
            task: The task description
            complexity_score: Optional pre-computed complexity score
        
        Returns:
            True if extended thinking should be used
        """
        if not self.config.enabled:
            return False
        
        # Use provided score or compute it
        score = complexity_score if complexity_score is not None else self._assess_complexity(task)
        
        return score >= self.config.min_complexity_score
    
    def _assess_complexity(self, task: str) -> float:
        """
        Assesses task complexity on a 0-1 scale.
        
        Args:
            task: The task description
        
        Returns:
            Complexity score (0-1)
        """
        # Complexity indicators
        indicators = {
            'high': ['algorithm', 'optimize', 'prove', 'derive', 'calculate', 
                    'analyze', 'compare', 'evaluate', 'design', 'architect'],
            'medium': ['explain', 'describe', 'implement', 'create', 'build',
                      'refactor', 'review', 'test'],
            'low': ['list', 'show', 'display', 'what is', 'define']
        }
        
        task_lower = task.lower()
        
        # Count indicators
        high_count = sum(1 for word in indicators['high'] if word in task_lower)
        medium_count = sum(1 for word in indicators['medium'] if word in task_lower)
        low_count = sum(1 for word in indicators['low'] if word in task_lower)
        
        # Length factor (longer tasks tend to be more complex)
        length_factor = min(len(task.split()) / 50.0, 1.0)
        
        # Calculate score
        if high_count > 0:
            base_score = 0.8
        elif medium_count > 0:
            base_score = 0.5
        elif low_count > 0:
            base_score = 0.2
        else:
            base_score = 0.4  # Default for ambiguous tasks
        
        # Adjust by length
        final_score = base_score * 0.7 + length_factor * 0.3
        
        return min(final_score, 1.0)
    
    def format_prompt_with_thinking(self, prompt: str) -> str:
        """
        Formats prompt to enable extended thinking.
        
        Args:
            prompt: Original prompt
        
        Returns:
            Formatted prompt with thinking instructions
        """
        thinking_instruction = f"""
Before answering, take time to think through this problem carefully. You have up to {self.config.thinking_budget} tokens to reason through the solution.

<thinking_guidelines>
1. Break down the problem into smaller parts
2. Consider multiple approaches
3. Identify potential pitfalls or edge cases
4. Reason step-by-step
5. Verify your logic before concluding
</thinking_guidelines>

Enclose your reasoning in <thinking> tags, then provide your final answer in <answer> tags.
"""
        
        return f"{thinking_instruction}\n\n{prompt}"
    
    def parse_thinking_response(self, response: str) -> Dict[str, str]:
        """
        Parses response with thinking and answer sections.
        
        Args:
            response: Raw response from API
        
        Returns:
            Dictionary with 'thinking' and 'answer' keys
        """
        import re
        
        # Extract thinking
        thinking_match = re.search(r'<thinking>(.*?)</thinking>', response, re.DOTALL)
        thinking = thinking_match.group(1).strip() if thinking_match else ""
        
        # Extract answer
        answer_match = re.search(r'<answer>(.*?)</answer>', response, re.DOTALL)
        answer = answer_match.group(1).strip() if answer_match else response
        
        return {
            'thinking': thinking,
            'answer': answer
        }
    
    def display_thinking_process(self, thinking: str):
        """
        Displays the thinking process to the user.
        
        Args:
            thinking: The thinking content
        """
        if not thinking or not self.config.show_thinking:
            return
        
        console.print(Panel(
            Markdown(thinking),
            title="[cyan]💭 Extended Thinking Process[/cyan]",
            border_style="cyan",
            padding=(1, 2)
        ))
    
    def display_answer(self, answer: str):
        """
        Displays the final answer.
        
        Args:
            answer: The answer content
        """
        console.print(Panel(
            Markdown(answer),
            title="[green]✅ Answer[/green]",
            border_style="green",
            padding=(1, 2)
        ))
    
    def get_thinking_stats(self, thinking: str) -> Dict[str, Any]:
        """
        Computes statistics about the thinking process.
        
        Args:
            thinking: The thinking content
        
        Returns:
            Dictionary with statistics
        """
        words = thinking.split()
        lines = thinking.split('\n')
        
        return {
            'word_count': len(words),
            'line_count': len(lines),
            'estimated_tokens': len(words) * 1.3,  # Rough estimate
            'has_steps': any(line.strip().startswith(('1.', '2.', '3.', '-', '*')) for line in lines)
        }


# Example usage
if __name__ == "__main__":
    # Test extended thinking
    config = ThinkingConfig(
        enabled=True,
        show_thinking=True,
        thinking_budget=5000
    )
    
    et = ExtendedThinking(config)
    
    # Test complexity assessment
    tasks = [
        "What is Python?",
        "Explain how to use list comprehensions",
        "Design a scalable microservices architecture for an e-commerce platform",
        "Prove that the sum of angles in a triangle is 180 degrees"
    ]
    
    console.print("[bold]Complexity Assessment:[/bold]\n")
    for task in tasks:
        score = et._assess_complexity(task)
        should_use = et.should_use_extended_thinking(task)
        console.print(f"Task: {task[:50]}...")
        console.print(f"  Complexity: {score:.2f} | Use Extended Thinking: {should_use}\n")
    
    # Test prompt formatting
    console.print("\n[bold]Formatted Prompt Example:[/bold]\n")
    original_prompt = "Design a distributed caching system"
    formatted = et.format_prompt_with_thinking(original_prompt)
    console.print(Panel(formatted, title="Formatted Prompt", border_style="blue"))
    
    # Test response parsing
    console.print("\n[bold]Response Parsing Example:[/bold]\n")
    sample_response = """
<thinking>
Let me break this down:
1. First, I need to consider the requirements
2. Then, I'll design the architecture
3. Finally, I'll identify potential issues
</thinking>

<answer>
Here's the distributed caching system design:
- Use Redis for in-memory caching
- Implement consistent hashing for distribution
- Add replication for fault tolerance
</answer>
"""
    
    parsed = et.parse_thinking_response(sample_response)
    et.display_thinking_process(parsed['thinking'])
    et.display_answer(parsed['answer'])
    
    # Show stats
    stats = et.get_thinking_stats(parsed['thinking'])
    console.print(f"\n[bold]Thinking Stats:[/bold] {stats}")
