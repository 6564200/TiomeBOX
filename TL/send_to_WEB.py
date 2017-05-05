#!/usr/bin/python
# -*- coding: utf-8 -*- 


from urllib import urlopen
from datetime import datetime
import os
import sys
import socket

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
  #printlog(sys.avg) 
  struct = {
  'cam':sys.argv[1],
  'temp':sys.argv[2],
  'water':sys.argv[3],
  'reg_on': datetime.now().strftime("%Y.%m.%d%H:%M:%S"),
  'capture':sys.argv[4],
  'errorcapture':sys.argv[5],
  'stopcapture':sys.argv[6],
  'setcapture':sys.argv[7],
  'cfile':sys.argv[8],
  'chec':sys.argv[9]

  }

  if internet_connection():
	if send_to_WEB(struct):
		printlog('Send OK')
	else:
		printlog('Send ERROR')
  else:
        printlog( "internet connection error" )

     

   
if __name__ == "__main__":
    if len (sys.argv) > 1:
        #print (sys.argv)
	main()
    else:
        printlog ("ERROR: No argument!!!")
