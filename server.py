import socket
import importlib
import json
import binascii
from src.app import Application

freeports=[50501,50502,50503,50504]
occports=[]
threads=[]
threadAssign = {}

adress="192.168.0.107"
serv_port=50500
path="users.json"
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((adress, serv_port))
sock.listen()

while(1):
	print("started")
	for thread in threads:
		if(not thread.isAlive()):
			uport=thread.app.adress[1]
			threads.remove(thread)
			occports.remove(uport)
			freeports.append(uport)

	so, adr=sock.accept()
	print("connected")
	mac=so.recv(1024)
	mac=binascii.hexlify(mac).decode()
	
	rf=open(path, "r")
	dic=json.load(rf)
	username=dic[mac]
	print(username)
	rf.close()

	port = 0
	if username in threadAssign and threadAssign[username]["thread"].isAlive():
		port = threadAssign[username]["port"]
		so.send(str(port).encode())
		so.close()

		threadAssign[username]["thread"].sendPinConfig()
	else:
		if username in threadAssign:
			threadAssign.pop(username)
		port=freeports[0]
		freeports.pop(0)
		occports.append(port)
		so.send(str(port).encode())
		so.close()

		UserMain = getattr(importlib.import_module(username+".main"), "Main")
		app=Application(adress, port, username, 0.05)
		user=UserMain(app)
		threads.append(user)

		threadAssign.__setitem__(username, {"thread": user, "port": port})
		user.start()
		
	print(threadAssign)
	print("Clients connected: ", len(threadAssign))