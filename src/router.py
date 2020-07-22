from PIL import Image, ImageDraw, ImageFont, ImageOps

class Router:
    def __init__(self):
        self.devices = []
        self.nearDevices = []
        self.streamingDevices = []
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
	
    def __updateNearDevices(self):
        for device in self.devices:
            if device.isNear:
                self.__addNearDevice(device)
            else:
                self.__removeNearDevice(device)

    def listNearDevices(self, user):
        self.__updateNearDevices()
        
        availableDevices = []

        for device in self.nearDevices:
            if device.streamingUser == "" or device.streamingUser == user:
                availableDevices.append(device)
        
        return availableDevices
    
    def streamOnDevice(self, dev, user):
        if dev.stream:
            dev.stream = False
            dev.streamingUser = ""
            self.streamingDevices.remove(dev)
            return 0
        else:
            dev.stream = True
            dev.streamingUser = user
            self.streamingDevices.append(dev)

            for device in self.nearDevices:
                if device != dev:
                    if device.streamingUser == user:
                        device.stream=False
                        device.streamingUser = ""
            
            return dev