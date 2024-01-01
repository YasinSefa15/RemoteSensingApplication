import socket
import threading
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs


class SensorServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data_dict = {'temperature': [], 'humidity': []}
        self.lock = threading.Lock()

    def start(self):
        threading.Thread(target=self.start_server).start()
        threading.Thread(target=self.start_http_server).start()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp, \
             socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp:
            s_tcp.bind((self.host, self.port + 1))
            s_tcp.listen()
            print(f"TCP/UDP Server listening on port {self.port + 1}")

            while True:
                try:
                    conn, addr = s_tcp.accept()
                    with conn:
                        print('Connected by', addr)
                        data = conn.recv(1024)
                        if not data:
                            break
                        self.handle_sensor_data(data.decode())
                except socket.error:
                    pass

                try:
                    data, addr = s_udp.recvfrom(1024)
                    self.handle_sensor_data(data.decode())
                except socket.error:
                    pass

    def start_http_server(self):
        handler = MyRequestHandler
        with socketserver.TCPServer((self.host, self.port), handler) as httpd:
            print(f"HTTP server listening on port {self.port}")
            httpd.sensor_server = self
            httpd.serve_forever()

    def handle_sensor_data(self, data):
        sensor_type, value, timestamp = data.split('|')
        with self.lock:
            self.data_dict[sensor_type.lower()].append({'value': float(value), 'timestamp': float(timestamp)})

    def get_sensor_data(self, sensor_type):
        with self.lock:
            return self.data_dict[sensor_type.lower()]


class MyRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_params = parse_qs(parsed_path.query)

        if path == '/temperature':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            data = self.server.sensor_server.get_sensor_data('temperature')
            self.wfile.write(str(data).encode())
        elif path == '/humidity':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            data = self.server.sensor_server.get_sensor_data('humidity')
            self.wfile.write(str(data).encode())
        elif path == '/gethumidity':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            data = self.server.sensor_server.get_sensor_data('humidity')
            if data:
                last_measurement = data[-1]
                self.wfile.write(f"Last Humidity Measurement: {last_measurement}".encode())
            else:
                self.wfile.write("No Humidity Data Available".encode())
        else:
            super().do_GET()


if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 8080

    server = SensorServer(host=server_host, port=server_port)
    server.start()
