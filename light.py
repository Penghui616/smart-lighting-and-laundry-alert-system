import time
import RPi.GPIO as GPIO
import board
import busio 
import requests
import adafruit_dht
from adafruit_apds9960.apds9960 import APDS9960
import BlynkLib

# ==== Blynk Configuration ====
BLYNK_AUTH = '-EJ3V8RZ4qp-hqyep4Zy0MU2-3wHNekw'
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# ==== GPIO Pin Definitions ====
PIR_PIN = 17         # PIR motion sensor
WARM_LED_PIN = 27    # Warm light LED
COLD_LED_PIN = 5     # Cool light LED
ALARM_LED_PIN = 6    # Alarm LED
BUZZER_PIN = 13      # Buzzer
DHT_PIN = board.D4   # DHT11 data pin (GPIO4)

# ==== Threshold Settings ====
LIGHT_THRESHOLD = 100           # lux, threshold for darkness
TEMP_THRESHOLD_COLDWARM = 25    # Temperature threshold to switch between warm/cool
TEMP_THRESHOLD_ALARM = 31       # High temperature alarm threshold

# ==== ThingSpeak Configuration ====
THINGSPEAK_API_KEY = "NTQY3ZYUKQY0LDN8"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# ==== GPIO Initialization ====
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(WARM_LED_PIN, GPIO.OUT)
GPIO.setup(COLD_LED_PIN, GPIO.OUT)
GPIO.setup(ALARM_LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.output(WARM_LED_PIN, GPIO.LOW)
GPIO.output(COLD_LED_PIN, GPIO.LOW)
GPIO.output(ALARM_LED_PIN, GPIO.LOW)
GPIO.output(BUZZER_PIN, GPIO.LOW)

# ==== Sensor Initialization ====
i2c = busio.I2C(board.SCL, board.SDA)
apds = APDS9960(i2c)
apds.enable_color = True
dht = adafruit_dht.DHT11(DHT_PIN)
time.sleep(2)

# ==== Control Variables ====
force_on = False         # Force light on
light_color = "cold"     # Default light color
temp = None              # Current temperature

# ==== Blynk Handlers ====
@blynk.on("V0")
def v0_handler(value):
    global force_on
    force_on = bool(int(value[0]))
    print(f"[Blynk] force_on = {force_on}")

@blynk.on("V1")
def v1_handler(value):
    global light_color
    light_color = "warm" if int(value[0]) == 1 else "cold"
    print(f"[Blynk] light_color = {light_color}")

# ==== Upload Function ====
def upload_to_thingspeak(motion, lux, led_status, temp):
    try:
        payload = {
            "api_key": THINGSPEAK_API_KEY,
            "field1": motion,
            "field2": lux,
            "field3": led_status,
            "field4": temp if temp is not None else ""
        }
        requests.post(THINGSPEAK_URL, params=payload, timeout=5)
    except:
        print("[Warning] Failed to upload to ThingSpeak")

# ==== Main Loop ====
last_upload_time = time.time()

try:
    print("System starting... Press Ctrl+C to exit")
    while True:
        blynk.run()
        led_status = 0

        # Step 1: Read Temperature
        try:
            temperature = dht.temperature
            if temperature is not None:
                temp = temperature
                print(f"temperature: {temp} °C")

                blynk.virtual_write(2, temp)  # Send temperature to V2

                if temp >= TEMP_THRESHOLD_ALARM:
                    for _ in range(3):
                        GPIO.output(ALARM_LED_PIN, GPIO.HIGH)
                        GPIO.output(BUZZER_PIN, GPIO.HIGH)
                        time.sleep(0.1)
                        GPIO.output(ALARM_LED_PIN, GPIO.LOW)
                        GPIO.output(BUZZER_PIN, GPIO.LOW)
                        time.sleep(0.1)
                else:
                    GPIO.output(ALARM_LED_PIN, GPIO.LOW)
                    GPIO.output(BUZZER_PIN, GPIO.LOW)
            else:
                print("Failed to read temperature: None returned")
        except Exception as e:
            print("Failed to read temperature:", e)

        # Step 2: Read Motion and Light
        motion = GPIO.input(PIR_PIN)
        lux = apds.color_data[0]
        print(f"motion: {motion}, light: {lux:.2f} lux")
        blynk.virtual_write(3, lux)  # Send light value to V3

        # Step 3: Control Light Logic
        if force_on:
            selected_color = light_color
        else:
            selected_color = "cold" if (temp is not None and temp >= TEMP_THRESHOLD_COLDWARM) else "warm"

        if force_on or (motion == 1 and lux < LIGHT_THRESHOLD):
            GPIO.output(WARM_LED_PIN, GPIO.HIGH if selected_color == "warm" else GPIO.LOW)
            GPIO.output(COLD_LED_PIN, GPIO.HIGH if selected_color == "cold" else GPIO.LOW)
            led_status = 1
        else:
            GPIO.output(WARM_LED_PIN, GPIO.LOW)
            GPIO.output(COLD_LED_PIN, GPIO.LOW)

        # Step 4: Upload Data
        if time.time() - last_upload_time >= 15:
            upload_to_thingspeak(motion, lux, led_status, temp)
            last_upload_time = time.time()

        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting system...")
finally:
    GPIO.cleanup()
