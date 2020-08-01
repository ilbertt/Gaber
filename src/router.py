from PIL import Image, ImageDraw, ImageFont, ImageOps
import json

class Router:
    def __init__(self):
        self.devices = []
        self.nearDevices = {}
        self.streamingDevices = []
        self.users = {}
        self.text = ''

        with open("src/userDevices.json", "r") as rf:
            self.userDevices = json.load(rf)

    def addDevice(self, device):
        self.devices.append(device)
    
    def removeDevice(self, device):
        if device in self.devices:
            self.devices.remove(device)
    
    def addUser(self, user):
        self.users.__setitem__(user["name"], user["uid"])
    
    def removeUser(self, username):
        if username in self.users:
            self.users.pop(username)

    def __addNearDevice(self, device, user):
        if not (user in self.nearDevices):
            self.nearDevices.__setitem__(user, [])
        
        if not (device in self.nearDevices[user]):
            self.nearDevices[user].append(device)
	
    def __removeNearDevice(self, device, user):
        if user in self.nearDevices:
            if device in self.nearDevices[user]:
                device.stream=False
                self.nearDevices[user].remove(device)
	
    def __updateNearDevices(self, user):
        for device in self.devices:
            if device.isNear:
                if device.getNFC() == self.users[user]:
                    if device.name in self.userDevices[user]:
                        self.__addNearDevice(device, user)
            else:
                self.__removeNearDevice(device, user)

    def listNearDevices(self, user):
        self.__updateNearDevices(user)
        
        availableDevices = []
        #print(self.nearDevices)
        if user in self.nearDevices:
            for device in self.nearDevices[user]:
                #if device.streamingUser == "" or device.streamingUser == user:
                availableDevices.append(device)
        
        #print(availableDevices)
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
    
    def getText(self):
        return self.text
    
    def setText(self, text):
        self.text = text
    
    def addToText(self, text):
        self.text += text
    
    def removeFromText(self,nChar):
        self.text = self.text[:-nChar]