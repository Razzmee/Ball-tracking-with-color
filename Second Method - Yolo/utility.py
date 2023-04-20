import cv2
import numpy as np




def find_quardent(quardent_region,x,y):
    """    
    Determine the quadrant in which the given ball is located.

    Args:
    quardent_region: A dictionary containing the (x, y) coordinates of each quardent.
    x,y : center of ball
    
    Returns:
    str: The quadrant number (1, 2, 3, or 4) in which the ball is located.
    """
    x = int(x*2.59615384615)
    y = int(y*2.59615384615)
    for q,(xd,yd) in quardent_region.items():
        if x in range(xd[0],xd[1]) and y in range(yd[0],yd[1]):
            return q


def check_ball_state(frame, init_frame,ball_info):
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
        
        ih, iw = init_frame[int(i)-1].shape[:2]
    
        #ch,  cw= current_frame[int(i)-1].shape[:2]
    
        diff = cv2.subtract(init_frame[int(i)-1], current_frame[int(i)-1])
        err = np.sum(diff**2)
        mse = err/(float(ih*iw))
        
        if mse < 5 :
            ball_info[i]["current_state"] = 0
        else:
            ball_info[i]["current_state"] = 1
    
    return ball_info


def save_init_frame(frame):
        iframe = frame.copy()
        iframe = cv2.cvtColor(iframe,cv2.COLOR_BGR2GRAY)
        
        first_quard_f = iframe[0:0+560,0:0+539] 
        sec_quard_f   = iframe[0:0+560,539:539+539] 
        third_quard_f = iframe[560:560+539,539:539+539] 
        fourth_quard_f = iframe[560:560+539,0:0+539] 
        
        #Split all the 4 frame and make list
        
        comb_iframe = [first_quard_f,sec_quard_f,third_quard_f,fourth_quard_f]
        
        return comb_iframe
    

    
    

            