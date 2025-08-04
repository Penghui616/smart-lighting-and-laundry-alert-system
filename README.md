# smart-lighting-and-laundry-alert-system
An integrated home automation project that combines energy-efficient smart lighting with a laundry completion alert system. The system uses sensors, Raspberry Pi, and cloud platforms to create a seamless and user-friendly smart home experience.
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
