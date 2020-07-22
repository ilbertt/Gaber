from PIL   			import Image
import time
import threading

class NotifyService(threading.Thread):
    def __init__(self, app, router):
        self.app=app
        self.i=0
        self.devices=0
        self.router=router
        self.nearDeavices=[]
        self.refused=[]
        threading.Thread.__init__(self)

    def run(self):
        while(self.device==0):
            devs=self.router.listNearDevices(self.app.username)
            if(devs!=self.devices):
                for devices
            


