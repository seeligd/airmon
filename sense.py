#!/usr/bin/env python3

from sds011 import *
import csv
import datetime
import time


sensor = SDS011("/dev/ttyUSB0")

WARMUP_SEC = 15
INTERVAL_SEC = 60

with open("samples.csv", "a") as file:
    writer = csv.writer(file, delimiter = ",")
    writer.writerow(["date", "pm25", "pm10"])

    # 1 week
    end = time.time() + 60 * 60 * 24 * 7
    while True:
        if time.time() > end:
            break
        else:
            # run for 15 seconds to get ready to make a reading
            sensor.sleep(sleep=False)
            time.sleep(WARMUP_SEC)

            # get reading
            reading = sensor.query()  # Gets (pm25, pm10)
            sensor.sleep()  # Turn off fan and diode
            writer.writerow([datetime.datetime.now().isoformat(), *reading])
            file.flush()

            # wait until next reading
            time.sleep(INTERVAL_SEC - WARMUP_SEC)
