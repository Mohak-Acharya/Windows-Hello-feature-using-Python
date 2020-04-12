import cv2,os
import numpy as np    
from PIL import Image

# function to check path 
def check_path(path):           
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

# Create Local Binary Patterns Histograms for face recognization
recog = cv2.face.LBPHFaceRecognizer_create()  
detect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

#method to get the data related to images
def imgdata(path):

    #this gives list of all imagepaths 
    imgpaths = [os.path.join(path,f) for f in os.listdir(path)]     

     # create empty face sample list & ids list
    facesamp=[]        
    ids = []        

    # Loop for all the file path
    for img in imgpaths:  

        # ignore if the file does not have jpg extension :
        if(os.path.split(img)[-1].split(".")[-1]!='jpg'):
            continue   

        #Converting img to grayscale & then to numpy array
        pil_img = Image.open(img).convert('L')    
        img_numpy = np.array(pil_img,'uint8')       

        #retreiving img id 
        id = int(os.path.split(img)[-1].split(".")[1])

        faces = detect.detectMultiScale(img_numpy)  # Get the face from the training images

        for (x,y,w,h) in faces:   # Loop for each face

            # Adding the img to facesamp list & id to ids list
            facesamp.append(img_numpy[y:y+h,x:x+w])        
            ids.append(id)

    return facesamp,ids  

faces,ids = imgdata('C:/Users/hp/Desktop/Face_Recog/dataset')  
recog.train(faces, np.array(ids)) # Train the model using the faces and IDs

check_path('C:/Users/hp/Desktop/Face_Recog/train/') 

#saving our results to a yaml file
recog.save('C:/Users/hp/Desktop/Face_Recog/train/train.yml')
