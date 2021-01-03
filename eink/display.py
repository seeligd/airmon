from waveshare_epd import epd2in7
from PIL import Image,ImageDraw,ImageFont
import time
import logging
import requests
import urllib.request, json

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

logging.basicConfig(level=logging.DEBUG)
epd = epd2in7.EPD()
epd.init()
image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)    # 255: clear the image with white

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
    #font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)

    draw.text((20, 50), string, fill = 0)
    #draw.rectangle((epd2in7.EPD_WIDTH/2-10, epd2in7.EPD_HEIGHT/2-10, epd2in7.EPD_WIDTH/2+10, epd2in7.EPD_HEIGHT/2+10), fill = 0)
    print('update display')
    epd.display(epd.getbuffer(image))
    #epd.sleep()
    #epd.display_frame(epd.get_frame_buffer(image))

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

    #epd = epd2in7.EPD()
    
    logging.info("init and Clear")
    #epd.init()
    epd.Clear(0xFF)

    Himage = Image.open(fname)
    epd.display(epd.getbuffer(Himage))
    #time.sleep(10)

    logging.info("done")

    logging.info("Goto Sleep...")
    #epd.sleep()

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
            lastRun = time.time() - 100
            time.sleep(0.2)
        elif key4state == False:
            print('Key4 Pressed')
            lastOne = "Stats"
            lastRun = time.time() - 100
            time.sleep(0.2)

        else:
            if time.time() - lastRun > 60 * 10:
                lastRun = time.time()
                time.sleep(.2)
                if lastOne == "Graph":
                    getGraph()
                elif lastOne == "Stats":
                    updateDisplay(getSummary())

if __name__ == '__main__':
    main()
