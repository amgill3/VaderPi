# VaderPi
Files necessary to setup a VaderPi and connect to AWS

Download the latest Raspbian image from the link provided below.
https://www.raspberrypi.org/downloads/raspbian/

Load the image onto an SD Card using the following instructions provided by raspberrypi.org.
https://www.raspberrypi.org/documentation/installation/installing-images/README.md

https://console.aws.amazon.com/console/home
Login to the console
Click on the link to open IAM
- On the left panel click on Users
- Click on Vaders
- Open the Security Credentials Tab
- Click on Create access key
- download the .csv file and open it for later use

git clone https://github.com/amgill3/VaderPi.git
cd VaderPi
chmod 777 install.sh
./install.sh
Enter the name of the Vader you are setting up and press enter
note: Use the prefix "vader-" before the name to ensure that the name is available ie. "vader-blackspace"
Using the opened csv file copy and paste the Access ID into the prompt and press enter
repeat for the Access Key


connmanctl enable bluetooth
