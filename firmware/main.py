import network
import socket
import gbros_fw

wlan=network.WLAN()
mac=wlan.config('mac')

while not wlan.isconnected():
    pass

connport=50500
adress="192.168.0.8"
#adress = socket.getaddrinfo("server.domain.com",connport)[0][-1][0]

so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.connect((adress, connport))
so.send(mac)
port=int(so.read())
so.close()
gbros_fw.run((adress, port))