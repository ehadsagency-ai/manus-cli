# Manus CLI v2.0 🚀

A powerful, feature-rich command-line interface for interacting with Manus AI, inspired by Claude CLI and OpenAI best practices. Built with Python and Typer.

## ✨ What's New in v2.0

### 🎭 Professional Roles & System Prompts
Choose from 12 predefined professional roles to get specialized responses:
- **Developer** - Expert software development assistance
- **Data Scientist** - Advanced data analysis and insights
- **Writer** - Professional content creation
- **Teacher** - Patient, educational explanations
- And 8 more specialized roles!

### ⚡ Streaming Responses
Get real-time responses as they're generated - no more waiting for the complete response!

### 💾 Conversation History
Save, load, and manage your conversation history with persistent storage.

### 🛡️ Enhanced Error Handling
Automatic retries, rate limit handling, and clear error messages for a reliable experience.

### ⚙️ Advanced Configuration
Configure default mode, role, and streaming preferences for a personalized experience.

## Features

- 🚀 **Fast and intuitive** - Simple commands to interact with Manus AI
- 💬 **Interactive chat mode** - Have conversations with Manus AI directly in your terminal
- 🎭 **12 Professional roles** - Specialized AI personas for different tasks
- ⚡ **Streaming responses** - See responses in real-time
- 💾 **Conversation history** - Save and resume conversations
- 🔐 **Secure configuration** - API key stored securely in your home directory
- 🎨 **Beautiful output** - Rich formatting with colors and markdown support
- 🛡️ **Robust error handling** - Automatic retries and clear error messages
- 📦 **Easy installation** - Install via pip or from source

## Installation

### From GitHub (Recommended)

```bash
pip install git+https://github.com/ehadsagency-ai/manus-cli.git
```

### From Source

```bash
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli
pip install .
```

## Quick Start

### 1. Configure your API key and preferences

```bash
# Basic configuration
manus configure --api-key sk-your-api-key-here

# Advanced configuration with defaults
manus configure \
  --api-key sk-your-api-key-here \
  --mode speed \
  --role developer \
  --stream
```

### 2. Explore available roles

```bash
manus roles
```

### 3. Start chatting

```bash
# Quick question
manus chat "Explain quantum computing"

# With specific role
manus chat "Write a REST API" --role developer

# With streaming
manus chat "Tell me a story" --role writer --stream

# Interactive session
manus chat --interactive
```

## Usage

### Available Commands

| Command | Description |
|---------|-------------|
| `manus configure` | Configure API key and preferences |
| `manus roles` | List all available roles/personas |
| `manus chat <message>` | Send a message to Manus AI |
| `manus chat -i` | Start interactive chat session |
| `manus task <prompt>` | Create a new task |
| `manus status <task-id>` | Check task status |
| `manus history` | List saved conversations |
| `manus --version` | Show version information |

### Chat with Different Roles

```bash
# Get code help from a developer
manus chat "Debug this Python code" --role developer

# Get data insights from a data scientist
manus chat "Analyze this dataset" --role data-scientist

# Get writing help from a content writer
manus chat "Write a blog post intro" --role writer

# Get teaching from a patient teacher
manus chat "Explain machine learning" --role teacher
```

### Streaming Responses

```bash
# Enable streaming for a single message
manus chat "Write a long essay" --stream

# Disable streaming (use default from config)
manus chat "Quick question" --no-stream

# Toggle in interactive mode
manus chat -i
You: /stream  # Toggle streaming on/off
```

### Interactive Mode Commands

When in interactive mode (`manus chat -i`), you can use these commands:

| Command | Description |
|---------|-------------|
| `/quit` or `/exit` | Exit the chat |
| `/clear` | Clear the screen |
| `/mode <mode>` | Change execution mode |
| `/role <role>` | Switch to a different role |
| `/stream` | Toggle streaming on/off |
| `/save` | Save current conversation |
| `/history` | View conversation history |
| `/roles` | List available roles |
| `/help` | Show all commands |

### Example Interactive Session

```bash
$ manus chat -i

╭─────────────────────────────────────────────────╮
│ Manus AI - Interactive Chat                    │
│                                                  │
│ Current Role: Software Developer                │
│ Mode: speed                                      │
│ Streaming: Enabled                               │
│                                                  │
│ Commands:                                        │
│   /quit or /exit - Exit the chat                │
│   /role <role> - Change role/persona            │
│   /stream - Toggle streaming                     │
│   ... and more                                   │
╰─────────────────────────────────────────────────╯

You: Write a Python hello world function
Manus: Here's a simple hello world function in Python:

def hello_world():
    print("Hello, World!")

You: /role teacher
Role changed to: Patient Teacher

You: Explain what this function does
Manus: Great question! Let me break it down for you...

You: /save
Conversation saved: abc123...

You: /quit
Save conversation before exiting? [y/n]: y
Goodbye!
```

## Available Roles

| Role Key | Name | Best For |
|----------|------|----------|
| `assistant` | Helpful Assistant | General queries (default) |
| `developer` | Software Developer | Code, debugging, technical help |
| `data-scientist` | Data Scientist | Data analysis, statistics, ML |
| `writer` | Content Writer | Articles, blogs, creative writing |
| `teacher` | Patient Teacher | Learning, explanations, education |
| `analyst` | Business Analyst | Business strategy, market analysis |
| `researcher` | Research Assistant | Research, fact-finding, citations |
| `debugger` | Code Debugger | Finding and fixing code issues |
| `architect` | Software Architect | System design, architecture |
| `copywriter` | Marketing Copywriter | Marketing copy, persuasive text |
| `consultant` | Technical Consultant | Tech advice, recommendations |
| `reviewer` | Code Reviewer | Code review, best practices |

## Configuration

The CLI stores configuration in `~/.config/manus/config.json`:

```json
{
  "api_key": "sk-your-api-key-here",
  "default_mode": "speed",
  "default_role": "developer",
  "stream": true
}
```

Conversation history is stored in `~/.config/manus/history/`.

## Advanced Usage

### Custom Role in Single Command

```bash
manus chat "Analyze this code" \
  --role reviewer \
  --mode quality \
  --stream
```

### View Conversation History

```bash
manus history
```

Output:
```
╭─────────────────────────────────────────────────╮
│ Saved Conversations                             │
├─────────────┬──────────────────┬─────────────────┤
│ ID          │ Date             │ Messages        │
├─────────────┼──────────────────┼─────────────────┤
│ abc123...   │ 2025-12-14 10:30 │ 15              │
│ def456...   │ 2025-12-13 15:20 │ 8               │
└─────────────┴──────────────────┴─────────────────┘
```

### Error Handling

The CLI automatically handles:
- **Rate limits**: Retries with exponential backoff
- **Network errors**: Automatic retry mechanism
- **Timeouts**: Clear timeout messages
- **Invalid API keys**: Helpful configuration guidance

## Environment Variables

- `MANUS_API_KEY` - Your Manus API key (alternative to configuration file)

## Development

### Setup Development Environment

```bash
git clone https://github.com/ehadsagency-ai/manus-cli.git
cd manus-cli
pip install -e .
```

### Project Structure

```
manus-cli/
├── manus_cli/
│   ├── __init__.py           # Package initialization
│   ├── api_enhanced.py       # Enhanced API client with retry logic
│   ├── cli_enhanced.py       # Enhanced CLI with all features
│   ├── roles.py              # Role definitions and system prompts
│   ├── api.py                # Original API client (v1.0)
│   └── cli.py                # Original CLI (v1.0)
├── setup.py                  # Setup script
├── pyproject.toml            # Modern Python packaging
├── requirements.txt          # Dependencies
├── README.md                 # This file
├── CHANGELOG.md              # Version history
├── INSTALLATION.md           # Installation guide
├── EXAMPLES.md               # Usage examples
└── LICENSE                   # MIT License
```

## What's Different from v1.0?

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Roles/System Prompts | ❌ | ✅ 12 professional roles |
| Streaming | ❌ | ✅ Real-time responses |
| Conversation History | ❌ | ✅ Save/load/list |
| Error Handling | Basic | ✅ Retry with backoff |
| Configuration | API key only | ✅ Mode, role, streaming |
| Interactive Commands | 3 commands | ✅ 8+ commands |

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions, please visit:
- GitHub Issues: https://github.com/ehadsagency-ai/manus-cli/issues
- Documentation: https://github.com/ehadsagency-ai/manus-cli#readme

## Acknowledgments

- Built with [Typer](https://typer.tiangolo.com/) - The framework for building CLI applications
- Styled with [Rich](https://rich.readthedocs.io/) - Beautiful terminal output
- Inspired by Claude CLI and OpenAI best practices
- Enhanced based on research from Claude and OpenAI documentation

---

Made with ❤️ by the Manus CLI Team
