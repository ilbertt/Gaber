import socket
from PIL import Image, ImageDraw, ImageFont, ImageOps
import time

class Application:

	def __init__(self, adress, port, heigth,width):
		self.heigth=heigth
		self.width=width
		self.fonts = [ImageFont.truetype("Arial.ttf",11),ImageFont.truetype("Arial.ttf",30)]
		self.img=Image.new("L",(self.heigth,self.width))
		self.d=ImageDraw.Draw(self.img)
		self.d.rectangle((0,0,self.heigth,self.width),fill=0)
		self.addr=(adress, port)
		self.contrast=0
		self.rotation=0

	def __send(self,data):
		sc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sc.connect(self.addr)
		sc.send(data)
		sc.close()

	def __recv(self):
		sc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sc.connect(self.addr)
		data=sc.recv(1024)
		sc.close()
		return data

	def sendImg(self):
		if (self.rotation):
			pic=self.img
		else:
			pic=self.img.rotate(180)
		
		if(self.contrast):
			pic=ImageOps.colorize(pic, (255,255,255), (0,0,0))

		pic=pic.convert('1')
		pic=pic.tobytes()
		self.__send(pic)
		time.sleep(0.05)
		self.__recv()
		time.sleep(0.05)

	def recvData(self):
		self.__send(b'')
		time.sleep(0.1)
		data=self.__recv()
		time.sleep(0.05)
		return data

	def setLed(self, status):
		self.__send(str(int(status)).encode())
		time.sleep(0.05)
		self.__recv()
		time.sleep(0.05)

	def setNeopixel(self, status):
		self.__send((str(status[0]).zfill(3)+str(status[1]).zfill(3)+str(status[2]).zfill(3)).encode())
		time.sleep(0.05)
		self.__recv()
		time.sleep(0.05)

	def sendImg_and_recvData(self):
		if (self.rotation):
			pic=self.img
		else:
			pic=self.img.rotate(180)

		if(self.contrast):
			pic=ImageOps.colorize(pic, (255,255,255), (0,0,0))

		pic=pic.convert('1')
		pic=pic.tobytes()
		self.__send(pic)
		time.sleep(0.05)
		data=self.__recv()
		time.sleep(0.05)
		return data

	def setText(self,pos,txt, txt_color, txt_font):
		self.d.text(pos, txt, txt_color,font=txt_font)

	def setContrast(self, contrast):
		self.contrast = int(contrast)

	def setRotation(self, rotation):
		self.rotation = int(rotation)

	def getFonts(self):
		return self.fonts

	def setImg(self, img):
		self.img=img.convert('L')

	def addFont(self, font, font_size):
		self.fonts.append(ImageFont.truetype(font, font_size))

	def newImg(self):
		self.img=Image.new("L",(self.heigth,self.width))
		self.d=ImageDraw.Draw(self.img)
		self.d.rectangle((0,0,self.heigth,self.width),fill=0)

	def fillImg(self, img_color):
		self.d.rectangle((0,0,self.heigth,self.width),fill=img_color)

