class Settings:
	def __init__(self, app):
		self.app=app
		self.contrast=0
		self.rotation=0

	def run(self, menu):
		change=True
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
				self.app.sendImg_and_recvData()
			else:
				self.app.recvData()

			#print(data)	
			if (self.app.isPinUp("DOWN")):
				if(i==2):
					i=0
				else:
					i+=1

				change=True
			elif (self.app.isPinUp("UP")):
				if(i==0):
					i=2
				else:
					i-=1

				change=True
			elif(self.app.isPinUp("SELECT")):
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
			
			self.app.storeData()

			if (next_app):
				next_app=False
				menu.run()


