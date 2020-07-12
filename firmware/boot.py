

# This file is executed on every boot (including wake-boot from deepsleep)

#import esp

#esp.osdebug(None)

import uos, machine
import time


#uos.dupterm(None, 1) # disable REPL on UART(0)

import gc


#import webrepl

#webrepl.start()
gc.collect()

import network
import socket
import gbros_fw

time.sleep(2)
adress="192.168.0.107"
connport=1234
wlan=network.WLAN()
mac=wlan.config('mac')
so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.connect((adress, connport))
so.send(mac.encode())
port=so.read()
so.close()
gbros_fw.run((adress, port))