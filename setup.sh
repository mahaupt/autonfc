#!/bin/bash

rm "/etc/modprobe.d/ftdi.conf"
touch "/etc/modprobe.d/ftdi.conf"
echo "blacklist ftdi_sio" >> "/etc/modprobe.d/ftdi.conf"
echo "blacklist usbserial" >> "/etc/modprobe.d/ftdi.conf"

groupadd usb_access
usermod -a -G dialout marcel
usermod -a -G usb_access marcel
usermod -a -G video marcel

apt install python3 python3-pip libgl1 libzbar0
pip install -r requirements.txt

cat <<EOT >> /root/.bashrc
if [ \$(tty) == /dev/tty1 ]; then
  python3 $(pwd)/main.py
fi
EOT

# TODO
# edit /etc/inittab
# scroll down to
# 1:2345:respawn:/sbin/getty 115200 tty1
# change to
# #1:2345:respawn:/sbin/getty 115200 tty1
# add line
# 1:2345:respawn:/bin/login -f root tty1 </dev/tty1 >/dev/tty1 2>&1