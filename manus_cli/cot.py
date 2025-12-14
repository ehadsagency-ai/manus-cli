"""
Chain of Thought (CoT) module for Manus CLI v5.0

Implements structured Chain-of-Thought prompting to improve accuracy
on complex tasks by encouraging step-by-step reasoning.

Based on Claude documentation analysis.
"""

import re
from typing import Tuple, Optional
from rich.console import Console
from rich.panel import Panel

console = Console()


class ChainOfThought:
    """Implements structured Chain-of-Thought prompting."""
    
    def __init__(self, enabled: bool = False, verbose: bool = False):
        """
        Initialize CoT engine.
        
        Args:
            enabled: Whether CoT is enabled
            verbose: Whether to display thinking process
        """
        self.enabled = enabled
        self.verbose = verbose
    
    def wrap_prompt(self, user_input: str, task_complexity: str = "medium") -> str:
        """
        Wraps user input with CoT instructions.
        
        Args:
            user_input: Original user prompt
            task_complexity: Complexity level (simple/medium/complex)
        
        Returns:
            Enhanced prompt with CoT instructions
        """
        if not self.enabled:
            return user_input
        
        complexity_instructions = {
            "simple": "Think through this briefly before answering.",
            "medium": "Think through this step-by-step before providing your answer.",
            "complex": "Think through this problem deeply and systematically before answering."
        }
        
        cot_instruction = f"""
{complexity_instructions.get(task_complexity, complexity_instructions["medium"])}

Before providing your final answer, please enclose your step-by-step reasoning within <thinking> tags.
Then provide your final, clean output within <answer> tags.

Structure your thinking as follows:
1. Understand the request - What is being asked?
2. Identify key requirements - What are the constraints and goals?
3. Consider edge cases - What could go wrong?
4. Plan the approach - What's the best way to solve this?
5. Execute the solution - Implement the plan

Do not include any text outside these tags.

User Request: {user_input}
"""
        
        return cot_instruction.strip()
    
    def parse_output(self, model_output: str) -> Tuple[Optional[str], str]:
        """
        Parses CoT output to extract thinking and answer.
        
        Args:
            model_output: Raw output from the model
        
        Returns:
            Tuple of (thinking_process, final_answer)
        """
        # Extract thinking block
        thinking_match = re.search(
            r"<thinking>(.*?)</thinking>", 
            model_output, 
            re.DOTALL | re.IGNORECASE
        )
        
        # Extract answer block
        answer_match = re.search(
            r"<answer>(.*?)</answer>", 
            model_output, 
            re.DOTALL | re.IGNORECASE
        )
        
        thinking = thinking_match.group(1).strip() if thinking_match else None
        answer = answer_match.group(1).strip() if answer_match else model_output.strip()
        
        return thinking, answer
    
    def should_enable_cot(self, command: str, user_input: str) -> bool:
        """
        Determines if CoT should be automatically enabled.
        
        Auto-enable for:
        - Spec-driven commands (create, build, plan)
        - Complex analysis tasks
        - Multi-step reasoning
        
        Args:
            command: CLI command being executed
            user_input: User's input text
        
        Returns:
            True if CoT should be enabled
        """
        # Keywords that trigger CoT
        cot_triggers = [
            "create", "build", "plan", "design", "architect",
            "analyze", "evaluate", "compare", "debug",
            "refactor", "optimize", "review", "implement"
        ]
        
        # Check command
        if any(trigger in command.lower() for trigger in cot_triggers):
            return True
        
        # Check input complexity (heuristic)
        if len(user_input.split()) > 50:  # Long input
            return True
        
        if "?" in user_input and user_input.count("?") > 1:  # Multiple questions
            return True
        
        # Check for spec-driven keywords
        spec_keywords = ["specification", "requirements", "architecture", "system design"]
        if any(keyword in user_input.lower() for keyword in spec_keywords):
            return True
        
        return False
    
    def display_thinking(self, thinking: str):
        """Displays the thinking process in a panel."""
        if thinking and self.verbose:
            console.print(Panel(
                thinking,
                title="[cyan]💭 Thinking Process[/cyan]",
                border_style="cyan",
                padding=(1, 2)
            ))
    
    def display_answer(self, answer: str):
        """Displays the final answer in a panel."""
        console.print(Panel(
            answer,
            title="[green]✅ Answer[/green]",
            border_style="green",
            padding=(1, 2)
        ))
    
    def assess_complexity(self, user_input: str) -> str:
        """
        Assesses the complexity of the user's request.
        
        Args:
            user_input: User's input text
        
        Returns:
            Complexity level: "simple", "medium", or "complex"
        """
        word_count = len(user_input.split())
        question_count = user_input.count("?")
        
        # Simple heuristics
        if word_count < 20 and question_count <= 1:
            return "simple"
        elif word_count > 100 or question_count > 2:
            return "complex"
        else:
            return "medium"


# Example usage
if __name__ == "__main__":
    cot = ChainOfThought(enabled=True, verbose=True)
    
    # Test prompt
    test_prompt = "Design a microservices architecture for a real-time chat application"
    
    # Wrap prompt
    enhanced_prompt = cot.wrap_prompt(test_prompt, task_complexity="complex")
    print("Enhanced Prompt:")
    print(enhanced_prompt)
    print("\n" + "="*80 + "\n")
    
    # Simulate model output
    simulated_output = """
<thinking>
1. Understanding: Need to design microservices for real-time chat
2. Key requirements: Real-time messaging, scalability, reliability
3. Edge cases: Network failures, message ordering, user presence
4. Approach: Use WebSockets, message queue, separate services
5. Solution: API Gateway, Auth Service, Chat Service, Presence Service, Message Store
</thinking>

<answer>
# Microservices Architecture for Real-Time Chat

## Services
1. **API Gateway** - Entry point, routing, rate limiting
2. **Auth Service** - User authentication and authorization
3. **Chat Service** - WebSocket connections, message routing
4. **Presence Service** - User online/offline status
5. **Message Store** - Persistent message storage

## Communication
- WebSockets for real-time messaging
- Redis Pub/Sub for inter-service communication
- PostgreSQL for message persistence
</answer>
"""
    
    # Parse output
    thinking, answer = cot.parse_output(simulated_output)
    
    # Display
    cot.display_thinking(thinking)
    cot.display_answer(answer)
