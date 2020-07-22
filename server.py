import socket
import importlib
import json
import binascii
from src.app 		import Application
from src.device 	import Device
from src.router 	import Router

threadAssign = {}

users_path="users.json"
devices_path="devices.json"

users = {}
devices = {}

with open(users_path, "r") as rf:
	users = json.load(rf)

with open(devices_path, "r") as rf:
	devices = json.load(rf)

adress="192.168.1.4"
serv_port=50500
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((adress, serv_port))
sock.listen()

router = Router()

print("SERVER STARTED")
while(1):

	so, adr=sock.accept()
	so.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)	# send data separately
	print("-----\nNEW CONNECTION")
	print(adr)
	mac=so.recv(1024)
	mac=binascii.hexlify(mac).decode()
	print(mac)

	username = ''
	device = ''

	if mac in users:
		username=users[mac]

		if username in threadAssign and threadAssign[username]["thread"].isAlive():
			print("resuming USER:", username)
			threadAssign[username]["thread"].resumeConnection(so)
			
		else:
			if username in threadAssign:
				print("dead USER", username)
				threadAssign.pop(username)

			print("connecting USER:", username)
			UserMain = getattr(importlib.import_module(username+".main"), "Main")
			app = Application(so, adr, username, router)
			user=UserMain(app)

			threadAssign.__setitem__(username, {"thread": user})
			user.start()

	elif mac in devices:
		device = devices[mac]
		

		if device in threadAssign and threadAssign[device]["thread"].isAlive():
			print("resuming DEVICE:", device)
			threadAssign[device]["thread"].resumeConnection(so)
			
		else:
			if device in threadAssign:
				print("dead DEVICE", device)
				threadAssign.pop(device)
				router.removeDevice(device)
		
			print("connecting DEVICE:", device)
			deviceApp = Application(so, adr, device, router)
			dev = Device(deviceApp, device)
			dev.start()
			threadAssign.__setitem__(device, {"thread": dev})
			router.addDevice(dev)

	print("Clients connected:", len(threadAssign))
	print("-----")
