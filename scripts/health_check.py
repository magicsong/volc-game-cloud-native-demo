import http.server
import socketserver
import requests

PORT = 8080

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            response = requests.get('http://localhost:14005/metrics')
            metrics = response.text.split('\n')
            clients_connected = None
            clients_disconnected = None
            
            for line in metrics:
                if line.startswith('#'):
                    continue
                if 'clients_connected' in line:
                    clients_connected = int(line.split(' ')[1])
                if 'clients_disconnected' in line:
                    clients_disconnected = int(line.split(' ')[1])
            
            if clients_connected is None or clients_disconnected is None:
                raise ValueError('Metrics not found')

            actual_clients = clients_connected - clients_disconnected

            if actual_clients <= 0:
                status = 'idle'
            elif actual_clients > 10:
                status = 'busy'
            else:
                status = 'allocated'
                
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(status.encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error fetching metrics: {str(e)}'.encode())

httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.serve_forever()
