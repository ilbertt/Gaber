from PIL import Image, ImageDraw, ImageFont, ImageOps

class Router:
    def __init__(self):
        self.devices = []
        self.nearDevices = []
        self.streamingDevice = None
        self.img = None
        self.d = None
        self.dim = (128, 64)    # default size

    def addDevice(self, device):
        self.devices.append(device)
    
    def removeDevice(self, device):
        if device in self.devices:
            self.devices.remove(device)
    
    def __addNearDevice(self, device):
        if not (device in self.nearDevices):
            self.nearDevices.append(device)
	
    def __removeNearDevice(self, device):
        if device in self.nearDevices:
            device.stream=False
            self.nearDevices.remove(device)
	
    def listNearDevices(self):
        for device in self.devices:
            if device.isNear:
                self.__addNearDevice(device)
            else:
                self.__removeNearDevice(device)
        
        return self.nearDevices

    def newImg(self):
        if self.streamingDevice:
            self.dim = (self.streamingDevice.app.heigth, self.streamingDevice.app.width)

        self.img = Image.new("L", self.dim)
        self.d = ImageDraw.Draw(self.img)
        self.d.rectangle((0,0,self.dim[0],self.dim[1]),fill=0)
    
    def setText(self,pos,txt, txt_color, txt_font):
        self.d.text(pos, txt, txt_color,font=txt_font)

    def streamOnDevice(self, dev):
        if dev.stream:
            dev.stream = False
            self.streamingDevice = None
        else:
            dev.stream = True
            self.streamingDevice = dev

        for device in self.nearDevices:
            if device != dev:
                device.stream=False