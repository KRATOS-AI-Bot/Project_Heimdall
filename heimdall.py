
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

# Define the think function to call GROQ
def think(prompt):
    try:
        client = requests.Session()
        client.headers.update({'Authorization': f'Bearer {GROK_API_KEY}'})
        completion = client.post('https://api.groq.com/v1/chat/completions', json={
            'model': 'llama-3.3-70b-versatile',
            'messages': [
                {'role': 'system', 'content': 'You are K.R.A.T.O.S., an elite DevOps Engineer. You write precise production-ready and secure code'},
                {'role': 'user', 'content': prompt}
            ],
            'temperature': 0.1,
            'stop': None,
            'stream': False
        })
        return completion.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

# Read log lines from stdin
log_lines = sys.stdin.readlines()[-50:]

# Initialize table
table = Table(title="Log Analysis")
table.add_column("Line", style="cyan")
table.add_column("Log", style="magenta")

# Initialize error lines
error_lines = []

# Iterate over log lines to detect errors
for i, line in enumerate(log_lines):
    if 'error' in line.lower():
        error_lines.append((i, line.strip()))

# If no errors detected, print everything's fine
if not error_lines:
    console.print("[green]Everything's fine[/green]")
    sys.exit(0)

# Iterate over error lines and call GROQ for each error
for error_line in error_lines:
    error_index, error_log = error_line
    context = '\n'.join(log_lines[max(0, error_index-10):error_index+11])
    prompt = f"Why did the following error happen and how to fix it?\n{context}"
    response = think(prompt)
    table.add_row(str(error_index), error_log)
    console.print(f"[red]Error detected at line {error_index}[/red]")
    console.print(f"[yellow]Summary: {error_log}[/yellow]")
    console.print(f"[blue]Response from GROQ: {response}[/blue]")

# Print table
console.print(table)
