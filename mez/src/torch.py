class Torch:
	def __init__(self, app):
		self.app=app
		self.ledstatus=0
		self.npstatus=0

	def run(self):
		change=True
		i=0
		j=0
		red=0
		green=0
		blue=0
		datau_old=0
		datad_old=0
		datas_old=0
		data={}
		color_picker = False
		second_column = False
		next_app=False
		close_app=False
		while(not close_app):
			if (change):
					change=False
					self.app.newImg()
					if not color_picker:
						self.app.setText((45,0), "TORCH ", 255,self.app.getFonts()[0])
						self.app.setText((10,10),"TOP ", 255,self.app.getFonts()[0])
						self.app.setText((10,20),"SIDE ", 255,self.app.getFonts()[0])
						self.app.setText((10,30),"MENU ", 255,self.app.getFonts()[0])
						self.app.setText((1,10+i*10),">", 255,self.app.getFonts()[0])
					else:
						self.app.setText((10,0),"RED ", 255,self.app.getFonts()[0])
						self.app.setText((70,0),str(red), 255,self.app.getFonts()[0])

						self.app.setText((10,10),"GREEN ", 255,self.app.getFonts()[0])
						self.app.setText((70,10),str(green), 255,self.app.getFonts()[0])

						self.app.setText((10,20),"BLUE ", 255,self.app.getFonts()[0])
						self.app.setText((70,20),str(blue), 255,self.app.getFonts()[0])

						self.app.setText((10,30),"SET ", 255,self.app.getFonts()[0])
						self.app.setText((10,40),"RESET ", 255,self.app.getFonts()[0])
						self.app.setText((10,50),"BACK ", 255,self.app.getFonts()[0])

						if second_column:
							self.app.setText((60,j*10),">", 255,self.app.getFonts()[0])
						else:
							self.app.setText((1,j*10),">", 255,self.app.getFonts()[0])

					data=self.app.sendImg_and_recvData()
			else:
				data=self.app.recvData()
			
			#print(data)	
			if (data['DOWN']!=datad_old):
				datad_old=data['DOWN']
				if(datad_old):
					if color_picker:
						if second_column:
							if j==0:
								if red > 0:
									red -=1
							if j==1:
								if green > 0:
									green -= 1
							if j==2:
								if blue > 0:
									blue -= 1
						else:
							if j==5:
								j=0
							else:
								j+=1
					else:
						if(i==2):
							i=0
						else:
							i+=1

					change=True
			elif (data['UP']!=datau_old):
				datau_old=data['UP']
				if(datau_old):
					if color_picker:
						if second_column:
							if j==0:
								if red < 255:
									red +=1
							if j==1:
								if green < 255:
									green += 1
							if j==2:
								if blue < 255:
									blue += 1
						else:
							if j==0:
								j=5
							else:
								j-=1
					else:
						if(i==0):
							i=2
						else:
							i-=1

					change=True
			elif(data['SELECT']!=datas_old):
				datas_old=data['SELECT']
				if(datas_old):
					if color_picker:
						if second_column:
							second_column = False
						else:
							if j==3:
								self.app.setNeopixel([red,green,blue])
							elif j==4:
								red = 0
								green = 0
								blue = 0
								self.app.setNeopixel([red,green,blue])
							elif j==5:
								color_picker = False
								j=0
							else:
								second_column = True
					else:
						if(i==2):
							next_app=True
						elif(i==1):
							self.ledstatus=not self.ledstatus
							self.app.setOutPin(16, self.ledstatus)
						elif(i==0):
							'''self.npstatus= not self.npstatus
							self.app.setNeopixel([255*self.npstatus,255*self.npstatus,255*self.npstatus])'''
							color_picker = True

					change = True

			#self.app.setNeopixel([red,green,blue])

			if (next_app and data['SELECT']==0):
				next_app=False
				close_app=True

		return -1


