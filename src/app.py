import socket
from PIL import Image, ImageDraw, ImageFont, ImageOps
import time
import json

class Application:

	def __init__(self, adress, port):
		self.heigth=0
		self.width=0
		self.fonts = [ImageFont.truetype("Arial.ttf",11),ImageFont.truetype("Arial.ttf",30)]
		self.img=Image.new("L",(self.heigth,self.width))
		self.d=ImageDraw.Draw(self.img)
		self.d.rectangle((0,0,self.heigth,self.width),fill=0)
		self.addr=(adress, port)
		self.so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.so.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.so.bind(("0.0.0.0", 1234))
		self.so.listen(1)
		self.confpath=""
		self.config={"contrast": 0,  "rotation": 0}
		self.sc=0
		self.data=0
		self.ispic=False
		self.neoPins=[15]
		self.inPins = {}
		self.outPins = {}

	def __send(self,data):
		self.sc.send(data)
		self.sc.close()

	def __recv(self):
		self.sc, adr=self.so.accept()
		self.sc.settimeout(0.01)
		try:
			self.data=int(self.sc.recv(1024))
		except:
			pass

		return self.data
	
	def getPinConfig(self, path):
		with open(path, "r") as rf:
			tmp = json.load(rf)
			self.inPins = tmp["in"]
			self.outPins = tmp["out"]
			self.setInPins()
			for neo in tmp["neopixel"]:
				self.setNeoPin(tmp["neopixel"][neo]["number"])

			if(tmp["display"]):
				self.heigth=tmp["display"]["heigth"]
				self.width=tmp["display"]["width"]
				self.setDisplqy(tmp["display"]["sda"], tmp["display"]["scl"], self.heigth, self.width)


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
		self.__send(str(pin*10+int(not value)).encode())
		time.sleep(0.05)

	def setInPin(self, pin):
		self.__recv()
		self.__send(str(pin).encode())
		time.sleep(0.05)

	def setDisplqy(self, sda, scl, heigth, width):
		self.heigth = heigth
		self.width = width
		self.__recv()
		self.__send((str(sda).zfill(2)+str(scl).zfill(2)+str(heigth).zfill(3)+str(width).zfill(3)).encode())
		time.sleep(0.05)
		
	def setNeopixel(self, status, pin=-1):
		if(len(self.neoPins)):
			self.__recv()
			if(pin==-1):
				self.__send((str(self.neoPins[0]).zfill(2)+str(status[0]).zfill(3)+str(status[1]).zfill(3)+str(status[2]).zfill(3)).encode())
			elif(pin in self.neoPins):
				self.__send((str(pin).zfill(2)+str(status[0]).zfill(3)+str(status[1]).zfill(3)+str(status[2]).zfill(3)).encode())
			else:
				self.__send(b'')

			time.sleep(0.05)

	def recvData(self):
		data=self.__recv()
		self.__send(b'')
		time.sleep(0.05)
		buttons={}
		for pin in self.inPins:
			if(data & 1<<self.inPins[pin]["number"]):
				buttons[pin]=1
			else:
				buttons[pin]=0
		print(buttons)
		return data

	def sendImg_and_recvData(self):
		if (self.config["rotation"]):
			pic=self.img
		else:
			pic=self.img.rotate(180)

		if(self.config["contrast"] and not(self.ispic)):
			pic=ImageOps.colorize(pic, (255,255,255), (0,0,0))
			self.ispic=False

		pic=pic.convert('1')
		pic=pic.tobytes()
		data=self.__recv()
		buttons={}
		#time.sleep(0.05)
		if(self.heigth and self.width):
			self.__send(pic)
		else:
			self.__send(b'')

		time.sleep(0.05)
		for pin in self.inPins:
			if(data & 1<<self.inPins[pin]["number"]):
				buttons[pin]=1
			else:
				buttons[pin]=0
		print(buttons)

		return data

	def sendImg(self):
		if(self.heigth and self.width):
			if (self.config["rotation"]):
				pic=self.img
			else:
				pic=self.img.rotate(180)

			if(self.config["contrast"] and not(self.ispic) ):
				pic=ImageOps.colorize(pic, (255,255,255), (0,0,0))
				self.ispic=False

			pic=pic.convert('1')
			pic=pic.tobytes()
			self.__recv()
			self.__send(pic)
			time.sleep(0.05)

	def setText(self,pos,txt, txt_color, txt_font):
		self.d.text(pos, txt, txt_color,font=txt_font)

	def setContrast(self, contrast):
		self.config["contrast"]=contrast
		with open(self.confpath, "w") as rf:
			json.dump(self.config, rf)

	def setRotation(self, rotation):
		self.config["rotation"]=rotation
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

