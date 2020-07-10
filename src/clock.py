import time
class Clock:
	def __init__(self, app):
		self.app=app

	def run(self, menu):
		sec_old=-1
		data_old=0
		next_app=False
		while(1):
			t=time.localtime()
			sec=t.tm_sec
			if(sec!=sec_old):
				sec_old=sec
				self.app.newImg()
				self.app.setText((5,16),str(t.tm_hour).zfill(2)+":"+str(t.tm_min).zfill(2)+":"+str(sec).zfill(2), 255,self.app.getFonts()[1])
				data=int(self.app.sendImg_and_recvData())
			else:
				data=int(self.app.recvData())

			#print(data)
			if(data!=data_old and data==4):
				next_app=True

			if (next_app and data==0):
				next_app=False
				print("menu")
				menu.run()

			if (data!=data_old):
				data_old=data


