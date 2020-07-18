import socket
from PIL import Image, ImageDraw, ImageFont, ImageOps
import time
import json
import sys

class Application:

	def __init__(self, sc, username, devicesList=None):
		self.heigth=0
		self.width=0
		self.username = username

		self.devicesList = devicesList
		self.availableDevices = []

		self.fonts = [ImageFont.truetype("Arial.ttf",11),ImageFont.truetype("Arial.ttf",30)]
		self.img=Image.new("L",(self.heigth,self.width))
		self.d=ImageDraw.Draw(self.img)
		self.d.rectangle((0,0,self.heigth,self.width),fill=0)
		self.confpath=0
		self.config={"contrast": 0,  "rotation": 0}
		self.sc=sc
		self.data=0
		#self.dead=False
		self.buttons={}
		self.ispic=False
		self.neoPins=[15]
		self.inPins = {}
		self.outPins = {}
		self.pwmPins= {}
		#self.path=""
		self.dispList= {"sh1106":0, "ssd1306":1}
		#self.sc, adr=self.so.accept()
		self.sc.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY,1)

	def __send(self,data):
		self.sc.settimeout(10)
		try:
			self.sc.send(data)
		except:
			pass
		"""try:
			self.sc.send(data)
		except:
			print("dead")
			self.dead=True
			while(self.dead):
				time.sleep(0.01)
			
			self.getPinConfig(self.path)"""

	def __recv(self):
		self.sc.settimeout(0.05)
		try:
			self.data=int(self.sc.recv(1024))
		except:
			pass

		return self.data
	
	def getPinConfig(self, path):
		with open(path, "r") as rf:
			#self.path=path
			tmp = json.load(rf)
			self.inPins = tmp["in"]
			self.outPins = tmp["out"]
			self.setInPins()
			if("pwm" in tmp):
				self.pwmPins= tmp["pwm"]

			for neo in tmp["neopixel"]:
				self.setNeoPin(tmp["neopixel"][neo]["number"])

			if(tmp["display"]):
				self.heigth=tmp["display"]["heigth"]
				self.width=tmp["display"]["width"]
				self.setDisplay(tmp["display"]["sda"], tmp["display"]["scl"], self.heigth, self.width, tmp["display"]["type"])

	"""def changeSocket(self, sc):
		self.sc=sc
		self.dead=False"""

	def getConfig(self, path):
		self.confpath=path
		with open(path, "r") as rf:
			self.config=json.load(rf)

	def setInPins(self):
		for pin in self.inPins:
			self.setInPin(self.inPins[pin]['number'])

	def setNeoPin(self, pin):
		self.neoPins.append(pin)

	def setOutPin(self, pin, value):
		self.__recv()
		self.__send(str(pin*10+int(not value)).zfill(3).encode())
		time.sleep(0.01)

	def setInPin(self, pin):
		self.__recv()
		self.__send(str(pin).zfill(2).encode())
		time.sleep(0.01)

	def setDisplay(self, sda, scl, heigth, width, dispType):
		self.heigth = heigth
		self.width = width
		disp=self.dispList[dispType]
		self.__recv()
		self.__send((str(sda).zfill(2)+str(scl).zfill(2)+str(heigth).zfill(3)+str(width).zfill(3)+str(disp).zfill(2)).encode())
		time.sleep(0.01)

	def setPwm(self, pin, freq, duty):
		self.__recv()
		self.__send((str(pin).zfill(2)+str(freq).zfill(3)+str(duty).zfill(4)).encode())
		time.sleep(0.01)
		
	def setNeopixel(self, status, pin=-1):
		if(len(self.neoPins)):
			self.__recv()
			if(pin==-1):
				self.__send((str(self.neoPins[0]).zfill(2)+str(status[0]).zfill(3)+str(status[1]).zfill(3)+str(status[2]).zfill(3)).encode())
			elif(pin in self.neoPins):
				self.__send((str(pin).zfill(2)+str(status[0]).zfill(3)+str(status[1]).zfill(3)+str(status[2]).zfill(3)).encode())
			else:
				self.__send(b'')

			time.sleep(0.01)

	def recvData(self):
		data=self.__recv()
		self.__send(b'')
		for pin in self.inPins:
			if(data & 1<<self.inPins[pin]["number"]):
				self.buttons[pin]=1
			else:
				self.buttons[pin]=0

		time.sleep(0.01)
		#print(self.buttons)
		return self.buttons

	def sendImg_and_recvData(self):
		if (self.config["rotation"]):
			pic=self.img
		else:
			pic=self.img.rotate(180)

		if(self.config["contrast"] and not(self.ispic)):
			pic=ImageOps.colorize(pic, (255,255,255), (0,0,0))
		
		if(self.ispic):
			self.ispic=False

		pic=pic.convert('1')
		pic=pic.tobytes()
		self.data=self.__recv()
		#time.sleep(0.05)
		if(self.heigth and self.width):
			self.__send(pic[:512])
			time.sleep(0.01)
			self.__recv()
			self.__send(pic[512:])
		else:
			self.__send(b'')

		for pin in self.inPins:
			if(self.data & 1<<self.inPins[pin]["number"]):
				self.buttons[pin]=1
			else:
				self.buttons[pin]=0

		time.sleep(0.01)
		#print(self.buttons)
		return self.buttons

	def sendImg(self):
		if(self.heigth and self.width):
			if (self.config["rotation"]):
				pic=self.img
			else:
				pic=self.img.rotate(180)

			if(self.config["contrast"] and not(self.ispic) ):
				pic=ImageOps.colorize(pic, (255,255,255), (0,0,0))
			
			if(self.ispic):
				self.ispic=False

			pic=pic.convert('1')
			pic=pic.tobytes()
			self.__recv()
			self.__send(pic[:512])
			#time.sleep(0.01)
			self.__recv()
			self.__send(pic[512:])
				
			time.sleep(0.01)

	def setText(self,pos,txt, txt_color, txt_font):
		self.d.text(pos, txt, txt_color,font=txt_font)

	def setContrast(self, contrast):
		self.config["contrast"]=contrast
		if(self.confpath):
			with open(self.confpath, "w") as rf:
				json.dump(self.config, rf)

	def setRotation(self, rotation):
		self.config["rotation"]=rotation
		if(self.confpath):
			with open(self.confpath, "w") as rf:
				json.dump(self.config, rf)

	def getFonts(self):
		return self.fonts

	def setImg(self, img):
		self.img=img.convert('L')
		self.ispic = True

	def addFont(self, font, font_size):
		self.fonts.append(ImageFont.truetype(font, font_size))

	def newImg(self):
		self.img=Image.new("L",(self.heigth,self.width))
		self.d=ImageDraw.Draw(self.img)
		self.d.rectangle((0,0,self.heigth,self.width),fill=0)

	def fillImg(self, img_color):
		self.d.rectangle((0,0,self.heigth,self.width),fill=img_color)

	def addAvailDevice(self, device):
		print("adding", device)
		if not (device in self.availableDevices):
			self.availableDevices.append(device)

		#print(self.availableDevices)
	
	def removeAvailDevice(self, device):
		print("removing", device)
		if device in self.availableDevices:
			self.availableDevices.remove(device)
		#print(self.availableDevices)