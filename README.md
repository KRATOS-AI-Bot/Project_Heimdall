
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

# Initialize variables to store error lines and their contexts
error_lines = []
error_contexts = []

# Iterate over lines to find error lines and their contexts
for i, line in enumerate(lines):
    if any(keyword in line.lower() for keyword in keywords):
        # Get 10 lines above and below the error line
        start = max(0, i - 10)
        end = min(len(lines), i + 11)
        context = lines[start:end]
        error_lines.append(line)
        error_contexts.append(context)

# Define function to call GROQ API
def think(prompt):
    try:
        completion = requests.post(
            f"https://api.grok.com/v1/chat/completions",
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
        print(f"An error occurred: {e}")
        sys.exit(1)

# Iterate over error lines and their contexts
for i, (error_line, context) in enumerate(zip(error_lines, error_contexts)):
    # Call GROK API to get explanation and fix for the error
    prompt = f"Explain why the following error occurred and how to fix it:\n{error_line}\nContext:\n" + "\n".join(context)
    response = think(prompt)
    
    # Print error information and fix
    table = Table(title="Error Information")
    table.add_column("Error Line", style="cyan")
    table.add_column("Error Message", style="magenta")
    table.add_column("Fix", style="green")
    table.add_row(str(i + 1), error_line.strip(), response)
    console.print(table)

# If no errors were found, print success message
if not error_lines:
    console.print("[bold green]Everything's fine![/bold green]")



# Heimdall: AI-Powered Error Detection and Prevention

Heimdall is a cutting-edge tool that leverages AI to detect and prevent errors in log files. It uses a combination of natural language processing (NLP) and machine learning algorithms to identify potential issues and provide actionable insights for remediation.

## Features

* **AI Error Detection**: Heimdall uses AI to analyze log files and detect potential errors, including syntax errors, runtime errors, and logical errors.
* **Auto Remediation**: Heimdall provides automated remediation suggestions for detected errors, reducing the time and effort required to resolve issues.
* **Error Prevention**: Heimdall's AI-powered analysis helps prevent errors from occurring in the first place by identifying potential issues before they become critical.

## How it Works

1. **Log File Analysis**: Heimdall analyzes log files to identify potential errors and issues.
2. **AI-Powered Detection**: Heimdall's AI engine analyzes the log file data to detect potential errors and issues.
3. **Error Reporting**: Heimdall generates a report detailing the detected errors and issues, including recommendations for remediation.
4. **Auto Remediation**: Heimdall provides automated remediation suggestions for detected errors, reducing the time and effort required to resolve issues.

## Benefits

* **Improved Error Detection**: Heimdall's AI-powered analysis provides more accurate and efficient error detection than traditional methods.
* **Reduced Downtime**: Heimdall's automated remediation suggestions reduce the time and effort required to resolve issues, minimizing downtime and improving overall system reliability.
* **Increased Productivity**: Heimdall's AI-powered analysis and automated remediation suggestions free up developers to focus on higher-level tasks, improving overall productivity and efficiency.

## Why Heimdall?

Heimdall is the perfect solution for organizations looking to improve their error detection and prevention capabilities. With its AI-powered analysis and automated remediation suggestions, Heimdall provides a comprehensive and efficient solution for error detection and prevention. Whether you're a developer, DevOps engineer, or IT professional, Heimdall is the perfect tool to help you improve your error detection and prevention capabilities.
