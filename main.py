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
app=Application("watch ip adress", 1234, heigth,width)
app.setText((10,0),"GBROS", 255,app.getFonts()[1])
app.setText((32,32),"V 0.1", 255,app.getFonts()[1])
app.sendImg()
time.sleep(2)
applications=[["CLOCK", Clock(app)],["TORCH", Torch(app)],["WEATHER", Weather(app)],["SETTINGS",Settings(app)]]
Menu(app, applications).run()
