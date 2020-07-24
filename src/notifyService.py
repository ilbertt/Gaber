from PIL   				import Image
import time
import threading
from src.iot_funct.door import  Door
from numpy.random 		import randint
#from application import Application

class NotifyService(threading.Thread):
	def __init__(self, app, router):
		threading.Thread.__init__(self)
		self.app=app
		self.router=router
		self.username=self.app.username
		self.recentDevices=[]
		#self.nearDeavices=[]
		self.device=0
		self.name = "notifyService_"+self.username
		self.appList={"door": Door()} #{"dev.type": IOT_Functions()}

	def run(self):
		print(self.app.username+": notify started")
		while (self.app.isAlive()):
			devs=self.router.listNearDevices(self.username)
			for dev in devs: 
				if((not (dev in self.recentDevices)) and (dev.getStreamingUser()=="")):
					dev.setStreamingUser(self.username)
					self.device=dev
					self.recentDevices.append(dev)

			for dev in self.recentDevices:
				if(not (dev in devs)):
					self.recentDevices.remove(dev)

			if(self.device):
				self.app.startNotify()
				color = list(randint(0,32,3))
				self.app.setNeopixel(color, -1, True)
				self.app.setText((40,0), "NOTIFY", 255,self.app.getFonts()[0], True)
				self.app.setText((10,20), "FOUND", 255,self.app.getFonts()[0], True)
				
				notifMsg = self.appList[self.device.getDeviceType()].getNotificationMessage(self.device)
				for line in notifMsg:
					self.app.setText(line[0], line[1], 255,self.app.getFonts()[0], True)

				self.app.sendImg(True)
				data=self.app.recvData(True)
				datad_old=data['DOWN']
				datau_old=data['UP']
				datas_old=data['SELECT']
				stop=False
				accepted=False
				startTime = time.time()
				while(not stop):
					data=self.app.recvData(True)
					if (data['DOWN']!=datad_old):
						datad_old=data['DOWN']
						if(datad_old):
							stop=True
							
					elif (data['UP']!=datau_old):
						datau_old=data['UP']
						if(datau_old):
							stop=True	
					
					elif(data['SELECT']!=datas_old):
						datas_old=data['SELECT']
						if(datas_old):
							stop=True
							accepted=True

					elif(time.time() - startTime > 10):
						stop = True

				if(accepted):
					self.appList[self.device.getDeviceType()].run(self.device)

				self.app.setNeopixel([0, 0, 0], -1, True)
				self.app.stopNotify()
				self.device.resetStreamingUser()
				self.device=0
			
	def getUsedDevices(self):
		return self.recentDevices

