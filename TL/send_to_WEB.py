#!/usr/bin/python
# -*- coding: utf-8 -*- 

from urllib import urlopen
from datetime import datetime, timedelta, time, date
import os
import mmap
import sys
import socket

CAM_ID = 3
ISO = 0
START_TIME = 0
STOP_TIME = 0
INTERVAL = 30

USED = '0G'
AVAIL = '0G'
USE = '0%'


def printlog(text = "text"):  ##---------------------------------
  #print text
  f = open('/home/pi/TL/sendWEB.log', 'a')
  f.write(str(datetime.now())[:-7] + '\t' + text + '\n')
  f.close()

def internet_connection():
    try:
        socket.gethostbyaddr('kazmaz.pythonanywhere.com')
    except socket.gaierror as e:
        return False
    except socket.herror:
        return False
    return True

##https://kazmaz.pythonanywhere.com/max/default/reglog.html?cam=2&t=22&w=12&p=2016.01.01%2012:23:11&r=2016.01.01%2022:20:44&c=1&st=1&sp=0&set=8:00%2012:30&mv=0

def send_to_WEB(s={}):
    global urlopen
    
    url_api = "https://kazmaz.pythonanywhere.com/max/default/reglog.html?cam=%s&t=%s&w=%s&p=%s&r=%s&seting=%s&ch=%s" % (s['cam'], s['temp'], s['water'], s['reg_on'], s['reg_on'], s['setcapture'], s['chec'])
    #print url_api
    while 1:
            try:
                html_doc = urlopen(url_api).read()
            except (urllib.socket.error, IOError):
                printlog( "urllib.socket.error wait 5 sec" )
                time.sleep(5)
                continue
            else:
                break

    return True

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

def main():
  #printlog(sys.avg) 

  SetUp()

  filename = "/home/pi/TL/weather.txt"
  File = open(filename, "r+b")
  size = os.path.getsize(filename)
  data = mmap.mmap(File.fileno(), size)


  struct = {
  'cam':str(CAM_ID),
  'temp': data[0:7],
  'water': data[20:27],
  'reg_on': datetime.now().strftime("%Y.%m.%d%H:%M:%S"),
  'setcapture': str(ISO)+str(STOP_TIME)+str(START_TIME)+str(INTERVAL),
  'chec':sys.argv[1]
  }

  data.close()
  File.close()

  if internet_connection():
	if send_to_WEB(struct):
		printlog('Send OK')
		print struct 
	else:
		printlog('Send ERROR')
  else:
        printlog( "internet connection error" )
	printlog( struct ['temp'])

     

   
if __name__ == "__main__":
    if len (sys.argv) > 1:
        #print (sys.argv)
	main()
    else:
        printlog ("ERROR: No argument!!!")
