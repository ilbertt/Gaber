import socket
import importlib
import json

freeports=[1235,1236,1237, 1238]
occports=[]
threads=[]
adress="0.0.0.0"
serv_port=1234
path="users.json"


while(1):
	for thread in threads:
		if(not thread.isAlive()):
			uport=thread.port
			threads.remove(thread)
			occports.remove(uport)
			freeports.append(uport)

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((adress, serv_port))
	sock.listen()
	so, adr=sock.accept()
	mac=so.recv(1024)
	port=freeports[0]
	freeports.pop(0)
	occports.append(port)
	so.send(port)
	so.close()
	rf=open(path, "r")
	dic=json.load(rf)
	username=dic[mac]
	MyClass = getattr(importlib.import_module(username+".main"), "Main")
	user=MyClass(adress, port, username)
	threads.append(user)
	user.start()
	