#!/usr/bin/env python

import imaplib2
import time
import re

import RPi.GPIO as GPIO

DEBUG = True

HOSTNAME = 'imap.gmail.com'
USERNAME = 'niklas.hoesl@gmail.com'
PASSWORD = ''
MAILBOX = 'Inbox'

NEWMAIL_OFFSET = 0   # my unread messages never goes to zero, yours might
MAIL_CHECK_FREQ = 60 # check mail every 60 seconds

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GREEN_LED = 18
RED_LED = 23
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(RED_LED, GPIO.OUT)

def loop():

    server = imaplib2.IMAP4_SSL(HOSTNAME)
    server.login(USERNAME, PASSWORD)
    answer, raw_data = server.status(MAILBOX, '(MESSAGES UNSEEN)')

    newmails=0
    print answer
    if answer == "OK":
	dec = raw_data[0].decode()
	print dec
	newmails = int(re.search('UNSEEN\s+(\d+)',dec).group(1))
	print newmails    

    if newmails > NEWMAIL_OFFSET:
        GPIO.output(GREEN_LED, True)
        GPIO.output(RED_LED, False)
    else:
        GPIO.output(GREEN_LED, False)
        GPIO.output(RED_LED, True)

    time.sleep(MAIL_CHECK_FREQ)

if __name__ == '__main__':
    try:
        print 'Press Ctrl-C to quit.'
        while True:
            loop()
    finally:
        GPIO.cleanup()
