
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

# Define keywords to look for in log lines
keywords = ['error', 'critical', 'fatal', 'traceback', 'exception', 'panic', 'warn']

# Read last 50 lines from stdin
lines = sys.stdin.readlines()[-50:]

# Initialize variables to store error lines and context
error_lines = []
context = []

# Loop through lines to find error lines and build context
for i, line in enumerate(lines):
    if any(keyword in line.lower() for keyword in keywords):
        error_lines.append((i, line.strip()))
        # Build context by adding 10 lines above and below error line
        start = max(0, i - 10)
        end = min(len(lines), i + 11)
        context.extend(lines[start:end])

# If no error lines found, print success message and exit
if not error_lines:
    console.print("[green]Everything's fine![/green]")
    sys.exit(0)

# Aggregate error lines and context into a single prompt
prompt = "Why did the following error occur and how can it be fixed?\n\n"
prompt += "\n".join(context)

# Define function to call GROK API
def think(prompt):
    try:
        completion = requests.post(
            "https://api.grok.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROK_API_KEY}"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are K.R.A.T.O.S., an elite DevOps Engineer. You write precise production-ready and secure code"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.1,
                "stop": None,
                "stream": False
            }
        ).json()
        return completion["choices"][0]["message"]["content"]
    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")
        sys.exit(1)

# Call GROK API and print response
response = think(prompt)
console.print("[yellow]Error detected![/yellow]")
console.print(f"[blue]Error lines: {', '.join(str(line[0]) for line in error_lines)}[/blue]")
console.print(f"[blue]Summary: {response.split('\n')[0]}[/blue]")
console.print(f"[green]How to fix: {response}[/green]")

# Create a table to display error information
table = Table(title="Error Information")
table.add_column("Line Number", style="cyan")
table.add_column("Error Message", style="magenta")
table.add_column("Summary", style="blue")
table.add_column("How to Fix", style="green")

# Add rows to the table
for line in error_lines:
    table.add_row(str(line[0]), line[1], response.split('\n')[0], response)

# Print the table
console.print(table)
