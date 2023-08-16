#! /usr/bin/env python3
import RPi.GPIO as GPIO
import time
import signal
import sys

# The Noctua PWM control actually wants 25 kHz (kilo!), see page 6 on:
# https://noctua.at/pub/media/wysiwyg/Noctua_PWM_specifications_white_paper.pdf
# However, the RPi.GPIO library causes high CPU usage when using high
# frequencies - probably because it can currently only do software PWM.
# So we set a lower frequency in the 10s of Hz here. You should expect that
# this value doesn't work very well and adapt it to what works in your setup.
# We will work on the issue and try to use hardware PWM in the future:
PWM_FREQ = 25           # [Hz] PWM frequency

# Scan-Station Options
FAN_PIN = 18            # BCM pin used to drive PWM fan don't forget to add a PULLDOWN Resistor 10kOhm to Ground!
WAIT_TIME = 1           # [s] Time to wait between each refresh

FAN_RUN_TIME = 60       # [s] Time to drive the fan (minimal time)
OFF_TEMP = 40           # [°C] temperature below which to stop the fan
MIN_TEMP = 45           # [°C] temperature above which to start the fan
MAX_TEMP = 60           # [°C] temperature at which to operate at max fan speed
FAN_LOW = 1
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100
FAN_GAIN = float(FAN_HIGH - FAN_LOW) / float(MAX_TEMP - MIN_TEMP)

# Zustandsvariable und Zeitstempel
fan_running = False
fan_start_time = None


def getCpuTemperature():
    with open('/sys/class/thermal/thermal_zone0/temp') as f:
        return float(f.read()) / 1000


def handleFanSpeed(fan, temperature):
    global fan_running, fan_start_time

    if temperature > MIN_TEMP:
        delta = min(temperature, MAX_TEMP) - MIN_TEMP
        fan.start(FAN_LOW + delta * FAN_GAIN)
        
        if not fan_running:
            fan_running = True
            fan_start_time = time.time()

    elif temperature < OFF_TEMP:
        # Wenn der Lüfter bereits läuft, überprüfen, ob er seit mindestens 60 Sekunden läuft
        if fan_running and (time.time() - fan_start_time < FAN_RUN_TIME):
            return
        else:
            fan.start(FAN_OFF)
            fan_running = False


def shutdown_handler(signal, frame):
    GPIO.output(FAN_PIN, GPIO.LOW)
    sys.exit(0)


if "--shutdown" in sys.argv:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT)
    GPIO.output(FAN_PIN, GPIO.LOW)
    GPIO.cleanup()
    sys.exit()


try:
    signal.signal(signal.SIGTERM, shutdown_handler)
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
    while True:
        handleFanSpeed(fan, getCpuTemperature())
        time.sleep(WAIT_TIME)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
