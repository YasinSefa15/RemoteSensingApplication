import socket
import threading
import logging
import time
from datetime import datetime

import html_parser

logging.basicConfig(level=logging.DEBUG, filename='server.log', filemode='w')
logger = logging.getLogger(__name__)


class SensorServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.data_dict = {'temperature': [], 'humidity': []}
        self.lock = threading.Lock()
        self.last_measured_humidity = 0

    def start(self):
        threading.Thread(target=self.start_server).start()

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp:
            s_tcp.bind((self.host, self.port))  # self.host
            s_tcp.listen()
            print(f"TCP Server listening on port {self.port}")

            while True:
                conn, addr = s_tcp.accept()
                print('Connected by', addr)
                data = conn.recv(1024)
                if not data:
                    print("Connection to gateway data is null. Connection is broken.")
                    continue
                self.handle_received_data(conn, data.decode())

    def handle_received_data(self, conn, data):
        # data is decoded by the caller side

        logging_message = f'Received_at : {data}'
        logger.debug(logging_message)

        if data.__contains__('GET'):
            self.html_handler(conn, data)
            return
        elif (data.__contains__('GATEWAY ON')
              or data.__contains__('TEMP SENSOR OFF')) \
                or data.__contains__('ALIVE') \
                or data.__contains__('HUMIDITY SENSOR OFF'):

            logger_message = f'Received_at : {get_time()} ; Gateway Message: {data}'
            logger.info(logger_message)
            print(logger_message)
            return

        self.record_sensor_data(data)

    def record_sensor_data(self, decoded_data):
        data = decoded_data

        data = data.split(",")

        sensor_information = data[0].split(":")
        sensor_type = sensor_information[0]
        value = sensor_information[1]

        if sensor_type == "TEMP":
            sensor_type = "temperature"
        elif sensor_type == "HUMIDITY":
            sensor_type = "humidity"

        with self.lock:
            self.data_dict[sensor_type.lower()].append({'value': value, 'timestamp': data[1]})

    def html_handler(self, conn, data):
        # requested url is /temperature or /humidity
        if data.__contains__('/temperature '):
            html = html_parser.return_html_file((self.get_sensor_data('temperature')), 'html files/temperature.html')
            conn.sendall(b'HTTP/1.1 200 OK\n')
            conn.sendall(b'Content-Type: text/html\n')
            conn.sendall(b'\n')
            conn.sendall(html.encode())
            conn.close()
            print("GET")
            return
        elif data.__contains__('/humidity '):
            html = html_parser.return_html_file((self.get_sensor_data('humidity')), 'html files/humidity.html')
            conn.sendall(b'HTTP/1.1 200 OK\n')
            conn.sendall(b'Content-Type: text/html\n')
            conn.sendall(b'\n')
            conn.sendall(html.encode())
            conn.close()
            print("GET")
            return
        elif data.__contains__('/gethumidity '):
            get_last_measured_humidity_thread = threading.Thread(target=self.get_last_measured_humidity)
            get_last_measured_humidity_thread.start()
            get_last_measured_humidity_thread.join()
            html = html_parser.return_html_file(self.last_measured_humidity, 'html files/last_measured_humidity.html')
            conn.sendall(b'HTTP/1.1 200 OK\n')
            conn.sendall(b'Content-Type: text/html\n')
            conn.sendall(b'\n')
            conn.sendall(html.encode())
            conn.close()
            print("GET")
            return
        conn.sendall(b'HTTP/1.1 200 OK\n')
        conn.sendall(b'Content-Type: text/html\n')
        conn.sendall(b'\n')
        conn.sendall(b'<h1>404 Not Found</h1>')
        conn.close()

    def get_last_measured_humidity(self):
        # sent to the gateway and get the data from the gateway
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_tcp:
            s_tcp.connect(('localhost', 6666))
            s_tcp.sendall(b'GET LAST HUMIDITY')
            print("GET LAST HUMIDITY")
            data = s_tcp.recv(1024)
            print("received" + data.decode())
            self.last_measured_humidity = data.decode()
            s_tcp.close()

    def get_sensor_data(self, sensor_type):
        with self.lock:
            return self.data_dict[sensor_type.lower()]


# Getting the current time in a formatted way
def get_time():
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 8080

    server = SensorServer(host=server_host, port=server_port)
    server.start()
