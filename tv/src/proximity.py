import time
class Proximity:
	def __init__(self, app):
		self.app=app

	def run(self):
		changed=True
		datap_old=0
		while(1):
			if(changed):
				self.app.newImg()
				self.app.setText( (45,0), str(datap_old),255,self.app.getFonts()[1])
				data=self.app.sendImg_and_recvData()
				changed=False
			else:
				data=self.app.recvData()

			#print(data)
			if(data['PROXIMITY']!=datap_old):
				datap_old=data['PROXIMITY']
				changed=True

			



