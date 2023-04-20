import numpy as np
import cv2
from utility import find_quardent,check_ball_state,save_init_frame
#import time
# Constants.
INPUT_WIDTH = 416
INPUT_HEIGHT = 416
SCORE_THRESHOLD = 0.45
NMS_THRESHOLD = 0.70
CONFIDENCE_THRESHOLD = 0.60
 
# Text parameters.
FONT_FACE = cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.9
THICKNESS = 3

# Colors.
WHITE  = (255,255,255)

quardent_region = {"1":((0,539),(0,560)),
                   "2":((539,1080),(0,560)),
                   "3":((539,1080),(560,1080)),
                   "4":((0,539),(539,1080))
                   }


ball_info={ "1":{"previous_state":0,"current_state":0,"time":" ","color":" "},
            "2":{"previous_state":0,"current_state":0,"time":" ","color":" "},
            "3":{"previous_state":0,"current_state":0,"time":" ","color":" "},
            "4":{"previous_state":0,"current_state":0,"time":" ","color":" "}
          }

data_ball = [] #Store all information

init_frame_save = 1
global sec,frame_num,frame_count
frame_num =0
frame_count=0
sec =0
def draw_label(im, label, x, y):
    """Draw text onto image at location."""
    # Get text size.
    text_size = cv2.getTextSize(label, FONT_FACE, FONT_SCALE, THICKNESS)
    dim,baseline = text_size[0],text_size[1]
    cv2.rectangle(im, (x,y), (x + dim[0], y + dim[1] + baseline), (0,0,0), cv2.FILLED);
    # Display text inside the rectangle.
    cv2.putText(im, label, (x, y  + dim[1]), FONT_FACE, FONT_SCALE,WHITE , THICKNESS, cv2.LINE_AA)

def pre_process(input_image, net):
      # Create a 4D blob from a frame.
      blob = cv2.dnn.blobFromImage(input_image, 1/255,  (INPUT_WIDTH, INPUT_HEIGHT), [0,0,0], 1, crop=False)
 
      # Sets the input to the network.
      net.setInput(blob)
 
      # Run the forward pass to get output of the output layers.
      outputs = net.forward(net.getUnconnectedOutLayersNames())
      return outputs
  
def post_process(input_image, outputs,classes,init_frame,ball_info):
    bbox=[]
    class_id=[]
    confidences=[]
    factor =  2.59615384615  # value to convert pixel value from frame size 416 to 1080
    outputs = np.transpose(outputs[0][0]) # shape (8, 3549) to shape (3549,8)
    
    for row in outputs: 
        box = row[:4]          #starting 4th column x,y,w,h.
        classes_conf = row[4:] #last 4th column confidence value for each class.
        
        for i in range(4):
            if classes_conf[i] >= SCORE_THRESHOLD:  # filter out low score value prediction
                class_id.append(classes[i])
                confidences.append(classes_conf[i])
                bbox.append(box)
                
    indices = cv2.dnn.NMSBoxes(bbox, confidences,CONFIDENCE_THRESHOLD, NMS_THRESHOLD)       
    
    for i in indices:
        box = bbox[i]
        Color = class_id[i]
        
        center_x,center_y,w,h = int(box[0]),int(box[1]),int(box[2]),int(box[3])
        x1 = int((center_x - w//2)*factor) 
        y1 = int((center_y - h//2)*factor)
        x2 = int((center_x + w//2)*factor)
        y2 = int((center_y + h//2)*factor)
       
        cv2.rectangle(input_image, (x1, y1), (x2, y2),(0,255,0), 2)
        
        quardent_num = find_quardent(quardent_region,center_x,center_y)
        
        ball_info[quardent_num]["color"] =Color
        ball_info[quardent_num]["points"] = (center_x,center_y)
        ball_info = check_ball_state(input_image, init_frame,ball_info)
        
        label = "Color:{} Q:{}".format(Color,quardent_num)
        draw_label(input_image, label, x1, y1)
        
    if frame_num==30:
  
        ball_info = check_ball_state(input_image, init_frame,ball_info) #update quardent state and update ball current state 
        
        for j in ball_info.keys():
           
            if ball_info[j]["previous_state"] != ball_info[j]["current_state"] and ball_info[j]["color"]!=" ":
                
                if ball_info[j]["current_state"]==1: #Enter
                    x=quardent_region[j][0][0]
                    y=quardent_region[j][1][0]
                    
                    print("ball enter ",ball_info[j]["color"])
                    data_ball.append([sec,j,ball_info[j]["color"],"Entry"])
                    cv2.putText(frame,str(Color)+"Ball Entered at" + str(sec),(x,y),FONT_FACE,1,(0,255,0),2, cv2.LINE_AA)
                   
               
                else:                                  #Exit
                    
                    x=quardent_region[j][0][0]
                    y=quardent_region[j][1][0]
                    
                    print("ball exit ",ball_info[j]["color"])
                    data_ball.append([sec,j,ball_info[j]["color"],"Entry"])
                    cv2.putText(frame,str(Color)+"Ball Exit at" + str(sec),(x,y),FONT_FACE,1,(0,255,0),2, cv2.LINE_AA)
                ball_info[j]["previous_state"]=ball_info[j]["current_state"]
                
            
              
                
                
    return input_image



video_cap = cv2.VideoCapture("C:/Users/sanje/Projects/Assign_ball_track/rcrop_video.mp4")
modelWeights = "C:/Users/sanje/Projects/Assign_ball_track/bestnde50.onnx"
net = cv2.dnn.readNet(modelWeights)

# Load class names.
classesFile = "C:/Users/sanje/Projects/Assign_ball_track/dark.names"
classes = None
with open(classesFile, 'rt') as f:
      classes = f.read().rstrip('\n').split('\n')
      
cv2.namedWindow("Opt_window", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Opt_window", 720, 640)


file_data = open("info.txt", "a")
file_data.write("Time|Quardent|Color|Type")
# Load image.
while True:
    ret,frame = video_cap.read()
    
    if ret:
        
              if init_frame_save:
                  init_frame = save_init_frame(frame) #save initial frame
                  init_frame_save=0
              
              frame_416 = cv2.resize(frame,(416,416))
              detections = pre_process(frame_416, net)
              img = post_process(frame, detections,classes,init_frame,ball_info) #perform NMS and Draw Labels
              
              
              if img is not None:
                  cv2.imshow('Opt_window', img)
                  #time.sleep(0.2)
    
                  
              if cv2.waitKey(1)==27:
                break
              # Utility Counters
              if frame_num==30:
                  frame_num = 0 
                  sec = sec+1
              frame_count +=1
              frame_num = frame_num+1
              
    else:
        break
            
for time,quard,color,types in data_ball: #Write txt file
    f.write(str(time)+" "+str(quard)+" "+color+" "+types)
    f.write("\n") 
    
video_cap.release()
cv2.destroyAllWindows()

