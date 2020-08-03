import threading
import time

class Keyboard(threading.Thread):
    def __init__(self, username, device, router):
        self.device = device
        self.username = username
        self.router = router
        self.counter = 0
        self.started = False
        self.deviceChanged = False
        self.text = ''
        self.ris = ''

    def __startThread(self):
        threading.Thread.__init__(self)
        self.name = self.username+"_keyboard"
        self.start()
        self.started=True

    def getNotificationMessage(self, device, username=None):

        msg = []

        msg.append([(10, 35), device.getName().replace("_", " ").upper()])
        msg_status = "ENABLE KEYBOARD?"
        
        msg.append([(10,50), msg_status])

        return msg

    def handleStreaming(self, device):
        if self.device!=device:
            old_device = self.device
            self.__setDevice(device)
            self.deviceChanged = True
            if old_device != 0:
                old_device.resetStreamingUser()
            if not self.started:
                self.__startThread()
    
    def __setDevice(self, device):
        self.device = device

    def run(self):
        old_c=''
        while True:
            c=self.device.readI2C(8,1)

            if c != old_c:
                #print(c)
                old_c = c
                if c != b'\x00':
                    if c != b'\x7f': #backspace
                        self.router.addToText(c.decode())
                    else:
                        self.router.removeFromText(1)