from gaber.src.app   		import Application
from gaber.src.menu  		import Menu
from gaber.src.clock 		import Clock
from gaber.src.torch 		import Torch
from gaber.src.weather	import Weather
from gaber.src.settings 	import Settings
from PIL   			import Image
import time
import threading

class Main(threading.Thread):
    def __init__(self, adress, port, username):
        self.adress = adress
        self.port = port
        self.username = username
        threading.Thread.__init__(self)
    
    def run(self):
        app=Application(self.adress, self.port, self.username)
        app.getPinConfig("gaber/src/config/pinout.json")
        print("dkdk")
        app.getConfig("gaber/src/config/config.json")
        pic=Image.open('gaber/src/images/pic.png')
        app.setImg(pic)
        app.sendImg()
        time.sleep(4)
        app.newImg()
        app.setText((10,0),"GBROS", 255,app.getFonts()[1])
        app.setText((32,32),"V 0.1", 255,app.getFonts()[1])
        app.sendImg()
        time.sleep(2)
        applications=[["CLOCK", Clock(app)],["TORCH", Torch(app)],["WEATHER", Weather(app)],["SETTINGS",Settings(app)]]
        menu=Menu(app, applications)
        applications[0][1].run(menu)


