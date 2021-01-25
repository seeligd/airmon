from PIL import Image,ImageDraw,ImageFont
import time
import datetime
import logging
import requests
import urllib.request, json
import urllib

TEST = False

OUTDOOR=('http://rhubarb:5000/static/eink_graph.png', 'http://rhubarb:5000/summary')
INDOOR=('http://burdock:5000/static/eink_graph.png', 'http://burdock:5000/summary')

logging.basicConfig(level=logging.INFO,format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
key1 = 5
key2 = 6
key3 = 13
key4 = 19

if not TEST:
    from waveshare_epd import epd2in7
    import RPi.GPIO as GPIO
    epd = epd2in7.EPD()
    epd.init()

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


fontFile = 'PierSans-Bold.otf'
font = ImageFont.truetype(fontFile, 16)
fontSmall = ImageFont.truetype(fontFile, 12)
fontMicro = ImageFont.truetype(fontFile, 10)

UPDATE_INTERVAL = 10 * 60 # 10 min


def updateDisplay(url):
    if not TEST:
        epd.Clear(0xFF)

    image = Image.new('1', (264, 176), 255)    # 255: clear the image with white

    summary = getSummary(url)
    draw = ImageDraw.Draw(image)
    draw.text((5, 50), summary, font = fontSmall, fill = 0)
    addName(url, draw)

    image.save("output.png", "PNG")

    if not TEST:
        epd.display(epd.getbuffer(image))

def download(fname, url):
    r = requests.get(url, allow_redirects=True)
    open(fname, 'wb').write(r.content)

def getSummary(url):
    try:
        with urllib.request.urlopen(url) as url:
            #data = json.loads(url.read().decode())
            return url.read().decode()
            #print(data)
    except urllib.error.HTTPError:
        return "{}"

def addName(url, draw):
    urlMap = {
            INDOOR[0]: 1,
            OUTDOOR[0]: 2,
            INDOOR[1]: 3,
            OUTDOOR[1]: 4,
    }
    urlMapName = {
            INDOOR[0]: 'inside',
            OUTDOOR[0]: 'outside',
            INDOOR[1]: 'inside stats',
            OUTDOOR[1]: 'outside stats',
    }

    draw.text((8, 162), str(urlMap.get(url)) + "/4 - " + urlMapName.get(url), font = fontMicro, fill = 0)

def getGraph(url):
    if not TEST:
        epd.Clear(0xFF)

    logging.info("downloading graph: " + url)
    fname = 'outside.png'
    download(fname, url)
    graph = Image.open(fname)
    
    image = Image.new('1', (264, 176), 255)    # 255: clear the image with white
    image.paste(graph, (10, 0))

    draw = ImageDraw.Draw(image)

    summaryURL = OUTDOOR[1]
    if url == INDOOR[0]:
        summaryURL = INDOOR[1]

    response = json.loads(getSummary(summaryURL))
    lastUpdated = response.get('Updated')
    if lastUpdated:
        lastUpdated = datetime.datetime.fromisoformat(lastUpdated).strftime("%a %b %d %I:%M%p")
    aqi24 = response.get('AQI_2.5_24')
    aqiNow = response.get('AQI_2.5_Now')
    if aqi24 and aqiNow:
        draw.text((6, 2), 'AQI 24h:', font = fontSmall, fill = 0)
        draw.text((63, 0), str(aqi24), font = font, fill = 0)
        draw.text((86, 2), 'now:', font = fontSmall, fill = 0)
        draw.text((119, 0), str(aqiNow), font = font, fill = 0)

    draw.text((160, 4), lastUpdated if lastUpdated else '> Error Updating...', font = fontMicro, fill = 0)
    addName(url, draw)
    image.save("output.png", "PNG")

    if not TEST:
        epd.display(epd.getbuffer(image))

def main():
    logging.info("starting...")
    lastRun = time.time() - 100
    lastOne = OUTDOOR[0]

    while True:
        if not TEST:
            key1state = GPIO.input(key1)
            key2state = GPIO.input(key2)
            key3state = GPIO.input(key3)
            key4state = GPIO.input(key4)

        if key1state == False:
            logging.info('Key1 Pressed')
            lastOne = INDOOR[0]
            getGraph(lastOne)
            time.sleep(0.2)
        elif key2state == False:
            logging.info('Key2 Pressed')
            lastOne = OUTDOOR[0]
            getGraph(lastOne)
            time.sleep(0.2)
        elif key3state == False:
            logging.info('Key3 Pressed')
            lastOne = INDOOR[1]
            updateDisplay(lastOne)
            time.sleep(0.2)
        elif key4state == False:
            logging.info('Key4 Pressed')
            lastOne = OUTDOOR[1]
            updateDisplay(lastOne)
            time.sleep(0.2)

        else:
            currentHour = datetime.datetime.now().hour
            if time.time() - lastRun > UPDATE_INTERVAL and currentHour > 6:
                lastRun = time.time()
                time.sleep(.2)
                if lastOne in [INDOOR[0], OUTDOOR[0]]:
                    getGraph(lastOne)
                elif lastOne in [INDOOR[1], OUTDOOR[1]]:
                    updateDisplay(lastOne)

if __name__ == '__main__':
    if TEST:
        #updateDisplay(OUTDOOR[1])
        getGraph(OUTDOOR[0])
    else:
        main()
