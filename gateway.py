import socket
import threading
import time
import logging
from datetime import datetime

# Gateway:
# The gateway is an application that reads values from the sensors and sends them,
# along with their timestamps, to the server. Additionally, the gateway monitors sensor activities.
# If the temperature sensor fails to send any values for 3 seconds,
# a 'TEMP SENSOR OFF' message will be sent to the server. Similarly,
# if an 'ALIVE' message is not received from the humidity sensor for more than 7 seconds,
# a 'HUMIDITY SENSOR OFF' message will be sent to the server.

# eksik kalanlar:
# 1. server'a gönderme
# 3. sensorların çalışıp çalışmadığını server'a gönderme

logging.basicConfig(level=logging.DEBUG, filename='gateway.log', filemode='w')
logger = logging.getLogger(__name__)


# Getting the current time in a formatted way
def get_time():
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


# Check if data is received from the temperature sensor
def check_data_received(last_data_received_time):
    while True:
        # If no data is received for 3 seconds, send a 'TEMP SENSOR OFF' message
        if time.time() - last_data_received_time[0] > 3:
            logger_message = f'No data received for 3 seconds. Sending "TEMP SENSOR OFF" message. Checked_At :{get_time()}'
            print(logger_message)
            logger.debug(logger_message)
            # Burada server'a 'TEMP SENSOR OFF' mesajını gönderme işlemi yapılacak.

        # Check every 3 seconds
        time.sleep(3)


# Receive data from the temperature sensor
def receive_tcp_data(conn, last_data_received_time):
    while True:
        data = conn.recv(1024)
        if not data:
            print("Connection to gateway data is null. Connection is broken.")
            break

        decoded_data = data.decode()
        logger_message = f'Received_at : {get_time()} ; Temperature Sensor: {decoded_data}'
        logger.debug(logger_message)
        print(logger_message)

        # If data is received, update the last data received time
        last_data_received_time[0] = time.time()

        # server'a gönderilme işlemi yapılacak...


# Check if 'ALIVE' message is received from the humidity sensor
def check_alive_received(last_alive_received_time):
    while True:
        # If no 'ALIVE' message is received for 7 seconds, send a 'HUMIDITY SENSOR OFF' message
        if time.time() - last_alive_received_time[0] > 7:
            logger_message = (f'No "ALIVE" message received for 7 seconds. Sending "HUMIDITY SENSOR OFF" message. '
                              f'Checked_At :{get_time()}')
            print(logger_message)
            logger.debug(logger_message)
            # Burada server'a 'HUMIDITY SENSOR OFF' mesajını gönderme işlemi yapılacak.

        time.sleep(7)


# Receive data from the humidity sensor
def receive_udp_data(s_udp, last_alive_received_time):
    while True:
        data, addr = s_udp.recvfrom(2048)
        decoded_data = data.decode()
        logger_message = f'Received_at : {get_time()} ; Humidity Sensor: {decoded_data}'
        logger.debug(logger_message)
        print("Received UDP: " + logger_message)

        # If 'ALIVE' message is received, update the last alive received time
        if decoded_data == 'ALIVE':
            last_alive_received_time[0] = time.time()

        # server'a gönderilme işlemi yapılacak...


# Gateway class
class Gateway:
    def __init__(self, host, port, temperature_port, humidity_port):
        self.host = host
        self.port = port
        self.temperature_port = temperature_port
        self.humidity_port = humidity_port
        self.server_socket = None

    # Start the gateway
    def start(self):
        # initialize the sockets
        threading.Thread(target=self.startTCP).start()
        threading.Thread(target=self.startUDP).start()
        # self.connect_to_server()

    # Connect to the server
    def connect_to_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            print(f"Connected to server {self.host}:{self.port}")
            self.server_socket = s  # Bağlantıyı güncelle

    # Start TCP server
    def startTCP(self):
        s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_tcp.bind(('', self.temperature_port))
        s_tcp.listen()
        print("TCP Server is listening...")

        # Keep track of the last time data was received, this is used to check if the sensor is alive
        # also, considered the time while waiting for connection establishment
        last_data_received_time = [time.time()]

        # Create a thread to check if data is received from the sensor
        check_thread = threading.Thread(target=check_data_received, args=(last_data_received_time,))
        check_thread.start()

        conn, addr = s_tcp.accept()
        print('Connected by', addr)

        # Create a thread to receive data from the sensor
        receive_tcp_thread = threading.Thread(target=receive_tcp_data, args=(conn, last_data_received_time))
        receive_tcp_thread.start()

    def startUDP(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp:
            s_udp.bind(('localhost', self.humidity_port))
            print("UDP Server is listening...")

            # To keep track of the last time 'ALIVE' message was received
            last_alive_received_time = [time.time()]

            # Create a thread to receive data from the sensor
            receive_thread = threading.Thread(target=receive_udp_data, args=(s_udp, last_alive_received_time))
            receive_thread.start()

            # Create a thread to check if 'ALIVE' message is received from the sensor
            check_thread = threading.Thread(target=check_alive_received, args=(last_alive_received_time,))
            check_thread.start()

            # Main thread, waits for other threads to finish
            receive_thread.join()
            check_thread.join()

            return;
            while True:
                data, addr = s_udp.recvfrom(2048)
                decoded_data = data.decode()
                logger_message = f'Received_at : {get_time()} ; Humidity Sensor: {decoded_data}'
                logger.info(logger_message)
                # print(logger_message) # eğer console'a yazdırmak isterseniz bu satırı açın
                # server'a gönderilme işlemi yapılacak...
                # time.sleep(1)

    # gateway'den sunucuya veri gönderme işlemi burada yapılıyor
    def send_to_server(self, data):
        try:
            self.server_socket.sendTo(data.encode(), (self.host, self.port))
        except (socket.error, AttributeError):
            print("sunucuya gönderme başarısız.")
            pass

    # zamanı almak için kullanılıyor


# Main function
if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 8080
    gateway = Gateway(server_host, server_port, temperature_port=5559, humidity_port=5556)
    gateway.start()
