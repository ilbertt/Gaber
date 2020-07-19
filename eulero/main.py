from eulero.src.menu  		import Menu
from eulero.src.clock 		import Clock
from eulero.src.torch 		import Torch
from eulero.src.weather	    import Weather
from eulero.src.settings 	import Settings
from eulero.src.stream      import Stream
from PIL   			import Image
import time
import threading

class Main(threading.Thread):
    def __init__(self, app):
        self.app=app
        threading.Thread.__init__(self)
    
    def run(self):
        self.app.getPinConfig("eulero/src/config/pinout.json")
        self.app.getConfig("eulero/src/config/config.json")
        pic=Image.open('eulero/src/images/pic.png')
        self.app.setImg(pic)
        self.app.sendImg()
        for _ in range(100):
            self.app.recvData()

        self.app.newImg()
        self.app.setText((10,0),"GBROS", 255,self.app.getFonts()[1])
        self.app.setText((32,32),"V 0.1", 255,self.app.getFonts()[1])
        self.app.sendImg()
        for _ in range(100):
            self.app.recvData()

        applications=[["CLOCK", Clock(self.app)],["STREAM", Stream(self.app)],["TORCH", Torch(self.app)],["WEATHER", Weather(self.app)],["SETTINGS",Settings(self.app)]]
        menu=Menu(self.app, applications)
        menu.run(0)

    def resumeConnection(self, so):
        self.app.changeSocket(so)
        self.app.getPinConfig("eulero/src/config/pinout.json")
        print("resumed")


