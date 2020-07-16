import network
import socket
import gbros_fw
import time

adress="192.168.0.111"
connport=1234
wlan=network.WLAN()
mac=wlan.config('mac')
so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.connect((adress, connport))
so.send(mac)
time.sleep(1)
gbros_fw.run(so)