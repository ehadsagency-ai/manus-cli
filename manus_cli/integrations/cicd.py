"""
CI/CD Integration
Generate CI/CD configurations for various platforms
"""

from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

console = Console()


class CICDIntegration:
    """CI/CD configuration generation"""
    
    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.cicd_dir = project_dir / ".github" / "workflows"
    
    def generate_github_actions(self, plan_content: str) -> Path:
        """
        Generate GitHub Actions workflow
        
        Returns:
            Path to generated workflow file
        """
        console.print(Panel(
            "[bold cyan]Generating CI/CD Configuration[/bold cyan]\n"
            "Creating GitHub Actions workflow...",
            border_style="cyan"
        ))
        
        # Create .github/workflows directory
        self.cicd_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract tech stack from plan
        tech_stack = self._extract_tech_stack(plan_content)
        
        # Generate workflow based on tech stack
        workflow = self._generate_workflow(tech_stack)
        
        # Save workflow file
        workflow_file = self.cicd_dir / "ci.yml"
        workflow_file.write_text(workflow)
        
        console.print(f"✓ GitHub Actions workflow created: [cyan]{workflow_file}[/cyan]")
        
        return workflow_file
    
    def generate_docker_compose(self, plan_content: str) -> Optional[Path]:
        """
        Generate Docker Compose configuration
        
        Returns:
            Path to docker-compose.yml if generated
        """
        # Extract services from plan
        services = self._extract_services(plan_content)
        
        if not services:
            return None
        
        # Generate docker-compose.yml
        compose_content = self._generate_docker_compose(services)
        
        # Save file
        compose_file = self.project_dir / "docker-compose.yml"
        compose_file.write_text(compose_content)
        
        console.print(f"✓ Docker Compose created: [cyan]{compose_file}[/cyan]")
        
        return compose_file
    
    def _extract_tech_stack(self, plan_content: str) -> Dict[str, str]:
        """Extract technology stack from plan"""
        tech_stack = {
            "language": "python",  # default
            "framework": "",
            "database": "",
            "test_framework": ""
        }
        
        content_lower = plan_content.lower()
        
        # Detect language
        if "python" in content_lower:
            tech_stack["language"] = "python"
        elif "node" in content_lower or "javascript" in content_lower or "typescript" in content_lower:
            tech_stack["language"] = "node"
        elif "java" in content_lower:
            tech_stack["language"] = "java"
        elif "go" in content_lower or "golang" in content_lower:
            tech_stack["language"] = "go"
        
        # Detect framework
        if "django" in content_lower:
            tech_stack["framework"] = "django"
        elif "flask" in content_lower:
            tech_stack["framework"] = "flask"
        elif "fastapi" in content_lower:
            tech_stack["framework"] = "fastapi"
        elif "express" in content_lower:
            tech_stack["framework"] = "express"
        elif "react" in content_lower:
            tech_stack["framework"] = "react"
        
        # Detect database
        if "postgres" in content_lower:
            tech_stack["database"] = "postgres"
        elif "mysql" in content_lower:
            tech_stack["database"] = "mysql"
        elif "mongodb" in content_lower:
            tech_stack["database"] = "mongodb"
        elif "redis" in content_lower:
            tech_stack["database"] = "redis"
        
        # Detect test framework
        if "pytest" in content_lower:
            tech_stack["test_framework"] = "pytest"
        elif "jest" in content_lower:
            tech_stack["test_framework"] = "jest"
        elif "mocha" in content_lower:
            tech_stack["test_framework"] = "mocha"
        
        return tech_stack
    
    def _generate_workflow(self, tech_stack: Dict[str, str]) -> str:
        """Generate GitHub Actions workflow YAML"""
        
        language = tech_stack["language"]
        
        if language == "python":
            return self._generate_python_workflow(tech_stack)
        elif language == "node":
            return self._generate_node_workflow(tech_stack)
        else:
            return self._generate_generic_workflow(tech_stack)
    
    def _generate_python_workflow(self, tech_stack: Dict[str, str]) -> str:
        """Generate Python-specific workflow"""
        test_cmd = "pytest" if tech_stack["test_framework"] == "pytest" else "python -m unittest"
        
        return f"""name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install {tech_stack["test_framework"] or "pytest"}
    
    - name: Run tests
      run: {test_cmd}
    
    - name: Run linter
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Docker image
      run: docker build -t app:latest .
    
    - name: Push to registry
      run: echo "Push to your container registry"
"""
    
    def _generate_node_workflow(self, tech_stack: Dict[str, str]) -> str:
        """Generate Node.js-specific workflow"""
        test_cmd = "npm test"
        
        return f"""name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Node.js
      uses: actions/setup-node@v3
      with:
        node-version: '18'
    
    - name: Install dependencies
      run: npm ci
    
    - name: Run tests
      run: {test_cmd}
    
    - name: Run linter
      run: npm run lint
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build
      run: npm run build
    
    - name: Build Docker image
      run: docker build -t app:latest .
"""
    
    def _generate_generic_workflow(self, tech_stack: Dict[str, str]) -> str:
        """Generate generic workflow"""
        return """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Run tests
      run: echo "Configure your test command"
  
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Build
      run: echo "Configure your build command"
"""
    
    def _extract_services(self, plan_content: str) -> List[str]:
        """Extract services from plan"""
        services = []
        
        content_lower = plan_content.lower()
        
        if "postgres" in content_lower:
            services.append("postgres")
        if "mysql" in content_lower:
            services.append("mysql")
        if "mongodb" in content_lower:
            services.append("mongodb")
        if "redis" in content_lower:
            services.append("redis")
        if "nginx" in content_lower:
            services.append("nginx")
        
        return services
    
    def _generate_docker_compose(self, services: List[str]) -> str:
        """Generate Docker Compose configuration"""
        compose = """version: '3.8'

services:
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
"""
        
        for service in services:
            compose += f"      - {service}\n"
        
        compose += "\n"
        
        # Add service definitions
        for service in services:
            if service == "postgres":
                compose += """  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: app_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

"""
            elif service == "mysql":
                compose += """  mysql:
    image: mysql:8
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: app_db
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

"""
            elif service == "mongodb":
                compose += """  mongodb:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

"""
            elif service == "redis":
                compose += """  redis:
    image: redis:7
    ports:
      - "6379:6379"

"""
            elif service == "nginx":
                compose += """  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf

"""
        
        # Add volumes
        compose += "\nvolumes:\n"
        if "postgres" in services:
            compose += "  postgres_data:\n"
        if "mysql" in services:
            compose += "  mysql_data:\n"
        if "mongodb" in services:
            compose += "  mongo_data:\n"
        
        return compose
