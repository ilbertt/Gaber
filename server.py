import socket
import importlib
import json
import binascii
from src.app import Application
from src.device import Device

threadAssign = {}

users_path="users.json"
devices_path="devices.json"

users = {}
devices = {}

devicesList = []

with open(users_path, "r") as rf:
	users = json.load(rf)

with open(devices_path, "r") as rf:
	devices = json.load(rf)

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
	print(mac)

	username = ''
	device = ''

	if mac in users:
		username=users[mac]
		print("connecting USER:", username)

		if username in threadAssign and threadAssign[username]["thread"].isAlive():
			threadAssign[username]["thread"]
			#threadAssign[username]["thread"].resumeConnection(so)
		else:
			if username in threadAssign:
				threadAssign.pop(username)

		UserMain = getattr(importlib.import_module(username+".main"), "Main")
		app = Application(so, username, devicesList)
		user=UserMain(app)

		threadAssign.__setitem__(username, {"thread": user})
		user.start()

	elif mac in devices:
		device = devices[mac]
		deviceApp = Application(so, device)
		print("connecting DEVICE:", device)
		dev = Device(deviceApp, device)
		dev.start()
		#dev.run()
		devicesList.append(dev)

	print("-----")
	#print(threadAssign)
	#print("Clients connected: ", len(threadAssign))