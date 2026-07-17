#!/bin/bash
# This script keeps the Replit bot alive by responding to pings

from flask import Flask
from threading import Thread
import logging

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Bot is running! ✅', 200

def run_flask():
    app.run(host='0.0.0.0', port=8080, debug=False)

def start_web_server():
    """Start Flask server in background to prevent Replit spindown"""
    thread = Thread(target=run_flask, daemon=True)
    thread.start()

if __name__ == '__main__':
    run_flask()
