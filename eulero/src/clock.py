import time
import math

class Clock:
	def __init__(self, app):
		self.app=app

	def run(self, menu):
		sec_old=-1
		data_old=0
		next_app=False

		self.cx = int(self.app.heigth/2)
		self.cy = int(self.app.width/2)
		self.r = self.cy

		bounding_box = [(self.cx-self.r, self.cy-self.r),(self.cx+self.r, self.cy+self.r - 1)]

		clock_type = "analogic"
		old_clock_type = ""
		while(1):
			t=time.localtime()
			sec=t.tm_sec
			min=t.tm_min
			hour=t.tm_hour

			if(sec!=sec_old or clock_type != old_clock_type):
				sec_old=sec
				self.app.newImg()

				if(clock_type=="analogic"):

					self.app.d.ellipse(bounding_box, fill = 0, outline="white", width=2)

					#seconds
					shape = self.needleShape(sec, self.r - 1)
					self.app.d.line(shape, fill="white", width = 1)

					#minutes
					shape = self.needleShape(min, self.r - 5)
					self.app.d.line(shape, fill="white", width = 1)

					#hours
					hour = hour if (hour<=12) else (hour-12)
					shape = self.needleShape(int((hour/12)*60), self.r - 10)
					self.app.d.line(shape, fill="white", width = 1)
				elif(clock_type=="digital"):
					self.app.setText((5,16),str(t.tm_hour).zfill(2)+":"+str(t.tm_min).zfill(2)+":"+str(sec).zfill(2), 255,self.app.getFonts()[1])
				
				data=int(self.app.sendImg_and_recvData())

				old_clock_type = clock_type
			else:
				data=int(self.app.recvData())

			#print(data)
			if(data!=data_old and data==2**self.app.inPins['SELECT']['number']):
				next_app=True
			elif(data!=data_old and data==2**self.app.inPins['DOWN']['number']):
				clock_type = "digital"
			elif(data!=data_old and data==2**self.app.inPins['UP']['number']):
				clock_type = "analogic"

			if (next_app and data==0):
				next_app=False
				print("menu")
				menu.run()

			if (data!=data_old):
				data_old=data

	def needleShape(self, angle, radius):
    
		sx = self.cx
		sy = self.cy - radius + 2

		if angle == 30:
			sx = self.cx
			sy = self.cy + radius - 2
			#print(angle, [(self.cx, self.cy),(sx, sy)])

		if angle > 0:
			rad = (angle/30) * math.pi - math.pi/2
			m = math.tan( rad )
			if angle < 30:
				sx = int( radius / math.sqrt(1+math.pow(m,2)) ) + self.cx
				sy = int(  m*(sx-self.cx) ) + self.cy
			elif angle > 30:
				sx = -int( radius / math.sqrt(1+math.pow(m,2)) ) + self.cx
				sy = int(  m*(sx-self.cx) ) + self.cy

		return [(self.cx, self.cy),(sx, sy)]

