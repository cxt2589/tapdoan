import webbrowser
import http.server
import socketserver
import os

PORT = 8501
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

print(f"=======================================================")
print(f"  TRADINGAGENTS: XAU/USD GOLD CONSOLE")
print(f"  Dang khoi chay may chu web tai: http://localhost:{PORT}/gold_dashboard.html")
print(f"=======================================================")

webbrowser.open(f"http://localhost:{PORT}/gold_dashboard.html")

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDa dung may chu web.")
