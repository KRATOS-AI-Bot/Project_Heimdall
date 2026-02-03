
from ..brain.groq import think
import json

def analyze_log_text(log_text: str) -> dict:
    if not log_text:
        return {"error": "No logs provided"}

    lines = log_text.splitlines()[-50:]
    keywords = ['error', 'critical', 'fatal', 'traceback', 'exception', 'panic', 'warn']
    indices = []

    for i, line in enumerate(lines):
        for keyword in keywords:
            if keyword in line.lower():
                indices.append(i)
                break

    if not indices:
        return {"status": "Healthy"}

    min_index = min(indices)
    max_index = max(indices)

    aggregated_text = '\n'.join(lines[max(0, min_index - 10):min_index + 11])

    try:
        result = think(aggregated_text)
        result_dict = json.loads(result)
        return result_dict
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response"}
    except Exception as e:
        return {"error": str(e)}
