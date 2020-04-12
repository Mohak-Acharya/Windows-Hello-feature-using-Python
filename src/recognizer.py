import cv2,sys,pyttsx3
import numpy as np
import pyautogui, os, ctypes, csv
import datetime,time
import pyHook,win32gui,logging
from threading import Timer

# This code prevents any user to provide input by blocking keyboard and mouse events 
# thus making code more secure
class blockInput():
    def OnKeyboardEvent(self,event):
        return False

    def OnMouseEvent(self,event):
        return False

    def unblock(self):
        try: self.hm.UnhookKeyboard()
        except: pass
        try: self.hm.UnhookMouse()
        except: pass

    def block(self,keyboard = True, mouse = True):
        if mouse:
            self.hm.MouseAll = self.OnMouseEvent
            self.hm.HookMouse()
        if keyboard:
            self.hm.KeyAll = self.OnKeyboardEvent
            self.hm.HookKeyboard()
        win32gui.PumpWaitingMessages()

    def __init__(self):
        self.hm = pyHook.HookManager()

# function to check path
def check_path(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

block=blockInput()
block.block()
#create dict from csv file
reader = csv.reader(open('C:/Users/hp/Desktop/Face_Recog/data.csv', 'r'))
idn = {}
for row in reader:
    k, v = row
    k=int(k) 
    idn[k] = v
        
#Counter to detect whether person is authorized or not 
correct = 0  
wrong = 0

recog = cv2.face.LBPHFaceRecognizer_create()
check_path("C:/Users/hp/Desktop/Face_Recog/train/")

#loading training model (our .yaml trainer file)
recog.read('C:/Users/hp/Desktop/Face_Recog/train/train.yml')  
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml");  

font = cv2.FONT_HERSHEY_COMPLEX_SMALL  

#Extract current time(in seconds)
now = datetime.datetime.now()        
now = now.second        

cam = cv2.VideoCapture(0) #Start capturing live video

while True:

    #initializing pyttsx3 engine 
    eng = pyttsx3.init() 
    eng.setProperty('rate', 150) #Sets voice rate of audio

    #program will lock station after 10 seconds if it doesn't see any faces.
    now1 = datetime.datetime.now()          
    now1 = now1.second
    if(now1 > now + 10):
        cam.release()
        cv2.destroyAllWindows()
        block.unblock()
        eng.say('No faces found')
        eng.runAndWait()
        ctypes.windll.user32.LockWorkStation()
        sys.exit()

    _, im =cam.read()
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,1.2,5)

    for(x,y,w,h) in faces:

        # Recognize the face using trainer.yml file and id,confidence are returned
        cv2.rectangle(im, (x-20,y-20), (x+w+20,y+h+20), (0,255,0), 4)       
        Id, confid = recog.predict(gray[y:y+h,x:x+w])
        if Id in idn.keys():
                id=str(idn.get(Id)).capitalize()
        else:
                id='Unknown'   

        #High values of confidence indicates an unauthorized user
        # confid>70 works fine for me but one may need to adjust it for more efficient face-recognition 
        if(confid>70):                 
            wrong += 1
            print("Illegal Access")
            Id = id+" +{0:.2f}%".format(round(100 - confid, 2)) 
            print(confid)
            print("Wrong - " + str(wrong))
            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (0,0,255), -1)
            cv2.putText(im, str(Id), (x,y-40), font, 1, (0,0,0), 2)

        #Low values of confidence indicate correct user(s)
        else:                             
            Id = id+" +{0:.2f}%".format(round(100 - confid, 2)) 
            print("Verified")
            print(confid)
            correct += 1
            print("Correct - " + str(correct))
            cv2.rectangle(im, (x-22,y-90), (x+w+22, y-22), (255,255,255), -1)
            cv2.putText(im, str(Id), (x,y-40), font, 1, (0,0,0), 2)

        #Tolerance of correct & wrong counters & locking/unlocking pc based on these constraints         
        if(wrong >= 3):
            sid="Unauthorized Access!"
            eng.say(sid)
            eng.runAndWait()
            pyautogui.moveTo(48,748)
            pyautogui.click(48,748)
            pyautogui.typewrite("Access Denied!!")
            cam.release()
            cv2.destroyAllWindows()
            block.unblock()
            ctypes.windll.user32.LockWorkStation()
            sys.exit()

        if(correct >= 2):
            if id!='Unknown':
                sid="Welcome"+id+"!"
            else:
                sid="" 
            eng.say(sid)
            eng.runAndWait() #To greet user through audio
            block.unblock()    
            cam.release()
            cv2.destroyAllWindows()
            sys.exit()

    cv2.imshow('Scanning...',im)

    #For terminating press '*'
    if cv2.waitKey(10) & 0xFF == ord('*'):      
        break

# Releasing back the resources
cam.release()
cv2.destroyAllWindows()
