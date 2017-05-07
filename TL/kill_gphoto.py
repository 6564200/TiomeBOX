#!/usr/bin/python
# -*- coding: utf-8 -*-


import subprocess
from datetime import datetime, timedelta, time, date
from time import sleep
import logging
import os
import sys

CAM_ID = 3
ISO = 0
START_TIME = 0
STOP_TIME = 0
INTERVAL = 30

USED = '0G'
AVAIL = '0G'
USE = '0%'


def SetUp():
	global START_TIME, STOP_TIME, ISO ,CAM_ID, INTERVAL

	file_set = open('/home/pi/TL/settings.txt', 'r+b')
	settings = file_set.read()
	file_set.close()
	dct = eval(settings)

	H = []
	for sta in dct['START'].split(','): H.append(int(sta))
	START_TIME = time(H[0],H[1],H[2])

	H = []
	for sta in dct['STOP'].split(','): H.append(int(sta))
	STOP_TIME = time(H[0],H[1],H[2])

	ISO = dct['ISO']
	CAM_ID = dct['ID']
	INTERVAL = dct['INTERVAL']

	return True

def printlog(text = "text"):  ##---------------------------------
	#print text
        f = open('/home/pi/TL/kill_timelapse.log', 'a')
        f.write(str(datetime.now())[:-7] + '\t' + text + '\n')
	f.close()


def send_to_WEB(chec=60):
        mess = str(chec)
        ##print mess
        proc = subprocess.Popen('/home/pi/TL/send_to_WEB.py '+ mess, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return True


def read_use_filesys():
	global USED, AVAIL, USE
	proc3 = subprocess.Popen('df -h -T', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc3.wait()
	res = proc3.communicate()[0]
        ft = res.find('fuse')
	if ft > 0:
		resf = res[ft:].split()
		USED = resf[2]
	        AVAIL = resf[3]
        	USE = resf[4]

	return True
##-----------------------------------------------------------------------------------------------------
def main():

	read_use_filesys()
	KILL_P = 0
	PID = PID_NEW = 0
	printlog('Start '+USED+AVAIL+USE)
	send_to_WEB(80)
	while True:
		proc = subprocess.Popen('pidof gphoto2', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.wait()
		res = proc.communicate()
		if res[0] <> '':
			PID_NEW = int(res[0])
			if PID_NEW == PID:
				timeout += 1
			else:
				PID = PID_NEW
				timeout = 0

			if timeout > 10:
				printlog('kill process ' + str(KILL_P))
				proc2 = subprocess.Popen('sudo kill ' + str(PID), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
				proc2.wait()
				send_to_WEB()
				KILL_P += 1
				if KILL_P > 8:
					send_to_WEB(chec=100)
					subprocess.call('sudo reboot now', shell=True)
				timeout = 0


		else: timeout = 0
		#print str(timeout) + ' PID - ' + str(PID) + ' / ' + str(PID_NEW) + ' \ ' + str(KILL_P)
		sleep(4)


if __name__ == "__main__" :
	main()


