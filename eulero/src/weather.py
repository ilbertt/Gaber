import time
from pyowm import OWM
from ip2geotools.databases.noncommercial import DbIpCity

class Weather:
	def __init__(self, app):
		self.app=app
		api_key = "b52881efed55c850de4de596b8a001b7"
		self.owm = OWM(api_key)
		self.min_old=-1
		self.weather=0
		self.page=1
		self.i=0

	def run(self):
		ip=self.app.getIpAddress()
		lat=45.7513025
		lon=9.0308275
		if not ("192.168" in ip):
			response = DbIpCity.get(ip, api_key='free')
			lat=response.latitude
			lon=response.longitude
			
		show=True
		datau_old=0
		datad_old=0
		datas_old=0
		next_app=False
		close_app=False
		while((not close_app) and self.app.isAlive()):
			t=time.localtime()
			m=t.tm_min
			if(m!=self.min_old):
				self.min_old = m
				self.weather = self.owm.weather_at_coords(lat, lon).get_weather()
		
			if(show):
				self.app.newImg()
				if(self.i==0):
					temp = self.weather.get_temperature().get('temp')
					self.app.setText((24,0), "TEMPERATURE ", 255,self.app.getFonts()[0])
					self.app.setText((24,21),str(int(temp))+" K", 255,self.app.getFonts()[1])
				elif(self.i==1):
					hum = self.weather.get_humidity()
					self.app.setText((40,0), "HUMIDITY ", 255,self.app.getFonts()[0])
					self.app.setText((32,21),str(int(hum))+" %", 255,self.app.getFonts()[1])

				data=self.app.sendImg_and_recvData()
				show=False
			else:
				data=self.app.recvData()

			#print(data)
			

			if (data['UP']!=datau_old):
				datau_old=data['UP']
				if(datau_old):
					show=True
					if(self.i==1):
						self.i=0
					else:
						self.i+=1

			elif (data['DOWN']!=datad_old):
				datad_old=data['DOWN']
				if(datad_old):
					show=True
					if(self.i==0):
						self.i=1
					else:
						self.i-=1

			elif(data['SELECT']!=datas_old):
				datas_old=data['SELECT']
				if(datas_old):
					next_app=True
			
			if (next_app and data['SELECT']==0):
				next_app=False
				#print("menu")
				close_app=True

		return -1
