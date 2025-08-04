# smart-lighting-and-laundry-alert-system
This project was originally developed as two separate individual projects. I designed and implemented the Intelligent Sensor Lighting System, which uses a motion sensor, ambient light sensor, and temperature sensor to automate lighting based on room occupancy, natural light conditions, and ambient temperature.

For example, the system can turn on different types of lights (e.g., warm or cool LEDs) depending on the current temperature, and it can activate alerts (such as a buzzer or flashing lights) in case of abnormal conditions.

Meanwhile, my classmate developed the Laundry Done Alert System, which detects when the washing machine finishes and sends notifications. After both systems were completed, we integrated them into a single smart home solution.

In the final version, the lighting system not only saves energy and improves convenience, but also provides visual notifications (such as flickering lights) when the laundry is done—creating a more interactive and efficient user experience.

PROJECT VIDEO LINK: https://udmercy0-my.sharepoint.com/:v:/g/personal/chenpe3_udmercy_edu/EfWldXh-9LBFjobxOBUc5TsBiALQZTliqOzVgUaG_zsMMQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=B6ftnG

How to Run the Code:
-----------------------
1. source myenv/bin/activate
2. python3 light.py

Dependencies:
----------------
Make sure the following Python libraries are installed:

- RPi.GPIO
- adafruit-circuitpython-dht
- adafruit-circuitpython-apds9960
- requests
- BlynkLib
- board
- busio

To install them, run:
pip install RPi.GPIO adafruit-circuitpython-dht adafruit-circuitpython-apds9960 requests BlynkLib


Setup Instructions:
-----------------------
Hardware Connections:
- PIR motion sensor → GPIO17
- Warm LED → GPIO27
- Cold LED → GPIO5
- Alarm LED → GPIO6
- Buzzer → GPIO13
- DHT11 sensor → GPIO4 (physical pin 7)
- APDS9960 sensor → Connected via I2C (SCL/SDA)

Software Setup:
1. Enable I2C on your Raspberry Pi using:
   `sudo raspi-config` → Interface Options → I2C → Enable

2. Install system packages (if not yet installed):
sudo apt update sudo apt install python3-pip python3-venv python3-dev i2c-tools -y

3. Create a virtual environment:
python3 -m venv myenv source myenv/bin/activate pip install -r requirements.txt # if you have one

FLOWCHART

<img width="440" height="451" alt="image" src="https://github.com/user-attachments/assets/ee5da87c-e38a-40cc-a53b-f0cd86bfff1f" />


Cloud Integration:
-----------------------
- Blynk:
- Connect app to your project using the BLYNK_AUTH token in the code.
- Control switches and temperature/light display on virtual pins V0, V1, V2, V3.

- ThingSpeak:
- Use the provided API key to send motion, light level, LED status, and temperature data.
