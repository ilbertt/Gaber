# firmware v 0.3.2
from machine import Pin, I2C, PWM, ADC
import neopixel
import socket
import framebuf
import time
import struct

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        try:
            sock.settimeout(0.05)
            packet = sock.recv(n - len(data))
            '''if not packet:
                return None'''
            data.extend(packet)
        except:
            pass
    return data

def run(so):
    pin_in=[]
    oled_width = 1
    oled_heigth = -1
    oled = 0
    adc=0
    i2c_msg=0
    send_type=0 # 0: data, 1: nfc, 2: adc
    #so.settimeout(0.05)
    disp=False
    data=b''
    rdr=0
    nfc='0'
    while(1):
        #so.setsockopt(socket.TCP_NODELAY,1)
        
        s=b''
        '''try:
            s=so.recv(1024)
        except:
            pass'''
        
        s=bytes(recv_msg(so))
        
        d=s
        print(len(s))
        if(len(s)==1): # send NFC
            nfc='0'
            send_type=1
            if(rdr):
                (stat, _ ) = rdr.request(rdr.REQIDL)
                if stat == rdr.OK:
                    (stat, raw_uid) = rdr.anticoll()
                    if stat == rdr.OK:
                        nfc=":%02x%02x%02x%02x:" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])

        elif(len(s)==2): # set Input Pin
            if( not ( int(s) in pin_in)):
                pin_in.append(int(s))
   
        elif(len(s)==3): # set Output Pin
            pin = int(int(s)/10)
            Pin(pin, Pin.OUT).value(int(s)%10)
            if pin in pin_in:
                pin_in.remove(pin)

        elif(len(s)==4): # read ADC
            pin=int(s)
            adc=ADC(pin)
            send_type=2
            if pin in pin_in:
                pin_in.remove(pin)
        
        elif(len(s)==8): # read I2C
            #print("i2c")
            s=int(s)
            nbytes = s%100
            s=int(s/100)
            addr = s%100
            s=int(s/100)
            scl = s%100
            sda=int(s/100)
            #print(sda,scl,addr,nbytes)
            
            i2c=I2C(-1, scl=Pin(scl), sda=Pin(sda))
            i2c_msg=i2c.readfrom(addr,nbytes)
            send_type=3
            #print(i2c_msg)
            
        elif(len(s)==9): # set PWM
            s=int(s)
            duty=s%10000
            s=int(s/10000)
            freq=s%1000+1
            pin=int(s/1000)
            PWM(Pin(pin), freq=freq, duty=duty)
            if pin in pin_in:
                pin_in.remove(pin)    
                    
        elif(len(s)==10): # set NFC
            s=s.decode()
            sda=int(s[-2:])
            s=int(s[:-2])
            rst=s%100
            s=int(s/100)
            miso=s%100
            s=int(s/100)
            mosi=s%100
            s=int(s/100)
            sclk=s%100
            from mfrc522 import MFRC522
            rdr=MFRC522(sclk, mosi,miso,rst,sda)

        elif(len(s)==11): # set Neopixel
            s=int(s)
            val=[0,0,0]
            val[2]=(s%1000)
            s=int(s/1000)
            val[1]=(s%1000)
            s=int(s/1000)
            val[0]=(s%1000)
            pin=int(s/1000)
            np = neopixel.NeoPixel(Pin(pin), 1)
            np[0]=val
            np.write()
            if pin in pin_in:
                pin_in.remove(pin)
        
        elif(len(s)==12): #set Display
            s=s.decode()
            disp=int(s[-2:])
            s=s[:-2]
            s=int(s)
            oled_heigth=s%1000
            s=int(s/1000)
            oled_width=s%1000
            s=int(s/1000)
            scl=s%100
            sda=int(s/100)
            i2c = I2C(-1, scl=Pin(scl), sda=Pin(sda))
            print(disp, oled_heigth, oled_width, sda, scl)

            if(disp==0):
                from sh1106 import SH1106_I2C
                oled = SH1106_I2C(oled_width, oled_heigth, i2c)
            elif(disp==1):
                from ssd1306 import SSD1306_I2C
                oled = SSD1306_I2C(oled_width, oled_heigth, i2c)
        
        elif(len(s) != 0):
            p=bytearray(s)
            fbuf=framebuf.FrameBuffer(p,oled_width, oled_heigth,framebuf.MONO_HLSB)
            oled.blit(fbuf,0,0)
            oled.show()
        
        #****** send ******#   
        msg=0
        if(send_type==0):
            for p in pin_in:
                msg += ((not Pin(p, Pin.IN, Pin.PULL_UP).value())<<p)

        try:
            if(send_type==0):
                so.send(str(msg).encode())
            elif(send_type==1):
                so.send(str(nfc).encode())
            elif(send_type==2):
                so.send(str(adc).encode())
            elif(send_type==3):
                so.send(i2c_msg)

            send_type=0
        except:
            import machine
            machine.reset()

        #time.sleep(0.01)


#so.close()

 




