class Settings:
	def __init__(self, app):
		self.app=app
		self.contrast=0
		self.rotation=0

	def run(self, menu):
		change=True
		data_old=0
		next_app=False
		i=0
		while(1):
			if (change):
				change=False
				self.app.newImg()
				self.app.setText((35,0), "SETTINGS ", 255,self.app.getFonts()[0])
				self.app.setText((10,10),"CONTRAST ", 255,self.app.getFonts()[0])
				self.app.setText((10,20),"ROTATION ", 255,self.app.getFonts()[0])
				self.app.setText((10,30),"MENU ", 255,self.app.getFonts()[0])
				self.app.setText((1,10+i*10),">", 255,self.app.getFonts()[0])
				data=int(self.app.sendImg_and_recvData())
			else:
				data=int(self.app.recvData())

			print(data)	
			if (data!=data_old and data==2):
				data_old=data
				if(i==2):
					i=0
				else:
					i+=1

				change=True
			elif (data!=data_old and data==1):
				data_old=data
				if(i==0):
					i=2
				else:
					i-=1

				change=True
			elif(data!=data_old and data==4):
				data_old=data
				if(i==2):
					i_tmp=i
					next_app=True
				elif(i==1):
					self.rotation = not self.rotation
					self.app.setRotation(self.rotation)
					change=True
				elif(i==0):
					self.contrast = not self.contrast
					self.app.setContrast(self.contrast)
					change=True

			if (next_app and data==0):
				next_app=False
				menu.run()

			if (data!=data_old):
				data_old=data


