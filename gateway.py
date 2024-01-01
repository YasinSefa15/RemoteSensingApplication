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
# 2. sensorların çalışıp çalışmadığını kontrol etme
# 3. sensorların çalışıp çalışmadığını server'a gönderme
# 4. server'a gönderilen verileri loglama

logging.basicConfig(level=logging.DEBUG, filename='gateway.log', filemode='w')
logger = logging.getLogger(__name__)


def startTCP():
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp.bind(('', 5559))
    s_tcp.listen()
    print("TCP Server is listening...")

    conn, addr = s_tcp.accept()
    while True:
        print('Connected by', addr)
        data = conn.recv(1024)
        if not data:
            print("Connection to gateway data is null. Connection is broken.")
            break
        decoded_data = data.decode()
        logger_message = f'Received_at : {get_time()} ; Temperature Sensor: {decoded_data}'
        logger.info(logger_message)
        # print(logger_message) # eğer console'a yazdırmak isterseniz bu satırı açın
        # server'a gönderilme işlemi yapılacak...



def startUDP():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_udp:
        s_udp.bind(('localhost', 5556))
        print("UDP Server is listening...")

        while True:
            data, addr = s_udp.recvfrom(2048)
            decoded_data = data.decode()
            logger_message = f'Received_at : {get_time()} ; Humidity Sensor: {decoded_data}'
            logger.info(logger_message)
            # print(logger_message) # eğer console'a yazdırmak isterseniz bu satırı açın
            # server'a gönderilme işlemi yapılacak...
            # time.sleep(1)


def gateway():
    # TCP ve UDP işlemlerini aynı anda başlatmak için iki thread oluşturun
    tcp_thread = threading.Thread(target=startTCP)
    udp_thread = threading.Thread(target=startUDP)

    # Her iki thread'i başlatın
    tcp_thread.start()
    udp_thread.start()

    # Her iki thread'in bitmesini bekleyin
    tcp_thread.join()
    udp_thread.join()


# gateway ve sunucu arasındaki bağlantı buradan kuruluyor
def connect_to_server(host, port):
    # thread oluşturulup bağlanacak..
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to server {host}:{port}")


# gateway'den sunucuya veri gönderme işlemi burada yapılıyor
def send_to_server():
    # sunucuya buradan gönderilecek, ama bir class oluşturmak daha mı mantıklı olur?
    # çünkü bağlanılan socket'e erişmek gerekiyor, bu yüzden class yapısı gerekecek
    # benzeri gateway1.py de var.
    return


def get_time():
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


if __name__ == "__main__":
    server_host = 'localhost'
    server_port = 8080
    connect_to_server(host=server_host, port=server_port)
    gateway()
