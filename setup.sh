#!/bin/bash

rm "/etc/modprobe.d/ftdi.conf"
touch "/etc/modprobe.d/ftdi.conf"
echo "blacklist ftdi_sio" >> "/etc/modprobe.d/ftdi.conf"
echo "blacklist usbserial" >> "/etc/modprobe.d/ftdi.conf"

usermod -a -G dialout ubuntu
usermod -a -G video ubuntu

apt install python3 python3-pip libgl1 libzbar0
pip install -r requirements.txt

cat <<EOT >> /root/.bashrc
if [ \$(tty) == /dev/tty1 ]; then
  cd $(pwd)
  python3 main.py
fi
EOT

# TODO
# copy contents of "/lib/systemd/system/getty@.service"
# launch "systemctl edit getty@tty1.service"
# Change the ExecStart=- line to "/sbin/agetty -a $DESIRED_USERNAME --noclear %I $TERM"
