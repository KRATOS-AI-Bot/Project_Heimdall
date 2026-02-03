
from brain.groq import think
import sys
from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import json
from datetime import datetime
import os

console = Console()

def read_logs():
    logs = sys.stdin.readlines()
    if not logs:
        console.print("[red]Please provide log input[/red]")
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
        console.print("[green]System Healthy[/green]")
        sys.exit(0)
    min_index = min(indices)
    max_index = max(indices)
    return '\n'.join(logs[max(0, min_index-10):max_index+11])

def call_brain(text):
    with console.status("[bold cyan] Heimdall is analyzing...[/bold cyan]"):
        prompt = f"""
            - Act as a Senior Site Reliability Engineer (SRE)
            - Analyze the following log aggregation and identify the critical failure.
            
            LOGS: {text}
            
            INSTRUCTIONS:
                1. Identify the Root Cause.
                2. Suggest a specific Fix.
                3. RETURN ONLY RAW JSON. Do not use Markdown formatting.
                
            JSON STRUCTURE:
            {{
                "title": "Short Error Name",
                "root_cause": "Detailed explanation",
                "fix": "Command or Code fix"
            }}
        """
        
        response = think(prompt)
        response = response.replace("```json", "").replace("```", "").strip()
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            console.print("[red]Invalid JSON response[/red]")
            sys.exit(1)

def print_report(response, indices, logs):
    table = Table(title="Error Snippets")
    table.add_column("Line Number", style="cyan")
    table.add_column("Error Snippet", style="magenta")
    for index in indices:
        table.add_row(str(index+1), logs[index].strip())
    console.print(Panel(f"[bold purple]**Incident Report**[/bold purple]\n\n"
                         f"[bold cyan]### Title:[/bold cyan] {response['title']}\n\n"
                         f"[bold red]### Root Cause:[/bold red] {response['root_cause']}\n\n"
                         f"[bold green]### Fix:[/bold green] {response['fix']}",
                         title="Incident Report"))
    console.print(table) 

def save_reports(response, logs, indices):
    """ Saves the incident report to a local file for audit history. """
    os.makedirs("incidents", exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    incident_file = f"incidents/incident_{timestamp}.json"
    
    record = {
        "Timestamp": timestamp,
        "Analysis": response,
        "raw_error_snippit": [logs[i] for i in indices]
    }
    
    with open(incident_file, "w") as f:
        json.dump(record, f, indent=4)
        
    console.print(f"[bold violet] Incident wrote to {incident_file} successfully [/bold violet]")

def main():
    logs = read_logs()
    indices = scan_logs(logs)
    text = aggregate_logs(logs, indices)
    response = call_brain(text)
    print_report(response, indices, logs)
    save_reports(response, logs, indices)
    
if __name__ == "__main__":
    main()
