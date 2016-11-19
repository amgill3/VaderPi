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
updatecmd = ['aws', 's3', 'sync', 's3://vader-blackspace', '/home/pi/audio', '--exclude', '"*"', '--include', '"*.mp3"', '--delete']
blueSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
clientSocket = None
activeDir = '/home/pi/scripts'
btData = ''
audiolist = []
top = 0
green = Button(23, hold_time=2)
red = Button(5, hold_time=2)
led = LED(16)

counter = 0

def green_pressed():
        print("Button one pressed")
        if red.is_pressed: print("BOTH")
                
def green_released():
        global p, counter, audiolist, top
        print("Button one released")
        if p.poll() is None:
                p.send_signal(signal.SIGINT)
                sleep(0.5)
        p = subprocess.Popen(['play',audiolist[counter]])
        counter = counter+1
        if (counter == top): counter = 0

def green_held():
        print("Green held")
        
def red_pressed():
        print("Button two pressed")
        if green.is_pressed: print("BOTH")
        
def red_released():
        global p, counter, audiolist, top
        print("Button two released")
        if p.poll() is None:
                p.send_signal(signal.SIGINT)
                sleep(0.4)
        counter = counter-1
        p = subprocess.Popen(['play',audiolist[counter]])

def red_held():
        print("Two held")

def hardwareThread():
	green.when_pressed = green_pressed
	green.when_released = green_released
	green.when_held = green_held
	red.when_pressed = red_pressed
	red.when_released = red_released
	red.when_held = red_held

def createAudiolists():
        global audiolist, top
        audiolist = glob.glob("/home/pi/audio/*.m4a")
        audiolist.sort(key=os.path.getmtime)
        top = len(audiolist)

def sync():
        global updatecmd
        subprocess.Popen(updatecmd)

def blueClientThread(clientSocket):

	# Client commands
	while True:
		
		# Accept Command
		btData = str(clientSocket.recv(1024))
		#print btData


		# Execute Directory Refresh Command
		if ('<rfDir>' in btData):
			print "Received [%s]" % btData

			audiolist = glob.glob("/home/pi/audio/*.mp3")

			# Sort by Time
			audiolist.sort(key=os.path.getmtime)

			# Send Files via Bluetooth
			for i in audiolist:
				#btData = clientSocket.recv(1024)
				print i
				if 'home/pi/audio/' in i:
					i = i[15:]
				clientSocket.send('<' + i + '>')
				sleep(0.005)

			print audiolist
			clientSocket.send('<stop>')

		# Play Sound
		elif ('<dvPlay>' in btData):
			print "Received [%s]" % btData
			btData = clientSocket.recv(1024)
			try:
				os.system('play /home/pi/audio/"' + btData[btData.index('<')+1:btData.index('>')] + '" </dev/null &>/dev/null &')
			except Exception, recE:
				print "Received [%s]" % btData
				"Error: " + recE
		
		# Play Modulated Sound		
		elif ('<modPlay>' in btData):

			print "Received [%s]" % btData
			# Filename
			btData = clientSocket.recv(1024)

			# Pitch: -1000 to 1000
			pitch = clientSocket.recv(1024)
			# Speed: 0.1 to 1 to 10
			speed = clientSocket.recv(1024)
			# Treble: -20 to 20
			treble = clientSocket.recv(1024)
			# Bass: -20 to 20
			bass = clientSocket.recv(1024)
			# Overdrive: 0 to 100
			overdrive = clientSocket.recv(1024)
			# Loudness -10 to 50
			loudness = clientSocket.recv(1024)
			
			# ECHO
			# Gain In: 0.1 to 2
			echoGainIn = clientSocket.recv(1024)
			# Gain Out: 0.1 to 2
			echoGainOut = clientSocket.recv(1024)
			# Delay: 1 to 1000
			echoDelay = clientSocket.recv(1024)
			# Decay: 0 to 1
			echoDecay = clientSocket.recv(1024)

			# Play file with passed parameters
			os.system('play /home/pi/audio/"' + btData[btData.index('<')+1:btData.index('>')] + '" pitch ' + pitch[pitch.index('<')+1:pitch.index('>')] + ' speed ' + speed[speed.index('<')+1:speed.index('>')] + ' treble ' + treble[treble.index('<')+1:treble.index('>')] + ' bass ' + bass[bass.index('<')+1:bass.index('>')] + ' overdrive ' + overdrive[overdrive.index('<')+1:overdrive.index('>')] + ' loudness ' + loudness[loudness.index('<')+1:loudness.index('>')] + ' echo ' + echoGainIn[echoGainIn.index('<')+1:echoGainIn.index('>')] + ' ' + echoGainOut[echoGainOut.index('<')+1:echoGainOut.index('>')] + ' ' + echoDelay[echoDelay.index('<')+1:echoDelay.index('>')] + ' ' + echoDecay[echoDecay.index('<')+1:echoDecay.index('>')] + ' </dev/null &>/dev/null &')

			#BACKUP
			#os.system('play "' + btData[btData.index('<')+1:btData.index('>')] + '" pitch -921 speed 1.09 bass 10 overdrive 20 loudness -10 echo 0.7 1 55 0.5 </dev/null &>/dev/null &')
		

		# Escape loop if disconnected
		elif not btData:
			break

	# Disconnect if loop escapes
	clientSocket.close


########################
#### Main Function #####
#  Runtime Execution   #
########################
def main():
        input = ''
        tfm = sox.Transformer()
        tfm.pitch(-8.0)
        tfm.gain(+2,limiter=True)

        # Init
        start_new_thread(createAudiolists,())
        start_new_thread(hardwareThread,())

        # Runtime
        p = subprocess.Popen(['play','yesmymaster.wav'])


        try:	
                # Bind Bluetooth Socket
                blueSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                blueSocket.bind(("",0))
                blueSocket.listen(1)

                uuid = "1e0ca4ea-666d-4335-93eb-69fcfe7fa848"
                bluetooth.advertise_service(blueSocket, "idvBlueServer", uuid)

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


if __name__ == '__main__':
        main()
