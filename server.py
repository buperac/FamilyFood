import http.server
import socketserver
import urllib.request
import urllib.error
import json
import os
import sys

PORT = 8765
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_OPTIONS(self):
        # Allow CORS preflight requests
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type, Authorization")
        self.end_headers()

    def do_POST(self):
        # Set CORS headers
        if self.path == '/api/chat':
            self.handle_chat_proxy()
        elif self.path == '/api/image':
            self.handle_image_proxy()
        else:
            self.send_error(404, "Endpoint not found")

    def handle_chat_proxy(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            provider = req_data.get('provider')
            model = req_data.get('model')
            api_key = req_data.get('apiKey')
            messages = req_data.get('messages')
            
            if not provider or not api_key:
                self.send_error_response(400, "Missing provider or apiKey in request")
                return

            if provider == 'openai':
                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                body = json.dumps({
                    "model": model or "gpt-4o-mini",
                    "messages": messages,
                    "response_format": { "type": "json_object" } if req_data.get('jsonMode') else None
                }).encode('utf-8')
                
            elif provider == 'anthropic':
                url = "https://api.anthropic.com/v1/messages"
                headers = {
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "Content-Type": "application/json"
                }
                # For Anthropic, we need to extract system prompt if there is one
                system_prompt = ""
                api_messages = []
                for m in messages:
                    if m['role'] == 'system':
                        system_prompt = m['content']
                    else:
                        api_messages.append(m)
                
                body_dict = {
                    "model": model or "claude-3-5-sonnet-20241022",
                    "messages": api_messages,
                    "max_tokens": 4000
                }
                if system_prompt:
                    body_dict["system"] = system_prompt
                    
                body = json.dumps(body_dict).encode('utf-8')
                
            elif provider == 'gemini':
                # Gemini can use direct request, but proxy helps unify key handling
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model or 'gemini-2.5-flash'}:generateContent?key={api_key}"
                headers = {
                    "Content-Type": "application/json"
                }
                # Translate messages format from OpenAI style to Gemini style
                gemini_contents = []
                system_instruction = None
                
                for m in messages:
                    if m['role'] == 'system':
                        system_instruction = {"parts": [{"text": m['content']}]}
                    else:
                        role = "user" if m['role'] == 'user' else "model"
                        gemini_contents.append({
                            "role": role,
                            "parts": [{"text": m['content']}]
                        })
                
                body_dict = {
                    "contents": gemini_contents
                }
                if system_instruction:
                    body_dict["systemInstruction"] = system_instruction
                
                if req_data.get('jsonMode'):
                    body_dict["generationConfig"] = {
                        "responseMimeType": "application/json"
                    }
                    
                body = json.dumps(body_dict).encode('utf-8')
                
            elif provider == 'grok':
                url = "https://api.x.ai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                body = json.dumps({
                    "model": model or "grok-2",
                    "messages": messages,
                    "response_format": { "type": "json_object" } if req_data.get('jsonMode') else None
                }).encode('utf-8')
                
            else:
                self.send_error_response(400, f"Unsupported provider: {provider}")
                return

            # Forward the request
            req = urllib.request.Request(url, data=body, headers=headers, method='POST')
            with urllib.request.urlopen(req) as response:
                res_body = response.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(res_body)

        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', errors='ignore')
            print(f"HTTPError from upstream: {e.code} - {err_body}")
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(err_body.encode('utf-8'))
        except Exception as e:
            print(f"Error handling proxy: {str(e)}")
            self.send_error_response(500, f"Internal Proxy Error: {str(e)}")

    def handle_image_proxy(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            req_data = json.loads(post_data.decode('utf-8'))
            provider = req_data.get('provider')
            prompt = req_data.get('prompt')
            api_key = req_data.get('apiKey')
            
            if not provider or not prompt or not api_key:
                self.send_error_response(400, "Missing provider, prompt, or apiKey in request")
                return

            if provider == 'openai':
                url = "https://api.openai.com/v1/images/generations"
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                }
                body = json.dumps({
                    "model": "dall-e-3",
                    "prompt": prompt,
                    "n": 1,
                    "size": "1024x1024"
                }).encode('utf-8')
                
                req = urllib.request.Request(url, data=body, headers=headers, method='POST')
                with urllib.request.urlopen(req) as response:
                    res_body = response.read()
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(res_body)
            else:
                self.send_error_response(400, f"Upstream image generation not supported for: {provider}")
                
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', errors='ignore')
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(err_body.encode('utf-8'))
        except Exception as e:
            self.send_error_response(500, f"Internal Image Proxy Error: {str(e)}")

    def send_error_response(self, code, message):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"error": {"message": message}}).encode('utf-8'))

# Run server
if __name__ == '__main__':
    handler = ProxyHandler
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    try:
        with socketserver.ThreadingTCPServer(("", PORT), handler) as httpd:
            print(f"Serving at http://localhost:{PORT} (concurrency enabled)")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\nShutting down server.")
                sys.exit(0)
    except OSError as e:
        if e.errno == 98 or getattr(e, 'winerror', None) == 10048 or "already in use" in str(e):
            print(f"[Error] Port {PORT} is already in use. Is server.py already running in another terminal/session?")
            print(f"You can close the other process, or edit the PORT = {PORT} variable at the top of server.py to run on a different port.")
            sys.exit(1)
        raise e
