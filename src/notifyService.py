from PIL   			import Image
import time
import threading
#from application import Application

class NotifyService(threading.Thread):
	def __init__(self, app, router):
		self.app=app
		self.router=router
		self.username=self.app.username
		self.i=0
		self.recentDevices=[]
		#self.nearDeavices=[]
		self.device=0
		self.refused=[]
		threading.Thread.__init__(self)
		self.appList={} #{"devname": Application}

	def run(self):
		while(not self.device):
			devs=self.router.listNearDevices(self.username)
			for dev in devs: 
				if(not (dev in self.recentDevices)):
					dev.setStreamingUser(self.username)
					self.device=dev
					self.recentDevices.append(dev)

			for dev in self.recentDevices:
				if(not (dev in devs)):
					self.recentDevices.remove(dev)
			

		self.app.startNotify()
		self.app.setText((40,0), "NOTIFY", 255,self.app.getFonts()[0])
		self.app.setText((10,20), "FOUND", 255,self.app.getFonts()[0])
		self.app.setText((10,35), self.device.getDeviceName(), 255,self.app.getFonts()[0])
		self.app.setText((10,50), "CONNECT?", 255,self.app.getFonts()[0])
		self.app.sendImg()
		data=self.app.recvData()
		datad_old=data['DOWN']
		datau_old=data['UP']
		datas_old=data['SELECT']
		stop=False
		accepted=False
		while(not stop):
			data=self.app.recvData()
			if (data['DOWN']!=datad_old):
				datad_old=data['DOWN']
				if(not datad_old):
					stop=True
					accepted=False

					
			elif (data['UP']!=datau_old):
				datau_old=data['UP']
				if(not datau_old):
					stop=True
					accepted=False
					
			
			elif(data['SELECT']!=datas_old):
				datas_old=data['SELECT']
				if(not datas_old):
					stop=True
					accepted=True

		if(accepted):
					self.appList[self.device.getDeviceName()].run(self.device, self.app)

		self.app.stopNotify()
		self.app.device.resetStreamingUser()
		self.app.device=0
			
	def getUsedDevices(self):
		return self.recentDevices

