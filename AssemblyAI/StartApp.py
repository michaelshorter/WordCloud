#Repeats the script that:

#reads the contents.txt file words and transfroms them into a wordcloud

#Resizes and formats the word cloud, dithers it sorts out colours
#etc to make compatible with Inky and saves as latestWordCloud.png

#Pushes the latestWordCloud.png file to Inky

#Repeats the process every XX seconds + 30secs run time (its a slow upload)


import os
import time
import datetime


while True:
    
    print('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
    print ("Activating Script")
    os.system("python3 /home/pi/WordCloudGenerator.py")
    print ("Completed Script")
    time.sleep(100)
    print ("Finished sleep")