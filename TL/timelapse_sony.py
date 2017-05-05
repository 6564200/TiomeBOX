#!/usr/bin/python


##----------------------------------
##--- FOR RAW IMAGES
##--- test send to WEB
##----------------------------------

import subprocess
from datetime import datetime, timedelta, time, date
from time import sleep
import logging
import os
import sys


START_TIME = time(2,30,00)
STOP_TIME = time(23,55,00)
ISO = 100
CAM_ID = 3
INTERVAL = 300



def init_time():
	import ctypes
	import ctypes.util
	import time
	proc2 = subprocess.Popen('gphoto2 --set-config=iso=10000', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc2.wait()
	proc = subprocess.Popen('gphoto2 --capture-image-and-download --filename /home/pi/TL/datetime.jpg --force-overwrite', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	res = proc.communicate()
	list_f = res[0]
	if list_f.find("debug") == -1:
		proc = subprocess.Popen('exiftool /home/pi/TL/datetime.jpg', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.wait()
		res = proc.communicate()
		find_Date = res[0].find("Date/Time Original")
		cam_datetime = res[0][find_Date+34:find_Date+53]
		print cam_datetime
		f_datatime = datetime.strptime(cam_datetime, '%Y:%m:%d %H:%M:%S')
		#print f_datatime
		time_tuple = ( f_datatime.year,	
				f_datatime.month,
				f_datatime.day,
				f_datatime.hour,
				f_datatime.minute,
				f_datatime.second,
				0)
		#print time_tuple
		CLOCK_REALTIME = 0
		class timespec(ctypes.Structure): 
			_fields_ = [("tv_sec", ctypes.c_long), ("tv_nsec", ctypes.c_long)]
		librt = ctypes.CDLL(ctypes.util.find_library("rt"))
		ts = timespec()
		ts.tv_sec = int( time.mktime( datetime( *time_tuple[:6]).timetuple() ) )
		ts.tv_nsec = time_tuple[6] * 1000000 # Millisecond to nanosecond			  
		librt.clock_settime(CLOCK_REALTIME, ctypes.byref(ts))
	else: 
		printlog("CAMERA DATA ERROR")
	TIMES = datetime.now()
	return TIMES

def cam_config():
	#gphoto_config = {'imagequality': 1, 'iso': 100, 'whitebalance': 10, 'colortemperature': 6500, 'aperture': 2, 'focusmode': 0, 'capturemode': 0, 'aspectratio': 0 }
	#cfg = ['--set-config=%s=%s' % (k, v) for k, v in gphoto_config.items()]
	#proc = subprocess.Popen('gphoto2 ' + ' '.join(cfg), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc = subprocess.Popen('gphoto2 --set-config=iso='+str(ISO), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	res = proc.communicate()
	list_f = res[0]
	if list_f.find("debug") == -1:
		printlog("CAMERA SET OK")
		send_to_WEB('0 0 0', 0, 90)
	else:
		printlog("CAMERA SET ERROR")
		send_to_WEB('0 0 0', 0, 105)
		return False
	return True


##-----------------------------------------------------------------------------------------------------
def capture(COUNT = 0):
	zero = ('0' * (4-len(str(COUNT)))) + str(COUNT)
	#sys.stdout.write("c")
	proc = subprocess.Popen('gphoto2 --capture-image-and-download --filename /home/pi/TL/DATA/%y_%m_%d/c%H%M_'+zero+'.%C', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	res = proc.communicate()
	list_f = res[0]

	if list_f.find("debug") <> -1:
		printlog('CAM CAPTUR ERROR:')
		proc = subprocess.Popen('gphoto2 --reset', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.wait()
		return False
	return True

def printlog(text = "text"):  ##---------------------------------
	#print text
        f = open('/home/pi/TL/timelapse.log', 'a')
        f.write(str(datetime.now())[:-7] + '\t' + text + '\n')
	f.close()

def send_to_WEB(captureinfo = "0 0 0", COUNT=0, chec=99):
	mess = str(CAM_ID) + ' 0 0 ' + captureinfo + ' ISO' + str(ISO) + ' ' + str(COUNT) + ' ' + str(chec)
	print mess
	proc = subprocess.Popen('/home/pi/TL/send_to_WEB.py '+ mess, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	return True

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
	TIMES = init_time()
	send_to_WEB('')
	printlog(TIMES.strftime("%A, %d. %B %Y %I:%M%p"))

	DELTA = timedelta(seconds=INTERVAL)
	printlog("SET INTERVAL: " + str(DELTA)) 
	printlog("START-STOP TIME: " + str(START_TIME) + ' - ' + str(STOP_TIME)) 
	
	cam_config()

	COUNT_SHOT = 0
	while True:
		TIME_C = datetime.now()
                if TIME_C.time() > START_TIME and TIME_C.time() < STOP_TIME:
					COUNT_SHOT += 1
                                        ret = capture(COUNT_SHOT)
                                        TIME_I = datetime.now() - TIME_C
					if ret: send_to_WEB('1 0 0', COUNT_SHOT, 99)
					else: send_to_WEB('0 1 0', COUNT_SHOT, 66)
                                        printlog("SHOT: " + str(COUNT_SHOT) + " ; TIME SHoT: " + str(TIME_C))
                                        
                                        while TIME_I < DELTA:
                                                TIME_I = datetime.now() - TIME_C

                                                if (DELTA.seconds - (datetime.now() - TIME_C).seconds) > 2:
                                                        printlog( "sleep" + str(DELTA.seconds - (datetime.now() - TIME_C).seconds - 1))
                                                        sleep(DELTA.seconds - (datetime.now() - TIME_C).seconds - 1)

                else:
				send_to_WEB('0 0 1', COUNT_SHOT, 100)
				printlog(str(INTERVAL))
                                sleep(INTERVAL)

		

if __name__ == "__main__" :
	main()
