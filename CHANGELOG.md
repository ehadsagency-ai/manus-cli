# Changelog

All notable changes to Manus CLI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-14

### Added

#### Major Features
- **Streaming Responses**: Real-time response streaming for better user experience
  - Enable with `--stream` flag or configure as default
  - See responses as they're generated
  - Toggle in interactive mode with `/stream` command

- **System Prompts & Roles**: 12 predefined professional roles
  - `assistant` - Helpful Assistant (default)
  - `developer` - Software Developer
  - `data-scientist` - Data Scientist
  - `writer` - Content Writer
  - `teacher` - Patient Teacher
  - `analyst` - Business Analyst
  - `researcher` - Research Assistant
  - `debugger` - Code Debugger
  - `architect` - Software Architect
  - `copywriter` - Marketing Copywriter
  - `consultant` - Technical Consultant
  - `reviewer` - Code Reviewer
  - Use with `--role <role>` flag or `/role <role>` in interactive mode
  - View all roles with `manus roles` command

- **Conversation History Management**
  - Automatic conversation saving in interactive mode
  - List conversations with `manus history` command
  - Save/load conversations with `/save` and `/load` commands
  - Persistent storage in `~/.config/manus/history/`

- **Enhanced Error Handling**
  - Automatic retry with exponential backoff for failed requests
  - Rate limit detection and handling
  - Clear, actionable error messages
  - Network error recovery
  - Timeout handling

- **Advanced Configuration System**
  - Configure default mode: `--mode <speed|quality>`
  - Configure default role: `--role <role>`
  - Configure streaming preference: `--stream/--no-stream`
  - View current configuration after saving
  - All settings persist in `~/.config/manus/config.json`

#### New Commands
- `manus roles` - List all available roles/personas
- `manus history` - View saved conversation history
- Enhanced `manus configure` with more options

#### Interactive Mode Enhancements
- `/role <role>` - Switch role/persona
- `/stream` - Toggle streaming on/off
- `/save` - Save current conversation
- `/history` - View conversation history
- `/roles` - List available roles
- `/help` - Show all available commands
- Improved status display showing current role, mode, and streaming state
- Better command handling and error messages

### Changed
- Updated to version 2.0.0
- Enhanced API client with retry logic and better error handling
- Improved terminal output with Rich library enhancements
- Better configuration management with more options
- More informative status messages and progress indicators

### Technical Improvements
- New `api_enhanced.py` module with advanced features
- New `roles.py` module for role management
- New `cli_enhanced.py` with all new commands and features
- Exponential backoff retry mechanism
- Conversation persistence system
- Better separation of concerns in code architecture

### Documentation
- Updated README with new features
- Added comprehensive CHANGELOG
- Enhanced EXAMPLES with new features
- Updated INSTALLATION guide

## [1.0.0] - 2025-12-14

### Added
- Initial release of Manus CLI
- Basic chat functionality
- Task creation and status checking
- API key configuration
- Interactive chat mode
- Multiple execution modes (speed, quality)
- Rich terminal formatting
- Typer-based CLI framework

### Features
- `manus configure` - Configure API key
- `manus chat` - Send messages to Manus AI
- `manus task` - Create tasks
- `manus status` - Check task status
- Interactive mode with `/quit`, `/clear`, `/mode` commands
- Beautiful terminal output with colors and panels
- Secure API key storage

[2.0.0]: https://github.com/ehadsagency-ai/manus-cli/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/ehadsagency-ai/manus-cli/releases/tag/v1.0.0
