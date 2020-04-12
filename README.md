# Windows Hello feature using Python
## *Unlock your PC using your face*

This project is developed for those PC and laptops which are not compatible for Windows Hello because they lack proper IR camera. 

After properly setting all the requirements your laptop will be able to recognize difference between you and any other person and will unlock/lock itself accordingly. It will also greet you after your authorization. 

## *Requirements* 
+ Proper Web camera
+ Python 3 or any higher version 
+ Python Modules 
  * OpenCV 
  * Numpy
  * Pillow
  * pyautogui
  * Some other requirements are mentioned in requirements.txt 

## *Working*
Program has been divided into three scripts :
* database.py - This script will create a dataset of your face by capturing your 300 photos and will store them in dataset folder. 
  #### _Note:-Make sure you give different facial expressions so that model can be trained efficiently._

* training.py - From previously created dataset folder this python script will train your model so that next time your laptop/PC can recognize you. This is  acheived by using `train()` function from opencv library.   

* recognizer.py - This is the main script that identifies your face in real-time. It will check whether the model is trained for this face and if the face seems to be unknown then it will lock your machine.

* script_runner.bat - This is a bat file that will run your script through cmd, provided path to your python interpreter is properly set.

#### _Note:- In all these python scripts and script_runner.bat, make sure that you set the path according to your PC.(i.e. Changing address of python.exe in bat file as path may differ in your machine)_

## *How to Setup?*  
* Download the files to fixed location.
* Install the requirements using `pip install -r requirements.txt`
* Compile database.py and make sure that dataset folder is created. 
* Now compile training.py and check whether .yml file is created.
* Change script's name in .bat file to recognizer.py and run .bat file. This will run recognizer.py as mentioned above. 
* In order to make this file run everytime on log on you need to set up a task using Windows Task Scheduler. For this create a task, click on New in Triggers Tab and select '_On workstation Unlock_', now select '_Start a Program_' from Action Tab and browse for your .bat file.
* If done properly your PC would have now a custom Windows Hello feature.

