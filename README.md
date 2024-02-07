# Remote Sensing Application Project

## Overview
This project implements a networked system for a remote sensing application. It includes two sensors (temperature and humidity), a gateway, and a server. The entire system is simulated using software applications without the need for physical hardware.

### Sensors
- **Temperature Sensor**: Simulated sensor generating values between 20-30°C, sends data every second via TCP.
- **Humidity Sensor**: Simulated sensor generating values between 40-90%, sends data when values exceed 80% and an 'ALIVE' message every 3 seconds via UDP.

### Gateway
The gateway application reads sensor values, monitors their activities, and forwards the data with timestamps to the server. It also sends alerts if sensors fail to communicate within specified time frames.

### Server
The server, connected to the gateway, stores all sensor data and features a web interface accessible via `http://localhost:8080`. It displays temperature and humidity data and optionally allows user-triggered humidity data requests.

## Implementation
Implemented in [Python](Python). Utilizes socket programming and multi-threaded server processes without external libraries.

Here's a concise guide for running the applications in your project:

## Running the Applications

1. **Temperature Sensor & Humidity Sensor**
   - Open a terminal.
   - Navigate to the sensor directory.
   - Run the application using `python sensor_apps.py`.
   - The sensor will start sending data every second.
   - The sensor will send data on exceeding 80% humidity and an 'ALIVE' message every 3 seconds.

2. **Gateway**
   - Open a third terminal.
   - Navigate to the gateway directory.
   - Start the gateway using `python gateway.py`.
   - It will receive data from both sensors and forward it to the server.

3. **Server**
   - In a new terminal, go to the server directory.
   - Launch the server with `python server.py`.
   - The server begins storing data and serves the web interface at `http://localhost:8080`.

Make sure Python is installed and ensure that each application is in its correct directory. Modify the commands according to your specific file names if they differ.

## Contributors
- Yasin Sefa Kırman [GitHub Profile](https://github.com/YasinSefa15)
- Doğukan Şahin [GitHub Profile](https://github.com/dogukan-sahin)


## Contact

For any inquiries or collaboration opportunities, feel free to reach out:

- **Email**: [yasekirman@gmail.com](mailto:yasekirman@gmail.com)

Alternatively, you can open an issue in this repository for project-related discussions.
