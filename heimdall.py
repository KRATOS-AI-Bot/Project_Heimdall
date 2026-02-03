
from brain.groq import think
import sys
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import json

console = Console()

def read_logs():
    logs = sys.stdin.readlines()
    if not logs:
        print("[red]Please provide log input[/red]")
        sys.exit(1)
    return logs[-50:]

def scan_logs(logs):
    keywords = ['error', 'critical', 'fatal', 'traceback', 'exception', 'panic', 'warn']
    indices = []
    for i, log in enumerate(logs):
        for keyword in keywords:
            if keyword in log.lower():
                indices.append(i)
                break
    return indices

def aggregate_logs(logs, indices):
    if not indices:
        print("[green]System Healthy[/green]")
        sys.exit(0)
    min_index = min(indices)
    max_index = max(indices)
    return '\n'.join(logs[max(0, min_index-10):min(len(logs), max_index+11)])

def call_brain(text):
    console.status("Waiting for API response...")
    try:
        response = think(text)
        console.status("API response received")
        return json.loads(response)
    except json.JSONDecodeError:
        console.status("Failed to parse JSON response")
        return None

def print_report(response, indices, logs):
    table = Table(title="Error Snippets")
    table.add_column("Line Number", style="cyan")
    table.add_column("Error Snippet", style="magenta")
    for index in indices:
        table.add_row(str(index+1), logs[index].strip())
    console.print(Panel(f"[bold]Incident Report[/bold]\n"
                         f"### Title: {response['title']}\n"
                         f"### Root Cause: {response['root_cause']}\n"
                         f"### Fix: {response['fix']}\n",
                         title="Incident Report", border_style="red"))
    console.print(table)

def main():
    logs = read_logs()
    indices = scan_logs(logs)
    text = aggregate_logs(logs, indices)
    response = call_brain(text)
    if response:
        print_report(response, indices, logs)

if __name__ == "__main__":
    main()
