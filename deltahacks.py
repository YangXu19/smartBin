import io
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
 
# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
 
from gpiozero import DistanceSensor
from time import sleep
 
from picamera import PiCamera



import RPi.GPIO as GPIO  # Imports the standard Raspberry Pi GPIO library
#from time import sleep   # Imports sleep (aka wait or pause) into the program

# GPIO.cleanup()
GPIO.setmode(GPIO.BCM) # Sets the pin numbering system to use the physical layout
GPIO.setwarnings(False)
GPIO.setup(17,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
big_servo = GPIO.PWM(17, 50)


GPIO.setup(2,GPIO.OUT)  # Sets up pin 11 to an output (instead of an input)
small_servo = GPIO.PWM(2, 50)     # Sets up pin 11 as a PWM pin



 
sensor=DistanceSensor(trigger=18,echo=24)
 
camera=PiCamera()
 
recycle = ['Plastic', 'Plastic bottle', "Paper", "Carton", "Newspaper", "Cardboard", 'Water']
organic = ['Egg', "Food", "Paper Towel", "Vegetable", "Fruit"]
 
 
 
 
cred = credentials.Certificate("INSET CREDENTIALS")





def sortGarbage(): 
    # Set up pin 11 for PWM
    option=garbage_type()
    print(option)
    
    print()
    if option == 'recycle':
           # Sets up pin 11 as a PWM pin
                   # Starts running PWM on the pin and sets it to 0
        big_servo.start(0)
        big_servo.ChangeDutyCycle(12)     # Changes the pulse width to 3 (so moves the servo)
        sleep(0.8)                 # Wait 1 second
        big_servo.ChangeDutyCycle(0)
        sleep(1.2)  # Changes the pulse width to 12 (so moves the servo)
        big_servo.stop()



        small_servo.start(0) 
        sleep(1)                  # Wait 1 second
        small_servo.ChangeDutyCycle(12)    # Changes the pulse width to 12 (so moves the servo)
        sleep(3)
        small_servo.stop() # At the end of the program, stop the PWM

#     sleep(1)
#     big_servo.start(0)               # 
#     big_servo.ChangeDutyCycle(100)     # Changes the pulse width to 3 (so moves the servo)
#     sleep(1.2)
#     big_servo.ChangeDutyCycle(0)     # Changes the pulse width to 3 (so moves the servo)
#     sleep(1.2)
#     big_servo.stop()



#might need to change this to shaahbaz's project id
firebase_admin.initialize_app(cred, {
  'projectId': "smartbin-1be82",
})
 
db = firestore.client()
 
 
def garbage_type():
    # Instantiates a client
    client = vision.ImageAnnotatorClient()
 
    # The name of the image file to annotate
    file_name = os.path.abspath('resources/image.jpg')
 
    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()
 
    image = types.Image(content=content)
 
    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
 
    #print('Labels:')
    #label: plastic, bottle, water..., label.description: plastic
    category=""
    item_tag=""
    for label in labels:
        print(label.description)
        for r in recycle:
            if label.description ==r:
                return 'recycle'
            #return 'recycle'
        if label.description in organic:
            category= 'organic'
            item_tag=label.description
        else:
            category='garbage'
            item_tag=label.description
    doc_ref = db.collection(u'items').document()
    doc_ref.set({
        u'item_cat':category,
        u'item_tag': item_tag,
    })
    return category
 
while True:
    sleep(1)
   
    distance=sensor.distance *100
   
    print(distance)
    if distance < 15:
        camera.capture('/home/pi/Documents/deltahacks/resources/image.jpg')
        #print(garbage_type())
        sortGarbage()
        

GPIO.cleanup()
        
