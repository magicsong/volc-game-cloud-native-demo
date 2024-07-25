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
            clients_disconnected_total = 0  # Total disconnected clients
            
            for line in metrics:
                if line.startswith('#'):
                    continue
                if 'clients_connected' in line:
                    # Extract the value after the metric name
                    clients_connected = int(line.split(' ')[1])
                elif 'clients_disconnected' in line:
                    # Accumulate the value after the metric name
                    clients_disconnected_total += int(line.split(' ')[1])
            
            if clients_connected is None:
                raise ValueError('clients_connected metric not found')

            # Calculate the actual number of connected clients
            actual_clients = clients_connected - clients_disconnected_total

            # Determine server status based on the number of actual clients
            if actual_clients == 0:
                status = 'idle'
            elif actual_clients > 10:
                status = 'busy'
            else:
                status = 'allocated'
                
            # Send the status as the response
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
