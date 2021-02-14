logger "Checking local network connectivity"
ping -c10 192.168.1.1 > /dev/null
if [ $? != 0 ] 
then
  logger "could not find local network - restarting self"
  sudo /sbin/shutdown -r now
fi
