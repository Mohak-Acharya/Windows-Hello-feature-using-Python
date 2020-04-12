import cv2,os,csv,sys            

# function to check path 
def check_path(path):            
    dir = os.path.dirname(path)  
    if not os.path.exists(dir):
        os.makedirs(dir)

def func(path):
    if not os.path.exists(path):
        with open('data.csv','w') as o:
            pass

#Creates an empty csv file if not present
func('data.csv')

#create dict from csv file 
reader = csv.reader(open('C:/Users/hp/Desktop/Face_Recog/data.csv', 'r'))
idn = {}
for row in reader:
    if not row:
        break
    k,v = row
    k=int(k) 
    idn[k] = v
    
b=not idn

#Assigning unique ID to each person and related conditions
count=0; idn={}; flag=0; 
while(count==0):
    name=input('Enter your name:')
    name=name.lower()
    if(name in idn.values()):
        temp=input('Are you already registered user?(Y/N)')
        temp=temp[0].lower()
        if temp=='y':
            idv=int(input('Enter your id'))
            if(idn.get(idv) == name):
                print('Verified\nDataset already exsists')
                flag=1
                sys.exit()
            else:
                print('Sorry! ID is incorrect\nTry Again!!')
                flag=0
                continue
        elif temp == 'n':   
            id=1 if b else (max(idn.keys())+1)
            idn[id]=name
            print('ID assigned to '+name+' is :   '+str(id))
            count+=1
            flag=1
        else:
            print('Only Y and N are allowed')
            flag=0
            continue
    if flag == 0:           
        id=1 if b else (max(idn.keys())+1)
        idn[id]=name
        print('ID assigned to '+name+' is :   '+str(id))
        count+=1
    flag=0

#Saving a dict to a csv file
with open('C:\\Users\\hp\\Desktop\\Face_Recog\\data.csv', 'w') as f:
    for key in idn.keys():
        f.write("%s,%s\n"%(key,idn[key]))

cam = cv2.VideoCapture(0)  #Start video capturing, 0 indicates my webcam

# Detect face object in video stream using Haarcascade Frontal Face 
facecasc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

face_id = id  # Unique ID assigned to each person
count = 0    # Initialize count to 0

# check_path function is called to create dataset folder 
check_path("dataset/")

# Try giving different facial expressions so that model can be trained more efficiently

while(True):

    # Capture video frame _, is used to ignored first value because cam.read() is returning a bool & a img_frame
    _,imgframe = cam.read()   

    gray = cv2.cvtColor(imgframe, cv2.COLOR_BGR2GRAY) # Convert frame to grayscale
    faces = facecasc.detectMultiScale(gray, 1.4, 5) 
    
    for (x,y,w,h) in faces:

        #Crop the image frame into rectangle and count++
        cv2.rectangle(imgframe, (x,y), (x+w,y+h), (255,0,0), 2) 
        count += 1

        #Saving images in a proper naming convention for future use  
        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w]) 
        cv2.imshow('Scanning...', imgframe)  #To display on title bar of cam window

   # Having a delay of 100 frames so every img has some unique characteristics
    if cv2.waitKey(100) & 0xFF == 27:                   
        break

    elif count>300:   # After 300 images are taken, loop breaks                                  
        break

#Stop video & close all windows
cam.release()
cv2.destroyAllWindows()
