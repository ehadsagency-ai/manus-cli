#!/usr/bin/env python3
"""
Comprehensive test script for Manus CLI v5.2 features
Tests: Cache, Context, Evaluation, Monitoring
"""

import sys
import time
import tempfile
from pathlib import Path

sys.path.insert(0, '/home/ubuntu/manus-cli')

from rich.console import Console
from rich.panel import Panel

console = Console()

def test_cache():
    """Test Prompt Caching."""
    console.print("\n[bold cyan]Testing Prompt Caching...[/bold cyan]")
    
    try:
        from manus_cli.cache import PromptCache
        
        # Test 1: Initialization
        with tempfile.TemporaryDirectory() as tmpdir:
            cache = PromptCache(cache_dir=Path(tmpdir), ttl=60)
            console.print("✅ Initialization successful")
            
            # Test 2: Set and get
            prompt = "Test prompt"
            params = {"model": "test", "temperature": 0.5}
            response = "Test response"
            
            cache.set(prompt, params, response)
            console.print("✅ Cache set working")
            
            cached = cache.get(prompt, params)
            assert cached == response
            console.print("✅ Cache get working")
            
            # Test 3: Cache miss
            cached = cache.get("different prompt", params)
            assert cached is None
            console.print("✅ Cache miss detection working")
            
            # Test 4: TTL expiration
            cache_short = PromptCache(cache_dir=Path(tmpdir) / "short", ttl=1)
            cache_short.set(prompt, params, response)
            time.sleep(2)
            cached = cache_short.get(prompt, params)
            assert cached is None
            console.print("✅ TTL expiration working")
            
            # Test 5: Clear cache
            cache.set(prompt, params, response)
            cache.clear()
            cached = cache.get(prompt, params)
            assert cached is None
            console.print("✅ Cache clearing working")
        
        console.print("[bold green]✅ Prompt Caching: ALL TESTS PASSED[/bold green]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Prompt Caching: FAILED[/bold red]")
        console.print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_context():
    """Test Conversation Context."""
    console.print("\n[bold cyan]Testing Conversation Context...[/bold cyan]")
    
    try:
        from manus_cli.context import ConversationContext, Message
        
        # Test 1: Initialization
        with tempfile.TemporaryDirectory() as tmpdir:
            context = ConversationContext(session_id="test_session", max_messages=5)
            context.context_dir = Path(tmpdir)
            console.print("✅ Initialization successful")
            
            # Test 2: Add messages
            context.add_message("user", "Hello")
            context.add_message("assistant", "Hi there!")
            assert len(context.messages) == 2
            console.print("✅ Message adding working")
            
            # Test 3: Get context
            ctx = context.get_context()
            assert len(ctx) == 2
            assert ctx[0]["role"] == "user"
            assert ctx[0]["content"] == "Hello"
            console.print("✅ Context retrieval working")
            
            # Test 4: Max messages limit
            for i in range(10):
                context.add_message("user", f"Message {i}")
            assert len(context.messages) <= 5
            console.print("✅ Max messages limit working")
            
            # Test 5: Save and load
            context2 = ConversationContext()
            context2.context_dir = Path(tmpdir)
            context2.load("test_session")
            assert len(context2.messages) > 0
            console.print("✅ Save/load working")
            
            # Test 6: List sessions
            sessions = context.list_sessions()
            assert "test_session" in sessions
            console.print("✅ Session listing working")
            
            # Test 7: Clear
            context.clear()
            assert len(context.messages) == 0
            console.print("✅ Context clearing working")
        
        console.print("[bold green]✅ Conversation Context: ALL TESTS PASSED[/bold green]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Conversation Context: FAILED[/bold red]")
        console.print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_evaluation():
    """Test Evaluation Framework."""
    console.print("\n[bold cyan]Testing Evaluation Framework...[/bold cyan]")
    
    try:
        from manus_cli.evaluation import EvaluationFramework, TestCase
        
        # Test 1: Initialization
        framework = EvaluationFramework()
        console.print("✅ Initialization successful")
        
        # Test 2: Add test cases
        framework.add_test(TestCase(
            name="Test 1",
            input="input1",
            expected_output="output1"
        ))
        framework.add_test(TestCase(
            name="Test 2",
            input="input2",
            validator=lambda x: "success" in x
        ))
        assert len(framework.test_cases) == 2
        console.print("✅ Test case adding working")
        
        # Test 3: Run tests
        def mock_executor(input_text):
            if input_text == "input1":
                return "output1"
            return "success result"
        
        results = framework.run_tests(mock_executor)
        assert len(results) == 2
        console.print("✅ Test execution working")
        
        # Test 4: Check results
        assert results[0].passed == True
        assert results[1].passed == True
        console.print("✅ Test validation working")
        
        # Test 5: Failed test
        framework2 = EvaluationFramework()
        framework2.add_test(TestCase(
            name="Failing test",
            input="test",
            expected_output="wrong"
        ))
        results2 = framework2.run_tests(lambda x: "correct")
        assert results2[0].passed == False
        console.print("✅ Failure detection working")
        
        console.print("[bold green]✅ Evaluation Framework: ALL TESTS PASSED[/bold green]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Evaluation Framework: FAILED[/bold red]")
        console.print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_monitoring():
    """Test Performance Monitoring."""
    console.print("\n[bold cyan]Testing Performance Monitoring...[/bold cyan]")
    
    try:
        from manus_cli.monitoring import PerformanceMonitor
        
        # Test 1: Initialization
        with tempfile.TemporaryDirectory() as tmpdir:
            monitor = PerformanceMonitor()
            monitor.metrics_dir = Path(tmpdir)
            console.print("✅ Initialization successful")
            
            # Test 2: Track operation
            monitor.start_operation("test_op")
            time.sleep(0.1)
            monitor.end_operation(tokens_used=100, success=True)
            assert len(monitor.metrics) == 1
            console.print("✅ Operation tracking working")
            
            # Test 3: Failed operation
            monitor.start_operation("failed_op")
            monitor.end_operation(tokens_used=50, success=False, error="Test error")
            assert len(monitor.metrics) == 2
            assert monitor.metrics[-1].success == False
            console.print("✅ Failure tracking working")
            
            # Test 4: Get stats
            stats = monitor.get_stats()
            assert "total_operations" in stats
            assert stats["total_operations"] == 2
            assert "success_rate" in stats
            console.print(f"  Stats: {stats['total_operations']} ops, {stats['success_rate']:.1f}% success")
            console.print("✅ Statistics computation working")
            
            # Test 5: Load metrics
            monitor2 = PerformanceMonitor()
            monitor2.metrics_dir = Path(tmpdir)
            loaded = monitor2.load_metrics(days=1)
            assert len(loaded) >= 2
            console.print("✅ Metrics loading working")
        
        console.print("[bold green]✅ Performance Monitoring: ALL TESTS PASSED[/bold green]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Performance Monitoring: FAILED[/bold red]")
        console.print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all v5.2 tests."""
    console.print(Panel.fit(
        "[bold cyan]Manus CLI v5.2 Feature Tests[/bold cyan]\n"
        "Testing: Cache, Context, Evaluation, Monitoring",
        border_style="cyan"
    ))
    
    results = {
        "Prompt Caching": test_cache(),
        "Conversation Context": test_context(),
        "Evaluation Framework": test_evaluation(),
        "Performance Monitoring": test_monitoring()
    }
    
    # Summary
    console.print("\n" + "="*60)
    console.print("[bold]Test Summary:[/bold]\n")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for name, result in results.items():
        status = "[green]✅ PASS[/green]" if result else "[red]❌ FAIL[/red]"
        console.print(f"  {name}: {status}")
    
    console.print(f"\n[bold]Total: {passed}/{total} tests passed[/bold]")
    
    if passed == total:
        console.print("\n[bold green]🎉 ALL v5.2 FEATURES WORKING CORRECTLY![/bold green]")
        return 0
    else:
        console.print("\n[bold red]⚠️  SOME TESTS FAILED - NEEDS FIXING[/bold red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
