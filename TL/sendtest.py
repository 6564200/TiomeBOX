#!/usr/bin/python
# -*- coding: utf-8 -*-
import mechanize
import cookielib
from mechanize import urlopen
from datetime import datetime, timedelta, time, date
from time import sleep
import os
import sys

def printlog(text = "text"):  ##---------------------------------
	print text
        f = open('/home/pi/TL/chek_send.log', 'a')
        f.write(str(datetime.now())[:-7] + '\t' + text + '\n')
	f.close()


def send_to_WEBFORM(img_file):
    printlog("Send WEB FORM test")
    myWEB = 'http://185.139.68.199/timebox/default/display_form.html'
    FILENAME = ''
    FILENAME = img_file
    printlog('Send test' + img_file)
    br = mechanize.Browser()
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    tri = 0
    connect = False
    while not connect:
       try:
         rr=br.open(myWEB)
         response = urlopen("http://185.139.68.199/timebox/default/display_form.html")
         br.select_form(nr=0)
         
         br['cam_id']=['1']
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

def find_file_send():
    send_to_WEBFORM('/home/pi/TL/SEND/thumbnail.jpeg')

def main():
	printlog('Start test')
	find_file_send()
	printlog("End message send")
	

if __name__ == "__main__" :
	main()


