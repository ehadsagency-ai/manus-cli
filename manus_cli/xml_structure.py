"""
XML-Structured Prompts module for Manus CLI v5.0

Implements XML-based prompt structuring for reliable, parseable output.
Separates data, instructions, and context for better model understanding.

Based on Claude documentation analysis.
"""

import re
import xml.etree.ElementTree as ET
from typing import Dict, List, Tuple, Optional, Any
from rich.console import Console

console = Console()


class XMLStructuredPrompt:
    """Manages XML-structured prompts for reliable parsing."""
    
    @staticmethod
    def build_prompt(
        role: str,
        context: str,
        data: str,
        instructions: List[str],
        output_schema: Dict[str, str]
    ) -> str:
        """
        Builds an XML-structured prompt.
        
        Args:
            role: System role description
            context: Contextual information
            data: Input data to process
            instructions: List of step-by-step instructions
            output_schema: Expected output structure {tag: description}
        
        Returns:
            Complete XML-structured prompt
        """
        # Format instructions as numbered list
        instructions_xml = "\n".join(
            f"{i+1}. {inst}" 
            for i, inst in enumerate(instructions)
        )
        
        # Format output schema
        output_schema_xml = "\n".join(
            f"  <{tag}>{desc}</{tag}>" 
            for tag, desc in output_schema.items()
        )
        
        prompt = f"""
<role>
{role}
</role>

<context>
{context}
</context>

<data>
{data}
</data>

<instructions>
{instructions_xml}
</instructions>

<output_format>
Please structure your response using these XML tags:
{output_schema_xml}

Ensure all tags are properly closed and content is well-formed.
</output_format>
"""
        return prompt.strip()
    
    @staticmethod
    def build_simple_prompt(
        instructions: str,
        data: str,
        output_tags: List[str]
    ) -> str:
        """
        Builds a simple XML-structured prompt.
        
        Args:
            instructions: Task instructions
            data: Input data
            output_tags: List of expected output tags
        
        Returns:
            Simple XML-structured prompt
        """
        output_format = "\n".join(f"<{tag}>...</{tag}>" for tag in output_tags)
        
        prompt = f"""
<instructions>
{instructions}
</instructions>

<data>
{data}
</data>

<output_format>
{output_format}
</output_format>
"""
        return prompt.strip()
    
    @staticmethod
    def parse_output(
        xml_output: str, 
        expected_tags: List[str]
    ) -> Dict[str, Optional[str]]:
        """
        Parses XML-structured output from the model.
        
        Args:
            xml_output: Raw model output
            expected_tags: List of tags to extract
        
        Returns:
            Dictionary mapping tag names to content
        """
        result = {}
        
        for tag in expected_tags:
            # Use regex to extract content between tags
            pattern = rf"<{tag}>(.*?)</{tag}>"
            match = re.search(pattern, xml_output, re.DOTALL | re.IGNORECASE)
            
            if match:
                result[tag] = match.group(1).strip()
            else:
                result[tag] = None
        
        return result
    
    @staticmethod
    def validate_output(
        parsed: Dict[str, Optional[str]], 
        required_tags: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Validates that all required tags are present.
        
        Args:
            parsed: Parsed output dictionary
            required_tags: List of required tag names
        
        Returns:
            Tuple of (is_valid, missing_tags)
        """
        missing = [
            tag for tag in required_tags 
            if not parsed.get(tag)
        ]
        
        return len(missing) == 0, missing
    
    @staticmethod
    def extract_nested_tags(
        xml_output: str,
        parent_tag: str,
        child_tags: List[str]
    ) -> List[Dict[str, str]]:
        """
        Extracts nested XML structures.
        
        Args:
            xml_output: Raw model output
            parent_tag: Parent container tag
            child_tags: List of child tags to extract
        
        Returns:
            List of dictionaries, one per parent tag instance
        """
        results = []
        
        # Find all parent tag instances
        parent_pattern = rf"<{parent_tag}>(.*?)</{parent_tag}>"
        parent_matches = re.finditer(parent_pattern, xml_output, re.DOTALL | re.IGNORECASE)
        
        for parent_match in parent_matches:
            parent_content = parent_match.group(1)
            item = {}
            
            # Extract child tags
            for child_tag in child_tags:
                child_pattern = rf"<{child_tag}>(.*?)</{child_tag}>"
                child_match = re.search(child_pattern, parent_content, re.DOTALL | re.IGNORECASE)
                
                if child_match:
                    item[child_tag] = child_match.group(1).strip()
                else:
                    item[child_tag] = None
            
            results.append(item)
        
        return results


class XMLPromptBuilder:
    """Helper class for building complex XML prompts."""
    
    def __init__(self):
        self.role = ""
        self.context = ""
        self.data = ""
        self.instructions = []
        self.output_schema = {}
    
    def set_role(self, role: str) -> 'XMLPromptBuilder':
        """Sets the role."""
        self.role = role
        return self
    
    def set_context(self, context: str) -> 'XMLPromptBuilder':
        """Sets the context."""
        self.context = context
        return self
    
    def set_data(self, data: str) -> 'XMLPromptBuilder':
        """Sets the data."""
        self.data = data
        return self
    
    def add_instruction(self, instruction: str) -> 'XMLPromptBuilder':
        """Adds an instruction."""
        self.instructions.append(instruction)
        return self
    
    def add_output_tag(self, tag: str, description: str) -> 'XMLPromptBuilder':
        """Adds an output tag to the schema."""
        self.output_schema[tag] = description
        return self
    
    def build(self) -> str:
        """Builds the final prompt."""
        return XMLStructuredPrompt.build_prompt(
            role=self.role,
            context=self.context,
            data=self.data,
            instructions=self.instructions,
            output_schema=self.output_schema
        )


# Example usage
if __name__ == "__main__":
    # Example 1: Simple prompt
    simple_prompt = XMLStructuredPrompt.build_simple_prompt(
        instructions="Analyze this customer feedback and categorize the issues.",
        data="The new dashboard is slow and confusing. Fix it ASAP!",
        output_tags=["category", "sentiment", "priority"]
    )
    
    print("Simple Prompt:")
    print(simple_prompt)
    print("\n" + "="*80 + "\n")
    
    # Example 2: Complex prompt with builder
    complex_prompt = (
        XMLPromptBuilder()
        .set_role("You are a technical specification writer following spec-driven development.")
        .set_context("Project: Real-time chat application")
        .set_data("Build a user authentication system with OAuth and 2FA")
        .add_instruction("Analyze the request and extract key requirements")
        .add_instruction("Identify user stories and acceptance criteria")
        .add_instruction("Define functional and non-functional requirements")
        .add_instruction("Focus on WHAT, not HOW")
        .add_output_tag("feature_name", "Short, descriptive feature name")
        .add_output_tag("user_stories", "List of user stories")
        .add_output_tag("requirements", "Functional and non-functional requirements")
        .add_output_tag("acceptance_criteria", "Testable acceptance criteria")
        .build()
    )
    
    print("Complex Prompt:")
    print(complex_prompt)
    print("\n" + "="*80 + "\n")
    
    # Example 3: Parsing output
    simulated_output = """
<feature_name>User Authentication with OAuth and 2FA</feature_name>

<user_stories>
1. As a new user, I want to sign up with OAuth so that I can use my existing accounts
2. As a user, I want to enable 2FA so that my account is more secure
3. As a user, I want to log in with my credentials so that I can access the app
</user_stories>

<requirements>
Functional:
- OAuth 2.0 support (Google, GitHub, Microsoft)
- TOTP-based 2FA
- Email/password fallback
- Session management with JWT

Non-Functional:
- Login response time: <500ms
- 99.9% uptime
- GDPR compliant
</requirements>

<acceptance_criteria>
- [ ] User can sign up with OAuth provider
- [ ] User can enable 2FA
- [ ] User can log in with 2FA
- [ ] Sessions expire after 24 hours
</acceptance_criteria>
"""
    
    # Parse
    parsed = XMLStructuredPrompt.parse_output(
        simulated_output,
        expected_tags=["feature_name", "user_stories", "requirements", "acceptance_criteria"]
    )
    
    print("Parsed Output:")
    for tag, content in parsed.items():
        print(f"\n{tag}:")
        print(content if content else "[MISSING]")
    
    # Validate
    is_valid, missing = XMLStructuredPrompt.validate_output(
        parsed,
        required_tags=["feature_name", "user_stories", "requirements"]
    )
    
    print(f"\n\nValidation: {'✅ Valid' if is_valid else '❌ Invalid'}")
    if missing:
        print(f"Missing tags: {missing}")
