import numpy as np
import cv2
import time



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




def find_quardent(quard,x,y):
    
    for q,(xd,yd) in quard.items():
        if x in range(xd[0],xd[1]) and y in range(yd[0],yd[1]):
            return q
        

            
def find_color(ball_color,crop_img):
    hsv = cv2.cvtColor(crop_img,cv2.COLOR_BGR2HSV)
    
    max_sum = 0
    dominant_color = None
    for color, (lower, upper) in ball_color.items():
        mask = cv2.inRange(hsv, lower, upper)
        total_sum = sum(cv2.sumElems(mask)[:3])
        if total_sum > max_sum:
            max_sum = total_sum
            dominant_color = color

    return dominant_color
        
        
def find_loc(frame):
        colors = []
        bbox = []
        frame_copy = frame.copy()

        

        gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        gray_img = cv2.medianBlur(gray_img, 5)
        
        
        
        circles = cv2.HoughCircles(gray_img,cv2.HOUGH_GRADIENT,1,120,
                                       param1=100,param2=30,minRadius=45,maxRadius=70)
            
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for x,y,r in circles[0,:]:
                bx = x-int(r//1.5) 
                bh = x+int(r//1.5) 
                by = y-int(r//1.5) 
                bw = y+int(r//1.5)  
                
                crop_img = frame_copy[by:bw,bx:bh]       # crop the region of the ball
                color = find_color(ball_color,crop_img)  # detect the color of the region
                
                colors.append(color)
                bbox.append([bx,by,bh,bw])
         
            return (bbox,colors)
        else:
            
            return None
        
def check_quardent(frame, frame_list):
    occ_quard = []
    frame  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    first_quard_f = frame[0:0+560,0:0+539] 
    sec_quard_f   = frame[0:0+560,539:539+539]
    third_quard_f = frame[560:560+539,539:539+539] 
    fourth_quard_f = frame[560:560+539,0:0+539]
    merge_frame = [first_quard_f,sec_quard_f,third_quard_f,fourth_quard_f]
    for i in range(4):
        h, w = frame_list[i].shape
        diff = cv2.subtract(frame_list[i], merge_frame[i])
        err = np.sum(diff**2)
        mse = err/(float(h*w))
        if mse < 5 :
            occ_quard.append("False")
        else:
            occ_quard.append("True")
    return occ_quard


font = cv2.FONT_HERSHEY_SIMPLEX
cv2.namedWindow("Window", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Window", 720, 640)



while True:

    ret,frame = video_cap.read()
    
    if capture==1:  # save intial frame copy to check and compare quardent is empty or not 
        iframe = frame.copy()
        iframe = cv2.cvtColor(iframe,cv2.COLOR_BGR2GRAY)
        first_quard_f = iframe[0:0+560,0:0+539] #(x,y) = (0,0) & (w,h) = (539,560)
        sec_quard_f   = iframe[0:0+560,539:539+539] #(x,y)=(539,0)& (w,h) = (539.560)
        third_quard_f = iframe[560:560+539,539:539+539] #(x,y)=(539,560)&(w,h)=(539,520)
        fourth_quard_f = iframe[560:560+539,0:0+539] #(x,y)=(0,560)&(w,h)=(539,520)
        comb_iframe = [first_quard_f,sec_quard_f,third_quard_f,fourth_quard_f]
        capture = 0
    
    if ret:
        frame_copy = frame.copy()   

        result = find_loc(frame)
        
        if result is not None:
            bbox,colours_list = result
            
            idx = 0
            for (bx,by,bh,bw) in bbox:
                
           

                
                q = find_quardent(quardent, bx, by)
                color = colours_list[idx]
                if frame_num==30:
                    occ = check_quardent(frame,comb_iframe)
                    print(occ)

                
                
                cv2.line(frame,(539,1050),(539,10),(0,255,0),5) # Drawing y Axis
                cv2.line(frame,(0,560),(1050,560),(0,255,0),6)  # Drawing x Axis
                time = "FPS: "+str(frame_num)+"TIME: " +str(sec)
                cv2.putText(frame,time,(100,100),font,1,(0,255,0),2, cv2.LINE_AA)
                cv2.putText(frame,str(q)+" " +str(color),(bx,by),font,1,(0,255,0),2, cv2.LINE_AA)
                
                cv2.rectangle(frame,(bx,by),(bh,bw),(0,255,0),2)
                cv2.imshow("Window",frame)
                
            idx +=1
        if cv2.waitKey(1)==27:
            break
        
        # Utility Counters
        if frame_num==60:
            frame_num = 0 
            sec = sec+1
        frame_count +=1
        frame_num = frame_num+1

# Break the loop

    else:
        break

video_cap.release()
cv2.destroyAllWindows()

