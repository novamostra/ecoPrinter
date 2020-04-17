#!/bin/bash
# Setup Script for ecoPrinter
# author: novamostra
# April 2020

echo enable_uart=1 | tee -a /boot/config.txt
echo gpu_mem=16 | tee -a /boot/config.txt
echo dtoverlay=dwc2 | tee -a /boot/config.txt

sed -i 's/console=serial0,115200 //' /boot/cmdline.txt

echo 'dwc2' | tee -a /etc/modules
echo 'libcomposite' | tee -a /etc/modules

apt-get update
apt-get upgrade -y
apt-get install python3-pip -y

pip3 install rpi_ws281x adafruit-circuitpython-neopixel

mkdir -p /usr/bin/nm_gadget
mv gadget/ecoPrinter /usr/bin/nm_gadget/ecoPrinter
chmod +x /usr/bin/nm_gadget/ecoPrinter

sed -i '/exit 0/i\/usr\/bin\/nm_gadget\/ecoPrinter' /etc/rc.local

apt-get install ghostscript -y
apt-get install obexftp -y

pip3 install nfcpy

# get bluetooth mac address
(echo "Address =" `hciconfig | grep -oP -m 1 '(?s)(?<=BD Address: ).*(?= ACL)'`) | tee -a code/ecoPrinter.conf

chmod +x code/ecoPrinter.sh

sed -i "/exit 0/i$PWD/code\/ecoPrinter.sh" /etc/rc.local





