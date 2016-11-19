#!/usr/bin/env bash
#VaderPi installion script

Access_Key_ID="AKIAJJZTLOGGEBBUPNWQ"
Secret_Access_Key="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"
Region="us-west-2"

Vader_Name="testvaderthing"

## Run pre-install checks ##

me=$(whoami)

#sudo apt-get update
#sudo apt-get upgrade

## Install necessary dependencies ##

## Install sox ##
#sudo apt-get --force-yes --yes install sox
#pip install git+https://github.com/rabitt/pysox.git
#sudo apt-get --force-yes --yes install libsox-fmt-mp3

## Install bluetooth ##
#sudo apt-get --force-yes --yes install python-pexpect python-bluez bluetooth bluez

## Install AWS ##
sudo pip install awscli
#sudo pip install paho-mqtt
mkdir ~/.aws
touch ~/.aws/config
touch ~/.aws/credentials
echo "[default]" >> ~/.aws/config
echo "region = $Region" >> ~/.aws/config
echo "[default]" >> ~/.aws/credentials
echo "aws_access_key_id = $Access_Key_ID" >> ~/.aws/credentials
echo "aws_secret_access_key = $Secret_Access_Key" >> ~/.aws/credentials

## Setup Pi with AWS ##
#aws iot create-thing --thing-name $Vader_Name
#aws iot create-keys-and-certificate --set-as-active --certificate-pem-outfile cert.pem --public-key-outfile publicKey.pem --private-key-outfile privkey.pem

## Setup Audio DAC ##
#mv raspi-blacklist.conf /etc/modprobe.d/
#mv modules /etc/
#mv asound.conf /etc/
#mv config.txt /boot/