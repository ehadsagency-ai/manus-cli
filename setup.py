"""
Setup script for Manus CLI
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="manus-cli",
    version="2.0.0",
    author="Manus CLI Team",
    author_email="support@manus.ai",
    description="A command-line interface for Manus AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ehadsagency-ai/manus-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "typer>=0.9.0",
        "requests>=2.31.0",
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "manus=manus_cli.cli_enhanced:run",
        ],
    },
    keywords="manus ai cli command-line interface",
    project_urls={
        "Bug Reports": "https://github.com/ehadsagency-ai/manus-cli/issues",
        "Source": "https://github.com/ehadsagency-ai/manus-cli",
    },
)
