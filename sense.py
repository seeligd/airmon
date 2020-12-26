#!/usr/bin/env python3
from sds011 import *
import csv
import datetime
import time
import sys
import os

sensor = SDS011("/dev/ttyUSB0")

WARMUP_SEC = 15
INTERVAL_SEC = 60
OUTPUT = "samples.csv"

addHeader = True

print(datetime.datetime.now(), "opening", OUTPUT, file=sys.stderr)

with open(OUTPUT) as f:
    first_line = f.readline()
    if first_line:
        addHeader = False

with open("samples.csv", "a") as file:
    writer = csv.writer(file, delimiter = ",")
    if addHeader:
        writer.writerow(["date", "pm25", "pm10"])

    # 1 week
    end = time.time() + 60 * 60 * 24 * 7
    while True:
        if time.time() > end:
            break
        else:
            try: 
                # run for 15 seconds to get ready to make a reading
                print(datetime.datetime.now(), "warming up", file=sys.stderr)
                sensor.sleep(sleep=False)
                time.sleep(WARMUP_SEC)

                # get reading
                reading = sensor.query()  # Gets (pm25, pm10)
                time.sleep(1)

                sensor.sleep()  # Turn off fan and diode

                print(datetime.datetime.now(), "read values:" + str(reading), file=sys.stderr)
                writer.writerow([datetime.datetime.now().isoformat(), *reading])
                file.flush()

                print(datetime.datetime.now(), "sleeping", INTERVAL_SEC - WARMUP_SEC, "seconds", file=sys.stderr)
                # wait until next reading
                time.sleep(INTERVAL_SEC - WARMUP_SEC)
            except KeyboardInterrupt:
                print(datetime.datetime.now(), 'interrupted; turning off sensor')
                try:
                    sensor.sleep()  # Turn off fan and diode
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
