from ..brain.groq import think
import sys
import rich
from rich.console import Console
import json
import time
from datetime import datetime

console = Console()

def save_reports(response, logs, indices):
    timestamp = int(time.time())
    incident_file = f"incidents/incident_{timestamp}.json"
    record = {
        "Timestamp": timestamp,
        "Analysis": response,
        "raw_error_snippit": [logs[i] for i in indices]
    }
    with open(incident_file, 'w') as f:
        json.dump(record, f)
    return record

def heimdall(logs):
    if not logs:
        console.print("[red]No logs provided. Please provide logs to analyze.[/red]")
        return {"error": "No logs provided"}

    logs = logs[-50:]
    keywords = ['error', 'critical', 'fatal', 'traceback', 'exception', 'panic', 'warn']
    indices = [i for i, log in enumerate(logs) if any(keyword in log for keyword in keywords)]

    if not indices:
        return {"error": "No errors found in logs"}

    min_index = min(indices)
    max_index = max(indices)
    aggregated_text = '\n'.join(logs[max(min_index-10, 0):min(max_index+11, len(logs))])

    console.status("Waiting for API response...")
    try:
        response = think(aggregated_text)
        response = json.loads(response)
    except json.JSONDecodeError:
        console.print("[red]Invalid JSON response from API.[/red]")
        return {"error": "Invalid JSON response from API"}

    console.status("API response received")

    console.print(rich.panel.Panel(
        f"[bold]Incident Report[/bold]\n"
        f"### Title: {response['title']}\n"
        f"### Root Cause: {response['root_cause']}\n"
        f"### Fix: {response['fix']}",
        title="Incident Report"
    ))

    table = rich.table.Table(title="Error Snippets")
    table.add_column("Line Number", style="cyan")
    table.add_column("Error Snippet", style="magenta")

    for index in indices:
        table.add_row(str(index), logs[index])

    console.print(table)

    record = save_reports(response, logs, indices)
    return record

if __name__ == "__main__":
    logs = sys.stdin.readlines()
    logs = [log.strip() for log in logs]
    response = heimdall(logs)
    print(json.dumps(response))