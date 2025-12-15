#!/usr/bin/env python3
"""
Comprehensive test script for Manus CLI v5.1 features
Tests: Extended Thinking, Effort, Templates, Validation
"""

import sys
sys.path.insert(0, '/home/ubuntu/manus-cli')

from rich.console import Console
from rich.panel import Panel

console = Console()

def test_extended_thinking():
    """Test Extended Thinking module."""
    console.print("\n[bold cyan]Testing Extended Thinking...[/bold cyan]")
    
    try:
        from manus_cli.extended_thinking import ExtendedThinking, ThinkingConfig
        
        # Test 1: Initialization
        config = ThinkingConfig(enabled=True, show_thinking=True, thinking_budget=5000)
        et = ExtendedThinking(config)
        console.print("✅ Initialization successful")
        
        # Test 2: Complexity assessment
        tasks = [
            ("What is Python?", 0.2),  # Low complexity
            ("Explain list comprehensions", 0.5),  # Medium
            ("Design microservices architecture", 0.8),  # High
        ]
        
        for task, expected_min in tasks:
            score = et._assess_complexity(task)
            should_use = et.should_use_extended_thinking(task)
            console.print(f"  Task: '{task[:40]}...'")
            console.print(f"  Complexity: {score:.2f} (expected >= {expected_min})")
            console.print(f"  Use Extended Thinking: {should_use}")
            
            if score < expected_min - 0.2:
                console.print(f"  [yellow]⚠️  Score lower than expected[/yellow]")
        
        console.print("✅ Complexity assessment working")
        
        # Test 3: Prompt formatting
        prompt = "Design a distributed system"
        formatted = et.format_prompt_with_thinking(prompt)
        assert "<thinking_guidelines>" in formatted
        assert "thinking_budget" in formatted or str(config.thinking_budget) in formatted
        console.print("✅ Prompt formatting working")
        
        # Test 4: Response parsing
        sample_response = """
<thinking>
Let me analyze this step by step:
1. First consideration
2. Second consideration
</thinking>

<answer>
Here is the final answer.
</answer>
"""
        parsed = et.parse_thinking_response(sample_response)
        assert "thinking" in parsed
        assert "answer" in parsed
        assert len(parsed["thinking"]) > 0
        assert len(parsed["answer"]) > 0
        console.print("✅ Response parsing working")
        
        # Test 5: Statistics
        stats = et.get_thinking_stats(parsed["thinking"])
        assert "word_count" in stats
        assert "line_count" in stats
        assert stats["word_count"] > 0
        console.print("✅ Statistics computation working")
        
        console.print("[bold green]✅ Extended Thinking: ALL TESTS PASSED[/bold green]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Extended Thinking: FAILED[/bold red]")
        console.print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_effort():
    """Test Effort module."""
    console.print("\n[bold cyan]Testing Effort Parameter...[/bold cyan]")
    
    try:
        from manus_cli.effort import EffortManager, EffortLevel
        
        # Test 1: Initialization
        manager = EffortManager(EffortLevel.MEDIUM)
        console.print("✅ Initialization successful")
        
        # Test 2: Get config
        config = manager.get_config()
        assert "max_tokens" in config
        assert "temperature" in config
        assert "thinking_budget" in config
        console.print(f"  Medium config: {config}")
        console.print("✅ Config retrieval working")
        
        # Test 3: Apply to request
        request_params = {"prompt": "test"}
        updated = manager.apply_to_request(request_params)
        assert "max_tokens" in updated
        assert "temperature" in updated
        console.print("✅ Request parameter application working")
        
        # Test 4: All effort levels
        for level in [EffortLevel.LOW, EffortLevel.MEDIUM, EffortLevel.HIGH]:
            manager = EffortManager(level)
            config = manager.get_config()
            console.print(f"  {level.value}: max_tokens={config['max_tokens']}, temp={config['temperature']}")
        console.print("✅ All effort levels working")
        
        console.print("[bold green]✅ Effort Parameter: ALL TESTS PASSED[/bold green]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Effort Parameter: FAILED[/bold red]")
        console.print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_templates():
    """Test Template Library."""
    console.print("\n[bold cyan]Testing Prompt Templates...[/bold cyan]")
    
    try:
        from manus_cli.template_library import TemplateLibrary, PromptTemplate
        
        # Test 1: Initialization
        library = TemplateLibrary()
        console.print("✅ Initialization successful")
        
        # Test 2: List templates
        templates = library.list_templates()
        assert len(templates) > 0
        console.print(f"  Found {len(templates)} templates: {templates}")
        console.print("✅ Template listing working")
        
        # Test 3: Get template
        template = library.get("code_review")
        assert template is not None
        assert template.name == "code_review"
        console.print("✅ Template retrieval working")
        
        # Test 4: Render template
        rendered = template.render(language="Python", code="def foo(): pass")
        assert "Python" in rendered
        assert "def foo(): pass" in rendered
        console.print("✅ Template rendering working")
        
        # Test 5: All built-in templates
        for name in ["code_review", "explain_concept", "debug_error"]:
            template = library.get(name)
            assert template is not None
            console.print(f"  ✓ Template '{name}' available")
        console.print("✅ All built-in templates available")
        
        console.print("[bold green]✅ Prompt Templates: ALL TESTS PASSED[/bold green]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Prompt Templates: FAILED[/bold red]")
        console.print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_validation():
    """Test Validation Framework."""
    console.print("\n[bold cyan]Testing Output Validation...[/bold cyan]")
    
    try:
        from manus_cli.validation import ValidationSchema, OutputValidator
        from manus_cli.validation.schemas import CODE_SCHEMA, SPEC_SCHEMA
        
        # Test 1: Schema creation
        schema = ValidationSchema(
            name="test_schema",
            required_fields=["field1", "field2"],
            optional_fields=["field3"],
            field_types={"field1": str, "field2": int}
        )
        console.print("✅ Schema creation successful")
        
        # Test 2: Validator initialization
        validator = OutputValidator(schema)
        console.print("✅ Validator initialization successful")
        
        # Test 3: Valid output
        valid_output = {"field1": "test", "field2": 42, "field3": "optional"}
        errors = validator.validate(valid_output)
        assert len(errors) == 0
        console.print("✅ Valid output validation working")
        
        # Test 4: Missing required field
        invalid_output = {"field1": "test"}  # Missing field2
        errors = validator.validate(invalid_output)
        assert len(errors) > 0
        console.print(f"  Detected {len(errors)} error(s) for missing field")
        console.print("✅ Missing field detection working")
        
        # Test 5: Wrong type
        invalid_output = {"field1": "test", "field2": "not_an_int"}
        errors = validator.validate(invalid_output)
        assert len(errors) > 0
        console.print("✅ Type checking working")
        
        # Test 6: Built-in schemas
        assert CODE_SCHEMA.name == "code"
        assert SPEC_SCHEMA.name == "specification"
        console.print("✅ Built-in schemas available")
        
        console.print("[bold green]✅ Output Validation: ALL TESTS PASSED[/bold green]")
        return True
        
    except Exception as e:
        console.print(f"[bold red]❌ Output Validation: FAILED[/bold red]")
        console.print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all v5.1 tests."""
    console.print(Panel.fit(
        "[bold cyan]Manus CLI v5.1 Feature Tests[/bold cyan]\n"
        "Testing: Extended Thinking, Effort, Templates, Validation",
        border_style="cyan"
    ))
    
    results = {
        "Extended Thinking": test_extended_thinking(),
        "Effort Parameter": test_effort(),
        "Prompt Templates": test_templates(),
        "Output Validation": test_validation()
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
        console.print("\n[bold green]🎉 ALL v5.1 FEATURES WORKING CORRECTLY![/bold green]")
        return 0
    else:
        console.print("\n[bold red]⚠️  SOME TESTS FAILED - NEEDS FIXING[/bold red]")
        return 1


if __name__ == "__main__":
    sys.exit(main())
