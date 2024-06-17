#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time

RPM_FILE = '/var/run/fan_rpm.txt'  # File to read the current RPM value

def read_rpm():
    if os.path.exists(RPM_FILE):
        with open(RPM_FILE, 'r') as f:
            rpm = f.read()
            try:
                rpm = int(float(rpm))  # Konvertiert in eine Ganzzahl
                print(f"Current RPM: {rpm}")
            except ValueError:
                print("Invalid RPM value in file.")
    else:
        print("RPM file not found. Is the fan control service running?")

if __name__ == "__main__":
    try:
        while True:
            read_rpm()
            time.sleep(1)  # Delay to prevent constant reading
    except KeyboardInterrupt:   # trap a CTRL+C keyboard interrupt
        print("\nExiting...")  # Optional: Inform the user that the script is exiting