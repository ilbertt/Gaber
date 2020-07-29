import time
import threading
import os

class Screen(threading.Thread):
    def __init__(self, username, device):
        self.device = device
        self.username = username
        self.counter = 0
        self.started = False
        self.deviceChanged = False

    def __startThread(self):
        threading.Thread.__init__(self)
        self.name = self.username+"_screen"
        self.start()
        self.started=True

    def getNotificationMessage(self, device, username=None):

        msg = []

        msg.append([(10, 35), device.getName().replace("_", " ").upper()])
        msg_status = "START STREAM?"
        
        msg.append([(10,50), msg_status])

        return msg
    
    def run(self):
        startTime = time.time()

        commands = ['ls', 'vcgencmd measure_temp', 'ifconfig']
        i=0

        while True:
            if self.device:
                self.device.stream = True
                self.device.isNear = True

                if time.time() - startTime > 3 or self.deviceChanged:
                    self.deviceChanged = False
                    startTime = time.time()
                    self.device.newImg()
                    self.device.setText((35,0),"CONSOLE ", 255,self.device.getFonts()[0])
                    self.device.setText((1,10),">", 255,self.device.getFonts()[0])
                    self.device.setText((10,10), commands[i], 255,self.device.getFonts()[0])
                    stream = os.popen(commands[i])
                    output = stream.read()
                    self.device.setText((10,20), output, 255, self.device.getFonts()[0])
                    self.device.sendImg()
                    i+=1
                    if i > len(commands)-1:
                        i=0
    
    def handleStreaming(self, device):
        if self.device!=device:
            old_device = self.device
            self.__setDevice(device)
            self.deviceChanged = True
            if old_device != 0:
                old_device.stream = False
                old_device.isNear = False
            if not self.started:
                self.__startThread()
    
    def __setDevice(self, device):
        self.device = device