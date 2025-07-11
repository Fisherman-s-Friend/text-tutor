import requests
import json
import subprocess
import time
import re


def rephrase(text, model="mistral", retrying=False):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": f"Rephrase this text in a simpler way: {text}",
        "stream": False,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
    except requests.exceptions.ConnectionError:
        if not retrying:
            print("Ollama is not running. Trying to start it...")
            start_ollama()
            time.sleep(3)  # wait a moment for it to spin up
            return rephrase(text, model, retrying=True)
        else:
            return "Ollama could not be reached or started."

    if response.status_code == 200:
        result = response.json()
        thinking_pattern = r"<think>.*?</think>"
        response_str = result.get("response", "").strip()
        response_str = re.sub(thinking_pattern, "[reasoning steps hidden.] ", response_str, flags=re.DOTALL)
        return response_str

    elif (
        response.status_code == 404
        and f"model '{model}' not found" in response.text.lower()
    ):
        print(f"Pulling missing model: {model}")
        pull_model(model)
        return rephrase(text, model)  # Retry after pulling

    else:
        print("Error:", response.status_code, response.text)
        return f"Error: {response.text}"


def start_ollama():
    try:
        subprocess.Popen(["ollama", "serve"])
        print("Started Ollama in background.")
    except Exception as e:
        print("Failed to start Ollama:", e)


def pull_model(model):
    try:
        subprocess.run(["ollama", "pull", model], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull model '{model}':", e)
