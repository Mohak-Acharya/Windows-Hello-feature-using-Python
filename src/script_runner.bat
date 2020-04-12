@echo off
if not defined iammaximized (
    set iammaximized=1
    start /max "" "%0" "%*"
    exit
)
"C:\Users\hp\Anaconda3\python.exe" "C:\Users\hp\Desktop\Face_Recog\recognizer.py" %*
exit
