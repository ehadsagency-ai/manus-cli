"""Prompt Templates Library for Manus CLI v5.1"""
import os
from pathlib import Path
from typing import Dict, Optional
import re

class PromptTemplate:
    """Represents a reusable prompt template."""
    
    def __init__(self, name: str, content: str, variables: list[str]):
        self.name = name
        self.content = content
        self.variables = variables
    
    def render(self, **kwargs) -> str:
        """Renders template with provided variables."""
        result = self.content
        for var in self.variables:
            if var not in kwargs:
                raise ValueError(f"Missing variable: {var}")
            result = result.replace(f"{{{{{var}}}}}", str(kwargs[var]))
        return result

class TemplateLibrary:
    """Manages prompt templates."""
    
    BUILTIN_TEMPLATES = {
        "code_review": PromptTemplate(
            name="code_review",
            content="""Review this {{language}} code for:
- Code quality and best practices
- Potential bugs or issues
- Performance optimizations
- Security concerns

Code:
```{{language}}
{{code}}
```

Provide detailed feedback with specific recommendations.""",
            variables=["language", "code"]
        ),
        "explain_concept": PromptTemplate(
            name="explain_concept",
            content="""Explain {{concept}} in a way that a {{audience}} can understand.

Include:
- Simple definition
- Real-world analogy
- Practical example
- Common misconceptions

Keep it clear and concise.""",
            variables=["concept", "audience"]
        ),
        "debug_error": PromptTemplate(
            name="debug_error",
            content="""Help debug this error in {{language}}:

Error message:
```
{{error}}
```

Context:
{{context}}

Provide:
1. Root cause analysis
2. Step-by-step solution
3. Prevention tips""",
            variables=["language", "error", "context"]
        )
    }
    
    def __init__(self, custom_templates_dir: Optional[Path] = None):
        self.templates = self.BUILTIN_TEMPLATES.copy()
        if custom_templates_dir:
            self.load_custom_templates(custom_templates_dir)
    
    def get(self, name: str) -> Optional[PromptTemplate]:
        return self.templates.get(name)
    
    def list_templates(self) -> list[str]:
        return list(self.templates.keys())
    
    def load_custom_templates(self, directory: Path):
        """Loads custom templates from directory."""
        if not directory.exists():
            return
        for file in directory.glob("*.txt"):
            content = file.read_text()
            variables = re.findall(r'\{\{(\w+)\}\}', content)
            template = PromptTemplate(file.stem, content, variables)
            self.templates[file.stem] = template
