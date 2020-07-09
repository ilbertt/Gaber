import time
from pyowm import OWM
class Weather:
	def __init__(self, app):
		self.app=app
		api_key = "your api key"
		self.owm = OWM(api_key).weather_manager()
		self.min_old=-1
		self.weather=0
		self.page=1
		self.i=0

	def run(self, menu):
		show=True
		data_old=0
		next_app=False
		while(1):
			t=time.localtime()
			m=t.tm_min
			if(m!=self.min_old):
				self.min_old = m
				self.weather = self.owm.weather_at_place('Milan,IT').weather
		
			if(show):
				self.app.newImg()
				if(self.i==0):
					temp = self.weather.temperature().get('temp')
					self.app.setText((24,0), "TEMPERATURE ", 255,self.app.getFonts()[0])
					self.app.setText((24,21),str(int(temp))+" K", 255,self.app.getFonts()[1])
				elif(self.i==1):
					hum = self.weather.humidity
					self.app.setText((40,0), "HUMIDITY ", 255,self.app.getFonts()[0])
					self.app.setText((32,21),str(int(hum))+" %", 255,self.app.getFonts()[1])

				data=int(self.app.sendImg_and_recvData())
				show=False
			else:
				data=int(self.app.recvData())

			print(data)
			if(data!=data_old and data==4):
				next_app=True

			if (data!=data_old and data==2):
				show=True
				if(self.i==1):
					self.i=0
				else:
					self.i+=1

			elif (data!=data_old and data==1):
				show=True
				if(self.i==0):
					self.i=1
				else:
					self.i-=1
			
			if (next_app and data==0):
				next_app=False
				print("menu")
				menu.run()

			if (data!=data_old):
				data_old=data
