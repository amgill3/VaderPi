

## VaderPi Installation ## 
- Files necessary to setup a VaderPi and connect to AWS

Download the latest Raspbian image from the link provided: https://www.raspberrypi.org/downloads/raspbian/

Load the image onto an SD Card using the following instructions provided by raspberrypi.org:
https://www.raspberrypi.org/documentation/installation/installing-images/README.md

Load the SD Card into the Raspberry Pi and apply power. Once the Pi has booted up:
- Right click on the bluetooth icon in top top right corner and remove it from the panel
- Open

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




Enter the name of the Vader you are setting up and press enter
note: Use the prefix "vader-" before the name to ensure that the name is available ie. "vader-blackspace"
Using the opened csv file copy and paste the Access ID into the prompt and press enter
repeat for the Access Key


connmanctl enable bluetooth

## Wiring ##



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
