from __future__ import division
import RPi.GPIO as GPIO
import sys

from time import sleep

sleep(0.31)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3,GPIO.OUT)
pwm=GPIO.PWM(3,50)
pwm.start(0)

min_gap=0.1
def setAngle(angle):
	duty = (angle / 18) + 7
	GPIO.output(3, True)
	pwm.ChangeDutyCycle(duty)
	sleep(min_gap)
	GPIO.output(3, False)
	pwm.ChangeDutyCycle(0)

def openFor(openTime,closeTime):
	setAngle(50)
	sleep((openTime/1000)-min_gap)
	setAngle(70)
	sleep((closeTime/1000)-min_gap)
#def openFor(closeTime,openTime):
#	setAngle(70)
#	sleep((closeTime/1000)-min_gap)
#	setAngle(50)
#	sleep((openTime/1000)-min_gap)


setAngle(70)	 
print(sys.argv)
for i in range(int(len(sys.argv)/2)):
	openTime=int(sys.argv[2*i+1])
	closeTime=int(sys.argv[2*i+2])
	openFor(openTime,closeTime)
setAngle(70)	 
pwm.stop()
GPIO.cleanup()
