from gaber.src.menu  		import Menu
from gaber.src.clock 		import Clock
from gaber.src.torch 		import Torch
from gaber.src.weather	import Weather
from gaber.src.settings 	import Settings
from PIL   			import Image
import time
import threading

class Main(threading.Thread):
    def __init__(self, app):
        self.app=app
        threading.Thread.__init__(self)
    
    def run(self):
        self.app.getPinConfig("gaber/src/config/pinout.json")
        self.app.getConfig("gaber/src/config/config.json")
        pic=Image.open('gaber/src/images/pic.png')
        self.app.setImg(pic)
        self.app.sendImg()
        time.sleep(4)
        self.app.newImg()
        self.app.setText((10,0),"GBROS", 255,self.app.getFonts()[1])
        self.app.setText((32,32),"V 0.1", 255,self.app.getFonts()[1])
        self.app.sendImg()
        time.sleep(2)
        applications=[["CLOCK", Clock(self.app)],["TORCH", Torch(self.app)],["WEATHER", Weather(self.app)],["SETTINGS",Settings(self.app)]]
        menu=Menu(self.app, applications)
        applications[0][1].run(menu)


