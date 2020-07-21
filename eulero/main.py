from eulero.src.menu  		import Menu
from eulero.src.clock 		import Clock
from eulero.src.torch 		import Torch
from eulero.src.weather	    import Weather
from eulero.src.settings 	import Settings
from eulero.src.stream      import Stream
from eulero.src.profile     import ProfilePic
from PIL   			import Image
import time
import threading

class Main(threading.Thread):
    def __init__(self, app):
        self.app=app
        self.i=0
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

        applications_name=["CLOCK","STREAM","TORCH","ROULETTE","WEATHER", "SETTINGS"]
        applications=[Clock(self.app), Stream(self.app),Torch(self.app),ProfilePic(self.app),Weather(self.app),Settings(self.app)]
        menu=Menu(self.app, applications_name)
        while(1):
            if(self.i==-1):
                self.i=menu.run()
            else:
                self.i=applications[self.i].run()

    def resumeConnection(self, so):
        self.app.changeSocket(so)
        self.app.getPinConfig("eulero/src/config/pinout.json")
        print("resumed")


