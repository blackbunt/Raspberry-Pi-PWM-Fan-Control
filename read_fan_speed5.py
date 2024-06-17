#!/usr/bin/python
# -*- coding: utf-8 -*-
from gpiozero import DigitalInputDevice
from signal import pause
import time
import socket

# Pin configuration
TACH_PIN = 17   # Fan's tachometer output pin
PULSE = 2       # Noctua fans puts out two pulses per revolution
WAIT_TIME = 1   # [s] Time to wait between each refresh
RPM_FILE = '/var/run/fan_rpm.txt'  # File to store the current RPM value

# Setup variables
t = time.time()
rpm = 0

# Setup GPIO
tach = DigitalInputDevice(TACH_PIN, pull_up=True)

# Calculate pulse frequency and RPM
def fell():
    global t
    global rpm

    dt = time.time() - t
    if dt < 0.005:
        return  # Reject spuriously short pulses

    freq = 1 / dt
    rpm = (freq / PULSE) * 60
    t = time.time()

    # Write the RPM value to a file
    with open(RPM_FILE, 'w') as f:
        f.write(str(rpm))

# Add event to detect
tach.when_activated = fell

try:
    while True:
        time.sleep(WAIT_TIME)
        print("%.f RPM" % rpm)
        rpm = 0

except KeyboardInterrupt:  # trap a CTRL+C keyboard interrupt
    print("Cleanup")
finally:
    # Clean up and remove the RPM file
    GPIO.cleanup()
    if os.path.exists(RPM_FILE):
        os.remove(RPM_FILE)