import time
from PIL import Image
import time

class ProfilePic:
	def __init__(self, app):
		self.app=app
		self.i=0

	def run(self):
		datau_old=0
		datad_old=0
		datas_old=0
		next_app=False
		close_app=False
		pics = []
		pics.append(Image.open('mez/src/images/pic.png'))
		pics.append(Image.open('eulero/src/images/pic.png'))
		pics.append(Image.open('gaber/src/images/pic.png'))
		img_time = time.time()
		self.app.setImg(pics[0])
		self.app.sendImg()
		i = 1
		pause = False
		while(not close_app):
			if time.time() - img_time > 3 and not pause:
				self.app.setImg(pics[i])
        		self.app.sendImg()
				if i < len(pics)-1:
					i += 1
				else:
					i = 0
			data = self.app.recvData()
			if (data['UP']!=datau_old):
				datau_old=data['UP']
				if(datau_old):
					pause = not pause
					

			elif (data['DOWN']!=datad_old):
				datad_old=data['DOWN']
				if(datad_old):
					pause = not pause

			elif(data['SELECT']!=datas_old):
				datas_old=data['SELECT']
				if(datas_old):
					next_app=True
			
			if (next_app and data['SELECT']==0):
				next_app=False
				#print("menu")
				close_app=True

		return -1
