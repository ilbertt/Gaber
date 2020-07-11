from src.app   		import Application
from src.menu  		import Menu
from src.clock 		import Clock
from src.torch 		import Torch
from src.weather	import Weather
from src.settings 	import Settings
from PIL   			import Image
import time
heigth=128
width=64
app=Application("192.168.0.115", 1234, heigth,width)
pic=Image.open('src/images/pic.png').convert('1')
app.setImg(pic)
app.sendImg()
time.sleep(4)
app.newImg()
app.setText((10,0),"GBROS", 255,app.getFonts()[1])
app.setText((32,32),"V 0.1", 255,app.getFonts()[1])
app.sendImg()
app.getPinConfig("src/config/pins.json")
app.setInPins()

time.sleep(2)
applications=[["CLOCK", Clock(app)],["TORCH", Torch(app)],["WEATHER", Weather(app)],["SETTINGS",Settings(app)]]
Menu(app, applications).run()
