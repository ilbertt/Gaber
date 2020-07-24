class Settings:
	def __init__(self, app):
		self.app=app
		self.contrast=0
		self.rotation=0

	def run(self):
		change=True
		close_app=False
		datau_old=0
		datad_old=0
		datas_old=0
		next_app=False
		i=0
		while((not close_app) and self.app.isAlive()):
			if (change):
				change=False
				self.app.newImg()
				self.app.setText((35,0), "SETTINGS ", 255,self.app.getFonts()[0])
				self.app.setText((10,10),"CONTRAST ", 255,self.app.getFonts()[0])
				self.app.setText((10,20),"ROTATION ", 255,self.app.getFonts()[0])
				self.app.setText((10,30),"MENU ", 255,self.app.getFonts()[0])
				self.app.setText((1,10+i*10),">", 255,self.app.getFonts()[0])
				data=self.app.sendImg_and_recvData()
			else:
				data=self.app.recvData()

			#print(data)	
			if (data['UP']!=datau_old):
				datau_old=data['UP']
				if(datau_old):
					if(i==0):
						i=2
					else:
						i-=1

				change=True
			elif (data['DOWN']!=datad_old):
				datad_old=data['DOWN']
				if(datad_old):
					if(i==2):
						i=0
					else:
						i+=1

					change=True

			elif(data['SELECT']!=datas_old):
				datas_old=data['SELECT']
				if(datas_old):
					if(i==2):
						next_app=True
					elif(i==1):
						self.rotation = not self.rotation
						self.app.setRotation(self.rotation)
						change=True
					elif(i==0):
						self.contrast = not self.contrast
						self.app.setContrast(self.contrast)
						change=True

			if (next_app and data['SELECT']==0):
				next_app=False
				close_app = True

		return -1



