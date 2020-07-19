import threading

class Device(threading.Thread):
    def __init__(self, app, deviceName):
        self.app=app
        threading.Thread.__init__(self)
        self.name=deviceName
        self.available=False
        self.stream = False
        #self.router = self.app.router

    def run(self):
        self.app.getPinConfig("src/"+self.name+"/pinout.json")
        self.app.getConfig("src/"+self.name+"/config.json")

        datap_old=0
        
        while(1):
            if (self.stream and self.available):
                self.app.getRouterImg()
                data=self.app.sendImg_and_recvData()
            else:
                self.app.newImg()
                data=self.app.sendImg_and_recvData()

            #print(data)	
            if (data['PROXIMITY']!=datap_old):
                datap_old=data['PROXIMITY']
                if(datap_old):
                    self.available=not self.available

            '''if (next_app and data['SELECT']==0):
                next_app=False
                #menu.run()'''