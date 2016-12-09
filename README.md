

## VaderPi Installation ##
- Files necessary to setup a VaderPi and connect to AWS

Download the latest Raspbian image from the link provided: https://www.raspberrypi.org/downloads/raspbian/

Load the image onto an SD Card using the following instructions provided by raspberrypi.org:
https://www.raspberrypi.org/documentation/installation/installing-images/README.md

Load the SD Card into the Raspberry Pi and apply power. Once the Pi has booted up:
- Right click on the bluetooth icon in top top right corner and remove it from the panel
- Open the menu in the top left
 - Preferences
 - Mouse and Keyboard Settings
 - Keyboard Tab (Click Keyboard Layout)
 - Set the layout to United States - English (US)

ENSURE THAT THE PI IS CONNECTED TO THE INTERNET BY ETHERNET TO PERFORM THE REST OF THE STEPS

Perform the following commands using the command prompt.
- git clone https://github.com/amgill3/VaderPi.git
- cd VaderPi
- chmod 777 install.sh
- ./install.sh
(make sure to type 'y' for 'yes' when asked)

Once the Pi has rebooted 

Using the browser on the Pi, Login to the AWS console: https://console.aws.amazon.com/console/home
- Find and Click on the link to open IAM
- On the left panel click on Users
- Click on Vaders
- Open the Security Credentials Tab
- Click on Create access key
- download the .csv file and open it for later use

Perform the following commands using the command prompt.
 - sudo aws configure
  - Using the opened csv file copy and paste the Access ID into the prompt and press enter
repeat for the Access Key
  - Type: 'us-west-2' for region
  - Leave output format blank
 - connmanctl enable bluetooth
 - sudo nano /etc/bluetooth/main.conf
   - navigate down to Discoverable Timout and remove the '#' in front
   - Crtl X (To Exit)
   - 'y' for yes
   - Press Enter
 - Create a name for the new vader - note: Use the prefix "vader-" before the name to ensure that the name is available. example: "vader-blackspace"
  - sudo aws s3 mb s3://'new vader name goes here'
 - ifconfig wlan0
  - Take note of the HWaddr along with the accosicated Pi (vader name)
   - In some cases to setup wifi such as on a school network they will need this address to bypass web-sign in

Open the file manager
 - Open scripts folder
 - Open idv.py
  - Scroll down to vader_name and edit to the new vader name
  - note: Use the prefix "vader-" before the name to ensure that the name is available. example: "vader-blackspace"

THE VADER SOFTWARE IS NOW SETUP YOU CAN REBOOT OR SHUTDOWN THE PI AND PROCEED WITH HARDWARE
 - Reboot - sudo reboot
 - Shutdown - sudo shutdown now

## Wiring ##

- Wiring the Audio Amplifier

Helpful instructions can be found at the links below:
 - https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/assembly
 - https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/raspberry-pi-wiring
  
- Wiring the Power Circuit
 ![circuit](https://raw.github.com/amgill3/VaderPi/master/pictures/powercircuit.png)
  
- Wiring the Playback Buttons
 ![circuit](https://raw.github.com/amgill3/VaderPi/master/pictures/button_bb.png)
 ![circuit](https://raw.github.com/amgill3/VaderPi/master/pictures/button_schem.png)



## Functionality ##
- How the Raspberry Pi operates

Top Button
- Single Press
  - Plays an audio file moving forward through the playlist
  
Middle Button
- Single Press
  - Plays an audio file moving backwards through the playlist
- Long Press (Two Seconds)
  - Switches the explicit playback mode
  
(Holding both the top and middle button for a couple seconds will allow you to pair an android device to the Pi)

Bottom Button - Power Button
(used to turn the Pi off and On)

When the Pi is removed from the Ethernet and not connected to a Wifi Network it will create a hotspot called VaderPi
 - On a phone, tablet, or computer with wifi access
  - navigate to connect to a wifi network
  - Select VaderPi
  - Setup the wireless connection
