from machine import Pin, I2C, PWM
import neopixel
import sh1106
import socket
import framebuf
import machine
import time
def run(adress):
	pin_in=[]
	oled_width = 0
	oled_heigth = 0
	oled = 0

	while(1):
		so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			so.connect(adress)
			msg=0
			for p in pin_in:
				msg += ((not Pin(p, Pin.IN, Pin.PULL_UP).value())<<p)

			so.send(str(msg).encode())
			try:
				s=so.read()
				so.close()
				if(len(s)==2):
					if( not ( int(s) in pin_in)):
						pin_in.append(int(s))

				elif(len(s)==3):
					pin = int(int(s)/10)
					Pin(pin, Pin.OUT).value(int(s)%10)
					if pin in pin_in:
						pin_in.remove(pin)

				elif(len(s)==9):
					s=int(s)
					duty=s%10000
					s=int(s/10000)
					freq=s%1000+1
					pin=int(s/1000)
					PWM(Pin(pin), freq=freq, duty=duty)
					if pin in pin_in:
						pin_in.remove(pin)

				elif(len(s)==10):
					s=int(s)
					oled_heigth=s%1000
					s=int(s/1000)
					oled_width=s%1000
					s=int(s/1000)
					scl=s%100
					sda=int(s/100)
					i2c = I2C(-1, scl=Pin(scl), sda=Pin(sda))
					oled = sh1106.SH1106_I2C(oled_width, oled_heigth, i2c)
				elif(len(s)==11):
					s=int(s)
					val=[0,0,0]
					val[2]=(s%1000)
					s=int(s/1000)
					val[1]=(s%1000)
					s=int(s/1000)
					val[0]=(s%1000)
					np = neopixel.NeoPixel(machine.Pin(int(s/1000)), 1)
					np[0]=val
					np.write()
				elif(len(s)!=0):
					p=bytearray(s)
					fbuf=framebuf.FrameBuffer(p,oled_width,oled_heigth,framebuf.MONO_HLSB)
					oled.blit(fbuf,0,0)
					oled.show()

			except:
				so.close()

		except:
			pass
			
		time.sleep(0.01)
