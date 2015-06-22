
#! /bin/bash
#! /etc/init.d/RPSS_start_script.sh

# start the RPSS manager when the pi reboots

python2.7 /home/pi/RPSS/RPSS_Pi_Manager.py > /home/pi/RPSS/Manager_log

