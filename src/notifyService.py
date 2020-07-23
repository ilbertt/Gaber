from PIL   			import Image
import time
import threading

class NotifyService(threading.Thread):
    def __init__(self, app, router):
        self.app=app
        self.router=router
        self.username=self.app.username
        self.i=0
        self.recentDevices=[]
        #self.nearDeavices=[]
        self.device=0
        self.refused=[]
        threading.Thread.__init__(self)

    def run(self):
        while(not self.device):
            devs=self.router.listNearDevices(self.username)
            for dev in devs: 
                if(not (dev in self.recentDevices)):
                    dev.setStreamingUser(self.username)
                    self.device=dev
                    self.recentDevices.append(dev)

            for dev in self.recentDevices:
                if(not (dev in devs)):
                    self.recentDevices.remove(dev)
            

        self.app.startNotify()
        self.app.setText()
        stop=False
        while(not stop):
            data=self.app.recvData()


        self.app.stopNotify()
        self.app.device.resetStreamingUser()
        self.app.device=0
            
    def getUsedDevices(self):
        return self.recentDevices

