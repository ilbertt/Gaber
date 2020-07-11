
from machine import Pin, I2C
import neopixel
import sh1106
import socket
import framebuf
import machine
import time
adress=("192.168.0.7", 1234)
i2c = I2C(-1, scl=Pin(4), sda=Pin(5))
btn1= Pin(12, Pin.IN, Pin.PULL_UP)
btn2= Pin(13, Pin.IN, Pin.PULL_UP)
btn3= Pin(14, Pin.IN, Pin.PULL_UP)
pin_in=[]
np = neopixel.NeoPixel(machine.Pin(15), 1)
led=machine.Pin(16, Pin.OUT)
oled_width = 128
oled_height = 64
oled = sh1106.SH1106_I2C(oled_width, oled_height, i2c)

while(1):
  so=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  so.connect(adress)
  msg=0
  for p in pin_in:
    msg += (not Pin(p, Pin.IN, Pin.PULL_UP).value())* 2**p
  so.send(str(msg).encode())
  s=so.read()
  so.close()
  if(len(s)==2):
    pin_in.append(int(s))
  elif(len(s)==3):
    pin = int(int(s)/10)
    Pin(pin, Pin.OUT).value(int(s)%10)
    if pin in pin_in:
      pin_in.remove(pin)
  elif(len(s)==9):
    s=int(s)
    val=[0,0,0]
    val[2]=(s%1000)
    s=int(s/1000)
    val[1]=(s%1000)
    val[0]=int(s/1000)
    np[0]=val
    np.write()
    
  elif(len(s)!=0):
    p=bytearray(s)
    fbuf=framebuf.FrameBuffer(p,oled_width,oled_height,framebuf.MONO_HLSB)
    oled.blit(fbuf,0,0)
    oled.show()
    
  time.sleep(0.01)
    
    







