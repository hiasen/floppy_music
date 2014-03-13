import RPi.GPIO as GPIO
import time

STEP = 1
DIRECTION= 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIRECTION, GPIO.OUT)
GPIO.output(DIRECTION, False)

settings = {}

def move(number, direction):
    periode = 0.1   
    GPIO.output(DIRECTION, direction)
    for i in xrange(number):
        GPIO.output(STEP, True)
        time.sleep(periode/2)
        GPIO.output(STEP, False)
        time.sleep(periode/2)
    

def reset():
    settings['position'] = 0
    periode = 0.01   
    direction = True
    number = 85
    GPIO.output(DIRECTION, direction)
    for i in xrange(number):
        GPIO.output(STEP, True)
        time.sleep(periode/2)
        GPIO.output(STEP, False)
        time.sleep(periode/2)
    
    
    

def play_frequency(freq, duration, direction):
    periode = 1.0/freq
    GPIO.output(DIRECTION, direction)
    step_number = int(duration/periode)
    settings['position'] += step_number

    for i in xrange(step_number):
        GPIO.output(STEP, True)
        time.sleep(periode/2)
        GPIO.output(STEP, False)
        time.sleep(periode/2)

def oysteins_melody():
    for i in xrange(100):
        play_frequency(10*2**(i/12.), 0.5, i%2==1)

def lisa_gikk_til_skolen():
   start = 55 
   duration = 0.75 
   play_frequency(start, duration, False)
   play_frequency(start*2**(2./12), duration, True)
   play_frequency(start*2**(4./12), duration, False)
   play_frequency(start*2**(5./12), duration, True)
   play_frequency(start*2**(7./12), 2*duration, False)
   play_frequency(start*2**(7./12), 2*duration, True)
   play_frequency(start*2**(9./12), duration, False)
   play_frequency(start*2**(9./12), duration, True)
   play_frequency(start*2**(9./12), duration, False)
   play_frequency(start*2**(9./12), duration, True)
   play_frequency(start*2**(9./12), duration, False)


def hunviks_melody():
    play_frequency(100, 0.3,False)
    play_frequency(30, 1.0, True)
    play_frequency(220, 0.5, False)
    play_frequency(55, 0.7, True)

