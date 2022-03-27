import cv2
from tracker2 import *
import numpy as np
import urllib.request
import serial
import pyrebase
from datetime import datetime
from time import sleep
import os
ser = serial.Serial('COM6',115200, timeout=0)
end = 0
check=0
n=0
firebaseConfig = {
    "apiKey": "AIzaSyDoVk0muUI3eEVxsNwqOl-9sDkNN5qH2J0",
    "authDomain": "giaothong-599e4.firebaseapp.com",
    "databaseURL": "https://giaothong-599e4-default-rtdb.firebaseio.com",
    "projectId": "giaothong-599e4",
    "storageBucket":"giaothong-599e4.appspot.com", 
    "serviceAccount":"serviceAccountKey.json"
}   
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

#Creater Tracker Object
tracker = EuclideanDistTracker()

os.chdir("C:/Users/Admin/Desktop/anh_vi_pham")

f = 55
w = int(1000/(f-1))
#print(w)
f_width = 320
f_height = 240
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
gioi_han = 50
#Object Detection
object_detector = cv2.createBackgroundSubtractorMOG2(history=25,varThreshold=55)
#100,5

#KERNALS
kernalOp = np.ones((3,3),np.uint8)
kernalOp2 = np.ones((5,5),np.uint8)
kernalCl = np.ones((5,5),np.uint8)
#fgbg=cv2.bgsegm.createBackgroundSubtractorMOG()#detefctShadows=True)
fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True)
kernal_e = np.ones((5,5),np.uint8)

while True:
    #cap = cv2.VideoCapture('http://172.20.10.5/cam-lo.jpg')
    #cap = cv2.VideoCapture('http://192.168.0.101/cam-lo.jpg',cv2.CAP_FFMPEG)
    #cap = cv2.VideoCapture('http://192.168.0.105/')
    ret,frame = cap.read()
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    frame = cv2.resize(frame, ( f_width, f_height))
    height,width,_ = frame.shape

    #Extract ROI
    #roi = frame[50:540,200:960]

    #MASKING METHOD 1
    mask = object_detector.apply(frame)
    _, mask = cv2.threshold(mask, 250, 255, cv2.THRESH_BINARY)

    #DIFFERENT MASKING METHOD 2 -> This is used
    fgmask = fgbg.apply(frame)
    ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    mask1 = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)
    mask2 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernalCl)
    e_img = cv2.erode(mask2, kernal_e)
    
    contours,_ = cv2.findContours(e_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    ##contours,_ = cv2.findContours(imBin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    detections = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        #THRESHOLD
        if area > 600:
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
            detections.append([x,y,w,h])

    #Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x,y,w,h,id = box_id
        vantoc=tracker.getsp(id)
        #time_dau=str(id)+' start '+str(tracker.s1[0,id])+' end '+str(tracker.s2[0,id])+'   '+(str(tracker.s2[0,id]-tracker.s1[0,id]))
        #print(time_dau)
        if(vantoc<gioi_han):
            cv2.putText(frame,str(id)+" "+str(vantoc),(x,y-15), cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if vantoc>0 and id>n:
                send_vt =str(vantoc)+'\n'
                print(send_vt)        
                n=id
                ser.write(bytes(send_vt,'utf-8'))
                
        else:   # nếu quá tốc 
            if vantoc>0 and id>n:
                cv2.putText(frame,str(id)+ " "+str(tracker.getsp(id)),(x, y-15),cv2.FONT_HERSHEY_PLAIN, 1,(0, 0, 255),2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 3) 
                duoi="xe"+str(id)+"vt"+str(vantoc)+".jpg"
                cv2.imwrite(duoi, frame) 
                send_vt =str(vantoc)+'\n'
                print(send_vt)        
                n=id
                ser.write(bytes(send_vt,'utf-8'))
                #storage.child(duoi).put(duoi)     
    cv2.line(frame, (0, 80), (460, 80), (0, 0, 255), 2)
    cv2.line(frame, (0, 100), (460,100), (0, 0, 255), 2)

    cv2.line(frame, (0, 130), (460, 130), (0, 0, 255), 2)
    cv2.line(frame, (0, 150), (460, 150), (0, 0, 255), 2)


    #cv2.imshow("Mask",mask2)
    #cv2.imshow("Erode", e_img)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(w-5)
    if key==27:
        tracker.end()
        end=1
        break

if(end!=1):
    tracker.end()

cap.release()
cv2.destroyAllWindows()
