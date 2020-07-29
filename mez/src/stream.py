import datetime

class Stream:
	def __init__(self, app):
		self.app = app
		self.dev = 0
	
	def run(self):
		change=True
		close_app=False
		i=0
		j=1
		datau_old=0
		datad_old=0
		datas_old=0
		next_app=False
		#devices = self.app.router.devices

		avail_devices = self.app.router.listNearDevices(self.app.getUsername())
		old_avail_devices = 0

		sec_old = -1
		counter = 0

		while((not close_app) and self.app.isAlive()):
			if (change or old_avail_devices!=len(avail_devices)):
				change=False
				old_avail_devices = len(avail_devices)
				self.app.newImg()
				self.app.setText((45,0), "STREAM ", 255,self.app.getFonts()[0])

				for device in avail_devices:
					self.app.setText((10,10*j),device.name, 255,self.app.getFonts()[0])
					if device.stream:
						self.app.setText((80,10*j),"<->", 255,self.app.getFonts()[0])
					j=j+1

				self.app.setText((10,10*j),"MENU ", 255,self.app.getFonts()[0])
				last_i = j-1
				j=1
				self.app.setText((1,10+i*10),">", 255,self.app.getFonts()[0])
				
				data=self.app.sendImg_and_recvData()
			else:
				data=self.app.recvData()
			
			avail_devices = self.app.router.listNearDevices(self.app.getUsername())


			if (data['UP']!=datau_old):
				datau_old=data['UP']
				if(datau_old):
					if(i==0):
						i=last_i
					else:
						i-=1

					change=True

			elif (data['DOWN']!=datad_old):
				datad_old=data['DOWN']
				if(datad_old):
					if(i==last_i):
						i=0
					else:
						i+=1

					change=True

			elif(data['SELECT']!=datas_old):
				datas_old=data['SELECT']
				if(datas_old):
					#print(i,j, last_i)
					if(i==last_i):
						next_app=True
					else:
						dev = avail_devices[i]
						self.dev = self.app.router.streamOnDevice(dev, self.app.getUsername())
						change=True
			
			sec = datetime.datetime.now().second
			if sec!=sec_old:
				sec_old = sec
				counter += 1
				if self.dev:
					self.dev.newImg()
					self.dev.setText((45,0),str(counter), 255,self.dev.getFonts()[1])
					self.dev.sendImg()

			if (next_app and data['SELECT']==0):
				next_app=False
				if self.dev:
					self.app.router.streamOnDevice(self.dev, self.app.getUsername())
				
				close_app=True

		return -1
