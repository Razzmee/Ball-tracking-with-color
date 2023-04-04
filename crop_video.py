import numpy as np
import cv2

video_cap = cv2.VideoCapture("video.mp4")
ret,frame = video_cap.read()

if video_cap.isOpened():
    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height= int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps   = int(video_cap.get(cv2.CAP_PROP_FPS))

else:
    print("Video could not opened")
    sys.exit()

print(f"width:{width}\nheight:{height}\nFPS:{fps} ")


video_output_file_name = "test_crop_video.mp4"
width = 1080
height= 1080
fps_write = 30 
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video_out = cv2.VideoWriter( video_output_file_name, fourcc, fps_write, (width, height) )

while(True):
    ret, frame = video_cap.read()
  
    if ret == True:
        crop_frame = frame[:,700:1780]
        crop_frame = cv2.rotate(crop_frame,cv2.ROTATE_180)
        # Write the frame into the file
        video_out.write(crop_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
  
    # Break the loop
    else:
        break
        
video_cap.release()
video_out.release()


