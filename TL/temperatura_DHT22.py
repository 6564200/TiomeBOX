#!/usr/bin/python
# -*- coding: utf-8 -*- 

import mmap
import os
import Adafruit_DHT
from datetime import datetime
import time

def printlog(text = "text"):  ##---------------------------------
  f = open('/home/pi/TL/temperature.log', 'a')
  f.write(str(datetime.now())[:-7] + '\t' + text + '\n')
  f.close()

def main():
  printlog('Start')

  filename = "/home/pi/TL/weather.txt"
  File = open(filename, "r+b")
  size = os.path.getsize(filename)
  data = mmap.mmap(File.fileno(), size)

  while True:
     (water, temp) = Adafruit_DHT.read_retry(22, 17)
     data.seek(0)
     data.write(str(temp))
     data.seek(20)
     data.write(str(water))

     #struct['temp'] = temp
     #struct['water'] = water
     #struct['reg_on'] = datetime.now().strftime("%Y.%m.%d%H:%M:%S")
     printlog(str(temp)+" C /" + str(water) + " % water")
     time.sleep(30)
     
if __name__=="__main__":
   main()
