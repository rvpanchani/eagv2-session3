# Talk2MCP - AI Agent with MCP Tools & Excalidraw Integration

An AI agent that uses Gemini to solve problems iteratively by calling MCP (Model Context Protocol) tools, with the ability to display final results in Excalidraw.

![Demo](excalidraw-mcp.gif)

## Overview

This project demonstrates:
- **MCP Server** (`example2.py`) - Exposes mathematical tools and Excalidraw integration via the Model Context Protocol
- **AI Agent** (`talk2mcp2.py`) - Uses Gemini to reason through problems, call tools, and output results to Excalidraw

## Features

- 🧮 Mathematical tools (add, subtract, multiply, divide, power, sqrt, factorial, log, trig functions)
- 🔤 String to ASCII conversion
- 📊 Exponential sum calculations
- 🎨 Excalidraw integration for visual output (macOS)

## Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) - Fast Python package manager
- macOS (for Excalidraw integration)
- [Excalidraw Desktop App](https://excalidraw.com/) (optional - falls back to browser)
- Gemini API Key

## Installation

1. **Clone the repository**

2. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies using uv**
   ```bash
   uv sync
   ```
   
   This will automatically create a virtual environment and install all dependencies defined in `pyproject.toml`.

4. **Set up environment variables**
   
   Create a `.env` file in the project root:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   
   # Optional: Customize Excalidraw text positioning
   TEXT_CLICK_X=800
   TEXT_CLICK_Y=500
   TEXT_KEY_INTERVAL=0.02
   TEXT_CLICK_WINDOW_TITLE=Excalidraw
   TEXT_CLICK_WINDOW_OFFSET_X=0
   TEXT_CLICK_WINDOW_OFFSET_Y=0
   ```

## Usage

### Running the AI Agent

```bash
uv run python talk2mcp2.py
```

This will:
1. Start the MCP server with available tools
2. Send a query to Gemini (default: "Find ASCII values of INDIA and return sum of exponentials")
3. Iteratively call tools based on Gemini's reasoning
4. Display the final answer in Excalidraw

### Running the MCP Server Standalone

```bash
uv run python example2.py
```

Or with the MCP dev server:
```bash
uv run python example2.py dev
```

### Inspecting MCP Tools

```bash
uv run python mcp_inspector.py
```

### Adding New Dependencies

```bash
uv add <package-name>
```

## Available MCP Tools

| Tool | Description |
|------|-------------|
| `add` | Add two numbers |
| `subtract` | Subtract two numbers |
| `multiply` | Multiply two numbers |
| `divide` | Divide two numbers |
| `power` | Raise a number to a power |
| `sqrt` | Square root |
| `cbrt` | Cube root |
| `factorial` | Factorial of a number |
| `log` | Natural logarithm |
| `sin`, `cos`, `tan` | Trigonometric functions |
| `strings_to_chars_to_int` | Convert string to ASCII values |
| `int_list_to_exponential_sum` | Sum of exponentials of a list |
| `fibonacci_numbers` | Generate Fibonacci sequence |
| `open_excalidraw` | Open Excalidraw app |
| `add_text_in_excalidraw` | Add text to Excalidraw canvas |

## How It Works

1. **Tool Discovery**: The agent connects to the MCP server and retrieves available tools
2. **Query Processing**: Gemini receives the query with tool descriptions
3. **Iterative Execution**: The agent calls tools as directed by Gemini (max 3 iterations)
4. **Result Display**: Final answer is displayed in Excalidraw

## Example Query

Default query: *"Find the ASCII values of characters in INDIA and then return sum of exponentials of those values."*

The agent will:
1. Call `strings_to_chars_to_int` → `[73, 78, 68, 73, 65]`
2. Call `int_list_to_exponential_sum` → `2.66e33`
3. Display result in Excalidraw

## Project Structure

```
├── talk2mcp2.py      # Main AI agent
├── example2.py       # MCP server with tools
├── models.py         # Pydantic models for tool I/O
├── mcp_inspector.py  # Tool inspection utility
├── pyproject.toml    # Project config & dependencies (uv)
├── uv.lock           # Locked dependency versions
└── .env              # Environment variables (create this)
```

## License

MIT
