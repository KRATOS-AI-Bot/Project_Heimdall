from brain.groq import think
import sys
from rich import print
from rich.console import Console
from rich.table import Table
import json

console = Console()

def heimdall():
    logs = sys.stdin.readlines()
    if not logs:
        print("[red]Please provide log input[/red]")
        return

    logs = logs[-50:]  # Keep only last 50 lines of logs

    keywords = ['error', 'critical', 'fatal', 'traceback', 'exception', 'panic', 'warn']
    error_indices = []
    for i, log in enumerate(logs):
        for keyword in keywords:
            if keyword in log.lower():
                error_indices.append(i)
                break

    if not error_indices:
        print("[green]System Healthy[/green]")
        return

    min_index = min(error_indices)
    max_index = max(error_indices)

    aggregated_text = ''.join(logs[max(0, min_index - 10):min_index + 11])

    console.status("Waiting for API response...")

    try:
        response = think(aggregated_text)
        response = json.loads(response)
        title = response['title']
        root_cause = response['root_cause']
        fix = response['fix']
    except Exception as e:
        print(f"Error parsing API response: {e}")
        return

    console.status("API response received")

    error_snippets = []
    for index in error_indices:
        error_snippets.append((index, logs[index].strip()))

    table = Table(title="Error Snippets")
    table.add_column("Line Number", style="cyan")
    table.add_column("Error Snippet", style="magenta")

    for snippet in error_snippets:
        table.add_row(str(snippet[0]), snippet[1])

    console.print(
        f"[bold]Incident Report[/bold]\n"
        f"### Title: {title}\n"
        f"### Root Cause: {root_cause}\n"
        f"### Fix: {fix}\n"
    )
    console.print(table)

if __name__ == "__main__":
    heimdall() 

# README
Heimdall is an AI-powered error detection and prevention tool that uses natural language processing to identify and diagnose errors in log files. It provides auto remediation suggestions to help developers quickly resolve issues.

Heimdall features AI error detection and prevention, auto remediation, and an aggregation architecture that combines multiple error logs into a single API call for cost savings.

The aggregation architecture works by scanning log files for error keywords, extracting the relevant text blocks, and combining them into a single string. This string is then passed to the AI engine for analysis.

To use Heimdall, simply pipe your log file into the heimdall.py script: cat error.log | python heimdall.py

Heimdall provides a number of benefits, including:

*   AI-powered error detection and diagnosis
*   Auto remediation suggestions
*   Aggregation architecture for cost savings
*   Easy to use and integrate into existing workflows

Overall, Heimdall is a powerful tool for developers and DevOps teams looking to improve their error detection and prevention capabilities. Its AI-powered engine and aggregation architecture make it an ideal solution for teams looking to reduce downtime and improve overall system reliability.