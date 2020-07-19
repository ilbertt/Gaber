import threading

class Device(threading.Thread):
    def __init__(self, app, deviceName):
        self.app=app
        threading.Thread.__init__(self)
        self.name=deviceName
        self.available=False
        self.stream = False
        

    def run(self):
        self.app.getPinConfig("src/"+self.name+"/pinout.json")
        self.app.getConfig("src/"+self.name+"/config.json")

        change=True
        datap_old=0
        next_app=False
        i=0
        while(1):
            if (self.stream and self.available):
                change=False
                self.app.newImg()
                self.app.setText((10,0),"GBROS", 255,self.app.getFonts()[1])
                self.app.setText((32,32),"V 0.1", 255,self.app.getFonts()[1])
                data=self.app.sendImg_and_recvData()
            else:
                self.app.newImg()
                data=self.app.sendImg_and_recvData()
            #data=self.app.recvData()

            #print(data)	
            if (data['PROXIMITY']!=datap_old):
                datap_old=data['PROXIMITY']
                if(datap_old):
                    self.available=not self.available

                change=True

            '''if (next_app and data['SELECT']==0):
                next_app=False
                #menu.run()'''