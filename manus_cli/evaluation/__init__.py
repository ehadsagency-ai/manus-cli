"""Evaluation & Testing Framework for Manus CLI v5.2"""
import time
from typing import List, Dict, Any, Callable
from dataclasses import dataclass, field
from rich.console import Console
from rich.table import Table

console = Console()

@dataclass
class TestCase:
    name: str
    input: str
    expected_output: Optional[str] = None
    validator: Optional[Callable] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TestResult:
    test_case: TestCase
    actual_output: str
    passed: bool
    duration: float
    error: Optional[str] = None

class EvaluationFramework:
    """Framework for testing and evaluating CLI performance."""
    
    def __init__(self):
        self.test_cases: List[TestCase] = []
        self.results: List[TestResult] = []
    
    def add_test(self, test_case: TestCase):
        """Adds a test case."""
        self.test_cases.append(test_case)
    
    def run_tests(self, executor: Callable[[str], str]) -> List[TestResult]:
        """Runs all test cases."""
        self.results = []
        
        for test_case in self.test_cases:
            console.print(f"Running: {test_case.name}...")
            start = time.time()
            
            try:
                output = executor(test_case.input)
                duration = time.time() - start
                
                # Validate output
                if test_case.validator:
                    passed = test_case.validator(output)
                elif test_case.expected_output:
                    passed = output == test_case.expected_output
                else:
                    passed = True  # No validation
                
                result = TestResult(
                    test_case=test_case,
                    actual_output=output,
                    passed=passed,
                    duration=duration
                )
            except Exception as e:
                result = TestResult(
                    test_case=test_case,
                    actual_output="",
                    passed=False,
                    duration=time.time() - start,
                    error=str(e)
                )
            
            self.results.append(result)
        
        return self.results
    
    def print_report(self):
        """Prints test results report."""
        table = Table(title="Test Results")
        table.add_column("Test", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Duration", style="yellow")
        table.add_column("Error", style="red")
        
        for result in self.results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            error = result.error or ""
            table.add_row(
                result.test_case.name,
                status,
                f"{result.duration:.2f}s",
                error
            )
        
        console.print(table)
        
        # Summary
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        console.print(f"\n[bold]Summary:[/bold] {passed}/{total} tests passed")
