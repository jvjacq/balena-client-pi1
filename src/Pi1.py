import socket
from datetime import datetime
import threading
import time
import random
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

#SERVER details=======================
SERVER_IP = '192.168.1.196'
SERVER_PORT = 5005
#20 is sufficiently large for our format
BUFF_SIZE = 20
#Flag for turning sending on/off
send_flag = True
#Stores time of last sample (sent with status)
lastsample = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#=======================

#Global rate to be sampled by the thread method
rate = 10
#Global channels to be sampled by the thread method
chan = None
chan1 = None

#======================
def main():
    global chan, chan1, rate,s,send_flag
    
    btn_num = 25

    #Server connection
    s.connect((SERVER_IP, SERVER_PORT))

    #HARDWARE============================================================
    # create the spi bus
    spi = busio.SPI(clock=board.SCLK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)
    
    #create button instance as an digital input
    btn = digitalio.DigitalInOut(board.D25)
    btn.direction = digitalio.Direction.INPUT
    btn.pull = digitalio.Pull.UP
    
    #Create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create an analog input channel on pin 2 - Light sensor
    chan = AnalogIn(mcp, MCP.P2)

    # create an analog input channe on pin 1 - Temperature sensor
    chan1 = AnalogIn(mcp, MCP.P1)

    #THREADING===========================================================    
    #Start thread with dedicated method, no args
    thread = threading.Thread(target=sample_thread)
    thread.daemon = True
    thread.start()

    #RECEIVING==============================================================
    while True:
        #Wait to receive server responses
        server_msg = s.recv(BUFF_SIZE)
        #Decode responses to text
        server_msg = server_msg.decode('utf-8')
        #Retreive command character
        cmd = server_msg[0]
        
        if(cmd == "O"):
            #O - turn sending/sensor on
            send_flag = True
        elif(cmd == "F"):
            #F - turn sending/sensor off
            send_flag = False
        elif(cmd == "K"):
            #K - call method to return current status
            sendstatus()
        elif(cmd == "X"):
            #X - server closing -> client closes
            print("Client exiting...")
            quit()
    #====================================================================

def sample_thread():
    #Thread method to sample values and send data over TCP repetitively
    while(True):
        lgt = chan.value
        tmp = round(chan1.voltage*100)
        #Send sampled values if flag enabled (sensor 'on')
        if(send_flag):
            senddata(lgt,tmp)
        
        #Wait for 10s     
        time.sleep(rate)
        
#SENDING=================================================================
#Send state of send_flag variable (sensor status) and time of last sample
def sendstatus():    
    #T - message code of 'STATUS' message
    char = "T"
    #Default value if no previous sample
    if lastsample == None: message = str(send_flag) + "#XX:XX:XX"
    else: message = str(send_flag) + "#" + lastsample
    length = len(message)
    message = char + " " + str(length) + " " + message
    #Message format: <cmd> <length> <flag>#<time>
    s.send(str.encode(message))

def senddata(lgt,tmp):
    global lastsample
    #S - message code of 'SENSOR' data message
    char = "S"
    message = str(lgt) + "#" + str(tmp)
    length = len(message)
    message = char + " " + str(length) + " " + message
    #Message format: <cmd> <length> <light>#<temp>
    s.send(str.encode(message))

    #Note time as the new latest sample   
    lastsample = str(datetime.now().time())[0:8]
#==================================================================

if __name__ == '__main__':
    main()