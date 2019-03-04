#!/usr/bin/python
# -*- coding: utf-8 -*- 

import subprocess
from datetime import datetime, timedelta, time, date
from time import sleep
import logging
import os
import sys

START_TIME = time(6,30,00)
STOP_TIME = time(23,30,00)
ISO = 100
CAM_ID = 2
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


def chek_USB():
	sleep(10)
	proc = subprocess.Popen('lsusb', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	res = proc.communicate()
	if res[0].find("Huawei") == -1:
		printlog('USB: OFF') 
		return False
	else: 
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
             sleep(10)
         sleep(5)
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
             sleep(5)

	proc = subprocess.Popen('sudo mount /dev/sda1 /mnt/SONY', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
	sleep(5)

def mount_SONY():
        proc = subprocess.Popen('ls -c /mnt/SONY/DCIM/', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	folder_new = proc.communicate()[0][:8]
	printlog(folder_new)
	proc = subprocess.Popen('ls -c /mnt/SONY/DCIM/'+folder_new, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	file_new = proc.communicate()[0][:12]
	printlog(file_new)
	proc = subprocess.Popen('cp //mnt//SONY//DCIM//'+folder_new+'//'+file_new+' '+'//home//pi//TL//fin_img.jpg', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	sleep(7)
	proc = subprocess.Popen('sudo umount /dev/sda1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
	sleep(1)

def init_time():
	import ctypes
	import ctypes.util
	import time

	if chek_USB() == True:
		proc = subprocess.Popen('sudo umount /dev/sda1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.wait()
		printlog('Umount USB')
		sleep(4)
		DOWN_USB()
	
	printlog('shot image fot time')
	proc = subprocess.Popen('irsend SEND_ONCE Minolta-Sony-RMT-DSLR1 S', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	sleep(50)
	UP_USB()

	proc = subprocess.Popen('ls -c /mnt/SONY/DCIM/', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	folder_new = proc.communicate()[0][:8]
	printlog(folder_new)
	proc = subprocess.Popen('ls -c /mnt/SONY/DCIM/'+folder_new, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	file_new = proc.communicate()[0][:12]
	printlog(file_new)
	proc = subprocess.Popen('cp //mnt//SONY//DCIM//'+folder_new+'//'+file_new+' '+'//home//pi//TL//datetime.jpg', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	sleep(7)
	proc = subprocess.Popen('sudo umount /dev/sda1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
	sleep(1)
	#if list_f.find("debug") == -1:
	if 1:
		proc = subprocess.Popen('exiftool /home/pi/TL/datetime.jpg', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.wait()
		res = proc.communicate()

		find_Date = res[0].find("Date/Time Original")
		cam_datetime = res[0][find_Date+34:find_Date+53]
		f_datatime = datetime.strptime(cam_datetime, '%Y:%m:%d %H:%M:%S')

		time_tuple = ( f_datatime.year,	
				f_datatime.month,
				f_datatime.day,
				f_datatime.hour,
				f_datatime.minute,
				f_datatime.second,
				0)

		CLOCK_REALTIME = 0
		class timespec(ctypes.Structure): 
			_fields_ = [("tv_sec", ctypes.c_long), ("tv_nsec", ctypes.c_long)]
		librt = ctypes.CDLL(ctypes.util.find_library("rt"))
		ts = timespec()
		ts.tv_sec = int( time.mktime( datetime( *time_tuple[:6]).timetuple() ) )
		ts.tv_nsec = time_tuple[6] * 1000000 # Millisecond to nanosecond			  
		librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))
	else: 
		printlog("DATA ERROR")
	TIMES = datetime.now()
	printlog(str(TIMES))
	DOWN_USB()

	return TIMES

##-----------------------------------------------------------------------------------------------------
def capture(COUNT = 0):
	proc = subprocess.Popen('irsend SEND_ONCE Minolta-Sony-RMT-DSLR1 S', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return True

def printlog(text = "text"):  ##---------------------------------
	print text
        f = open('/home/pi/TL/timelapse.log', 'a')
        f.write(str(datetime.now())[:-7] + '\t' + text + '\n')
	f.close()

def chek_time_work():
	now_time = datetime.now()
	cur_year = now_date.year 
	cur_month = now_date.month 
	cur_day = now_date.day 
	cur_hour = now_time.hour 
	cur_minute = now_time.minute 
	cur_second = now_time.second 
	num_week = now_date.isoweekday() 
	return True
	
##-----------------------------------------------------------------------------------------------------
def main():

	printlog("Start program")
	sleep(5)
	SetUp()
	
	TIMES = init_time()
	printlog(TIMES.strftime("%A, %d. %B %Y %I:%M%p"))

	DELTA = timedelta(seconds=INTERVAL)
	printlog("SET INTERVAL: " + str(DELTA)) 
	printlog("START-STOP TIME: " + str(START_TIME) + ' - ' + str(STOP_TIME))

	COUNT_SHOT = 0
	while True:
		TIME_C = datetime.now()
		#if TIME_C.weekday() < 5:
                if TIME_C.time() > START_TIME and TIME_C.time() < STOP_TIME:
					COUNT_SHOT += 1
                                        capture(COUNT_SHOT)
                                        TIME_I = datetime.now() - TIME_C
                                        printlog("SHOT: " + str(COUNT_SHOT) + " ; TIME SHoT: " + str(TIME_C)[11:-7])
                                        
                                        flag = True
                                        while TIME_I < DELTA:
                                                TIME_I = datetime.now() - TIME_C
                                                if (DELTA.seconds - (datetime.now() - TIME_C).seconds) > 1:
                                                        sleep(DELTA.seconds - (datetime.now() - TIME_C).seconds - 1)
                                                        
                else:
                        		sleep(INTERVAL)
					if TIME_C.time() > STOP_TIME:
						printlog("Stop program") 
						break
		

if __name__ == "__main__" :
	main()

