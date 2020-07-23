class Door:

    def __init__(self):
        self.state = False

    def openDoor(self, device):
        device.setPwm(4, 50, 100)

    def closeDoor(self, device):  
        device.setPwm(4, 50, 30)

    def getNotificationMessage(self, device, username=None):
        '''if "state" in device.customParams:
            self.state = device.customParams["state"]'''

        msg = []

        msg.append([(10, 35), device.getName().replace("_", " ").upper()])
        msg_status = "OPEN?"
        if self.state:
            msg_status = "CLOSE?"
        
        msg.append([(10,50), msg_status])

        return msg


    def run(self, device):
        self.state = not self.state
        if not self.state:
            self.closeDoor(device)
        else:
            self.openDoor(device)
        
        #device.customParams["state"]=self.state
        
