import socket
import importlib
import json
import binascii
from src.app import Application
#from src.device import Device

threadAssign = {}

users_path="users.json"
devices_path="devices.json"

users = {}
devices = {}

with open(users_path, "r") as rf:
	users = json.load(rf)

'''with open(devices_path, "r") as rf:
	devices = json.load(rf)'''

adress="192.168.1.14"
serv_port=50500
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((adress, serv_port))
sock.listen()

print("SERVER STARTED")
while(1):

	so, adr=sock.accept()
	print("-----\nNEW CONNECTION")
	mac=so.recv(1024)
	mac=binascii.hexlify(mac).decode()

	username = ''
	device = ''

	if mac in users:
		username=users[mac]
		print("connecting USER:", username)
	elif mac in devices:
		device = devices[mac]
		username=device
		print("connecting DEVICE:", device)
	
	'''deviceList[Device(), Device()]

	deviceList.append(Device())'''

	port = 0
	if username in threadAssign and threadAssign[username]["thread"].isAlive():
		port = threadAssign[username]["port"]
		threadAssign[username]["thread"]
		#threadAssign[username]["thread"].resumeConnection(so)
		UserMain = getattr(importlib.import_module(username+".main"), "Main")
		app = Application(so, username)
		user=UserMain(app)
		user.start()
	else:
		if username in threadAssign:
			threadAssign.pop(username)

		UserMain = getattr(importlib.import_module(username+".main"), "Main")
		app = Application(so, username)
		user=UserMain(app)

		threadAssign.__setitem__(username, {"thread": user, "port": port})
		user.start()

	print("-----")
	print(threadAssign)
	print("Clients connected: ", len(threadAssign))