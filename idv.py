#!/usr/bin/env python

# Import Modules for Runtime
import os
from os import listdir
from os.path import isfile, join
import glob
import time
from time import sleep
import RPi.GPIO as GPIO
import bluetooth
from thread import *
import sox
import subprocess
import signal
from gpiozero import Button, LED
from signal import pause

# Global Variables
blueSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
clientSocket = None
activeDir = '/home/pi/Desktop/Darth'
btData = ''

# Configure GPIO Pins
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(12, GPIO.OUT)

def one_pressed():
        global one_start
        print("Button one pressed")
        if two.is_pressed: print("BOTH")
        one_start = time.time()
        
def one_released():
        global one_start, p, counter
        print("Button one released")
        print(time.time() - one_start)
        #tfm.preview('playback.wav')
        if p.poll() is None:
                p.send_signal(signal.SIGINT)
                sleep(0.5)
        opn = "/home/pi/Desktop/Darth/audio_numbers/%d.wav" % counter
        #p = subprocess.Popen(['play',opn])
        #p.wait()
        p = subprocess.Popen(['play',audiolist[counter]])
        counter = counter+1
        if (counter == top): counter = 0
def two_pressed():
        global two_start
        print("Button two pressed")
        if one.is_pressed: print("BOTH")
        two_start = time.time()
        
def two_released():
        global two_start, p, counter
        print("Button two released")
        print(time.time() - two_start)
        if p.poll() is None:
                p.send_signal(signal.SIGINT)
                sleep(0.4)
        counter = counter-1
        opn = "/home/pi/Desktop/Darth/audio_numbers/%d.wav" % counter
        #p = subprocess.Popen(['play',opn])
        #p.wait()
        p = subprocess.Popen(['play',audiolist[counter]])

def reboot():
        os.system("sudo reboot")

def hardwareThread():
	one.when_pressed = one_pressed
	one.when_released = one_released
	two.when_pressed = two_pressed
	two.when_released = two_released
	three.when_held = reboot
	
def convertAudioThread():

	while True:		
		try:
			# M4A audio to convert
			convert = max(glob.iglob('*m4a'), key = os.path.getctime)
			# Break if no more files
			if not convert:
				break
			# Output WAV filename
			outputFile =  convert[:convert.index('.m4a')] + '.wav'
			# Convert M4A to WAV
			os.system('ffmpeg -y -i "' + convert + '" "' + outputFile +'"')
			# Cleanup M4A File
			os.system('rm "' + convert + '"')
		except Exception, cE:
			print cE
			break

def audioPullThread():
	os.system('wget -r -N --no-parent --reject *index.html* -P /home/pi/Desktop/Darth '
	+ '-nH --cut-dirs=1 http://107.170.41.241/upload/')
	# Convert Audio Silently
	start_new_thread(convertAudioThread,())

def blueClientThread(clientSocket):

	# Client commands
	while True:
		
		# Accept Command
		btData = str(clientSocket.recv(1024))
		#print btData


		# Execute Server Refresh Command
		if ('<rfDv>' in btData):
			start_new_thread(audioPullThread,())
		# Execute Directory Refresh Command
		elif ('<rfDir>' in btData):
			print "Received [%s]" % btData
			vaderFiles = glob.iglob('*wav') #[f for f in listdir(activeDir) if isfile(join(activeDir, f))]
			for i in vaderFiles:
				btData = clientSocket.recv(1024)
				if (btData == '<stop>'):
					break
				clientSocket.send('<' + i + '>')
				print i
			clientSocket.send('<stop>')

		# Play Sound
		elif ('<dvPlay>' in btData):
			print "Received [%s]" % btData
			btData = clientSocket.recv(1024)
			try:
				os.system('play "' + btData[btData.index('<')+1:btData.index('>')] + '" </dev/null &>/dev/null &')
			except Exception, recE:
				print "Received [%s]" % btData
				"Error: " + recE
		
		# Play Modulated Sound		
		elif ('<modPlay>' in btData):
			print "Received [%s]" % btData
			btData = clientSocket.recv(1024)
			os.system('play "' + btData[btData.index('<')+1:btData.index('>')] + '" pitch -921 speed 1.09 bass 10 overdrive 20 loudness -10 echo 0.7 1 55 0.5 </dev/null &>/dev/null &')
		

		# Escape loop if disconnected
		elif not btData:
			break

	# Disconnect if loop escapes
	clientSocket.close


########################
#### Main Function #####
#  Runtime Execution   #
########################

input = ''

start_new_thread(audioPullThread,())

one = Button(23)
two = Button(24)
three = Button(25, hold_time=2)
led = LED(16)

one_start=0
two_start=0
counter = 0

tfm = sox.Transformer()
tfm.pitch(-8.0)
tfm.gain(+2,limiter=True)

audiolist = glob.glob("/home/pi/Desktop/Darth/*.wav")
audiolist.sort(key=os.path.getmtime)
top = len(audiolist)

p = subprocess.Popen(['play','playback.wav </dev/null &>/dev/null &'])

start_new_thread(hardwareThread,())

try:	
	# Bind Bluetooth Socket
	blueSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	blueSocket.bind(("",25))
	blueSocket.listen(1)

except Exception, bindE:
	print bindE

print "SYS: Entering idvOS"
while True:
	try:
		try:
			# Attempt to establish a bluetooth connection
			clientSocket,address = blueSocket.accept()
			print "Accepted connection from ", address
		
			# Open client in new thread
			start_new_thread(blueClientThread ,(clientSocket,))
		
		except Exception, accE:
			# Connection attempt unsuccessful
			print 'Bluetooth: ' + accE

	except Exception, bigE:
		print 'SEVERE: Failure in idvOS runtime. Exceptions thrown \n\n' + bigE

blueSocket.close()
