
import sys
import os
from rich import print
from rich.console import Console
from rich.table import Table
import requests

from brain.groq import think

# Initialize console
console = Console()

# Define keywords to look for in log lines
keywords = ['error', 'critical', 'fatal', 'traceback', 'exception', 'panic', 'warn']

# Read last 50 lines from stdin
lines = sys.stdin.readlines()[-50:]

# Initialize variables to store error lines and context
error_lines = []
error_context = []

# Loop through each line to find error keywords
for i, line in enumerate(lines):
    for keyword in keywords:
        if keyword in line.lower():
            # If error keyword is found, store the line and its context
            error_lines.append((i, line.strip()))
            context = lines[max(0, i-10):i] + [line] + lines[i+1:min(len(lines), i+11)]
            error_context.append('\n'.join(context))

# If no error lines are found, print a success message
if not error_lines:
    console.print('[green]Everything is fine![/green]')
    sys.exit(0)

# Loop through each error line and its context
for i, (line_number, error_line) in enumerate(error_lines):
    context = error_context[i]
    # Call GROQ to get the reason and fix for the error
    prompt = f'Why did this error happen and how to fix it?\n{context}'
    response = think(prompt)
    # Parse the response to get the reason and fix
    reason = response.split('\n')[0]
    fix = '\n'.join(response.split('\n')[1:])
    # Print the error information and fix
    table = Table(title='Error Information')
    table.add_column('Line Number', style='cyan')
    table.add_column('Error Line', style='magenta')
    table.add_column('Reason', style='yellow')
    table.add_column('Fix', style='green')
    table.add_row(str(line_number), error_line, reason, fix)
    console.print(table)

