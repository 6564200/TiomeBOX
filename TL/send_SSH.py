#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import socket
import paramiko
from datetime import datetime, timedelta, time, date
from PIL import Image
from time import sleep

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
        #print text
        f = open('/home/pi/TL/send_SSH.log', 'a')
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


def SSH():
	SetUp()

	host = 'ssh.pythonanywhere.com'
	user = 'kazmaz'
	secret = '2oldpassword'
	port = 22

	#client = paramiko.SSHClient()
	#client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	#client.connect(hostname=host, username=user, password=secret, port=port)

	#channel = сlient.get_transport().open_session()
	

	#stdin, stdout, stderr = client.exec_command('ls -l')
	#data = stdout.read() + stderr.read()
	#print data
	#client.close()

	transport = paramiko.Transport((host, port))
	transport.connect(username=user, password=secret)
	sftp = paramiko.SFTPClient.from_transport(transport)

	remotepath = '/home/kazmaz/web2py/applications/max/static/images/TL/' + str(CAM_ID) + '_thumb.jpeg'
	localpath = '/home/pi/TL/SEND/thumbnail.jpeg'

	#sftp.get(remotepath, localpath)
	sftp.put(localpath, remotepath)

	sftp.close()
	transport.close()


def make_thumbnail(image_file, size=(800, 800)):
    im = Image.open(image_file)
    im.thumbnail(size, Image.ANTIALIAS)
    im.save('/home/pi/TL/SEND/thumbnail.jpeg')

def main():
    printlog('Start')
    sleep(120)
    if internet_connection():
       img_file = '/home/pi/TL/datetime.jpg'
       make_thumbnail(img_file)
       printlog('Convert')
       SSH()
       printlog('Send')
    else:
       printlog('no internet')


if __name__ == "__main__" :
    main()

