import time
import threading
import sys

class Screen(threading.Thread):
    def __init__(self, username, device):
        self.state = False
        self.device = device
        threading.Thread.__init__(self)
        self.name = username+"_screen"
        self.started = False

    def getNotificationMessage(self, device, username=None):

        msg = []

        msg.append([(10, 35), device.getName().replace("_", " ").upper()])
        msg_status = "START STREAM?"
        if self.state:
            msg_status = "STOP STREAM?"
        
        msg.append([(10,50), msg_status])

        return msg
    
    def run(self):
        self.started = True
        startTime = time.time()
        counter = 0
        self.state = not self.state

        while True:
            #print("streaming")
            while self.state:
                if self.device:
                    self.device.stream = True
                    if time.time() - startTime > 1:
                        startTime = time.time()
                        counter += 1
                        self.device.newImg()
                        self.device.setText((45,0),str(counter), 255, self.device.getFonts()[1])
                        self.device.sendImg()
            self.device = 0
    
    def handleStreaming(self, device):
        self.state = not self.state
        if self.state:
            self.setDevice(device)
    
    def setDevice(self, device):
        self.device = device