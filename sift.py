import numpy as np
import cv2
import time
def cordinates():
    global i,areao,zco
    if i==0:
        areao=area[0]
        zco.append(z0)
        i+=1
    else:
        dx=pts[i][0]-pts[i-1][0]
        dy=pts[i][1]-pts[i-1][1]
        z=areao*zco[0]/area[i]       
        #z=((areao*z0)/area[i])
        zco.append(z)
        dz=zco[i]-zco[i-1]
        dt=Time[i]-Time[i-1]
        i+=1
        if dx >25  and dy >25 and dz >25 :
            for j in range(0, len(pts)-1):
                if pts[j-1] is None or pts[j] is None:
                    return False
                cv2.line(frame,pts[j],pts[j+1],(0, 255, 255),2)
        cv2.putText(frame,'x :{0:<7.2f} , y: {1:<7.2f} , z: {2:<7.2f}'.format(x,y,z),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,150),1)
        cv2.putText(frame,'vx :{0:<7.2f} , vy: {1:<7.2f} , vz: {2:<7.2f}'.format(dx/dt,dy/dt,dz/dt),(10,frame.shape[0]-10),cv2.FONT_HERSHEY_SIMPLEX,0.75,(0,255,150),1)
    cv2.imshow('Ball Tracking',frame)
    k=cv2.waitKey(5)
    if  k==27:
        return True
i=0
areao=0
zco=[]
Time=[]
area=[]
z0=input('enter initial Z coordinate: ')
hl=input('Enter the lower hue: ')
sl=input('Enter the lower saturation: ')
vl=input('Enter the lower value: ')
hu=input('Enter the upper hue: ')
su=input('Enter the upper saturation: ')
vu=input('Enter the upper value: ')
p1=[hl,sl,vl]
p2=[hu,su,vu]
timer=time.clock
cap=cv2.VideoCapture(0)
time.sleep(1)
pts=()
while(True):
    #capture frame by frame
    ret,frame=cap.read()
    frame=cv2.resize(frame,(1080,720))
    mask=cv2.GaussianBlur(frame,(11,11),0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    upper_colour=np.array([p2])
    lower_colour=np.array([p1])
    mask = cv2.inRange(hsv,lower_colour,upper_colour)
    kernel = np.ones((5,5),np.uint8) 
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    mask = cv2.erode(mask,kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    kernel = np.ones((11,11),np.uint8) 
    mask=cv2.filter2D(mask,-1,kernel)
    adc,mask=cv2.threshold(mask,25,255,cv2.THRESH_BINARY)
    kernel = np.ones((5,5),np.uint8) 
    mask=cv2.GaussianBlur(mask,(5,5),0)
    mask=cv2.dilate(mask,kernel,iterations=1)
    mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)
    mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
    im2,contour,hiererchy=cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    con=contour[0]
    area.append(cv2.contourArea(con))
    if  len(con)>20:
        c=max(contour,key=cv2.contourArea)
        (x,y),radius=cv2.minEnclosingCircle(c)
        M=cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        centre=(int(x),int(y))
        radius=int(radius)
        if radius>5:
            frame=cv2.circle(frame,centre,radius,(0,255,0),2)
            cv2.circle(frame, centre, 5, (0, 0, 255), -1)
    Time.append(time.clock())
    pts=pts+(centre,)
    for i in range(0, len(pts)-1):
        if pts[i-1] is None or pts[i] is None:
            continue
        cv2.line(frame,pts[i],pts[i+1],(0, 255, 255),2)
    if cordinates():
                break
    else :
        continue
cap.release()
cv2.destroyAllWindows()

    
    
   
