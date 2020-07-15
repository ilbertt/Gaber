import network

my_wifi = [('<your_ssid_1>','<your_pw_1>'), ('<your_ssid_2>','<your_pw_2>')]

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        available_wifi = sta_if.scan()
        ssid = ''
        pw = ''
        end = 0
        for try_wifi in my_wifi:
            if end == 1:
                break
            for wifi in available_wifi:
                if wifi[0].decode() == try_wifi[0]:
                    ssid = try_wifi[0]
                    pw = try_wifi[1]
                    print(ssid, pw)
                    end = 1
                    break
                
        sta_if.connect(ssid, pw)   
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
do_connect()
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP-AP')