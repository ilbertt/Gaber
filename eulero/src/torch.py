class Torch:
	def __init__(self, app):
		self.app=app
		self.ledstatus=0
		self.npstatus=0

	def run(self, menu):
		change=True
		data_old=0
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
					data=int(self.app.sendImg_and_recvData())
			else:
				data=int(self.app.recvData())
			
			#print(data)	
			if (data!=data_old and data==2**self.app.inPins['DOWN']['number']):
				if(i==2):
					i=0
				else:
					i+=1

				change=True
			elif (data!=data_old and data==2**self.app.inPins['UP']['number']):
				if(i==0):
					i=2
				else:
					i-=1

				change=True
			elif(data!=data_old and data==2**self.app.inPins['SELECT']['number']):
				if(i==2):
					i_tmp=i
					next_app=True
				elif(i==1):
					self.ledstatus=not self.ledstatus
					self.app.setOutPin(16, self.ledstatus)
				elif(i==0):
					self.npstatus= not self.npstatus
					self.app.setNeopixel([255*self.npstatus,255*self.npstatus,255*self.npstatus])

			if (next_app and data==0):
				next_app=False
				menu.run()

			if (data!=data_old):
				data_old=data


