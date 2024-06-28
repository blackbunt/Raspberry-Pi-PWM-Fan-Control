#!/usr/bin/python
# -*- coding: utf-8 -*-
from gpiozero import DigitalInputDevice
import time

# GPIO-Pins, die geprüft werden sollen
GPIO_PINS = [4, 17, 18, 27, 22, 23, 24, 25, 5, 6, 12, 13, 19, 16, 26, 20, 21]

# Noctua-Lüfter erzeugen zwei Impulse pro Umdrehung
PULSE = 2
WAIT_TIME = 2  # [s] Wartezeit zwischen jeder Aktualisierung

# Initialisieren der Variablen
t = time.time()
rpm = 0

def calculate_rpm(dt):
    global rpm
    if dt < 0.005:
        return  # Verwerfen von spuriously kurzen Impulsen
    freq = 1 / dt
    rpm = (freq / PULSE) * 60

def detect_event(pin):
    global t
    tach = DigitalInputDevice(pin, pull_up=True)
    tach.when_activated = lambda: calculate_rpm(time.time() - t)
    t = time.time()
    time.sleep(WAIT_TIME)
    if rpm > 0:
        return True
    return False

def cleanup():
    print("Aufräumen...")
    # Hier können weitere Bereinigungsschritte eingefügt werden

try:
    for pin in GPIO_PINS:
        print(f"Prüfe Pin {pin}...")
        rpm = 0

        if detect_event(pin):
            print(f"Ein Lüfter scheint an Pin {pin} angeschlossen zu sein.")
            fan_status = input("Dreht sich der Lüfter gerade? (ja/nein): ").strip().lower()
            if fan_status in ["ja", "j"]:
                fan_speed = input("Dreht sich der Lüfter schnell? (ja/nein): ").strip().lower()
                if fan_speed in ["ja", "j"]:
                    print(f"Lüfter dreht sich schnell. Pin {pin} scheint korrekt zu sein.")
                else:
                    print(f"Lüfter dreht sich langsam. Pin {pin} scheint korrekt zu sein.")
                break
            else:
                print(f"Pin {pin} scheint nicht der richtige zu sein.")
        else:
            print(f"Keine RPM-Werte an Pin {pin} erkannt.")

    else:
        print("Kein Lüfter an den überprüften Pins gefunden.")

except KeyboardInterrupt:
    print("\nBenutzerabbruch erkannt.")

finally:
    cleanup()
