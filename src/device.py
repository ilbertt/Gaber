import threading

class Device(threading.Thread):
    def __init__(self, app, deviceName):
        self.__app=app
        threading.Thread.__init__(self)
        self.name=deviceName
        self.isNear=False
        self.stream = False
        self.streamingUser = ""
        self.sendType=''
        self.arguments=[]
        self.data={}
        self.adcvalue=0

        self.busy=False

    def run(self):
        self.__app.getPinConfig("src/"+self.name+"/pinout.json")
        self.__app.getConfig("src/"+self.name+"/config.json")

        datap_old=0
        disc=False
        self.newImg()
        while(1):
            if (self.stream and self.isNear):
                self.busy=True
                if(self.sendType=="image"):
                    self.sendType=""
                    self.data=self.__app.sendImg_and_recvData()
                elif(self.sendType=="neopixel"):
                    self.sendType=""
                    self.__app.setNeopixel(self.arguments[0],self.arguments[1])
                    self.arguments=[]
                elif(self.sendType=="outpin"):
                    self.sendType=""
                    self.__app.setOutPin(self.arguments[0],self.arguments[1])
                    self.arguments=[]
                elif(self.sendType=="inpin"):
                    self.sendType=""
                    self.__app.setInPin(self.arguments[0])
                    self.arguments=[]
                elif(self.sendType=="pwm"):
                    self.sendType=""
                    self.__app.setPwm(self.arguments[0],self.arguments[1], self.arguments[2])
                    self.arguments=[]
                elif(self.sendType=="adc"):
                    self.sendType=""
                    self.adcvalue=self.__app.readAdc(self.arguments[0],self.arguments[1])
                elif(self.sendType=="setdisplay"):
                    self.sendType=""
                    self.__app.setPwm(self.arguments[0],self.arguments[1], self.arguments[2], self.arguments[3], self.arguments[4])
                    self.arguments=[]
                else:
                    self.data=self.__app.recvData()
                disc=True
                
            else:
                if(disc):
                    disc=False
                    self.__app.newImg()
                    self.data=self.__app.sendImg_and_recvData()
                else:
                    self.data=self.__app.recvData()

            if(self.busy):
                self.busy=False

            #print(self.data)	
            if (self.data['PROXIMITY']!=datap_old):
                datap_old=self.data['PROXIMITY']
                if(datap_old):
                    self.isNear=not self.isNear
    
    def resumeConnection(self, so):
        self.__app.changeSocket(so)
        self.__app.getPinConfig("src/"+self.name+"/pinout.json")
        print("resumed")

    def sendImg(self):
        self.sendType="image"
        while(self.busy or self.sendType=="image"):
            pass

    def recvData(self):
        return self.data

    def sendImg_and_recvData(self):
        self.sendType="image"
        while(self.busy or self.sendType=="image"):
            pass

        return self.data

    def setNeopixel(self, status, pin=-1):
        self.sendType="neopixel"
        self.arguments.append(status)
        self.arguments.append(pin)
        while(self.busy or self.sendType=="neopixel"):
            pass

    def setOutPin(self, pin, value):
        self.sendType="outpin"
        self.arguments.append(pin)
        self.arguments.append(value)
        while(self.busy or self.sendType=="outpin"):
            pass
    
    def setInPin(self, pin):
        self.sendType="inpin"
        self.arguments.append(pin)
        while(self.busy or self.sendType=="inpin"):
            pass

    def setPwm(self, pin, freq, duty):
        self.sendType="pwm"
        self.arguments.append(pin)
        self.arguments.append(freq)
        self.arguments.append(duty)
        while(self.busy or self.sendType=="pwm"):
            pass

    def readAdc(self, pin, resolution=1024):
        self.sendType="adc"
        self.arguments.append(pin)
        self.arguments.append(resolution)
        while(self.busy or self.sendType=="adc"):
            pass

        return self.adcvalue

    def setDisplay(self, sda, scl, heigth, width, dispType):
        self.sendType="setdisplay"
        self.arguments.append(sda)
        self.arguments.append(scl)
        self.arguments.append(heigth)
        self.arguments.append(width)
        self.arguments.append(dispType)
        while(self.busy or self.sendType=="setdisplay"):
            pass

    def newImg(self):
        self.__app.newImg() 

    def fillImg(self, img_color):
        self.__app.fillImg(img_color)

    def addFont(self, font, font_size):
        self.__app.addFont(font, font_size)

    def getFonts(self):
        return self.__app.getFonts()

    def setRotation(self, rotation):
        self.__app.setRotation(rotation)

    def setContrast(self, contrast):
        self.__app.setContrast(contrast)

    def setText(self,pos,txt, txt_color, txt_font):
        self.__app.setText(pos, txt, txt_color, txt_font)

    def setNeoPin(self, pin):
        self.__app.setNeoPin(pin)