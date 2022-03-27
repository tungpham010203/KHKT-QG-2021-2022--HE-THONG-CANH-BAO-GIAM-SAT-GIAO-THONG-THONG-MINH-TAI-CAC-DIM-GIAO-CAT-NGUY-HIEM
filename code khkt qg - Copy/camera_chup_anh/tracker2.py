import cv2
import math
import time
import numpy as np
#limit = 80000 #M/S

class EuclideanDistTracker:
    def __init__(self):
        # Lưu trữ vị trí trung tâm của các đối tượng
        self.center_points = {} # điểm trung tâm

        self.id_count = 0
        #self.start = 0
        #self.stop = 0
        #self.et=0
        self.s1 = np.zeros((1,2000)) ##Trả về một mảng mới của hình dạng và loại nhất định, chứa đầy số 0.
        self.s2 = np.zeros((1,2000))
        self.s = np.zeros((1,2000))
        #self.f = np.zeros(1000)
        #self.capf = np.zeros(1000)
        #self.count = 0
        #self.exceeded = 0


    def update(self, objects_rect):
        objects_bbs_ids = []

        # Lấy điểm trung tâm của đối tượng mới
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x+x + w) // 2
            cy = (y+y + h) // 2

            # KIỂM TRA XEM ĐỐI TƯỢNG ĐÃ ĐƯỢC PHÁT HIỆN CHƯA
            same_object_detected = False

            for id, pt in self.center_points.items():#self.center_points.items()==dict_items([(1, (104, 129))])
                #dist = math.hypot(cx - pt[0], cy - pt[1])
                #cx11 ='cx '+str(cy)+'\n'
                #cx12 ='pt '+str(pt[1])+'\n'
                #print(self.center_points.items())
                #print(cx11+'  '+cx12)

                if abs(y - pt[1])<50 or abs(cx-pt[0])<50:
                    #self.center_points[id] = (cx, cy)     #update pt[0],pt[1]
                    self.center_points[id] = (x, y)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True

                    #START TIMER
                    if (220>= y and self.s1[0,id]==0 and self.s2[0,id]==0):
                        self.s1[0,id] = time.time()

                    #STOP TIMER and FIND DIFFERENCE
                    if (165>= y and self.s2[0,id]==0) and self.s1[0,id]>0:
                        self.s2[0,id] = time.time()
                        self.s[0,id] = self.s2[0,id] - self.s1[0,id]
                        

                    #CAPTURE FLAG
                    #if (y<155):
                    #    self.f[id]=1


            # PHÁT HIỆN ĐỐI TƯỢNG MỚI
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1
                self.s[0,self.id_count]=0
                self.s1[0,self.id_count]=0
                self.s2[0,self.id_count]=0

        # ĐĂNG ID MỚI cho ĐỐI TƯỢNG
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        self.center_points = new_center_points.copy()
        return objects_bbs_ids

    # velocity
    def getsp(self,id):
        if (self.s[0,id]>0):
            s = (0.83/ self.s[0, id])*3.6  #km/h
        else:
            s = 0

        return int(s)
