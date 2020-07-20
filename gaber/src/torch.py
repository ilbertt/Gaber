class Torch:
	def __init__(self, app):
		self.app=app
		self.ledstatus=0;
		self.npstatus=0;

	def run(self):
		change=True
		datau_old=0
		datad_old=0
		datas_old=0
		i=0
		next_app=False
		close_app=False
		while(not close_app):
			if (change):
				change=False
				self.app.newImg()
				self.app.setText((45,0), "TORCH ", 255,self.app.getFonts()[0])
				self.app.setText((10,10),"TOP ", 255,self.app.getFonts()[0])
				self.app.setText((10,20),"SIDE ", 255,self.app.getFonts()[0])
				self.app.setText((10,30),"MENU ", 255,self.app.getFonts()[0])
				self.app.setText((1,10+i*10),">", 255,self.app.getFonts()[0])
				data=self.app.sendImg_and_recvData()
			else:
				data=self.app.recvData()
			
			#print(data)	
			if (data['UP']!=datau_old):
				datau_old=data['UP']
				if(datau_old):
					if(i==2):
						i=0
					else:
						i+=1

					change=True

			elif (data['DOWN']!=datad_old):
				datad_old=data['DOWN']
				if(datad_old):
					if(i==0):
						i=2
					else:
						i-=1

					change=True

			elif(data['SELECT']!=datas_old):
				datas_old=data['SELECT']
				if(datas_old):
					if(i==2):
						next_app=True
					elif(i==1):
						self.ledstatus=not self.ledstatus
						self.app.setOutPin(16, self.ledstatus)
					elif(i==0):
						self.npstatus= not self.npstatus
						self.app.setNeopixel([255*self.npstatus,255*self.npstatus,255*self.npstatus])

			if (next_app and data['SELECT']==0):
				next_app=False
				close_app=True

		return -1


