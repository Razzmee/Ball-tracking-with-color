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
video_output_file_name = "test_crop_video.mp4"
width = 1080
height= 1080
fps_write = 30 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_out = cv2.VideoWriter( video_output_file_name, fourcc, fps_write, (width, height) )


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
        
    


font = cv2.FONT_HERSHEY_SIMPLEX
cv2.namedWindow("Window", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Window", 720, 640)

f = open("file.txt", "a")

while True:

    ret,frame = video_cap.read()
    
    if ret:
 

        result = find_loc(frame)  #detect ball location & ball colors
        
        if result is not None:
            bbox,colours_list = result
            
            
            idx = 0 
            for (bx,by,bh,bw) in bbox:
                
                color = colours_list[idx]

                
                q = find_quardent(quardent, bx, by) # find quardent value
  
                cv2.line(frame,(539,1050),(539,10),(0,255,0),5) # Drawing y Axis
                cv2.line(frame,(0,560),(1050,560),(0,255,0),6)  # Drawing x Axis
                time_str = "FPS: "+str(frame_num)+"TIME: " +str(sec)
                
                cv2.putText(frame,time_str,(100,100),font,
                            1,(0,255,0),2, cv2.LINE_AA)
                cv2.putText(frame,str(q)+" " +str(color),(bx,by),font,
                            1,(0,255,0),2, cv2.LINE_AA)
                
                cv2.rectangle(frame,(bx,by),(bh,bw),(0,255,0),2)
                video_out.write(frame)
                
                idx+=1
                if frame_num==5: # Write event data after 5 frames
                    f.write(str(color)+" "+str(q)+" "+str(sec))
                    f.write("\n")
    
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
f.close()
video_cap.release()
video_out.release()
cv2.destroyAllWindows()

