# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
import time
import subprocess
import webbrowser
from models import AddInput, AddOutput, SqrtInput, SqrtOutput, StringsToIntsInput, StringsToIntsOutput, ExpSumInput, ExpSumOutput


# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(input: AddInput) -> AddOutput:
    """Add two numbers"""
    print("CALLED: add(AddInput) -> AddOutput")
    return AddOutput(result=input.a + input.b)

@mcp.tool()
def sqrt(input: SqrtInput) -> SqrtOutput:
    """Square root of a number"""
    print("CALLED: sqrt(SqrtInput) -> SqrtOutput")
    return SqrtOutput(result=input.a ** 0.5)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)


# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(input: StringsToIntsInput) -> StringsToIntsOutput:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(StringsToIntsInput) -> StringsToIntsOutput")
    ascii_values = [ord(char) for char in input.string]
    return StringsToIntsOutput(ascii_values=ascii_values)

@mcp.tool()
def int_list_to_exponential_sum(input: ExpSumInput) -> ExpSumOutput:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(ExpSumInput) -> ExpSumOutput")
    result = sum(math.exp(i) for i in input.int_list)
    return ExpSumOutput(result=result)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


@mcp.tool()
async def draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict:
    """Draw a rectangle in Excalidraw from (x1,y1) to (x2,y2)"""
    try:
        # AppleScript to activate rectangle tool in Excalidraw
        script = f"""
        tell application "System Events"
            tell application "Excalidraw" to activate
            delay 0.5
            keystroke "r" -- Rectangle tool
            delay 0.3
        end tell
        """
        subprocess.run(['osascript', '-e', script], check=True)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle tool activated. Click at ({x1},{y1}) and drag to ({x2},{y2})"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def add_text_in_excalidraw(text: str) -> dict:
    """Add text in Excalidraw"""
    try:
        sanitized_text = text.replace("\\", "\\\\").replace("\"", "\\\"")
        # AppleScript to add text in Excalidraw
        script = f"""
        tell application "System Events"
            tell application "Excalidraw" to activate
            delay 0.5
            click at {{400, 300}} -- focus canvas; adjust as needed
            keystroke "t" -- Text tool
            delay 0.3
            keystroke "{sanitized_text}" -- Type the text
            delay 0.2
            key code 53 -- Escape to exit text mode
        end tell
        """
        print("Result: ", subprocess.run(['osascript', '-e', script], check=True))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text '{text}' added to Excalidraw successfully"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }

def get_window_bounds(window_title: str) -> tuple[int, int, int, int] | None:
    """Get window bounds (left, top, width, height) using AppleScript on macOS"""
    try:
        script = f'''
        tell application "System Events"
            set frontApp to first application process whose frontmost is true
            tell frontApp
                set win to first window whose name contains "{window_title}"
                set winPos to position of win
                set winSize to size of win
                return (item 1 of winPos) & "," & (item 2 of winPos) & "," & (item 1 of winSize) & "," & (item 2 of winSize)
            end tell
        end tell
        '''
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            parts = result.stdout.strip().split(',')
            if len(parts) == 4:
                return tuple(int(p.strip()) for p in parts)
    except Exception:
        pass
    return None

@mcp.tool()
async def add_text_in_excalidraw_pyauto(
    text: str,
    x: int = 400,
    y: int = 300,
    interval: float = 0.02,
    window_title: str | None = "Excalidraw",
    window_offset_x: int = 0,
    window_offset_y: int = 0,
) -> dict:
    """Add text in Excalidraw via pyautogui (requires Accessibility permission)"""
    try:
        import pyautogui
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"pyautogui not available: {str(e)}. Install with 'pip install pyautogui pillow'."
                )
            ]
        }

    try:
        subprocess.run([
            'osascript',
            '-e', 'tell application "Excalidraw" to activate'
        ], check=False, timeout=3)
    except Exception:
        pass

    try:
        target_x, target_y = x, y
        if window_title:
            bounds = get_window_bounds(window_title)
            if bounds:
                print("Window bounds:", bounds)
                left, top, width, height = bounds
                target_x = left + width // 2 + window_offset_x
                target_y = top + height // 2 + window_offset_y

        pyautogui.FAILSAFE = False
        time.sleep(0.8)
        pyautogui.click(target_x, target_y)
        time.sleep(0.1)
        pyautogui.press("t")
        time.sleep(0.2)
        pyautogui.click(target_x, target_y)
        time.sleep(0.2)
        pyautogui.typewrite(text, interval=interval)
        pyautogui.press("esc")
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text '{text}' added via pyautogui at ({target_x},{target_y})."
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"pyautogui error: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def open_excalidraw() -> dict:
    """Open Excalidraw application on macOS"""
    try:
        # Try to open Excalidraw app if installed
        script = 'tell application "Excalidraw" to activate'
        try:
            subprocess.run(['osascript', '-e', script], check=True, timeout=5)
            time.sleep(1)
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Excalidraw opened successfully"
                    )
                ]
            }
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Excalidraw desktop app not found, open via web browser
            webbrowser.open('https://excalidraw.com')
            time.sleep(2)
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Excalidraw opened in browser at https://excalidraw.com"
                    )
                ]
            }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Excalidraw: {str(e)}"
                )
            ]
        }
# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING THE EXCALIDRAW MCP SERVER FOR MACOS")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
