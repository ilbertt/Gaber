import datetime
import math

class Clock:
	def __init__(self, app):
		self.app=app

	def run(self, menu):
		sec_old=-1
		next_app=False
		datas_old=0
		datau_old=0
		datad_old=0

		self.cx = int(self.app.heigth/2)
		self.cy = int(self.app.width/2)
		self.r = self.cy

		bounding_box = [(self.cx-self.r, self.cy-self.r),(self.cx+self.r, self.cy+self.r-1)]

		clock_type = "analogic"
		old_clock_type = ""

		while(1):
			now = datetime.datetime.now()
			hour = now.hour
			min = now.minute
			sec = now.second

			date = now.strftime("%a, %b %d %Y")

			if(sec!=sec_old or clock_type != old_clock_type):
				sec_old=sec
				old_clock_type=clock_type
				self.app.newImg()

				if(clock_type=="analogic"):

					self.app.d.ellipse(bounding_box, fill = 0, outline="white")

					#seconds
					shape = self.needleShape(sec, self.r - 1)
					self.app.d.line(shape, fill="white", width = 1)

					#minutes
					shape = self.needleShape(min, self.r - 5)
					self.app.d.line(shape, fill="white", width = 1)

					#hours
					hour = hour if (hour<12) else (hour-12)
					shape = self.needleShape(int((hour/12)*60), self.r - 10)
					self.app.d.line(shape, fill="white", width = 1)
				elif(clock_type=="digital"):
					self.app.setText((5,7),str(hour).zfill(2)+":"+str(min).zfill(2)+":"+str(sec).zfill(2), 255,self.app.getFonts()[1])
					self.app.setText((20,42), date, 255, self.app.getFonts()[0])
				data=self.app.sendImg_and_recvData()
			else:
				data=self.app.recvData()

			#print(data)
			if(data['SELECT']!=datas_old):

				datas_old=data['SELECT']
				if(datas_old):	
					next_app=True
			elif(data['DOWN']!=datad_old):

				datad_old=data['DOWN']
				if(datad_old):	
					clock_type = "digital"
			elif(data['UP']!=datau_old):

				datau_old=data['UP']
				if(datau_old):	
					clock_type = "analogic"

			if (next_app and data['SELECT']==0):
				next_app=False
				#print("menu")
				menu.run()

	def needleShape(self, angle, radius):
    
		cx = self.cx
		cy = self.cy - 1
		sx = cx
		sy = cy - radius + 2

		if angle == 30:
			sx = cx
			sy = cy + radius - 2

		if angle > 0:
			rad = (angle/30) * math.pi - math.pi/2
			m = math.tan( rad )
			if angle < 30:
				sx = int( radius / math.sqrt(1+math.pow(m,2)) ) + cx
				sy = int(  m*(sx-cx) ) + cy
			elif angle > 30:
				sx = -int( radius / math.sqrt(1+math.pow(m,2)) ) + cx
				sy = int(  m*(sx-cx) ) + cy

		#print(angle, [(cx, cy),(sx, sy)])

		return [(cx, cy),(sx, sy)]

