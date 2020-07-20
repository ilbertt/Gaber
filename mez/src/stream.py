class Stream:
    def __init__(self, app):
        self.app = app
        self.screens = ["first", "second"]
    
    def run(self:
        change=True
        i=0
        j=1
        next_app=False
        close_app=False
        while(not close_app):
            if (change):
                change=False
                self.app.newImg()
                self.app.setText((45,0), "STREAM ", 255,self.app.getFonts()[0])

                for screen in self.screens:
                    self.app.setText((10,10*j),screen, 255,self.app.getFonts()[0])
                    j=j+1

                self.app.setText((10,10*j),"MENU ", 255,self.app.getFonts()[0])
                last_i = j-1
                j=1
                self.app.setText((1,10+i*10),">", 255,self.app.getFonts()[0])
                
                self.app.sendImg_and_recvData()
            else:
                self.app.recvData()

            #print(data)	
            if (self.app.isPinUp("DOWN")):
                if(i==last_i):
                    i=0
                else:
                    i+=1

                change=True
            elif (self.app.isPinUp("UP")):
                if(i==0):
                    i=last_i
                else:
                    i-=1

                change=True
            elif(self.app.isPinUp("SELECT")):
                print(i,j, last_i)
                if(i==last_i):
                    next_app=True
                elif(i==1):
                    '''self.ledstatus=not self.ledstatus
                    self.app.setOutPin(16, self.ledstatus)'''
                elif(i==0):
                    '''self.npstatus= not self.npstatus
                    self.app.setNeopixel([255*self.npstatus,255*self.npstatus,255*self.npstatus])'''

            self.app.storeData()

            if (next_app):
                next_app=False
                close_app=True

        return -1