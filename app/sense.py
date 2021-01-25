#!/usr/bin/env python3
from sds011 import *
import aqi
import csv
import datetime
import time
import sys
import os
import logging
import draw_graph

sensor = SDS011("/dev/ttyUSB0")

WARMUP_SEC = 15
INTERVAL_SEC = 60

SAMPLE_OUTPUT = "./output/samples.csv"
GRAPH_OUTPUT = "./static/eink_output.png"

addHeader = True

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')

def conv_aqi(pmt_2_5, pmt_10):
    try:
        aqi_2_5 = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pmt_2_5))
        aqi_10 = aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pmt_10))
        return aqi_2_5, aqi_10
    except:
        return 600, 600


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
    if not os.path.exists(SAMPLE_OUTPUT):
        logging.info("creating file " + SAMPLE_OUTPUT)
        with open(SAMPLE_OUTPUT, 'w'):
            pass

    with open(SAMPLE_OUTPUT) as f:
        first_line = f.readline()
        if first_line:
            addHeader = False

    with open(SAMPLE_OUTPUT, "a") as file:
        writer = csv.writer(file, delimiter = ",")
        if addHeader:
            #writer.writerow(["date", "pm25", "pm10"])
            writer.writerow(["date", "PM2.5", "PM10", "AQI (PM2.5)", "AQI (PM10)"])

        while True:
            try: 
                # get reading
                reading = takeReadings(sensor, 3)

                logging.info("got averaged value:" + str(reading))
                if reading:
                    writer.writerow([datetime.datetime.now().isoformat(), *reading, *conv_aqi(*reading)])
                    file.flush()
                
                draw_graph.draw_eink_graph(SAMPLE_OUTPUT, GRAPH_OUTPUT)
                logging.info("updated eink graph")

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
