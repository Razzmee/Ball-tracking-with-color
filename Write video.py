import numpy as np
import cv2
import time


frame_num = 0
frame_count = 0
sec = 0
capture = 1  # flag to save only initial frame 

ball_color = {"yellow":((20, 100, 100),(30, 255, 255)),
              "white":((0, 0, 211),(180, 30, 255)),
              "Green":((30, 50, 50),(80, 255, 255)),
              "RED":((0, 80, 150),(20, 255, 255)) }


quardent_region = {"1":((0,539),(0,560)),
                   "2":((539,1080),(0,560)),
                   "3":((539,1080),(560,1080)),
                   "4":((0,539),(539,1080))}

ball_info={ "1":{"previous_state":"Exit ","current_state":"Exit ","time":" ","color":" "},
            "2":{"previous_state":"Exit ","current_state":"Exit","time":" ","color":" "},
            "3":{"previous_state":"Exit ","current_state":"Exit","time":" ","color":" "},
            "4":{"previous_state":"Exit ","current_state":"Exit","time":" ","color":" "}
          }

video_cap = cv2.VideoCapture("rcrop_video.mp4")

frames = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
fps = video_cap.get(cv2.CAP_PROP_FPS)
seconds = round(frames / fps)

video_output_file_name = "result_video.mp4"
width = 1080
height= 1080
fps_write = 30 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_out = cv2.VideoWriter( video_output_file_name, fourcc, fps_write, (width, height) )

font = cv2.FONT_HERSHEY_SIMPLEX
cv2.namedWindow("Window", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Window", 720, 640)

def find_quardent(quardent_region,x,y):
    """    
    Determine the quadrant in which the given ball is located.

    Args:
    quardent_region: A dictionary containing the (x, y) coordinates of each quardent.
    x,y : center of ball
    
    Returns:
    str: The quadrant number (1, 2, 3, or 4) in which the ball is located.
    """

    for q,(xd,yd) in quardent_region.items():
        if x in range(xd[0],xd[1]) and y in range(yd[0],yd[1]):
            return q
        

            
def find_color(ball_color,crop_img):
    
    """
    Determine the color of the given ball.
    
    Args:
    ball_color : A dictionary representing the color of the ball.
    crop_img   : cropped region of the ball.
    
    Returns:
    str: The color of the ball.
    
    """
    
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
    
        """
        Determine the center coordinates of the given ball.
        
        Args:
        frame(array): A array contain cuurent frame of the video.
        
        Returns:
        bbox(list): A list containing the (x, y) coordinates of the center of 
                    the ball and if there is no ball present then it return None value. 
                    
        """
        
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
                
                
                bbox.append([(bx,by,bh,bw),color])
         
            return (bbox)
        else:
            
            return None
        
def check_quardent(frame, init_frame):
    """
    Determine the type of entry or exit.
    
    Args:
    frame(array): An array containing the current frame.
    init_frame(array): An array containing the initial frame to compare with 
                       current frame.
    
    Returns:
    update the dictionary Ball_info in which it's contain current state ,previous 
    state ,ball color  and time in which ball is enter or exit

    """
    frame  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    first_quard_f = frame[0:0+560,0:0+539]          # divide quardent region
    sec_quard_f   = frame[0:0+560,539:539+539]
    third_quard_f = frame[560:560+539,539:539+539] 
    fourth_quard_f = frame[560:560+539,0:0+539]
    current_frame = [first_quard_f,sec_quard_f,third_quard_f,fourth_quard_f] # add al frame
    
   
    
    for i in ball_info.keys():

        h, w = init_frame[int(i)-1].shape
        diff = cv2.subtract(init_frame[int(i)-1], current_frame[int(i)-1])
        err = np.sum(diff**2)
        mse = err/(float(h*w))
        
        if mse < 5 :
            ball_info[i]["current_state"] = "Exit"
        else:
            ball_info[i]["current_state"] = "Enter"


    



file = open("Information.txt","w")
file.write("TIME|Quardent Num|Ball Colour|Event Type \n")

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

            
            for i in range(len(result)):
                bbox,color = result[i]
                (bx,by,bh,bw) = bbox
                q = find_quardent(quardent_region, bx, by)
                
                
                if frame_num==30:
                    check_quardent(frame,comb_iframe) # update each quardent info
                    ball_info[q]["color"]=color
                    
                    

                cv2.line(frame,(539,1050),(539,10),(0,255,0),5) # Drawing y Axis
                cv2.line(frame,(0,560),(1050,560),(0,255,0),6)  # Drawing x Axis
                frame_time = "FPS: "+str(frame_num)+"TIME: " +str(sec)
                cv2.putText(frame,frame_time,(100,100),font,1,(0,255,0),2, cv2.LINE_AA)
                cv2.putText(frame,str(q)+" " +str(color),(bx,by),font,1,(0,255,0),2, cv2.LINE_AA)
                
                cv2.rectangle(frame,(bx,by),(bh,bw),(0,255,0),2)
                
                
            for i in ball_info.keys():
                ball_info[i]["time"]= sec
                if ball_info[i]["previous_state"] != ball_info[i]["current_state"] and ball_info[i]["color"] != ' ':
                    if ball_info[i]["current_state"]=="Enter":
                        
                        color = ball_info[i]["color"]
                        x=quardent_region[i][0][0]
                        y=quardent_region[i][1][0]
                        
                        cv2.putText(frame,str(color)+"Ball Entered at" + str(sec),(x,y),font,1,(0,255,0),2, cv2.LINE_AA)
                        file.write(str(ball_info[i]["time"])+"\t"+ i +"\t\t" + color + "\t Ball Enter\n")
                   
                    else:
                        color = ball_info[i]["color"]
                        x=quardent_region[i][0][0]
                        y=quardent_region[i][1][0]
                        
                        cv2.putText(frame,str(color)+"Ball Exit at" + str(sec),(x,y),font,1,(0,255,0),2, cv2.LINE_AA)
                        file.write(str(ball_info[i]["time"])+"\t"+i+"\t\t"+color+"\t Ball Exit\n")
                   
                    ball_info[i]["previous_state"] = ball_info[i]["current_state"]
                    
            video_out.write(frame)       
            cv2.imshow("Window",frame)
            #time.sleep(1) 
                
            
                
                    
              
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
file.close()
video_cap.release()
video_out.release()
cv2.destroyAllWindows()

