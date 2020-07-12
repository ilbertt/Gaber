import network
def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        #sta_if.connect('Vodafone-33866776', 'bdacpslt2mtdjvu')
        sta_if.connect('TP-LINK_FCA2', '19204109')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
    
do_connect()
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP-AP')
