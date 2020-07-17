from tv.src.proximity   import Proximity
from PIL   			import Image
import time
import threading

class Main(threading.Thread):
    def __init__(self, app):
        self.app=app
        threading.Thread.__init__(self)
    
    def run(self):
        self.app.getPinConfig("tv/src/config/pinout.json")
        self.app.getConfig("tv/src/config/config.json")
        pic=Image.open('tv/src/images/pic.png')
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

        prox=Proximity(self.app)
        prox.run()


