#!/usr/bin/python
# -*- coding: utf-8 -*-
import mechanize
from PIL import Image
import subprocess
from datetime import datetime, timedelta, time, date
from time import sleep
import logging
import os
import sys
import cookielib

CAM_ID = 2
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
	print text
        f = open('/home/pi/TL/chek_send.log', 'a')
        f.write(str(datetime.now())[:-7] + '\t' + text + '\n')
	f.close()


def chek_USB():
        proc = subprocess.Popen('lsusb', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        res = proc.communicate()
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
	 proc = subprocess.Popen('sudo umount /dev/sda1', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
         proc.wait()
         while chek_USB():
             co += 1
             printlog(str(co))
             for cc in range(0,co):
                proc = subprocess.Popen('sudo /home/pi/hub-ctrl.c/hub-ctrl -h 0 -P 2 -p 0', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                proc.wait()
             sleep(6)
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
             sleep(6)

        proc = subprocess.Popen('sudo mount /dev/sda1 /mnt/SONY', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()
        sleep(5)


def send_to_WEB(chec=60):
        mess = str(chec)
        printlog("Send WEB")
        proc = subprocess.Popen('/home/pi/TL/send_to_WEB.py '+ mess, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return True

def send_test():
        printlog("send broken")
        proc = subprocess.Popen('/home/pi/TL/sendtest.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return True
def send_SSH(chec=60):
        mess = str(chec)
        printlog("Send SSH")
        proc = subprocess.Popen('/home/pi/TL/send_SSH.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True

def send_to_WEBFORM(img_file):
    printlog("Send WEB FORM ")
    myWEB = 'http://185.139.68.199/timebox/default/display_form.html'
    FILENAME = ''
    FILENAME = img_file
    printlog('Send ' + img_file)
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    tri = 0
    connect = False
    while not connect:
       try:
         rr=br.open(myWEB)
         br.select_form(nr=0)
         
         br['cam_id']=[str(CAM_ID)]
         connect = True

       except mechanize.URLError as e:
         print e.reason.args
         tri += 1
         if rti > 4:
            exit()
         sleep(20)

    br.form.add_file(open(FILENAME), 'text/plain', FILENAME)
    br.form.set_all_readonly(False)
    br.submit()

def make_thumbnail(image_file, size=(800, 800)):
    print image_file
    im = Image.open(image_file)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save('/home/pi/TL/SEND/' + image_file[image_file.rfind('/')+1:])
    im.close()
    printlog('Convert')

def find_file_send():
    printlog("ffind file")
    find_files = [] 
    proc = subprocess.Popen("find /mnt/SONY/DCIM -type f -mmin -1440", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()
    find_f = proc.communicate()[0]
    find_f = find_f.split('\n')
    find_f.remove('')
    find_files.extend(find_f)
    ffile = find_files[::(len(find_files)/15)]
    print(ffile)
    for pfile in ffile:
        sleep(2)
        make_thumbnail(pfile)
        sleep(2)
        send_to_WEBFORM('/home/pi/TL/SEND/' + pfile[pfile.rfind('/')+1:])

def main():
	printlog('Start')
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
	sleep(10)
	send_SSH()
	sleep(10)
        send_test() #kostil broken send
        sleep(10)
	find_file_send()
	printlog("End message")
	

if __name__ == "__main__" :
	main()


