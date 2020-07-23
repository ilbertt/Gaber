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


    def run(self):
        self.__app.getPinConfig("src/"+self.name+"/pinout.json")
        self.__app.getConfig("src/"+self.name+"/config.json")

        datap_old=0
        disc=False
        self.newImg()
        while(1):
            if (self.stream and self.isNear):
                if(self.sendType=="image"):
                    self.data=self.__app.sendImg_and_recvData()
                    self.sendType=""
                elif(self.sendType=="neopixel"):
                    self.__app.setNeopixel(self.arguments[0],self.arguments[1])
                    self.arguments=[]
                    self.sendType=""
                elif(self.sendType=="outpin"):
                    self.__app.setOutPin(self.arguments[0],self.arguments[1])
                    self.arguments=[]
                    self.sendType=""
                elif(self.sendType=="inpin"):
                    self.__app.setInPin(self.arguments[0])
                    self.arguments=[]
                    self.sendType=""
                elif(self.sendType=="pwm"):
                    self.__app.setPwm(self.arguments[0],self.arguments[1], self.arguments[2])
                    self.arguments=[]
                    self.sendType=""
                elif(self.sendType=="adc"):
                    self.adcvalue=self.__app.readAdc(self.arguments[0],self.arguments[1])
                    self.sendType=""
                elif(self.sendType=="setdisplay"):
                    self.__app.setPwm(self.arguments[0],self.arguments[1], self.arguments[2], self.arguments[3], self.arguments[4])
                    self.arguments=[]
                    self.sendType=""
                else:
                    self.data=self.__app.recvData()
                disc=True
                
            else:
                if(disc):
                    disc=False
                    self.sendType=""
                    self.__app.newImg()
                    self.data=self.__app.sendImg_and_recvData()
                else:
                    self.data=self.__app.recvData()

                

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
        while( self.sendType=="image" and (self.stream and self.isNear) ):
            pass

    def recvData(self):
        return self.data

    def sendImg_and_recvData(self):
        self.sendType="image"
        while( self.sendType=="image" and (self.stream and self.isNear) ):
            pass

        return self.data

    def setNeopixel(self, status, pin=-1):
        self.sendType="neopixel"
        self.arguments.append(status)
        self.arguments.append(pin)
        while( self.sendType=="neopixel" and (self.stream and self.isNear)):
            pass

    def setOutPin(self, pin, value):
        self.sendType="outpin"
        self.arguments.append(pin)
        self.arguments.append(value)
        while( self.sendType=="outpin" and (self.stream and self.isNear)):
            pass
    
    def setInPin(self, pin):
        self.sendType="inpin"
        self.arguments.append(pin)
        while( self.sendType=="inpin" and (self.stream and self.isNear)):
            pass

    def setPwm(self, pin, freq, duty):
        self.sendType="pwm"
        self.arguments.append(pin)
        self.arguments.append(freq)
        self.arguments.append(duty)
        while( self.sendType=="pwm" and (self.stream and self.isNear)):
            pass

    def readAdc(self, pin, resolution=1024):
        self.sendType="adc"
        self.arguments.append(pin)
        self.arguments.append(resolution)
        while( self.sendType=="adc" and (self.stream and self.isNear)):
            pass

        return self.adcvalue

    def setDisplay(self, sda, scl, heigth, width, dispType):
        self.sendType="setdisplay"
        self.arguments.append(sda)
        self.arguments.append(scl)
        self.arguments.append(heigth)
        self.arguments.append(width)
        self.arguments.append(dispType)
        while( self.sendType=="setdisplay" and (self.stream and self.isNear)):
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

    def setSteamingUser(self, user):
        self.streamingUser=user
    
    def resetStreamingUser(self):
        self.streamingUser=""

    def getDeviceName(self):
        return self.name