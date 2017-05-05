#!/usr/bin/python
# -*- coding: utf-8 -*- 

from urllib import urlopen
import Adafruit_DHT
from datetime import datetime
import socket
import time

def printlog(text = "text"):  ##---------------------------------
  f = open('/home/pi/TL/temperature.log', 'a')
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

def send_to_WEB(s={}):
    global urlopen
    #print s
    url_api = "https://kazmaz.pythonanywhere.com/max/default/reglog.html?cam=%s&t=%s&w=%s&p=%s&r=%s&c=%s&er=%s&sp=%s&seting=%s&mv=%s&ch=%s" % (s['cam'], s['temp'], s['water'], s['reg_on'], s['reg_on'], s['capture'], s['errorcapture'], s['stopcapture'], s['setcapture'], s['cfile'], s['chec'])
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

def main():
  printlog('Start')
  struct = {
  'cam': '3',
  'temp': '0',
  'water': '0',
  'reg_on': '0',
  'capture': '0',
  'errorcapture': '0',
  'stopcapture': '0',
  'setcapture': '0',
  'cfile': '0',
  'chec': '83'
  }

  while True:
     (water, temp) = Adafruit_DHT.read_retry(22, 17)
     struct['temp'] = temp
     struct['water'] = water
     struct['reg_on'] = datetime.now().strftime("%Y.%m.%d%H:%M:%S")
     printlog(str(temp)+" C /" + str(water) + " % water")
     
     if internet_connection():
       if send_to_WEB(struct):
         printlog('Send OK')
       else:
         printlog('Send ERROR')
     else:
       printlog( "internet connection error" )
     time.sleep(300)
     
if __name__=="__main__":
   main()
