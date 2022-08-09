import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
from time import sleep

# PI Pin set up for the movement of the Robot
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)

def forward():
    GPIO.cleanup()
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(16, GPIO.HIGH)
   

    
def LEFT(x):
    GPIO.cleanup()
    GPIO.output(15, GPIO.HIGH)
    GPIO.output(16, GPIO.HIGH)
    sleep(x)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)

def RIGHT(x):
    GPIO.cleanup()
    GPIO.output(13, GPIO.HIGH)
    GPIO.output(18, GPIO.HIGH)
    sleep(x)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(18, GPIO.LOW)

def STOP(x):
    GPIO.cleanup()
    GPIO.output(13, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
    sleep(x)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)

#capturing video through webcam
cap=cv2.VideoCapture(0)


while(1):
    _, img = cap.read()
    forward()
    #converting frame(img i.e BGR) to HSV (hue-saturation-value)

    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

    #definig the range of red color
    red_lower=np.array([175,120,120],np.uint8)
    red_upper=np.array([220,255,255],np.uint8)

    #defining the Range of Blue color
    blue_lower=np.array([99,115,150],np.uint8)
    blue_upper=np.array([110,255,255],np.uint8)

    #defining the Range of yellow color
    yellow_lower=np.array([22,60,200],np.uint8)
    yellow_upper=np.array([60,255,255],np.uint8)

    #finding the range of red,blue and yellow color in the image
    red=cv2.inRange(hsv, red_lower, red_upper)
    blue=cv2.inRange(hsv,blue_lower,blue_upper)
    yellow=cv2.inRange(hsv,yellow_lower,yellow_upper)

    #Morphological transformation, Dilation
    kernal = np.ones((5 ,5), "uint8")

    red=cv2.dilate(red, kernal)
    res=cv2.bitwise_and(img, img, mask = red)

    blue=cv2.dilate(blue,kernal)
    res1=cv2.bitwise_and(img, img, mask = blue)

    yellow=cv2.dilate(yellow,kernal)
    res2=cv2.bitwise_and(img, img, mask = yellow)
    
    b=1
    while(b==1):
        
        #Tracking the Red Color
        (_,contours,hierarchy)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        a=0
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area>300):
                x,y,w,h = cv2.boundingRect(contour)
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
                cv2.putText(img,"RED color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255))
                a=1
                b=0
            else:
                a=0
                    
                        

        #Tracking the Blue Color
        (_,contours,hierarchy)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area>300):
                x,y,w,h = cv2.boundingRect(contour)
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.putText(img,"Blue color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0))
                a=2
                b=0
            else:
                a=0

        #Tracking the yellow Color
        (_,contours,hierarchy)=cv2.findContours(yellow,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for pic, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if(area>300):
                x,y,w,h = cv2.boundingRect(contour)
                img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(img,"yellow  color",(x,y),cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0))
                a=3
                b=0
            else:
                a=0
                 


        #cv2.imshow("Redcolour",red)
        cv2.imshow("Color Tracking",img)
        if (a==1):
            print ("LEFT")
            LEFT(10)
            time.sleep(9)
        elif(a==2):
            print("RIGHT")
            RIGHT(10)
            time.sleep(9)
        elif(a==3):
            print("STOP")
            STOP(10)
            time.sleep(9)
        if (b==0):
            break
        break
    sleep(5)
    #cv2.imshow("red",res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        GPIO.cleanup()
        cap.release()
        cv2.destroyAllWindows()
        break 
                
                






    
