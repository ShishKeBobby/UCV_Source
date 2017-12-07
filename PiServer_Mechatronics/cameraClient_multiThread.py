import numpy as np
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import imutils
import cv2
import testClient
import time

diluteKernel = np.ones((3,3), np.uint8)
dilateKernel = np.ones((7,7), np.uint8)
lower_blue = np.array([160,90,70])
upper_blue = np.array([180,255,255])

myClient = testClient.writeClient()
vs = WebcamVideoStream(src=0).start()

while(1):
    frame = vs.read()
    try:
        b,g,r = cv2.split(frame)
    except Exception as e:
        print(e)
	
    cv2.circle(frame,(400,200), 70, (0,255,0), 1)
    print("1")
    if(vs.grabbed):
	time.sleep(.1)
        print("2")
        frame = cv2.resize(frame, (0,0), fx = 1, fy = 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        frame = cv2.inRange(frame, lower_blue, upper_blue)
        frame = cv2.erode(frame, diluteKernel, iterations=2)
        frame= cv2.dilate(frame, dilateKernel, iterations=1)
        cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        if len(cnts)>0:
            print("3")
            c = max(cnts,key=cv2.contourArea)
            ((x,y),radius) = cv2.minEnclosingCircle(c)
            M=cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            print(radius)
            try:
                if radius > 20:
                    #money maker here
                    #setImgDist and setImgHeading are the commands of interest
                    myClient.setMessage('setImgDist',str(radius)+","+str(x))
                    print("x =",x," r=",radius)
                    #print(x)
                    myClient.setMessage('setImgHeading',str(x))
                    #y shouldn't really matter as height of the follow target would indicate terrain problems which
                    #is outside the scope of this project

                else:
                    #zero out heading and distance if the image isn't reliable (radius < 20 pixels)
                    #this will be the 'trigger' for the GPS to take over navigation
                    myClient.setMessage('setImgDist',str(0)+","+str(0))
                    myClient.setMessage('setImgHeading',str(0))
                    print("go-to gps")
            except Exception as e:
                print(e)
        else:
            print("no contours")
            myClient.setMessage('setImgDist',str(0)+","+str(0))
            myClient.setMessage('setImgHeading',str(0))   
    else:
        print("no frame")
        myClient.setMessage('setImgDist',str(0)+","+str(0))
        myClient.setMessage('setImgHeading',str(0))                

        
cv2.destroyAllWindows()
vs.stop()

#instatiate TCP write client
#myClient = testClient.writeClient()
#cap = cv2.VideoCapture(0)

#ret, frame = cap.read()
#if not cap.isOpened():
#    count = 0
#    while not cap.isOpened():
#        print("Waiting on camera")
#        sleep(1)
#        count = count + 1
#        if count > 2:
#            print ("Dumping old ref and reinitializing")
#            cap.release()
#            cv2.destroyAllWindows()
#            cap = cv2.VideoCapture(0)

#diluteKernel = np.ones((3,3), np.uint8)
#dilateKernel = np.ones((7,7), np.uint8)
#lower_blue = np.array([155,100,100])
#upper_blue = np.array([180,255,255])


#while(cap.isOpened()):
#    ret, frame = cap.read()
#    b,g,r = cv2.split(frame)
#    cv2.circle(frame,(400,200), 70, (0,255,0), 1)
#    if ret: #check !
#        frame = cv2.resize(frame, (0,0), fx = 0.5, fy = 0.5)
#        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
#        frame = cv2.inRange(frame, lower_blue, upper_blue)
#        frame = cv2.erode(frame, diluteKernel, iterations=2)
#        frame= cv2.dilate(frame, dilateKernel, iterations=1)
#        cnts = cv2.findContours(frame.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
#        if len(cnts)>0:
#            c = max(cnts,key=cv2.contourArea)
#            ((x,y),radius) = cv2.minEnclosingCircle(c)
#            M=cv2.moments(c)
#            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
#            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
#            cv2.circle(frame, center, 5, (0, 0, 255), -1)
#            try:
#                if radius > 20:
#                    #money maker here
#                    #setImgDist and setImgHeading are the commands of interest
#                    myClient.setMessage('setImgDist',str(radius))
#                    #print("x =",x," y=",y," r=",radius)
#                    print(x)
#                    myClient.setMessage('setImgHeading',str(x))
#                    #y shouldn't really matter as height of the follow target would indicate terrain problems which
                    #is outside the scope of this project

#                else:
                    #zero out heading and distance if the image isn't reliable (radius < 20 pixels)
                    #this will be the 'trigger' for the GPS to take over navigation
#                    myClient.setMessage('setImgDist',str(0))
#                    myClient.setMessage('setImgHeading',str(0))
#                    print("go-to gps")
#            except Exception as e:
#                pass
                #print(e)
        #cv2.imshow('outVideo',frame)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
    
print("done")
#cap.release()
#cv2.destroyAllWindows()
