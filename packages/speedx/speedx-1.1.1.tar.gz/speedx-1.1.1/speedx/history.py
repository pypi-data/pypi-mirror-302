# speedx/history.py

import json
import os

HISTORY_FILE = os.path.expanduser('~/.speedx_history.json')

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as file:
            return json.load(file)
    return []

def save_report(report):
    history = load_history()
    history.append(report)
    with open(HISTORY_FILE, 'w') as file:
        json.dump(history, file, indent=4)

def get_latest_reports(limit=5):
    history = load_history()
    return history[-limit:]
