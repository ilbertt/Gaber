class Torch:
	def __init__(self, app):
		self.app=app
		self.ledstatus=0
		self.npstatus=0

	def run(self, menu):
		change=True
		i=0
		next_app=False
		while(1):
			if (change):
					change=False
					self.app.newImg()
					self.app.setText((45,0), "TORCH ", 255,self.app.getFonts()[0])
					self.app.setText((10,10),"TOP ", 255,self.app.getFonts()[0])
					self.app.setText((10,20),"SIDE ", 255,self.app.getFonts()[0])
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
					self.ledstatus=not self.ledstatus
					self.app.setOutPin(16, self.ledstatus)
				elif(i==0):
					self.npstatus= not self.npstatus
					self.app.setNeopixel([255*self.npstatus,255*self.npstatus,255*self.npstatus])

			self.app.storeData()

			if (next_app):
				next_app=False
				menu.run()


