from gaber.src.menu  		import Menu
from gaber.src.clock 		import Clock
from gaber.src.torch 		import Torch
from gaber.src.weather	    import Weather
from gaber.src.settings 	import Settings
from gaber.src.stream       import Stream
from gaber.src.profile     import ProfilePic

from src.notifyService      import NotifyService

from PIL   			import Image
import time
import threading

class Main(threading.Thread):
    def __init__(self, app):
        self.app=app
        self.i=0
        threading.Thread.__init__(self)
        self.name = self.app.username
    
    def run(self):
        self.app.getPinConfig("gaber/src/config/pinout.json")
        self.app.getConfig("gaber/src/config/config.json")
        pic=Image.open('gaber/src/images/pic.png')
        self.app.setImg(pic)
        self.app.sendImg()
        self.app.appSleep(100)

        self.app.newImg()
        self.app.setText((10,0),"GBROS", 255,self.app.getFonts()[1])
        self.app.setText((32,32),"V 0.2", 255,self.app.getFonts()[1])
        self.app.sendImg()
        self.app.appSleep(100)

        NotifyService(self.app, self.app.router).start()

        applications_name=["CLOCK","TORCH", "WEATHER","STREAM","ROULETTE","SETTINGS"]
        applications=[Clock(self.app), Torch(self.app), Weather(self.app), Stream(self.app), ProfilePic(self.app), Settings(self.app)]
        menu=Menu(self.app, applications_name)
        while(self.app.isAlive()):
            if(self.i==-1):
                self.i=menu.run()
            else:
                self.i=applications[self.i].run()

    def resumeConnection(self, so):
        self.app.changeSocket(so)
        self.app.getPinConfig("gaber/src/config/pinout.json")
        self.app.resumeImg()
        print("resumed")

    def isRunning(self):
        return self.app.isAlive()


