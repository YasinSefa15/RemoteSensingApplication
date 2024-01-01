import socket
import threading
import time
import random
import logging
from datetime import datetime

# Sensors:
# You will have a temperature sensor and a humidity sensor. However, these are not actual sensors;
# they are two applications that generate sensor values randomly and periodically send them to the gateway.
# The temperature sensor is connected to the gateway via TCP, while the humidity sensor sends values
# to the gateway via UDP. Every second, the temperature sensor generates a value randomly between 20 and 30
# and sends it to the gateway along with the timestamp.
# Meanwhile, the humidity sensor generates random values between 40 and 90 every second but sends information
# only if the humidity value exceeds 80. Additionally, every 3 seconds, the humidity sensor should
# send an 'ALIVE' message to indicate that it is working properly.

logging.basicConfig(level=logging.DEBUG, filename='sensor_apps.log', filemode='w')
logger = logging.getLogger(__name__)


def temperature_sensor():
    host = "localhost"
    port = 5559

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        try:
            while True:
                temperature_value = random.uniform(20, 30)
                message = f"TEMP:{temperature_value},{get_time()}"
                s.sendto(message.encode(), (host, port))
                logger_message = f'Sent_at : {get_time()} ; Temperature Sensor: {message}'
                logger.info(logger_message)
                # print(logger_message) # eğer console'a yazdırmak isterseniz bu satırı açın
                time.sleep(1)
        except BrokenPipeError:
            print("Connection to gateway is broken.")


def humidity_sensor():
    host = "localhost"
    port = 5556

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        while True:
            humidity_value = random.uniform(40, 90)
            timestamp = time.time()
            message = f"HUMIDITY:{humidity_value},{get_time()}"
            logger_message = f'Generated_at : {get_time()} ; Humidity Sensor Value: {message}'
            logger.info(logger_message)
            # print(logger_message) # eğer console'a yazdırmak isterseniz bu satırı açın
            if humidity_value > 80:
                s.sendto(message.encode(), (host, port))
                logger_message = f'Sent_at : {get_time()} ; Humidity Sensor Value: {message}'
                logger.info(logger_message)
                # print(logger_message)  # eğer console'a yazdırmak isterseniz bu satırı açın

            # Send 'ALIVE' message every 3 seconds
            if int(timestamp) % 3 == 0:
                alive_message = "ALIVE"
                s.sendto(alive_message.encode(), (host, port))
                logger_message = f'Sent_at : {get_time()} ; Humidity Sensor Message: {alive_message}'
                logger.info(logger_message)

            time.sleep(1)


def handle_sensors():
    temperature_thread = threading.Thread(target=temperature_sensor)
    humidity_thread = threading.Thread(target=humidity_sensor)

    temperature_thread.start()
    humidity_thread.start()

    temperature_thread.join()
    humidity_thread.join()


def get_time():
    current_time = time.time()
    formatted_time = datetime.fromtimestamp(current_time).strftime('%Y-%m-%d %H:%M:%S')
    return formatted_time


if __name__ == "__main__":
    handle_sensors()
