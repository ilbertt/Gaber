class Door:

    def openDoor(self, device):
        device.setPwm(4, 50, 100)

    def closeDoor(self, device):  
        device.setPwm(4, 50, 30)

    def run(self, device):
        state=False
        if "state" in device.customParams:
            state = device.customParams["state"]

        if state:
            self.closeDoor(device)
        else:
            self.openDoor(device)
        
