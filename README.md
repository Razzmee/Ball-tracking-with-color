# Assignment_AI_Associate
In this assignment 
Task:
Create a program using Computer Vision to track the movement of the balls of
different colors across various quadrants in the video provided. The program
should record the event of each ball entering and exiting each numbered
quadrant. The event data should be recorded in the below format.
Time, Quadrant Number, Ball Colour, Type (Entry or Exit)
Timestamp: consider start of the video as 0 seconds and compute timestamp
based on video duration.
The program should have provisions for feeding a new video and output should
be saved in the local hard disk. Details of which need to be shared at the time of
submission 

#Approach

Task 1: Video Pre-processing
Crop and rotate the video to remove unwanted background and align the frames for accurate ball tracking.

Task 2: Ball Detection
Develop a function that can detect the presence of balls in each frame of the video.
The function should be able to identify the ball's position.

Task 3: Ball Color Recognition
Develop a function that can recognize the color of each ball.
The function should be able to differentiate between different colors of balls and provide accurate result.

Task 4: Ball Position Tracking
Develop a function that can track the movement of each ball and calculate its position in each frame.
The function should be able to identify the quadrant in which the ball is located.

Task 5: Event Detection
Develop an function that can detect when a ball crosses its quadrant boundary.
The function should be able to identify the type of event (entry or exit) and the time at which it occurred.

Task 6: Data Storage and Export
Store the information gathered from the video analysis in a text file.
Write the processed video with the ball tracking information overlaid on the frames.



![demo](https://user-images.githubusercontent.com/29145107/229869880-e8ea7d0f-ca98-4acb-b1fa-1460d10125ae.png)


All tasks were completed successfully, but there was a slight loss in accuracy during ball detection. Therefore, I am to build an object detection model that can more smoothly detect and recognize the balls to improve accuracy.
