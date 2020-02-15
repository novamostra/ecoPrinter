#!/usr/bin/env python
#ecoPrinter Printer Gadget handler
#author: novamostra.com
import os
import subprocess

import time
import logging

import board
from ledpanel import WS2812B


#init logger
logging.basicConfig(filename='log_printer',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
log = logging.getLogger()

infile = os.open("/dev/g_printer0", os.O_RDONLY)

indicator = WS2812B(board.D18,12)
indicator.loop((0,0,200),0.02,3)
indicator.reset()

while True:
    charout = os.read(infile,512)
    if b"%!PS-Adobe-3.0" in charout:
        indicator.looping_ball((0,5,0),0.02)
        #maybe here I have to find the index in order to split the file?
        localtime = time.localtime()
        timeString = time.strftime("%Y%m%d%H%M%S",localtime)
        log.info("New file {0}".format(timeString))
        filename = "prints/" + timeString + ".ps"
        f = open(filename,"wb")
        f.write(charout)
    elif b"%%EOF" in charout:
        localtime = time.localtime()
        timeString = time.strftime("%Y%m%d%H%M%S",localtime)
        f.write(charout)
        f.close()
        os.system("ps2pdf " + filename + " " + filename + ".pdf")
        output_file = filename + ".pdf"
        localtime = time.localtime()
        timeString = time.strftime("%Y%m%d%H%M%S",localtime)
        indicator.stop()
        log.info("Conversion completed at {0}".format(timeString))
        output = subprocess.call(["python3", "beam.py",output_file])
    else:
        if not f.closed:
            f.write(charout)
