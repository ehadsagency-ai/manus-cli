# Manus CLI - Usage Examples

## Basic Commands

### 1. Simple Chat

Send a single message and get a response:

```bash
manus chat "What is the capital of France?"
```

### 2. Interactive Chat Session

Start a conversation with Manus AI:

```bash
manus chat --interactive
```

Or use the short form:

```bash
manus chat -i
```

### 3. Create a Task

Create a task and get the task ID for tracking:

```bash
manus task "Write a blog post about machine learning"
```

### 4. Check Task Status

Check the status of a previously created task:

```bash
manus status abc123def456
```

## Advanced Examples

### Different Execution Modes

Use quality mode for more detailed responses:

```bash
manus chat "Explain quantum computing in detail" --mode quality
```

Use speed mode (default) for faster responses:

```bash
manus chat "Quick summary of Python" --mode speed
```

### Programming Tasks

Ask for code examples:

```bash
manus chat "Write a Python function to calculate fibonacci numbers"
```

Request code review:

```bash
manus chat "Review this code: def add(a,b): return a+b"
```

### Data Analysis

Request data analysis:

```bash
manus task "Analyze sales data and create visualizations" --mode quality
```

### Writing Tasks

Generate content:

```bash
manus task "Write a professional email to a client about project delays"
```

Create documentation:

```bash
manus chat "Create API documentation for a REST endpoint"
```

## Interactive Mode Commands

When in interactive mode (`manus chat -i`), you can use these special commands:

### Exit the Chat

```
/quit
```

or

```
/exit
```

### Clear the Screen

```
/clear
```

### Change Execution Mode

```
/mode quality
```

or

```
/mode speed
```

## Example Interactive Session

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

You: Hello! Can you help me with Python?
Manus: [Response about Python help]

You: /mode quality
Mode changed to: quality

You: Explain decorators in Python
Manus: [Detailed explanation of Python decorators]

You: Thanks!
Manus: [Response]

You: /quit
Goodbye!
```

## Configuration Examples

### Configure API Key Interactively

```bash
manus configure
```

You'll be prompted to enter your API key securely.

### Configure API Key Directly

```bash
manus configure --api-key sk-your-api-key-here
```

### Using Environment Variables

Instead of configuring, you can set an environment variable:

**Linux/macOS:**
```bash
export MANUS_API_KEY=sk-your-api-key-here
manus chat "Hello!"
```

**Windows (PowerShell):**
```powershell
$env:MANUS_API_KEY="sk-your-api-key-here"
manus chat "Hello!"
```

**Windows (Command Prompt):**
```cmd
set MANUS_API_KEY=sk-your-api-key-here
manus chat "Hello!"
```

## Practical Use Cases

### 1. Quick Research

```bash
manus chat "What are the latest trends in AI for 2025?"
```

### 2. Code Generation

```bash
manus chat "Create a REST API endpoint in Flask for user authentication"
```

### 3. Learning

```bash
manus chat -i
You: I want to learn about Docker
Manus: [Explanation]
You: Can you give me an example Dockerfile?
Manus: [Example]
You: How do I run it?
Manus: [Instructions]
```

### 4. Problem Solving

```bash
manus chat "I'm getting a 'ModuleNotFoundError' in Python. How do I fix it?"
```

### 5. Content Creation

```bash
manus task "Write a LinkedIn post about the importance of code reviews in software development"
```

### 6. Translation

```bash
manus chat "Translate this to French: Hello, how are you doing today?"
```

### 7. Brainstorming

```bash
manus chat -i
You: I need ideas for a mobile app
Manus: [Ideas]
You: Tell me more about the fitness tracking idea
Manus: [Details]
You: What features should it have?
Manus: [Feature list]
```

## Tips and Best Practices

1. **Be Specific**: The more specific your prompt, the better the response
   ```bash
   # Less specific
   manus chat "Tell me about Python"
   
   # More specific
   manus chat "Explain Python list comprehensions with 3 practical examples"
   ```

2. **Use Interactive Mode for Conversations**: For back-and-forth discussions, use interactive mode
   ```bash
   manus chat -i
   ```

3. **Choose the Right Mode**: Use quality mode for complex tasks, speed mode for quick queries
   ```bash
   manus chat "Complex analysis task" --mode quality
   manus chat "Quick fact check" --mode speed
   ```

4. **Track Long-Running Tasks**: For complex tasks, use the task command to get a task ID
   ```bash
   manus task "Generate a comprehensive report on market trends"
   # Save the task ID and check status later
   manus status <task-id>
   ```

5. **Secure Your API Key**: Never share your API key or commit it to version control
   ```bash
   # Good: Use configuration
   manus configure --api-key sk-xxx
   
   # Good: Use environment variable
   export MANUS_API_KEY=sk-xxx
   
   # Bad: Don't hardcode in scripts
   ```
