import socket
import threading
import time

class Gateway:
    def __init__(self, server_host, server_port, temperature_port, humidity_port):
        self.server_host = server_host
        self.server_port = server_port
        self.temperature_port = temperature_port
        self.humidity_port = humidity_port
        self.temperature_socket = None
        self.humidity_socket = None

    def start(self):
        threading.Thread(target=self.start_temperature_server).start()
        threading.Thread(target=self.start_humidity_server).start()
        self.connect_to_server()

    def start_temperature_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', self.temperature_port))
            s.listen()
            print(f"Temperature server listening on port {self.temperature_port}")
            conn, addr = s.accept()
            with conn:
                self.temperature_socket = conn
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    self.handle_temperature_data(data.decode())

    def start_humidity_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(('localhost', self.humidity_port))
            print(f"Humidity server listening on port {self.humidity_port}")
            while True:
                data, addr = s.recvfrom(1024)
                self.handle_humidity_data(data.decode())

    def handle_temperature_data(self, data):
        print(f"Temperature Data Received: {data}")
        # Server'a gönder
        self.send_to_server(data)

    def handle_humidity_data(self, data):
        print(f"Humidity Data Received: {data}")
        # Server'a gönder
        self.send_to_server(data)

    def connect_to_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print("bağlanma yeri")
            s.connect((self.server_host, self.server_port))
            print(f"Connected to server {self.server_host}:{self.server_port}")
            self.temperature_socket = s  # Bağlantıyı güncelle
            self.humidity_socket = s  # Aynı bağlantıyı kullan

    def send_to_server(self, data):
        try:
            self.temperature_socket.sendall(data.encode())
        except (socket.error, AttributeError):
            print("sunucuya gönderme başarısız.")
            pass

if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 8080
    gateway_port_temperature = 5557
    gateway_port_humidity = 5558

    gateway = Gateway(server_host, server_port, gateway_port_temperature, gateway_port_humidity)
    gateway.start()
