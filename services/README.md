## Services 
```
sudo cp airmon-web.service /lib/systemd/system/airmon-web.service
sudo systemctl daemon-reload
sudo systemctl enable airmon-web.service
sudo systemctl start airmon-web.service
sudo systemctl status airmon-web.service

sudo cp airmon-sense.service /lib/systemd/system/airmon-sense.service
sudo systemctl daemon-reload
sudo systemctl enable airmon-sense.service
sudo systemctl start airmon-sense.service
sudo systemctl status airmon-sense.service

sudo cp airmon-eink.service /lib/systemd/system/airmon-eink.service
sudo systemctl daemon-reload
sudo systemctl enable airmon-eink.service
sudo systemctl start airmon-eink.service
sudo systemctl status airmon-eink.service

# add to crontab to check for network connectivity every 5 minutes
#*/5 * * * * /usr/bin/sudo -H /home/pi/code/airmon/services >> /dev/null 2>&1
```
