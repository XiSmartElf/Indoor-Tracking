#!/usr/bin/python

import socket
import csv
from threading import Thread, Semaphore
import localization
import pygame, sys
from StdSuites.AppleScript_Suite import integer
import os

mutex = Semaphore(1)
xGraphic =0
yGraphic =0
zGraphic =0

'''
FindSignalStrength_RSSI() a sub function that returns a hardcoded dictionary, SignalStrength_RSSI. 
where the keys are the dBm values of signal strengths, and the values are the related RSSIs.
This function has no input. The signal strengths are converted to RSSIs following Cisco Conversion standard, 
which is the most granular dBm lookup table so far.
'''       
def FindSignalStrength_RSSI():
    SignalStrength_RSSI = {}
    
    SignalStrength_RSSI[-113]= 0
    SignalStrength_RSSI[-112]= 1 
    SignalStrength_RSSI[-111]= 2
    SignalStrength_RSSI[-110]= 3
    SignalStrength_RSSI[-109]= 4
    SignalStrength_RSSI[-108]= 5
    SignalStrength_RSSI[-107]= 6
    SignalStrength_RSSI[-106]= 7
    SignalStrength_RSSI[-105]= 8
    SignalStrength_RSSI[-104]= 9
    SignalStrength_RSSI[-103]= 10
    SignalStrength_RSSI[-102]= 11
    SignalStrength_RSSI[-101]= 12
    SignalStrength_RSSI[-100]= 12.5
    SignalStrength_RSSI[-99]= 13
    SignalStrength_RSSI[-98]= 14
    SignalStrength_RSSI[-97]= 15
    SignalStrength_RSSI[-96]= 16
    SignalStrength_RSSI[-95]= 17
    SignalStrength_RSSI[-94]= 18
    SignalStrength_RSSI[-93]= 19
    SignalStrength_RSSI[-92]= 20
    SignalStrength_RSSI[-91]= 21
    SignalStrength_RSSI[-90]= 22
    SignalStrength_RSSI[-89]= 23
    SignalStrength_RSSI[-88]= 24
    SignalStrength_RSSI[-87]= 25
    SignalStrength_RSSI[-86]= 26
    SignalStrength_RSSI[-85]= 27
    SignalStrength_RSSI[-84]= 28
    SignalStrength_RSSI[-83]= 29
    SignalStrength_RSSI[-82]= 30
    SignalStrength_RSSI[-81]= 31
    SignalStrength_RSSI[-80]= 32
    SignalStrength_RSSI[-79]= 33
    SignalStrength_RSSI[-78]= 34
    SignalStrength_RSSI[-77]= 35
    SignalStrength_RSSI[-76]= 35.5
    SignalStrength_RSSI[-75]= 36
    SignalStrength_RSSI[-74]= 37
    SignalStrength_RSSI[-73]= 38
    SignalStrength_RSSI[-72]= 39
    SignalStrength_RSSI[-71]= 39.5
    SignalStrength_RSSI[-70]= 40
    SignalStrength_RSSI[-69]= 41
    SignalStrength_RSSI[-68]= 42
    SignalStrength_RSSI[-67]= 43
    SignalStrength_RSSI[-66]= 43.5
    SignalStrength_RSSI[-65]= 44
    SignalStrength_RSSI[-64]= 45
    SignalStrength_RSSI[-63]= 46
    SignalStrength_RSSI[-62]= 47
    SignalStrength_RSSI[-61]= 47.5
    SignalStrength_RSSI[-60]= 48
    SignalStrength_RSSI[-59]= 49
    SignalStrength_RSSI[-58]= 50
    SignalStrength_RSSI[-57]= 50.5
    SignalStrength_RSSI[-56]= 51
    SignalStrength_RSSI[-55]= 52
    SignalStrength_RSSI[-54]= 52.5
    SignalStrength_RSSI[-53]= 53
    SignalStrength_RSSI[-52]= 54
    SignalStrength_RSSI[-51]= 54.5
    SignalStrength_RSSI[-50]= 55
    SignalStrength_RSSI[-49]= 57
    SignalStrength_RSSI[-48]= 58
    SignalStrength_RSSI[-47]= 60
    SignalStrength_RSSI[-46]= 61
    SignalStrength_RSSI[-45]= 62
    SignalStrength_RSSI[-44]= 63
    SignalStrength_RSSI[-43]= 65
    SignalStrength_RSSI[-42]= 66
    SignalStrength_RSSI[-41]= 68
    SignalStrength_RSSI[-40]= 69
    SignalStrength_RSSI[-39]= 70
    SignalStrength_RSSI[-38]= 71
    SignalStrength_RSSI[-37]= 72
    SignalStrength_RSSI[-36]= 72.5
    SignalStrength_RSSI[-35]= 73
    SignalStrength_RSSI[-34]= 74
    SignalStrength_RSSI[-33]= 75
    SignalStrength_RSSI[-32]= 76
    SignalStrength_RSSI[-31]= 76.5
    SignalStrength_RSSI[-30]= 77
    SignalStrength_RSSI[-29]= 78
    SignalStrength_RSSI[-28]= 79
    SignalStrength_RSSI[-27]= 80
    SignalStrength_RSSI[-26]= 80.5
    SignalStrength_RSSI[-25]= 81
    SignalStrength_RSSI[-24]= 82
    
    return SignalStrength_RSSI
    
def Get_APLocation():
    APlocation={}
    
    APlocation['phillips-101-ap'] = [992,735,199.05]
    APlocation['phillips-107-ap'] = [993,1521,199.05]
    APlocation['phillips-113-ap'] = [1445,1567,199.05]
    APlocation['phillips-121-ap'] = [2015,1590,199.05]
    APlocation['phillips-203-ap'] = [1008,475,650.65]
    APlocation['phillips-219-ap'] = [1023,1370,650.65]
    APlocation['phillips-400ca-ap'] = [1516,1575,650.65]
    APlocation['phillips-232-ap'] = [2117,1554,650.65]
    APlocation['phillips-238-ap'] = [1130,2229,650.65]
    APlocation['phillips-307-ap'] = [1012,562,1139.85]
    APlocation['phillips-318-ap'] = [1027,1360,1139.85]
    APlocation['phillips-300cc-ap'] = [1516,1575,1139.85]
    APlocation['phillips-330-ap'] = [2117,1554,1139.85]
    APlocation['phillips-339-ap'] = [1130,2269,1139.85]
    APlocation['phillips-405-ap'] = [1080,475,1466.35]
    APlocation['phillips-414b-ap'] = [1089,1329,1466.35]
    APlocation['phillips-200cb-ap'] = [1516,1575,1466.35]
    APlocation['phillips-428-ap'] = [2117,1554,1466.35]
    APlocation['phillips-422-ap'] = [2086,2142,1466.35]

    return APlocation 

# start of program
print ("S: Connecting...")

'''
Step 1: Read the  csv file
'''
'''the file contains the dictionary BSSID -> APID 
Return a dictionary BSSID_APinfo. 
A single AP has multiple BSSIDs(MAC addresses), 
for instance, AP Phillips-101-ap has BSSIDs such as d8:c7:c8:d3:d6:70, d8:c7:c8:d3:d6:71, 
d8:c7:c8:d3:d6:72, d8:c7:c8:d3:d6:73, d8:c7:c8:d3:d6:60, d8:c7:c8:d3:d6:61, 
d8:c7:c8:d3:d6:62 and d8:c7:c8:d3:d6:63.
'''
BSSID_APinfo = {}
fn = os.path.join(os.path.dirname(__file__), '2039_PhillipsHall_AP.csv')
with open(fn, 'rU') as csvfile:
    book1 = csv.reader(csvfile)
    for row in book1: 
        if row[1] in BSSID_APinfo:
            BSSID_APinfo[row[0]].append(row[1])
        else:
            BSSID_APinfo[row[0]] = [row[1]]

'''
Step 2: Create Signal Strength -> RSSI dictionary
'''
SignalStrength_RSSI = FindSignalStrength_RSSI()

'''
Step 3: Create Access Points Location Coordinates
'''
APlocation = Get_APLocation()

'''
Step 4: Create TCP connection
'''
SERVERIP = socket.gethostbyname(socket.gethostname())
SERVERPORT = 1395
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# mark the socket so we can rebind quickly to this port number
# after the socket is closed
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# bind the socket to the local loopback IP address and special port
serversocket.bind((SERVERIP, SERVERPORT))

# start listening with a backlog of 5 connections
serversocket.listen(5)

'''
Step 5: create 32 server threads
'''

class ConnectionHandler(Thread):
    def __init__(self, serversocket, BSSID_APinfo, SignalStrength_RSSI, APlocation):
        Thread.__init__(self)
        self.serversocket = serversocket
        self.BSSID_APinfo = BSSID_APinfo
        self.SignalStrength_RSSI = SignalStrength_RSSI
        self.APlocation = APlocation

    def run(self):
        while True:
            (clientsocket, address) = self.serversocket.accept()
            mutex.acquire()
            print ("S: Receiving...")
            try:
                message = clientsocket.recv(1024*5).decode()      
                print(message)
                (position, clientID, floorNum) = localization.start(message, self.BSSID_APinfo, self.SignalStrength_RSSI, self.APlocation)
                global xGraphic
                xGraphic=position[0]
                global yGraphic
                yGraphic=position[1]
                global zGraphic
                zGraphic=floorNum
                print ("Client %s is on the %d floor -> Predicted Location is:" % (clientID, floorNum))
                print ("*******************")
                print ("X:", position[0])
                print ("Y:", position[1])
                print ("Z:", position[2])
                print ("*******************")

               
            except:
                print ("S: Error")

            finally:
                clientsocket.close()
                print ("S: Done\n")
                mutex.release()

for i in range(32):
    ConnectionHandler(serversocket, BSSID_APinfo, SignalStrength_RSSI, APlocation).start() 
    
'graph handling'
pygame.init()
pygame.display.set_caption('Position Tracking')
backgroundPic = os.path.join(os.path.dirname(__file__), 'pics/PH2.jpg')
background=pygame.image.load(backgroundPic)
screen=pygame.display.set_mode(background.get_rect().size,0,32)
background=background.convert()
#mouse_c=pygame.image.load("/Users/BboyKellen/Documents/LiClipse Workspace/MENG/PH2.jpg").convert_alpha()
position=[300,176]  
color=[255,0,0]  
color_cross=[0,0,255]
radius=(6)
minus=True
clock=pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 15)

while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(background,(0,0))   
    x,y=pygame.mouse.get_pos()        
    if minus==True:
        radius -=1
        if radius==0:
            minus=False
    else:
        radius+=1
        if radius==6:
            minus=True
                
         
    'get the position in the map'
    #print (background.get_rect().size)
    position[0]= int((558 / 2550.0) * float(xGraphic))
    position[1]= int((799/ 3509.0) * float(yGraphic))
    'print mouse building location'
    labelX=int(x/558.0*2550.0)
    labelY=int(y/799.0*3509.0)
    label = myfont.render("("+str(labelX)+","+str(labelY)+")", 1, (255,0,0))
    #label = myfont.render("("+str(position[0])+","+str(position[1])+")", 1, (255,0,0))
    locationLabel=myfont.render("("+str(xGraphic)+","+str(yGraphic)+")", 1, (255,0,0))
    screen.blit(label, (300, 650))  
    screen.blit(locationLabel, (300, 600))  
    screen.lock()
    'draw positions'  
    pygame.draw.circle(screen,color, position,radius)
    pygame.draw.line(screen,color_cross,(x-10,y),(x+10,y),1)
    pygame.draw.line(screen,color_cross,(x,y+10),(x,y-10),1)  
    'draw routers'
    keys=APlocation.keys();
    apPosition=[1000,1000];
    for key in keys:
        if APlocation[key][2]==650.65:
            apPosition[0]= int((558 / 2550.0) * float(APlocation[key][0]))
            apPosition[1]= int((799/ 3509.0) * float(APlocation[key][1]))
            pygame.draw.circle(screen,[255,0,255], apPosition,3)  
            #print(str(APlocation[key][0])+" "+str(APlocation[key][1]))
    'release the canvas'
    screen.unlock()
    pygame.display.update()
    pygame.display.flip()
    clock.tick(30)
