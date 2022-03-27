import cv2
from tracker2 import *
import numpy as np
#import urllib.request
import serial
import pyrebase
from datetime import datetime
from time import sleep
import os
ser = serial.Serial('COM6',115200, timeout=0)
end = 0
check=0
n=-1
firebaseConfig = {
    "apiKey": "AIzaSyDoVk0muUI3eEVxsNwqOl-9sDkNN5qH2J0",
    "authDomain": "giaothong-599e4.firebaseapp.com",
    "databaseURL": "https:/ /giaothong-599e4-default-rtdb.firebaseio.com",
    "projectId": "giaothong-599e4",
    "storageBucket":"giaothong-599e4.appspot.com", 
    "serviceAccount":"serviceAccountKey.json"
}   
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()

#Creater Tracker Object
tracker = EuclideanDistTracker()
#url = 'http://172.20.10.5/cam-lo.jpg'
#cap = cv2.VideoCapture("file_tes.mp4")
os.chdir("C:/Users/Admin/Desktop/anh_vi_pham")
#cap = cv2.VideoCapture("http://10.65.167.254:8080/video")
#cap = cv2.VideoCapture(url)
#cap = cv2.VideoCapture('http://172.20.10.2/cam-lo.jpg')
f = 15
w = int(1000/(f-1))
#print(w)
f_width = 320
f_height = 240

gioi_han = 3
#giải thuật trừ nền
object_detector = cv2.bgsegm.createBackgroundSubtractorMOG()


#object_detector = cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=55)
#object_detector = cv2.createBackgroundSubtractorKNN()#(history=100,varThreshold=55)

#Tiền tố np là thư viện numpy.
# OpenCV sử dụng thư viện đó cho tất cả các hoạt động số, 
# bởi vì các mảng Python rất không hiệu quả cho các tính toán số
#KERNALS
# XÓI MÒN
kernalOp = np.ones((1,5),np.uint8)
#kernalOp2 = np.ones((5,5),np.uint8)
kernalCl = np.ones((5,5),np.uint8)
fgbg=cv2.bgsegm.createBackgroundSubtractorMOG()
#fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True)
#fgbg=cv2.createBackgroundSubtractorKNN()#detefctShadows=False)
kernal_e = np.ones((5,5),np.uint8)
#cap = cv2.VideoCapture("rtsp://admin:abcd1234@192.168.1.192/8000/tmpfs/auto.jpg",cv2.CAP_FFMPEG)
#cap = cv2.VideoCapture("rtsp://admin:abcd1234@192.168.1.192/cgi-bin/mjpg/video.cgi?&subtype=1",cv2.CAP_FFMPEG)
#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap = cv2.VideoCapture('rtsp://admin:abcd1234@192.168.0.109/8000',cv2.CAP_FFMPEG)

#cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FPS,20)
while True:
    #cap = cv2.VideoCapture("rtsp://admin:abcd1234@192.168.1.192/8000",cv2.CAP_DSHOW)
    #cap.set(cv2.CAP_PROP_FPS,30)
    #cap = cv2.VideoCapture("rtsp://admin:abcd1234@192.168.1.192/8000")#,cv2.CAP_FFMPEG)
    #cap = cv2.VideoCapture('http://172.20.10.5/cam-lo.jpg')
    ####cap = cv2.VideoCapture('http://192.168.0.101/cam-lo.jpg',cv2.CAP_FFMPEG)
    #cap = cv2.VideoCapture('http://192.168.0.105/')
    ret,frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    #frame = cv2.resize(frame, ( f_width, f_height))
    height,width,_ = frame.shape

    #Extract ROI
    #roi = frame[50:540,200:960]

    #MASKING METHOD 1  // pp đeo mặt nạ
    #mask = object_detector.apply(frame)
    #_, mask = cv2.threshold(mask, 200, 255, cv2.THRESH_BINARY)#chuyen sang anh den trang, neu mau >200 thi chuyen thanh trang

    #DIFFERENT MASKING METHOD 2 -> This is used  //PHƯƠNG PHÁP ĐẮP MẶT NẠ KHÁC NHAU
    fgmask = fgbg.apply(frame)
    #ret, imBin = cv2.threshold(fgmask, 150, 255, cv2.THRESH_BINARY)
    ret, imBin = cv2.threshold(fgmask, 100, 255, cv2.THRESH_BINARY)
    #Hàm sử dụng là threshold , tham số đầu tiên là 1 ảnh xám, tham số thứ 2 là giá trị ngưỡng, tham số thứ 3 maxval là giá trị được gán nếu giá pixel lớn hơn giá trị ngưỡng, tham số thứ 4 là loại phân ngưỡng. Tùy theo các loại phân ngưỡng mà pixel được gán giá trị khác nhau:

    '''THRESH_BINARY
    Nếu giá trị pixel lớn hơn ngưỡng thì gán bằng maxval
    Ngược lại bằng gán bằng 0
    THRESH_BINARY_INV
    Nếu giá trị pixel lớn hơn ngưỡng thì gán bằng 0
    Ngược lại bằng gán bằng maxval
    THRESH_TRUNC
    Nếu giá trị pixel lớn hơn ngưỡng thì gán giá trị bằng ngưỡng
    Ngược lại giữ nguyên giá trị
    THRESH_TOZERO
    Nếu giá trị pixel lớn hơn ngưỡng thì giữ nguyên giá trị
    Ngược lại gán bằng 0
    THRESH_TOZERO_INV
    Nếu giá trị pixel lớn hơn ngưỡng thì gán giá trị bằng 0
    Ngược lại giữ nguyên'''
    '''
    '''
    mask1 = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernalOp)#mở // loại bỏ điểm nhỏ
    mask2 = cv2.morphologyEx(mask1, cv2.MORPH_CLOSE, kernalCl)#đóng // làm đầy các điểm đen trong vùng trắng    
    e_img = cv2.erode(mask2, kernal_e)#erode nhr sẽ làm xói mòn
                                    #kernel: Một yếu tố cấu trúc được sử dụng để xói mòn.
                                    # Nếu phần tử = Mat(), một phần tử cấu trúc hình chữ nhật 3 x 3 được sử dụng.
                                    # Kernel có thể được tạo bằng cách sử dụng getStructuringElement.
                                    #https://www.geeksforgeeks.org/python-opencv-cv2-erode-method/
    ##contours,_ = cv2.findContours(imBin,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)   
    contours,_ = cv2.findContours(e_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #Xem, có ba đối số trong hàm cv.findContours()
    #thứ nhất là hình ảnh nguồn, thứ hai là chế độ truy xuất đường viền
    # thứ ba là phương pháp xấp xỉ đường viền. Và nó xuất ra các đường viền và hệ thống phân cấp.
    # Contours là một danh sách Python của tất cả các đường viền trong hình ảnh.
    # Mỗi đường viền riêng lẻ là một mảng Numpy (x,y) tọa độ của các điểm ranh giới của đối tượng.
    detections = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        #Khu vực đường viền được đưa ra bởi chức năng cv.contourArea() hoặc từ những khoảnh khắc, M ['m00']
        #Chức năng tính toán một khu vực đường viền
        # Tương tự như khoảnh khắc, khu vực này được tính bằng công thức Green
        # Do đó, diện tích trả về và số pixel không bằng không
        #THRESHOLD
        
        if area > 1400:
            x,y,w,h = cv2.boundingRect(cnt) #ve HCN
            if w > 4 :
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3) #ve HCN
                detections.append([x,y,w,h])
                # append thêm phần tử của danh sách vào một mảng

    #Object Tracking
    boxes_ids = tracker.update(detections)
    for box_id in boxes_ids:
        x,y,w,h,id = box_id
        vantoc=tracker.getsp(id)
        #time_dau=str(id)+' start '+str(tracker.s1[0,id])+' end '+str(tracker.s2[0,id])+'   '+(str(tracker.s2[0,id]-tracker.s1[0,id]))
        #print(time_dau)
        if(vantoc<gioi_han):
            cv2.putText(frame,str(id)+"   "+str(vantoc),(x,y-25), cv2.FONT_HERSHEY_PLAIN,1,(255,255,0),2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if vantoc>0 and id>n:
                send_vt =str(vantoc)+'\n'
                print(send_vt)        
                n=id
                ser.write(bytes(send_vt,'utf-8'))
                
        else:   # nếu quá tốc 
            if vantoc>0 and id>n:
                cv2.putText(frame,str(id)+ "   "+str(tracker.getsp(id)),(x, y-25),cv2.FONT_HERSHEY_PLAIN, 1,(0, 0, 255),2)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 165, 255), 3) 
                duoi="xe"+str(id)+"vt"+str(vantoc)+".jpg"
                cv2.imwrite(duoi, frame) 
                send_vt =str(vantoc)+'\n'
                print(send_vt)        
                n=id
                ser.write(bytes(send_vt,'utf-8'))
                #storage.child(duoi).put(duoi)     
    #cv2.line(frame, (0, 275), (4600, 275), (0, 0, 255), 2)
    cv2.line(frame, (0, 220), (4600,220), (0, 0, 255), 2)

    cv2.line(frame, (0, 165), (4600, 165), (0, 0, 255), 2)
    #cv2.line(frame, (0, 220), (4600, 220), (0, 0, 255), 2)


    #cv2.imshow("Mask",mask2)
    #cv2.imshow("Erode", e_img)
    cv2.imshow("frame", frame)

    key = cv2.waitKey(1)
    if key==27:
        tracker.end()
        end=1
        break

if(end!=1):
    tracker.end()

cap.release()#phat hanh video
cv2.destroyAllWindows() #dong frame
