#!/bin/bash

# Crontab script : cf "crontab -l"

d=$(date)
echo $d >> date.log
echo $d > dateee.log
exit 0

WIFI_STATE=$(nmcli networking connectivity)
if [[ $WIFI_STATE != "full" ]]; then
   echo $d >> date_off.log
   netplan apply
   sleep 20
   systemctl restart network-manager
   sleep 20
   IP_WIFI=$(ip a | grep '10.9.1.128' | cut -d '/'  -f 1 | awk '{print $2}')
   if [[ ${#IP_WIFI} == 0 ]];then
      STATE="ERROR"
   else
      STATE=$IP_WIFI
   fi
   (
   echo "From: robot.qa@luos.io"
   echo "To: jerome.galan@luos.io"
   echo "Subject: Wifi Alert on PC QA"
   echo "Content-Type: text/html"
   echo
   echo "<html><b>IP $IP_WIFI </b></html>"   
   echo
   ) | /usr/sbin/sendmail -t
fi

exit 0
