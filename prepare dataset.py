import numpy as np
import cv2
import time
import csv
import os


#-----------------------------------------------

entry_data = []
initiater_list = []
target_dict = {}
frame_num = 0
frame_count = 0
sec = 0
capture = 1

ball_color = {"yellow":((20, 100, 100),(30, 255, 255)),
              "white":((0, 0, 211),(180, 30, 255)),
              "Green":((30, 50, 50),(80, 255, 255)),
              "RED":((0, 80, 150),(20, 255, 255)) }


quardent = {"first":((0,539),(0,560)),
         "second":((539,1080),(0,560)),
         "third":((539,1080),(560,1080)),
         "fourth":((0,539),(539,1080))}


#--------------------------------------------------

video_cap = cv2.VideoCapture("rcrop_video.mp4")

frames = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = video_cap.get(cv2.CAP_PROP_FPS)
seconds = round(frames / fps)



        
def find_loc(frame):
        bbox = []
        frame_copy = frame.copy()

        

        gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray_img = cv2.medianBlur(gray_img, 5)
        
        
        
        circles = cv2.HoughCircles(gray_img,cv2.HOUGH_GRADIENT,1,120,
                                       param1=100,param2=30,minRadius=45,maxRadius=70)
            
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for x,y,r in circles[0,:]:

                bbox.append([x,y,r])
         
            return bbox
        else:
            
            return None
        

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.namedWindow("Window", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Window", 720, 640)

data = []
idx = 0
while True:

    ret,frame = video_cap.read()
    
    img_name = "img"
    if ret:
        frame_copy = frame.copy()   

        result = find_loc(frame)
        
        if result is not None:
            bbox = result
            
            for (bx,by,r) in bbox:
                img_name = "img"+str(idx)+str(".jpg")
                data.append([str(bx), str(by), str(r), img_name ])
                
                cv2.imwrite(os.path.join("data",img_name),frame)
                
                cv2.imshow("Window",frame)
                
                idx+=1
          
        if cv2.waitKey(1)==27:
            break
        
        # Utility Counters
        if frame_num==30:
            frame_num = 0 
            sec = sec+1
        frame_count +=1
        frame_num = frame_num+1

# Break the loop

    else:
        break
    
file = open("dataset.csv","w")
writer = csv.writer(file)
fileds = ["x_vlaue","y_value","radius"]
writer.writerow(fileds)
for row in data:
    writer.writerow([value.strip() for value in row])
file.close()

video_cap.release()
cv2.destroyAllWindows()

