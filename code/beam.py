#!/usr/bin/env python
#ecoPrinter Android NFC beam
#author: novamostra.com
import nfc
import ndef

import os
import sys
import threading
import subprocess

import logging

import configparser

# WS2812B requirements
import board
from ledpanel import WS2812B

# Init WS2812B led panel
indicator = WS2812B(board.D18,12)

# NFC Board serial port
NFC_DEVICE_PATH=""

# Raspberry PI's
LOCAL_BT_MAC=""
LOCAL_BT_NAME=""

#init logger
logging.basicConfig(filename='log',
                            filemode='w',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
log = logging.getLogger()


def init():
    #load device configuration
    load_config()
    
    #check if a file is supplied 
    log.debug(str(sys.argv[1]))
    if (len(sys.argv)==2):
        if (os.path.isfile(str(sys.argv[1]))):
            file = str(sys.argv[1])
            log.info("File {0} exists.".format(file))
            Beam().start(file)
        else:
            log.warning("File does not exist.")
    else:
        log.warning("Arguments mismatch.")

def load_config():
    global NFC_DEVICE_PATH, LOCAL_BT_NAME, LOCAL_BT_MAC
    config = configparser.ConfigParser()   
    configFilePath = r'ecoPrinter.conf'
    config.read(configFilePath)
    NFC_DEVICE_PATH = config['NFC_Device']['Path'].strip()
    LOCAL_BT_NAME = config['Bluetooth_Device']['Name'].strip()    
    LOCAL_BT_MAC = config['Bluetooth_Device']['Address'].strip()

    
def handover_connect(llc):
    client = nfc.handover.HandoverClient(llc)
    try:
        client.connect(recv_miu=128, recv_buf=2)
        log.info("connected to the remote handover server")
        return client
    except nfc.llcp.ConnectRefused:
        log.error("unable to connect to the handover server")

def handover_send(client, message, miu=128):
    if isinstance(message, (bytes, bytearray)):
        if not client.send_octets(message, miu):
            log.error("error sending handover request octets")
    else:
        if not client.send_records(message):
            log.error("error sending handover request records")

def handover_recv(client, timeout, raw=False):
    records = client.recv_records(timeout)

    if not records:
        log.error("no answer within {0} seconds".format(int(timeout)))

    if not records[0].type == "urn:nfc:wkt:Hs":
        log.error("unexpected message type '{0}'".format(records[0].type))

    return records

class Beam():
    def on_llcp_startup(self, llc):
        log.info("LLCP Startup")
        self.timer = threading.Timer(15.0, self.connection_timeout) 
        self.timer.start() 
        return llc

    def on_llcp_connect(self, llc):
        log.info("LLCP CONNECTED")
        self.timer.cancel()
        indicator.change_color((0,25,0))        
        threading.Thread(target=self.bluetooth_pair, args=(llc,)).start()
        llc.run()
        return False

    def terminate(self):
        indicator.stop()
        indicator.reset()        
        return self.status

    def start(self,file):
        indicator.looping_ball((20,0,0),0.02)
        self.status = False
        self.file=file
        self.init_connection()
        
    def connection_timeout(self):
        if(self.clf):
            self.clf.close()
        self.status=False
        self.terminate()

    def __init__(self):
        pass

    def bluetooth_pair(self, llc):
        client = handover_connect(llc)
        try:
            
            bt_record = ndef.BluetoothEasyPairingRecord(LOCAL_BT_MAC)
            bt_record.name = LOCAL_BT_NAME
            bt_record.device_name = LOCAL_BT_NAME
            bt_record.device_class = 0x10010C
            bt_record.add_service_class(0x1105)
            bt_record.add_service_class(0x1106)

            hr_record = ndef.HandoverRequestRecord("1.2", os.urandom(2))
            hr_record.add_alternative_carrier("active", bt_record.name)

            handover_send(client, [hr_record, bt_record])
            records = handover_recv(client, timeout=3.0)
            log.info("received {}".format(records[0].type))
            hs_record, bt_record = records

            if len(hs_record.alternative_carriers) != 1:
                log.warning("one selected carrier is expected")
            if bt_record.type != "application/vnd.bluetooth.ep.oob":
                log.warning("a Bluetooth carrier is expected")
            if bt_record.device_name == "":
                log.warning("empty local device name attribute")
            if bt_record.device_class is None:
                log.warning("there is no class of device attribute")
            if len(bt_record.service_class_list) == 0:
                log.warning("there are no service class UUIDs")
            if bt_record.simple_pairing_hash_256 is not None:
                log.warning("ssp hash not expected in just-works mode")
            if bt_record.simple_pairing_randomizer_256 is not None:
                log.warning("ssp rand not expected in just-works mode")

            if (not bt_record.device_address is None):
                indicator.change_color((0,0,25))
#                subprocess.call(["obexftp","-U","-b",str(bt_record.device_address.addr),"-B","12","-p",self.file])
                os.system("obexftp -U -b " + str(bt_record.device_address.addr) + " -B 12 -p " + self.file)
                self.status = True
        finally:
            self.terminate()            
            client.close()
            
    def init_connection(self):
        try:
            self.clf = nfc.ContactlessFrontend(NFC_DEVICE_PATH)
        except IOError as error:
            if error.errno == errno.ENODEV:
                log.info("no contactless reader found on " + path)
            elif error.errno == errno.EACCES:
                log.info("access denied for device with path " + path)
            elif error.errno == errno.EBUSY:
                log.info("the reader on " + path + " is busy")
            else:
                log.debug(repr(error) + "when trying " + path)

        llcp_options = {
            'on-startup': self.on_llcp_startup,
            'on-connect': self.on_llcp_connect,
            'role':       None,
            'brs':        2,
            'acm':        False,
            'rwt':        8,
            'miu':        2175,
            'lto':        500,
            'lsc':        3,
            'agf':        False,
            'sec':        False,
        }

        try:
            return self.clf.connect(llcp=llcp_options)
        finally:
            self.clf.close()

if __name__ == '__main__':
    init()

