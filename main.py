import time
import os

os.chdir(r'c:\\dir')
time_int = 10080

while (time_int > 0):
    os.system('autoCommit.py')
    time.sleep(86400)
    time_int = time_int - 1