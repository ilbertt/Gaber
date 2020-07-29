import socket
from PIL import Image, ImageDraw, ImageFont, ImageOps
import time
import json
import sys

class Application:

	def __init__(self, sc, address, userData, router=None):
		self.heigth=0
		self.width=0
		self.address=address
		self.userData = userData

		self.router = router

		self.fonts = [ImageFont.truetype("Arial.ttf",11),ImageFont.truetype("Arial.ttf",30)]
		self.img=Image.new("L",(self.heigth,self.width))
		self.imgOld=self.img
		self.d=ImageDraw.Draw(self.img)
		self.d.rectangle((0,0,self.heigth,self.width),fill=0)
		
		self.confpath=0
		self.config={"contrast": 0,  "rotation": 0}

		self.sc=sc
		self.data=0
		self.canSend=True
		self.recvTime=time.time()
		self.buttons={}

		self.ispic=False

		self.neoPins=[]
		self.inPins = {}
		self.outPins = {}
		self.pwmPins= {}
		self.imgIsNew=False
		self.notifyStarted=False
		self.alive=True
		self.dispList= {"sh1106":0, "ssd1306":1}	

	def __send(self,data):
		if (self.canSend and self.alive):
			self.sc.settimeout(10)
			try:
				self.sc.send(data)
			except:
				pass
	
	def __sendc(self, data):
		self.sc.settimeout(10)
		try:
			self.sc.send(data)
		except:
			pass

	def __recv(self):
		if(self.alive):
			self.sc.settimeout(0.05)
			try:
				self.data=int(self.sc.recv(1024))
				self.recvTime = time.time()
			except:
				if time.time() - self.recvTime > 20:
					print(self.getUsername()+": dead")
					self.sc.close()
					self.alive=False
					#sys.exit(0)
					
				pass

		return self.data

	def __recvNFC(self):
		data='0'
		if(self.alive):
			self.sc.settimeout(1.5)
			try:
				data=self.sc.recv(1024).decode()
				self.recvTime = time.time()
			except:
				pass
		if(data!='0'):
			data=data.split(":")
			if(len(data)>=2):
				data=data[1]
				if(not len(data)==8):
					data='0'
			
		
		return data
	
	def appSleep(self, recvNumber, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			for _ in range(recvNumber):
				self.recvData()
		else:
			time.sleep(0.01)

	def getPinConfig(self, path):
		with open(path, "r") as rf:
			tmp = json.load(rf)
			self.inPins = tmp["in"]
			self.outPins = tmp["out"]
			self.setInPins()
			if("pwm" in tmp):
				self.pwmPins= tmp["pwm"]

			if ("neopixel" in tmp):
				for neo in tmp["neopixel"]:
					self.setNeoPin(tmp["neopixel"][neo]["number"])

			if ("display" in tmp):
				self.heigth=tmp["display"]["heigth"]
				self.width=tmp["display"]["width"]
				self.setDisplay(tmp["display"]["sda"], tmp["display"]["scl"], self.heigth, self.width, tmp["display"]["type"])

			if ("nfc" in tmp):
				self.setNFC(tmp["nfc"]["sclk"],tmp["nfc"]["mosi"],tmp["nfc"]["miso"],tmp["nfc"]["rst"],tmp["nfc"]["sda"])
		
		self.canSend = True

	def getUsername(self):
		return self.userData["name"]
	
	def getUid(self):
		if "uid" in self.userData:
			return self.userData["uid"]

	def changeSocket(self, sc):
		print("changing socket...")
		self.recvTime = time.time()
		self.canSend = False
		self.sc=sc

	def getConfig(self, path):
		self.confpath=path
		with open(path, "r") as rf:
			self.config=json.load(rf)

	def setInPins(self):
		for pin in self.inPins:
			self.setInPin(self.inPins[pin]['number'])

	def setNeoPin(self, pin):
		if not (pin in self.neoPins):
			self.neoPins.append(pin)

	def setOutPin(self, pin, value, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.__recv()
			self.__send(str(pin*10+int(not value)).zfill(3).encode())

		time.sleep(0.01)

	def setInPin(self, pin, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.__recv()
			self.__sendc(str(pin).zfill(2).encode())

		time.sleep(0.01)

	def setDisplay(self, sda, scl, heigth, width, dispType, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.heigth = heigth
			self.width = width
			disp=self.dispList[dispType]
			self.__recv()
			self.__sendc((str(sda).zfill(2)+str(scl).zfill(2)+str(heigth).zfill(3)+str(width).zfill(3)+str(disp).zfill(2)).encode())
		
		time.sleep(0.01)

	def setPwm(self, pin, freq, duty, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.__recv()
			self.__send((str(pin).zfill(2)+str(freq).zfill(3)+str(duty).zfill(4)).encode())
		
		time.sleep(0.01)

	def readAdc(self, pin, resolution=1024, notify=False):
		data=0
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.__recv()
			self.__send(str(pin).zfill(4))
			time.sleep(0.01)
			data=int(self.__recv())%resolution
			self.__send(b'')

		time.sleep(0.01)
		return data

	def setNFC(self, sclk, mosi, miso, rst, sda, notify=True):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.__recv()
			self.__sendc((str(sclk).zfill(2)+str(mosi).zfill(2)+str(miso).zfill(2)+str(rst).zfill(2)+str(sda).zfill(2)).encode())
		
		time.sleep(0.01)

	def readNFC(self, notify=False):
		data='0'
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.__recv()
			self.__send(b'1')
			time.sleep(0.01)
			data=self.__recvNFC()
			self.__send(b'')

		time.sleep(0.01)
		return data
		
	def setNeopixel(self, status, pin=-1, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			if(len(self.neoPins)):
				self.__recv()
				if(pin==-1):
					self.__send((str(self.neoPins[0]).zfill(2)+str(status[0]).zfill(3)+str(status[1]).zfill(3)+str(status[2]).zfill(3)).encode())
				elif(pin in self.neoPins):
					self.__send((str(pin).zfill(2)+str(status[0]).zfill(3)+str(status[1]).zfill(3)+str(status[2]).zfill(3)).encode())
				else:
					self.__send(b'')

		time.sleep(0.01)

	def recvData(self, notify=False):
		data=0
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			data=self.__recv()
			self.__send(b'')
		buttons = {}
		for pin in self.inPins:
			if(data & 1<<self.inPins[pin]["number"]):
				buttons[pin]=1
			else:
				buttons[pin]=0

		time.sleep(0.01)
		#print(self.buttons)
		return buttons

	def sendImg_and_recvData(self, notify=False):
		data=0
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
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
			data=self.__recv()
			#time.sleep(0.05)
			if(self.heigth and self.width and self.imgIsNew):
				self.imgIsNew=False
				l=int(len(pic)/2)
				self.__send(pic[:l])
				time.sleep(0.01)
				self.__recv()
				self.__send(pic[l:])
				time.sleep(0.01)
				self.__send(b'')
				self.__recv()
			else:
				self.__send(b'')

		buttons = {}
		for pin in self.inPins:
			if(data & 1<<self.inPins[pin]["number"]):
				buttons[pin]=1
			else:
				buttons[pin]=0

		time.sleep(0.01)
		#print(self.buttons)
		return buttons

	def sendImg(self, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			if(self.heigth and self.width):
				if (self.config["rotation"]):
					pic=self.img
				else:
					pic=self.img.rotate(180)

				if(self.config["contrast"] and not(self.ispic) ):
					pic=ImageOps.colorize(pic, (255,255,255), (0,0,0))
				
				if(self.ispic):
					self.ispic=False

				if(self.imgIsNew):
					self.imgIsNew=False
					pic=pic.convert('1')
					pic=pic.tobytes()
					l=int(len(pic)/2)
					self.__recv()
					self.__send(pic[:l])
					time.sleep(0.01)
					self.__recv()
					self.__send(pic[l:])
					time.sleep(0.01)
					self.__send(b'')
					self.__recv()
				
		
		time.sleep(0.01)

	def resumeImg(self):
		self.imgIsNew=True
		self.sendImg()

	def setText(self,pos,txt, txt_color, txt_font, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.imgIsNew=True
			self.d.text(pos, txt+" ", txt_color,font=txt_font)

	def setContrast(self, contrast, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.imgIsNew=True
			self.config["contrast"]=contrast
			if(self.confpath):
				with open(self.confpath, "w") as rf:
					json.dump(self.config, rf)

	def setRotation(self, rotation, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.imgIsNew=True
			self.config["rotation"]=rotation
			if(self.confpath):
				with open(self.confpath, "w") as rf:
					json.dump(self.config, rf)

	def setCustomParams(self, customParams):
		self.config["custom"] = customParams
		if(self.confpath):
			with open(self.confpath, "w") as rf:
				json.dump(self.config, rf)
	
	def getCustomParams(self):
		if(self.confpath):
			with open(self.confpath, "r") as rf:
				tmp = json.load(rf)
				return tmp["custom"]

	def getFonts(self):
		return self.fonts

	def setImg(self, img, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.imgIsNew=True
			self.img=img.convert('L')
			self.ispic = True

	def addFont(self, font, font_size):
		self.fonts.append(ImageFont.truetype(font, font_size))

	def newImg(self, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.imgIsNew=True
			self.img=Image.new("L",(self.heigth,self.width))
			self.d=ImageDraw.Draw(self.img)
			self.d.rectangle((0,0,self.heigth,self.width),fill=0)
	
	def fillImg(self, img_color, notify=False):
		if((self.notifyStarted and notify) or (not self.notifyStarted)):
			self.imgIsNew=True
			self.d.rectangle((0,0,self.heigth,self.width),fill=img_color)
	
	def getIpAddress(self):
		return self.address[0]

	def startNotify(self):
		self.imgOld=self.img
		self.newImg()
		self.notifyStarted=True
		self.config["contrast"] = not self.config["contrast"]

	def stopNotify(self):
		self.notifyStarted=False
		self.newImg()
		self.img=self.imgOld
		self.config["contrast"] = not self.config["contrast"]
		self.sendImg()

	def isAlive(self):
		return self.alive
		