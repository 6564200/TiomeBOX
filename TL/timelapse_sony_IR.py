
import subprocess
from datetime import datetime, timedelta, time, date
from time import sleep
import logging
import os
import sys


START_TIME = time(0,1,00)
STOP_TIME = time(23,59,00)
 
INTERVAL = 20

LIST_FILE = []

def init_time():
	import ctypes
	import ctypes.util
	import time

	printlog('set time exif')

	proc = subprocess.Popen('sudo /home/pi/hub-ctrl.c/hub-ctrl -h 0 -P 2 -p 0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	sleep(2)
	proc = subprocess.Popen('irsend SEND_ONCE Minolta-Sony-RMT-DSLR1 Play', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	sleep(2)
	proc = subprocess.Popen('irsend SEND_ONCE Minolta-Sony-RMT-DSLR1 S', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	sleep(65)
	proc = subprocess.Popen('sudo /home/pi/hub-ctrl.c/hub-ctrl -h 0 -P 2 -p 1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	sleep(2)
	proc = subprocess.Popen('ls -c /media/usb0/DCIM/', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	folder_new = proc.communicate()[0][:8]
	proc = subprocess.Popen('ls -c /media/usb0/DCIM/'+folder_new, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	file_new = proc.communicate()[0][:12]
	proc = subprocess.Popen('cp /media/usb0/DCIM/'+folder_new+'//'+file_new+' '+'/home/pi/TL/datetime.jpg', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()

	res = proc.communicate()
	list_f = res[0]

	if list_f.find("debug") == -1:
		proc = subprocess.Popen('exiftool /home/pi/TL/datetime.jpg', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		proc.wait()
		res = proc.communicate()
		list_f = res[0]
		cam_datetime = (list_f.split('\n')[31][34:])
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
		printlog("DATA ERROR")
	TIMES = datetime.now()
	printlog(str(TIMES))
	proc = subprocess.Popen('sudo /home/pi/hub-ctrl.c/hub-ctrl -h 0 -P 2 -p 0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	sleep(2)
	proc = subprocess.Popen('irsend SEND_ONCE Minolta-Sony-RMT-DSLR1 Play', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	proc.wait()
	return TIMES

def cam_config():
	return True


##-----------------------------------------------------------------------------------------------------
def capture(COUNT = 0):
	proc = subprocess.Popen('irsend SEND_ONCE Minolta-Sony-RMT-DSLR1 S', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	return True

def printlog(text = "text"):  ##---------------------------------
	print text
        f = open('/home/pi/TL/timelapse.log', 'a')
        f.write(str(datetime.now()) + '\t' + text + '\n')
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
	TIMES = init_time()
	printlog(TIMES.strftime("%A, %d. %B %Y %I:%M%p"))

	DELTA = timedelta(seconds=INTERVAL)
	printlog("SET INTERVAL: " + str(DELTA)) 
	printlog("START-STOP TIME: " + str(START_TIME) + ' - ' + str(STOP_TIME)) 
	
	cam_config()

	COUNT_SHOT = 0
	while True:
		TIME_C = datetime.now()
		##if TIME_C.weekday() < 5:
                if TIME_C.time() > START_TIME and TIME_C.time() < STOP_TIME:
					COUNT_SHOT += 1
                    capture(COUNT_SHOT)
                    TIME_I = datetime.now() - TIME_C
                    printlog("SHOT: " + str(COUNT_SHOT) + " ; TIME SHoT: " + str(TIME_C))
                                        
                    flag = True
                    while TIME_I < DELTA:
                        TIME_I = datetime.now() - TIME_C
						if TIME_I.total_seconds() < 10 and flag:
                            flag = False
                            if (DELTA.seconds - (datetime.now() - TIME_C).seconds) > 2:
                                printlog( "sleep" + str(DELTA.seconds - (datetime.now() - TIME_C).seconds - 1))
                                sleep(DELTA.seconds - (datetime.now() - TIME_C).seconds - 1)

                else:
					printlog(str(INTERVAL))
                    sleep(INTERVAL)
        ##else:
		##  printlog("RELAX VIHODNOY")
        ##  sleep(3550)

		

if __name__ == "__main__" :
	main()
