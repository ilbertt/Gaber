class Led:

    def __init__(self):
        self.state = False

    def ledOn(self, device):
        device.setOutPin(16, 0)

    def ledOff(self, device):  
        device.setOutPin(16, 1)

    def getNotificationMessage(self, device, username=None):
        custom = device.getCustomParams()

        if "state" in custom:
            self.state = custom["state"]

        msg = []

        msg.append([(10, 35), device.getName().replace("_", " ").upper()])
        msg_status = "TURN ON?"
        if self.state:
            msg_status = "TURN OFF?"
        
        msg.append([(10,50), msg_status])

        return msg


    def run(self, device):
        self.state = not self.state
        if not self.state:
            self.ledOff(device)
        else:
            self.ledOn(device)
        
        device.setCustomParams({"state": self.state})
        
