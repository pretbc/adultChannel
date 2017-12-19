#Motion detector

import argparse
import datetime
import imutils
import time
import cv2
import subprocess
import os
from random import randint

"""
def motionDetection(slot=0 , key=''):
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
        args = vars(ap.parse_args())
        camera = cv2.VideoCapture(slot)
        time.sleep(0.25)
        # initialize the first frame in the video stream
        firstFrame = None

        # loop over the frames of the video
        while True:
                # grab the current frame and initialize the occupied/unoccupied
                # text
                (grabbed, frame) = camera.read()
                text = "Unoccupied"
         
                # if the frame could not be grabbed, then we have reached the end
                # of the video
                if not grabbed:
                        break
         
                # resize the frame, convert it to grayscale, and blur it
                frame = imutils.resize(frame, width=500)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
         
                # if the first frame is None, initialize it
                if firstFrame is None:
                        firstFrame = gray
                        continue
                # compute the absolute difference between the current frame and
                # first frame
                frameDelta = cv2.absdiff(firstFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
         
                # dilate the thresholded image to fill in holes, then find contours
                # on thresholded image
                thresh = cv2.dilate(thresh, None, iterations=2)
                (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE) #CHAIN_
         
                # loop over the contours
                for c in cnts:
                        # if the contour is too small, ignore it
                        if cv2.contourArea(c) < args["min_area"]:
                                continue
         
                        # compute the bounding box for the contour, draw it on the frame,
                        # and update the text
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        text = "Occupied"


                # draw the text and timestamp on the frame
                cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
         
                # show the frame and record if the user presses a key
                cv2.imshow("Security Feed", frame)
                #cv2.imshow("Thresh", thresh)
                #cv2.imshow("Frame Delta", frameDelta)
                key = cv2.waitKey(1) & 0xFF
         
                # if the `q` key is pressed, break from the lop
                if key == 'q':
                        break
         
        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()
"""

def channel():
        subprocess.call(['irsend','SEND_ONCE','newtv','KEY_MENU'], shell=False)
        time.sleep(2)
        subprocess.call(['irsend','SEND_ONCE','newtv','KEY_BACK'], shell=False)
        time.sleep(2)
        subprocess.call(['irsend','SEND_ONCE','newtv','KEY_6'], shell=False)
        time.sleep(0.4)
        subprocess.call(['irsend','SEND_ONCE','newtv','KEY_9'], shell=False)
        time.sleep(0.4)       
        subprocess.call(['irsend','SEND_ONCE','newtv','KEY_0'], shell=False)
        time.sleep(10)
        
def zappPlus(loop):
        for i in range (0,loop):
                subprocess.call(['irsend','SEND_ONCE','newtv','KEY_CHANNELUP'], shell=False)
                time.sleep(1)
        time.sleep(2)  
def zappMinus(loop):
        for i in range (0,loop):
                subprocess.call(['irsend','SEND_ONCE','newtv','KEY_CHANNELDOWN'], shell=False)
                time.sleep(1)
        time.sleep(5)

def cmd_output(to_find,lines):
    cmd = ('tail -n'+str(lines)+' /home/pi/Desktop/output.txt | grep -i "'+to_find+'"')
    output = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
    result = output.stdout.read()
    if to_find in result:
        return True
    else:
        return False

def saveCrash(i):
        cmd = ('tail -n500 /home/pi/Desktop/output.txt')
        output = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
        result = output.stdout.read()
        with open('/home/pi/Desktop/test_channel690/crash+'+str(i)+'.txt', 'w')as file:
                file = file.write(result)
def ZappOK():
        zappPlus(2)
        zappMinus(2)
        isChannelOK = checkChannel('690')
        while isChannelOK:
                channel()
                isChannelOK = checkChannel('690')
        checkOK = cmd_output('displayAdultCode() > start',50)
        return checkOK

def CrashCheck():
        toCheck = ['Loaded shared libraries','SIGNAL_handler','DM_DA']
        result = []
        for element in toCheck:
                checkIFcrash = cmd_output(element,500)
                if checkIFcrash != True:
                        pass
                else:
                        result.append(element)
        if len(result) > 0:
                return False
        else:
                return True

def checkChannel(idChannel):
        checkOK = cmd_output('Selecting channel '+idChannel,250)
        if checkOK:
                return False
        else:
                return True

def pin():
        for i in range(0,4):
                subprocess.call(['irsend','SEND_ONCE','newtv','KEY_1'], shell=False)
                time.sleep(1)
        subprocess.call(['irsend','SEND_ONCE','newtv','KEY_OK'], shell=False)
        time.sleep(2)
        
def randomEnterPIN():
        schedule = randint(0,3)
        if schedule == 2:
                pin()
                time.sleep(4)
                        
def main():
        for j in range (0,100):
                CRASH = True
                timeCount = 0
                i = 0
                print('Tune to channel 690 ')
                channel()
                isChannelOK = checkChannel('690')
                while isChannelOK:
                        channel()
                        isChannelOK = checkChannel('690')
                while CRASH or timeCount == 360000:
                        start = time.time()
                        print('Channel p+ || p- ')
                        AdultCode = ZappOK()
                        print(' Adul kode or crash check ')
                        if AdultCode is not True:
                                CRASH = CrashCheck()
                                if CRASH:
                                        isOK = 'No'
                                        end = time.time()

                                else:
                                        isOK = 'Yes'
                                        end = time.time()
                                        saveCrash(i)
                                        os.system('echo "a" > /dev/ttyUSB0')
                                        time.sleep(2)
                                        os.system('echo "reboot -f" > /dev/ttyUSB0')
                                        time.sleep(160)

                        else:
                                CRASH = True
                                isOK = 'No'
                                print('Adul kod widoczny')
                                pin()
                                PIN_ok = cmd_output("stb.pctrl> unlockMoralityLevel(1111)",300)
                                while PIN_ok is not True:
                                        pin()
                                        PIN_ok = cmd_output("getValue returns 1111",300)
                                        isChannelOK = checkChannel('690')
                                        while isChannelOK:
                                                channel()
                                                isChannelOK = checkChannel('690')
                                end = time.time()
                        
                        timeCount += round(end-start,2)
                        with open('/home/pi/Desktop/test_channel690/results.txt', 'a+')as file:
                                file = file.write(str(timeCount)+'_crash: '+isOK+'\n')
                        i += 1
                        print('Round: '+str(i)+' end')
        
main()     
