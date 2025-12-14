# Manus CLI - Installation Guide

## Quick Installation

### Method 1: Install from GitHub (Recommended)

```bash
pip install git+https://github.com/ehadsagency-ai/manus-cli.git
```

### Method 2: Clone and Install

```bash
# Clone the repository
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli

# Install
pip install .
```

### Method 3: Development Installation

If you want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli

# Install in development mode
pip install -e .
```

## Verify Installation

After installation, verify that the `manus` command is available:

```bash
manus --version
```

You should see:
```
Manus CLI version 1.0.0
```

## Configuration

Configure your API key:

```bash
manus configure --api-key sk-your-api-key-here
```

Or set it as an environment variable:

```bash
export MANUS_API_KEY=sk-your-api-key-here
```

## First Steps

Try your first command:

```bash
manus chat "Hello, Manus!"
```

Or start an interactive session:

```bash
manus chat --interactive
```

## Troubleshooting

### Command not found

If you get a "command not found" error, make sure your Python scripts directory is in your PATH:

**Linux/macOS:**
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Windows:**
Add `%APPDATA%\Python\Scripts` to your PATH environment variable.

### Permission Denied

If you encounter permission errors during installation, try:

```bash
pip install --user git+https://github.com/ehadsagency-ai/manus-cli.git
```

### API Key Issues

If you get an API key error:
1. Make sure you've configured your API key using `manus configure`
2. Or set the `MANUS_API_KEY` environment variable
3. Check that your API key is valid and active

## Updating

To update to the latest version:

```bash
pip install --upgrade git+https://github.com/ehadsagency-ai/manus-cli.git
```

## Uninstallation

To remove Manus CLI:

```bash
pip uninstall manus-cli
```

Your configuration file will remain at `~/.config/manus/config.json` and can be deleted manually if desired.
