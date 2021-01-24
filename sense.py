#!/usr/bin/env python3
from sds011 import *
import csv
import datetime
import time
import sys
import os
import logging

sensor = SDS011("/dev/ttyUSB0")

WARMUP_SEC = 15
INTERVAL_SEC = 60
OUTPUT = "samples.csv"

addHeader = True

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')

def takeReadings(sensor, n=3): 
    # run for 15 seconds to get ready to make a reading
    logging.info("warming up sensor")
    sensor.sleep(sleep=False)
    time.sleep(WARMUP_SEC)

    pmt_2_5 = 0
    pmt_10 = 0
    for i in range (n):
        x = sensor.query()
        logging.info("read values:" + str(x))
        pmt_2_5 = pmt_2_5 + x[0]
        pmt_10 = pmt_10 + x[1]
        time.sleep(2)
    pmt_2_5 = round(pmt_2_5/n, 1)
    pmt_10 = round(pmt_10/n, 1)
    sensor.sleep(sleep=True)

    return pmt_2_5, pmt_10

def main():
    if not os.path.exists(OUTPUT):
        logging.info("creating file " + OUTPUT)
        with open(OUTPUT, 'w'):
            pass

    with open(OUTPUT) as f:
        first_line = f.readline()
        if first_line:
            addHeader = False

    with open(OUTPUT, "a") as file:
        writer = csv.writer(file, delimiter = ",")
        if addHeader:
            writer.writerow(["date", "pm25", "pm10"])

        while True:
            try: 

                # get reading
                reading = takeReadings(sensor, 3)

                logging.info("got averaged value:" + str(reading))
                if reading:
                    writer.writerow([datetime.datetime.now().isoformat(), *reading])
                    file.flush()

                logging.info("sleeping " + str(INTERVAL_SEC - WARMUP_SEC) + " seconds")
                # wait until next reading
                time.sleep(INTERVAL_SEC - WARMUP_SEC)
            except KeyboardInterrupt:
                logging.info("interrupted; turning off sensor")
                try:
                    sensor.sleep()  # Turn off fan and diode
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)

if __name__ == '__main__':
    main()
