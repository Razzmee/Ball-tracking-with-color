In this approach, I utilized various object detection algorithms, including YOLOv3, YOLOv4, YOLOv5, and YOLOv8. After testing each algorithm, YOLOv8 produced the most accurate results.

Furthermore, to improve the accuracy of object tracking, I integrated various trackers, starting with OpenCV legacy trackers and eventually moving on to CAMSHIFT, SORT, and DeepSort trackers. However, the method used for quadrant information remains the same in this code(as used in first method).

![image](https://user-images.githubusercontent.com/29145107/233530046-2c5693d2-fd8c-4a12-823e-0ab02bd5ab52.png)

inferenceCQ.py file is used to detect ball and show result.

Write video result.py file is used to write result in video and text file.

utility.py file is used for utility function like find quaerdent & update ball inforamtion.

Information.txt file contain the required file.





