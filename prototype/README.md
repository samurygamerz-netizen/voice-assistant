# FOXSI Starter Prototype

This is a small, runnable first slice of the FOXSI plan—not the complete assistant.

## Run on Windows

1. Install Python 3.10+ and enable **Add Python to PATH**.
2. Open this folder in File Explorer.
3. Double-click `start.bat`, or open Command Prompt here and run `python main.py`.
4. The browser should open at http://127.0.0.1:8765.
5. Type `help`, `time`, `system info`, or `disk usage`.
6. Press Ctrl+C in the terminal to stop it.

## Implemented in this prototype

- Localhost-only web UI.
- Basic text command input.
- Small allowlist of deterministic, read-only commands.
- Health endpoint at `/health`.
- No third-party Python dependencies.
- No arbitrary shell execution.

## Not implemented yet

- LLM/provider integration, internet research, voice/STT/TTS, wake word, persistent memory, coding agent, multi-agent execution, and PC automation.
- It is not yet a general-purpose AI assistant and has not been tested on your PC.

## Safety

The server binds to `127.0.0.1`, not the public network. Do not expose it to a LAN or the internet without adding authentication and reviewing security. This prototype deliberately does not execute arbitrary shell commands.
