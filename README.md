
import sys
import os
from rich import print
from rich.console import Console
from rich.table import Table
import requests

# Load GROK API key from .env file
GROK_API_KEY = os.getenv('GROK_API_KEY')

# Initialize console
console = Console()

# Define think function to call GROQ API
def think(prompt):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are K.R.A.T.O.S., an elite DevOps Engineer. You write precise production-ready and secure code"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            stop=None,
            stream=False
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

# Read last 50 lines from stdin
lines = sys.stdin.readlines()[-50:]

# Initialize error lines and context
error_lines = []
context = []

# Check each line for keywords
for i, line in enumerate(lines):
    if any(keyword in line.lower() for keyword in ['error', 'critical', 'fatal', 'traceback', 'exception', 'panic', 'warn']):
        error_lines.append((i, line.strip()))
        # Get 10 lines above and below the error line
        start = max(0, i-10)
        end = min(len(lines), i+11)
        context.append(''.join(lines[start:end]))

# If no errors found, print success message
if not error_lines:
    console.print("[green]Everything's fine![/green]")
    sys.exit(0)

# Create table to display error information
table = Table(title="Error Information")
table.add_column("Line Number", style="cyan")
table.add_column("Error Message", style="magenta")
table.add_column("Summary", style="yellow")
table.add_column("Fix", style="green")

# Call GROQ API for each error context and print results
for i, (line_number, error_line) in enumerate(error_lines):
    prompt = f"Why did this happen? {context[i]}\nHow to fix it?"
    response = think(prompt)
    table.add_row(str(line_number), error_line, "Error detected", response)

# Print table
console.print(table)



# README.md
Heimdall is an AI-powered error detection and prevention tool that uses natural language processing to identify and remediate errors in log files. It is designed to help DevOps engineers and developers quickly identify and fix issues, reducing downtime and improving overall system reliability.

## Features

*   **AI Error Detection**: Heimdall uses a machine learning model to analyze log files and identify potential errors.
*   **Auto Remediation**: Once an error is detected, Heimdall uses a natural language processing model to generate a fix for the issue.
*   **Error Prevention**: Heimdall can be used to analyze log files before errors occur, helping to prevent issues from arising in the first place.

## How it Works

1.  **Log File Analysis**: Heimdall reads log files and analyzes them for potential errors.
2.  **Error Detection**: Heimdall uses a machine learning model to identify potential errors in the log files.
3.  **Context Generation**: Once an error is detected, Heimdall generates a context for the error, including the error message and surrounding log lines.
4.  **GROQ API Call**: Heimdall calls the GROQ API with the context and asks for a fix.
5.  **Fix Generation**: The GROQ API generates a fix for the issue and returns it to Heimdall.
6.  **Fix Display**: Heimdall displays the fix to the user, along with information about the error and the context in which it occurred.

## Why it's Worth it

*   **Reduced Downtime**: Heimdall helps to quickly identify and fix issues, reducing downtime and improving overall system reliability.
*   **Improved Productivity**: By automating error detection and remediation, Heimdall frees up DevOps engineers and developers to focus on more strategic tasks.
*   **Improved Accuracy**: Heimdall's machine learning model and natural language processing capabilities help to improve the accuracy of error detection and remediation.