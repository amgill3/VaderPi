#!/usr/bin/env bash
#VaderPi installion script

## Run pre-install checks ##

me=$(whoami)

sudo apt-get update
sudo apt-get upgrade

## Install necessary dependencies ##

## Install sox ##
sudo apt-get --force-yes --yes install sox
sudo apt-get --force-yes --yes install libsox-fmt-mp3
sudo pip install glob2

## Install bluetooth ##
sudo apt-get --force-yes --yes install python-pexpect python-bluez bluetooth bluez

## Install AWS ##
sudo pip install awscli
sudo pip install paho-mqtt

## Startup Services ##
sudo cp lipopi/lipopi.service /etc/systemd/system/
sudo systemctl enable lipopi.service
sudo systemctl start lipopi.service

sudo cp scripts/idv.service /etc/systemd/system/
sudo systemctl enable idv.service
sudo systemctl start idv.service

## Move folders ##
mv scripts /home/pi/
mv lipopi /home/pi/

## Setup WiFi Direct ##
git clone http://github.com/amgill3/provision.git
cd provision
sudo ./provision iptables node wifi-connect
sudo BRANCH=next rpi-update

## Setup Audio DAC ##
curl -sS https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh | bash
