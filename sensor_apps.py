import socket
import threading
import random
import time


class TemperatureSensor:
    def __init__(self, gateway_host, temperature_gateway_port):
        self.gateway_host = gateway_host
        self.temperature_gateway_port = temperature_gateway_port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.gateway_host, self.temperature_gateway_port))
            while True:
                temperature = random.uniform(20, 30)
                timestamp = time.time()
                message = f'TEMPERATURE|{temperature}|{timestamp}'
                s.sendall(message.encode())
                time.sleep(1)


class HumiditySensor:
    def __init__(self, gateway_host, humidity_gateway_port):
        self.gateway_host = gateway_host
        self.humidity_gateway_port = humidity_gateway_port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            while True:
                humidity = random.uniform(40, 90)
                timestamp = time.time()
                if humidity > 80:
                    message = f'HUMIDITY|{humidity}|{timestamp}'
                    s.sendto(message.encode(), (self.gateway_host, self.humidity_gateway_port))
                time.sleep(1)


if __name__ == "__main__":
    gateway_host = 'localhost'
    temperature_gateway_port = 5555  # Bu portu değiştirebilirsiniz, ancak gateway ile aynı olmalı
    humidity_gateway_port = 5556  # Bu portu değiştirebilirsiniz, ancak gateway ile aynı olmalı

    temperature_sensor = TemperatureSensor(gateway_host, temperature_gateway_port)
    humidity_sensor = HumiditySensor(gateway_host, humidity_gateway_port)

    threading.Thread(target=temperature_sensor.start).start()
    threading.Thread(target=humidity_sensor.start).start()
