# Manus CLI

A powerful command-line interface for interacting with Manus AI, inspired by Claude CLI. Built with Python and Typer.

## Features

- 🚀 **Fast and intuitive** - Simple commands to interact with Manus AI
- 💬 **Interactive chat mode** - Have conversations with Manus AI directly in your terminal
- 🔐 **Secure configuration** - API key stored securely in your home directory
- 🎨 **Beautiful output** - Rich formatting with colors and markdown support
- ⚡ **Multiple modes** - Support for different execution modes (speed, quality, etc.)
- 📦 **Easy installation** - Install via pip or from source

## Installation

### From PyPI (when published)

```bash
pip install manus-cli
```

### From Source

```bash
# Clone the repository
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Quick Install (One-liner)

```bash
pip install git+https://github.com/ehadsagency-ai/manus-cli.git
```

## Quick Start

### 1. Configure your API key

```bash
# Interactive configuration
manus configure

# Or provide the key directly
manus configure --api-key sk-your-api-key-here
```

Your API key will be securely stored in `~/.config/manus/config.json`.

Alternatively, you can set the `MANUS_API_KEY` environment variable:

```bash
export MANUS_API_KEY=sk-your-api-key-here
```

### 2. Start chatting

```bash
# Single message
manus chat "Hello, how are you?"

# Interactive chat session
manus chat --interactive

# Or simply
manus chat -i
```

## Usage

### Chat Commands

Send a single message:

```bash
manus chat "Write a Python function to calculate fibonacci numbers"
```

Start an interactive session:

```bash
manus chat --interactive
```

Use a specific mode:

```bash
manus chat "Explain quantum computing" --mode quality
```

### Interactive Mode Commands

When in interactive mode, you can use these commands:

- `/quit` or `/exit` - Exit the chat
- `/clear` - Clear the screen
- `/mode <mode>` - Change execution mode (e.g., `/mode quality`)

### Task Management

Create a task and get the task ID:

```bash
manus task "Analyze this data and create a report"
```

Check task status:

```bash
manus status <task-id>
```

### Configuration

View or update your configuration:

```bash
manus configure
```

### Version Information

```bash
manus --version
```

## Examples

### Example 1: Quick Question

```bash
$ manus chat "What is the capital of France?"
```

### Example 2: Interactive Session

```bash
$ manus chat -i

╭─────────────────────────────────────────────────╮
│ Manus AI - Interactive Chat                    │
│                                                  │
│ Type your messages and press Enter to send.    │
│ Commands:                                        │
│   /quit or /exit - Exit the chat                │
│   /clear - Clear the screen                     │
│   /mode <mode> - Change execution mode          │
╰─────────────────────────────────────────────────╯

You: Hello!
Manus: [Response from Manus AI]

You: /mode quality
Mode changed to: quality

You: Tell me about AI
Manus: [Detailed response in quality mode]

You: /quit
Goodbye!
```

### Example 3: Creating a Task

```bash
$ manus task "Write a blog post about machine learning" --mode quality

✓ Task created successfully!
Task ID: abc123def456
Status: pending
```

## Configuration

The CLI stores configuration in `~/.config/manus/config.json`:

```json
{
  "api_key": "sk-your-api-key-here"
}
```

The file is created with restrictive permissions (0600) to ensure security.

## Environment Variables

- `MANUS_API_KEY` - Your Manus API key (alternative to configuration file)

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dependencies
pip install -e .
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=manus_cli
```

### Project Structure

```
manus-cli/
├── manus_cli/
│   ├── __init__.py      # Package initialization
│   ├── __main__.py      # Entry point for module execution
│   ├── api.py           # Manus API client
│   └── cli.py           # CLI application (Typer)
├── setup.py             # Setup script
├── pyproject.toml       # Modern Python packaging
├── requirements.txt     # Dependencies
├── README.md            # This file
└── LICENSE              # MIT License
```

## API Reference

### ManusClient

The `ManusClient` class provides programmatic access to the Manus API:

```python
from manus_cli.api import ManusClient

# Initialize client
client = ManusClient(api_key="sk-your-api-key")

# Create a task
response = client.create_task(
    prompt="Hello, Manus!",
    mode="speed"
)

# Get task status
status = client.get_task_status(task_id="abc123")
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please visit:
- GitHub Issues: https://github.com/ehadsagency-ai/manus-cli/issues
- Documentation: https://github.com/ehadsagency-ai/manus-cli#readme

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) - The framework for building CLI applications
- Styled with [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- Inspired by Claude CLI and other modern CLI tools

---

Made with ❤️ by the Manus CLI Team
