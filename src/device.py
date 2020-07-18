import threading

class Device(threading.Thread):
    def __init__(self, app, deviceName):
        self.app=app
        threading.Thread.__init__(self)
        self.name=deviceName
        self.available=False
        

    def run(self):
        self.app.getPinConfig("src/"+self.name+"/pinout.json")
        self.app.getConfig("src/"+self.name+"/config.json")

        change=True
        datap_old=0
        next_app=False
        i=0
        while(1):
            '''if (change):
                change=False
                self.app.newImg()
                self.app.setText((35,0), "SETTINGS ", 255,self.app.getFonts()[0])
                self.app.setText((10,10),"CONTRAST ", 255,self.app.getFonts()[0])
                self.app.setText((10,20),"ROTATION ", 255,self.app.getFonts()[0])
                self.app.setText((10,30),"MENU ", 255,self.app.getFonts()[0])
                self.app.setText((1,10+i*10),">", 255,self.app.getFonts()[0])
                data=self.app.sendImg_and_recvData()
            else:
                data=self.app.recvData()'''
            data=self.app.recvData()

            #print(data)	
            if (data['PROXIMITY']!=datap_old):
                datap_old=data['PROXIMITY']
                if(datap_old):
                    self.available=not self.available

                change=True

            '''if (next_app and data['SELECT']==0):
                next_app=False
                #menu.run()'''