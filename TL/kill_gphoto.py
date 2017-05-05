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
USED = '0G'
AVAIL = '0G'
USE = '0%'



def printlog(text = "text"):  ##---------------------------------
	#print text
        f = open('/home/pi/TL/kill_timelapse.log', 'a')
        f.write(str(datetime.now())[:-7] + '\t' + text + '\n')
	f.close()


def send_to_WEB(captureinfo = "0 0 0",  COUNT=0, chec=104):
        mess = str(CAM_ID) + ' 0 0 ' + captureinfo + ' '+ USED + AVAIL + USE + ' ' + str(ISO) + ' ' + str(COUNT) + ' ' + str(chec)
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
	printlog('Start')
	send_to_WEB("0 0 0", 0, 33)
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
					subprocess.call('sudo reboot now', shell=True)
				timeout = 0


		else: timeout = 0
		#print str(timeout) + ' PID - ' + str(PID) + ' / ' + str(PID_NEW) + ' \ ' + str(KILL_P)
		sleep(4)


if __name__ == "__main__" :
	main()


