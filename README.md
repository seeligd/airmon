# Airmon
This project consists of sensing code, a web server to serve the recorded data values, as well as a small script to drive an e-ink display. In my case I have one indoor sensor and one outdoor sensor, both driven by different raspberry pis. The inside sensor also drives an e-ink display. The keys on the e-ink display select which sensor's graph to view.

## Hardware
- A Raspberry Pi - I used a 3 B+ since it has full-size USB ports
- An SD card and power supply (for the pi)
- A [SDS011 Nova PM sensor](https://www.amazon.com/DEVMO-Precision-Quality-Detection-Compatible/dp/B0899V46SS/ref=sr_1_2?dchild=1&keywords=SDS011&qid=1611473759&sr=8-2)
- I'm using a [Waveshare 2.7" e-Paper HAT](https://www.amazon.com/2-7inch-HAT-Resolution-Electronic-Communicating/dp/B075FQKSZ9) (optional, if you want a phsyical display in additon to a web page)

## Sensing / Serving
### Code
- `start_server.sh` - starts flask web service
- `web.py` - flask web service
- `sense.py` code to take readings from the air sensor; runs indefinitely and writes to
  `output/samples.csv`
  `static/eink_output.png`

```
sudo apt-get install libatlas-base-dev
sudo apt-get install libopenjp2-7
sudo apt install libtiff5
pip install wheel
cd ~/code && git clone git@github.com:ikalchev/py-sds011.git && cd py-sds011 && pip install .
pip install -r requirements.txt
```

## E-Ink Display
- `eink/display.py` code to render e-ink display and respond to touch events
  note: you'll want to update the indoor/outdoor URLs so as to display graphs from other sensors
- [waveshare github](https://github.com/waveshare/e-Paper/blob/master/RaspberryPi_JetsonNano/python/readme_rpi_EN.txt)
```
git clone git@github.com:waveshare/e-Paper.git
pip install e-Paper/RaspberryPi_JetsonNano/python
pip install -r eink/requirements.txt
```

![InAction](images/hardware.jpg)

## Credits:
I used [the following site extensively](https://www.instructables.com/A-Low-cost-IoT-Air-Quality-Monitor-Based-on-Raspbe/)
to build this project 

