import network
import socket
import gbros_fw

adress="192.168.0.107"
connport=1234
wlan=network.WLAN()
mac=wlan.config('mac')
so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.connect((adress, connport))
so.send(mac)
port=int(so.read())
so.close()
gbros_fw.run((adress, port))
