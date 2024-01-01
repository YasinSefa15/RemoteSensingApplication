import socket
import threading
import random
import time
import logging

logging.basicConfig(level=logging.INFO, filename='sensor_log.txt', filemode='w')
logger = logging.getLogger(__name__)


class TemperatureSensor:
    def __init__(self, host, port):
        self.gateway_host = host
        self.temperature_gateway_port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((self.gateway_host, self.temperature_gateway_port))
                while True:
                    temperature = random.uniform(20, 30)
                    timestamp = time.time()
                    message = f'TEMPERATURE|{temperature}|{timestamp}'
                    s.sendall(message.encode())
                    logger.info(f'Temperature Sensor: {message}')
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Temperature Sensor Error: {e}")


class HumiditySensor:
    def __init__(self, host, port):
        self.gateway_host = host
        self.humidity_gateway_port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            try:
                while True:
                    humidity = random.uniform(40, 90)
                    timestamp = time.time()
                    if humidity > 80:
                        message = f'HUMIDITY|{humidity}|{timestamp}'
                        s.sendto(message.encode(), (self.gateway_host, self.humidity_gateway_port))
                        logger.info(f'Humidity Sensor: {message}')
                    time.sleep(1)
            except Exception as e:
                logger.error(f"Humidity Sensor Error: {e}")


if __name__ == "__main__":
    gateway_host = 'localhost'
    temperature_gateway_port = 5557
    humidity_gateway_port = 5558

    temperature_sensor = TemperatureSensor(host=gateway_host, port=temperature_gateway_port)
    humidity_sensor = HumiditySensor(host=gateway_host, port=humidity_gateway_port)

    threading.Thread(target=temperature_sensor.start).start()
    threading.Thread(target=humidity_sensor.start).start()
