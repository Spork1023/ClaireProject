#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')

if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13_V2 as epd213
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

import socket

logging.basicConfig(level=logging.DEBUG)

BUF_SIZE = 2048

def main(text):
    try:
        epd = epd213.EPD()
        epd.init(epd.FULL_UPDATE)
        epd.Clear(0xFF)

        # Drawing and creating image
        fontt = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

        image = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the frame    
        draw = ImageDraw.Draw(image)

        draw.text((110, 90), text, font = fontt, fill = 0)
        epd.display(epd.getbuffer(image))

    except IOError as e:
        logging.info(e)


while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect(('clairepresent.duckdns.org', 25273))
        messageLength = int.from_bytes(s.recv(1), 'big')
        buf = bytearray()
        while len(buf) < messageLength:
            buf += s.recv(BUF_SIZE if len(buf) < messageLength - BUF_SIZE else messageLength - len(buf))
        main(buf.decode())
        # print(buf.decode())
        s.close()
    except socket.timeout:
        continue