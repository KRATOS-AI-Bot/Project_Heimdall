
import sys
import os
import re
from dotenv import load_dotenv

load_dotenv()
GROK_API_KEY = os.getenv('GROK_API_KEY')
import openai

openai.api_key = GROK_API_KEY

def think(prompt):
    try:
        completion = openai.ChatCompletion.create(
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

def detect_error(log_lines):
    error_keywords = ['throwback', 'error', 'critical', 'fatal', 'traceback', 'exception']
    for i, line in enumerate(log_lines):
        for keyword in error_keywords:
            if keyword in line.lower():
                return i, line
    return None, None

def get_context(log_lines, error_index):
    start_index = max(0, error_index - 10)
    end_index = min(len(log_lines), error_index + 11)
    context = log_lines[start_index:end_index]
    return context

def main():
    log_lines = sys.stdin.readlines()[-50:]
    error_index, error_line = detect_error(log_lines)
    if error_index is not None:
        context = get_context(log_lines, error_index)
        prompt = f"An error occurred at line {error_index + 1}: {error_line.strip()}. The context is:\n" + "\n".join(context) + "\nWhy did it happen and how to fix it?"
        response = think(prompt)
        print(f"Error detected at line {error_index + 1}: {error_line.strip()}. Summary: {response.split('.')[0]}. Fix: {response.split('.')[-1]}")
    else:
        print("Everything's fine")

if __name__ == "__main__":
    main()
