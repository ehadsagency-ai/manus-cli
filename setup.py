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
    version="5.5.6",
    author="Manus CLI Team",
    author_email="support@manus.ai",
    description="A command-line interface for Manus AI with Spec-Driven Development for rigorous thinking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ehadsagency-ai/manus-cli",
    packages=find_packages(),
    package_data={
        'manus_cli': ['templates/*.md'],
    },
    include_package_data=True,
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
        "urllib3>=1.26.0,<2.0.0",  # Pin to v1.x for macOS compatibility
    ],
    entry_points={
        "console_scripts": [
            "manus=manus_cli.cli_v4:main",
        ],
    },
    keywords="manus ai cli command-line interface",
    project_urls={
        "Bug Reports": "https://github.com/ehadsagency-ai/manus-cli/issues",
        "Source": "https://github.com/ehadsagency-ai/manus-cli",
    },
)
