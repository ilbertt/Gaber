import time
class Clock:
	def __init__(self, app):
		self.app=app

	def run(self, menu):
		sec_old=-1
		next_app=False
		while(1):
			t=time.localtime()
			sec=t.tm_sec
			if(sec!=sec_old):
				sec_old=sec
				self.app.newImg()
				self.app.setText((5,16),str(t.tm_hour).zfill(2)+":"+str(t.tm_min).zfill(2)+":"+str(sec).zfill(2), 255,self.app.getFonts()[1])
				self.app.sendImg_and_recvData()
			else:
				self.app.recvData()

			#print(data)
			if(self.app.isPinUp("SELECT")):
				next_app=True
			
			self.app.storeData()

			if (next_app):
				next_app=False
				print("menu")
				menu.run()


