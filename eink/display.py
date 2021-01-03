from waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
import time
import datetime
import logging
import requests
import urllib.request, json
import RPi.GPIO as GPIO

TEST = False

GPIO.setmode(GPIO.BCM)

logging.basicConfig(level=logging.DEBUG)

if not TEST:
    epd = epd2in7.EPD()
    epd.init()
image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white
font = ImageFont.truetype('gotham_med.ttf', 16)
fontSmall = ImageFont.truetype('gotham_med.ttf', 12)
fontMicro = ImageFont.truetype('gotham_med.ttf', 10)

UPDATE_INTERVAL = 10 * 60 # 10 min

key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def updateDisplay(string):
    draw = ImageDraw.Draw(image)
    draw.text((20, 50), string, font = font, fill = 0)
    #draw.rectangle((epd2in7.EPD_WIDTH/2-10, epd2in7.EPD_HEIGHT/2-10, epd2in7.EPD_WIDTH/2+10, epd2in7.EPD_HEIGHT/2+10), fill = 0)
    if not TEST:
        epd.Clear(0xFF)
        epd.display(epd.getbuffer(image))

def download(fname, url):
    r = requests.get(url, allow_redirects=True)
    open(fname, 'wb').write(r.content)

def getSummary():
    with urllib.request.urlopen("http://rhubarb:5000/summary") as url:
        #data = json.loads(url.read().decode())
        return url.read().decode()
        #print(data)

def getGraph():
    #urllib.error.HTTPError: HTTP Error 500: INTERNAL SERVER ERROR
    logging.info("downloading graph")
    fname = 'outside.png'
    url = 'http://rhubarb:5000/static/eink_output.png'
    download(fname, url)

    image = Image.open(fname)

    draw = ImageDraw.Draw(image)

    response = json.loads(getSummary())
    lastUpdated = response.get('Updated')
    if lastUpdated:
        lastUpdated = datetime.datetime.fromisoformat(lastUpdated).strftime("%a %b %d %I:%M%p")
    aqi24 = response.get('AQI_2.5_24')
    aqiNow = response.get('AQI_2.5_Now')
    if aqi24 and aqiNow:
        draw.text((0, 2), 'AQI 24h:', font = fontSmall, fill = 0)
        draw.text((57, 0), str(aqi24), font = font, fill = 0)
        draw.text((80, 2), 'now:', font = fontSmall, fill = 0)
        draw.text((113, 0), str(aqiNow), font = font, fill = 0)

    draw.text((160, 4), lastUpdated, font = fontMicro, fill = 0)
    image.save("output.png", "PNG")

    if not TEST:
        epd.Clear(0xFF)
        epd.display(epd.getbuffer(image))

def main():
    lastRun = time.time() - 100
    lastOne = None

    while True:
        key1state = GPIO.input(key1)
        key2state = GPIO.input(key2)
        key3state = GPIO.input(key3)
        key4state = GPIO.input(key4)

        if key1state == False:
            print('Key1 Pressed')
            time.sleep(0.2)
        elif key2state == False:
            print('Key2 Pressed')
            time.sleep(0.2)
        elif key3state == False:
            print('Key3 Pressed')
            lastOne = "Graph"
            getGraph()
            time.sleep(0.2)
        elif key4state == False:
            print('Key4 Pressed')
            lastOne = "Stats"
            updateDisplay(getSummary())
            time.sleep(0.2)

        else:
            if time.time() - lastRun > UPDATE_INTERVAL:
                lastRun = time.time()
                time.sleep(.2)
                if lastOne == "Graph":
                    getGraph()
                elif lastOne == "Stats":
                    updateDisplay(getSummary())

if __name__ == '__main__':
    main()
