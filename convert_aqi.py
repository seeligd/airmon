 #!usr/bin/env python3

import sys
import csv
import aqi

def conv_aqi(pmt_2_5, pmt_10):
    try:
        aqi_2_5 = aqi.to_iaqi(aqi.POLLUTANT_PM25, str(pmt_2_5))
        aqi_10 = aqi.to_iaqi(aqi.POLLUTANT_PM10, str(pmt_10))
        return aqi_2_5, aqi_10
    except:
        return 600, 600

data = sys.stdin.readlines()

with open("all.csv", "w") as file:
    writer = csv.writer(file, delimiter = ",")
    writer.writerow(["date", "PM2.5", "PM10", "AQI (PM2.5)", "AQI (PM10)"])

    first = True
    for line in csv.reader(data):
        #print(line)
        if first:
            first = False
            continue
        writer.writerow([line[0], line[1], line[2], *conv_aqi(line[1],line[2])])
