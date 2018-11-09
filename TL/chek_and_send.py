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
#	print text
        f = open('/home/pi/TL/chek_send.log', 'a')
        f.write(str(datetime.now())[:-7] + '\t' + text + '\n')
	f.close()


def chek_USB():
        proc = subprocess.Popen('lsusb', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        res = proc.communicate()
#	print res[0].find("Huawei")
#	print res[0].find("Sony")
        if (res[0].find("Huawei") == -1) and (res[0].find("Sony") == -1):
                printlog('USB: OFF')
               	return False
        if (res[0].find("Huawei") > -1) and (res[0].find("Sony") > -1):
                printlog('USB: ON')
                return True

def DOWN_USB():
         printlog('DOWN USB')
         co = 0
         while chek_USB():
             co += 1
             printlog(str(co))
             for cc in range(0,co):
                proc = subprocess.Popen('sudo /home/pi/hub-ctrl.c/hub-ctrl -h 0 -P 2 -p 0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                proc.wait()
             sleep(6)

         proc = subprocess.Popen('irsend SEND_ONCE Minolta-Sony-RMT-DSLR1 Play', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         proc.wait()
         sleep(5)

def UP_USB():
        printlog('UP USB')
        co = 0
        while not chek_USB():
             co += 1
             printlog(str(co))
             for cc in range(0,co):
                proc = subprocess.Popen('sudo /home/pi/hub-ctrl.c/hub-ctrl -h 0 -P 2 -p 1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                proc.wait()
             sleep(6)

        proc = subprocess.Popen('sudo mount /dev/sda1 /mnt/SONY', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        sleep(5)


def send_to_WEB(chec=60):
        mess = str(chec)
        printlog("Send WEB")
        proc = subprocess.Popen('/home/pi/TL/send_to_WEB.py '+ mess, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return True

def send_SSH(chec=60):
        mess = str(chec)
        printlog("Send SSH")
        proc = subprocess.Popen('/home/pi/TL/send_SSH.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return True

def main():
	printlog('Start')
	sleep(30)
	timeout = 0
	while True:
		proc = subprocess.Popen('ps -ef', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.wait()
		res = proc.communicate()
		if res[0].find("sony_TL_IR") > -1:
			PID_NEW = res[0]
			printlog('s')
		else: 
			timeout += 1
			if timeout > 2: break
		sleep(300)
	printlog('begin send')
	UP_USB()
	sleep(300)
	send_to_WEB(210)
	sleep(30)
	sent_SSH()
	sleep(300)
	DOWN_USB()
	printlog("End message")
	

if __name__ == "__main__" :
	main()


