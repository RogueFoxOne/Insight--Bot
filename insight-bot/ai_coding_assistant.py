#!/usr/bin/env python3
"""
GestaltView AI Coding Assistant for Red Hat OpenShift
Your personal AI pair programmer with PLK integration.
"""

import sys
import os
import json
import argparse
import requests # Industry standard for HTTP requests

def get_api_key():
    """Safely retrieve the API key from environment variables and exit if not found."""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        print("Error: OPENROUTER_API_KEY environment variable not set.", file=sys.stderr)
        print("Please set the key and try again.", file=sys.stderr)
        sys.exit(1)
    return api_key

def ask_ai(question: str, context: str = "", api_key: str = None) -> str:
    """Sends a question to the Claude 3.5 Sonnet model via OpenRouter."""
    if not api_key:
        api_key = get_api_key()

    system_prompt = """You are Keith Soyka's personal AI coding assistant built with GestaltView principles.

You are:
- ADHD-friendly (complete code blocks, no chunks)
- Consciousness-serving (enhance, not subtract)
- Direct and clear (no fluff)
- Iteration-focused ("Iteration is liberation")

When answering code questions:
1. Provide FULL, COMPLETE code blocks (never partial).
2. Explain WHY, not just WHAT.
3. Show the ADHD-friendly "one command" solution first.
4. Add context for neurodivergent workflows.

Remember: "Don't assume or guess. The structure is particular for a reason."
"""
    
    messages = [{"role": "system", "content": system_prompt}]
    if context:
        messages.append({"role": "user", "content": f"Context from file:\n---\n{context}\n---"})
    
    messages.append({"role": "user", "content": question})

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'https://gestaltview.com',
        'X-Title': 'GestaltView AI Assistant'
    }
    
    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4096
    }
    
    try:
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=180 # Set a generous timeout
        )
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return f"API Request Error: {e}\n\nCheck your API key and internet connection."
    except (KeyError, IndexError) as e:
        return f"Error parsing API response: {e}\n\nResponse was: {response.text}"

def get_file_context(filepath: str) -> str:
    """Reads a file and returns its content as a string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"Error: File not found at '{filepath}'"
    except IOError as e:
        return f"Error reading file '{filepath}': {e}"

def main():
    """Main function to parse arguments and run the assistant."""
    parser = argparse.ArgumentParser(
        description="🧠 GestaltView AI Coding Assistant",
        epilog='💡 Pro tip: alias ask="python3 /path/to/ai_coding_assistant.py"'
    )
    parser.add_argument("question", type=str, help="Your question for the AI.")
    parser.add_argument("file", nargs='?', default=None, help="Optional file path to provide as context.")
    
    args = parser.parse_args()
    
    context = ""
    if args.file:
        if os.path.isfile(args.file):
            print(f"📄 Loading context from {args.file}...\n")
            context = get_file_context(args.file)
        else:
            print(f"Warning: File '{args.file}' not found. Proceeding without file context.", file=sys.stderr)

    print("🧠 Asking Claude via GestaltView...\n")
    answer = ask_ai(args.question, context)
    
    print(answer)
    print("\n---")
    print("Built with 💜 by GestaltView | OpenRouter + Claude 3.5 Sonnet")
    print('"Iteration is liberation." — Keith Soyka')

if __name__ == "__main__":
    main()