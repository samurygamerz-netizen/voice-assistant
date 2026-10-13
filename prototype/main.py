"""FOXSI starter prototype: local UI + safe deterministic tools.
This is a Phase-1 scaffold, not the full voice/LLM assistant.
Run with: python prototype/main.py
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import platform
import shutil
import webbrowser

HOST, PORT = "127.0.0.1", 8765

HTML = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FOXSI — Starter</title><style>
:root{color-scheme:dark;font-family:system-ui,Segoe UI,sans-serif}body{margin:0;background:#10131b;color:#e8edf7}
main{max-width:850px;margin:5vh auto;padding:24px}h1{margin:0;color:#9ed0ff}p{color:#aab6ca}
.panel{background:#191f2b;border:1px solid #30394a;border-radius:16px;padding:18px;margin-top:18px}
#log{min-height:220px;white-space:pre-wrap;line-height:1.5}.row{display:flex;gap:8px;margin-top:12px}
input{flex:1;min-width:0;background:#0d1118;color:#fff;border:1px solid #414b60;border-radius:10px;padding:13px}
button{border:0;border-radius:10px;padding:12px 16px;background:#8dc7ff;color:#08111b;font-weight:700;cursor:pointer}
small{color:#9aa8bd}.tag{display:inline-block;border:1px solid #47556b;border-radius:999px;padding:4px 9px;margin:4px 4px 0 0}
</style></head><body><main><h1>FOXSI</h1><p>Windows-first assistant · starter prototype</p>
<div class="tag">Local UI</div><div class="tag">Safe tools</div><div class="tag">No API key needed for demo</div>
<section class="panel"><div id="log">FOXSI: Ready. Try “help”, “time”, “system info”, or “disk usage”. This prototype does not yet include an AI model or voice input/output.</div>
<div class="row"><input id="msg" placeholder="Type a command…" autofocus><button id="send">Send</button></div></section>
<section class="panel"><b>Current prototype scope</b><p>Text interface and a small allowlist of read-only local tools. Destructive commands are not implemented. AI provider, microphone, speech, memory, and web research are future phases.</p><small>Local address: http://127.0.0.1:8765</small></section></main>
<script>
const log=document.getElementById('log'), input=document.getElementById('msg');
async function send(){const text=input.value.trim();if(!text)return;log.textContent+='\n\nYou: '+text;input.value='';
try{const r=await fetch('/api/command',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text})});const d=await r.json();log.textContent+='\nFOXSI: '+d.reply;}catch(e){log.textContent+='\nFOXSI: Local server error. Check the terminal.'}}
document.getElementById('send').onclick=send;input.addEventListener('keydown',e=>{if(e.key==='Enter')send()});
</script></body></html>"""

def run_tool(text):
    command = text.strip().lower()
    if command in {"help", "commands"}:
        return "Available demo commands: help, time, system info, disk usage. No arbitrary shell commands are accepted."
    if command in {"time", "what time is it", "current time"}:
        from datetime import datetime
        return "Local computer time: " + datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    if command in {"system info", "system information", "pc info"}:
        return f"OS: {platform.platform()}\nPython: {platform.python_version()}\nCPU: {platform.processor() or 'Not reported'}\nRAM: see Windows Task Manager (not reliably available through Python stdlib)."
    if command in {"disk usage", "disk space"}:
        total, used, free = shutil.disk_usage(os.path.abspath(os.sep))
        gb = 1024 ** 3
        return f"System drive: total {total/gb:.1f} GB, used {used/gb:.1f} GB, free {free/gb:.1f} GB."
    return "I don't have an AI model connected yet, so I can only run the listed demo commands. Type “help” to see them."

class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type):
        raw = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)
    def do_GET(self):
        if self.path in {"/", "/index.html"}:
            self._send(200, HTML, "text/html; charset=utf-8")
        elif self.path == "/health":
            self._send(200, json.dumps({"ok": True, "stage": "prototype"}), "application/json")
        else:
            self._send(404, "Not found", "text/plain; charset=utf-8")
    def do_POST(self):
        if self.path != "/api/command":
            self._send(404, json.dumps({"error":"not found"}), "application/json"); return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size > 4096:
                raise ValueError("Request too large")
            data = json.loads(self.rfile.read(size).decode("utf-8"))
            text = data.get("text", "")
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Command must be non-empty text")
            reply = run_tool(text[:1000])
            self._send(200, json.dumps({"reply":reply}, ensure_ascii=False), "application/json")
        except (ValueError, json.JSONDecodeError, UnicodeDecodeError) as exc:
            self._send(400, json.dumps({"reply":f"Invalid request: {exc}"}), "application/json")
    def log_message(self, fmt, *args):
        print("[FOXSI]", fmt % args)

if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"FOXSI prototype running at http://{HOST}:{PORT}")
    print("Press Ctrl+C to stop. This server binds to localhost only.")
    try:
        webbrowser.open(f"http://{HOST}:{PORT}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping FOXSI safely...")
    finally:
        server.server_close()
