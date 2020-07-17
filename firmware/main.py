import network
import socket
import gbros_fw
import time

wlan=network.WLAN()

# get esp mac address
mac=wlan.config('mac')

while not wlan.isconnected():
    pass

# configuration port for new client
connport=50500

# server address
adress="192.168.0.8"
#adress = socket.getaddrinfo("server.domain.com",connport)[0][-1][0]

so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
so.connect((adress, connport))
so.send(mac)

time.sleep(1)

# run client firmware with communication port
gbros_fw.run(so)