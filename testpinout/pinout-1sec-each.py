print "- - - - Starting Test - - - -"

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
print "using BOARD mode to number the pins"
#  Pin Map - Power, Ground, and GPIO     #
# -------------------------------------- #
# 5v 3p Gd _8 10 12 Gd 16 18 Gd 22 24 26 # 
# 3p _3 _5 _7 Gd 11 13 15 3p 19 21 24 Gd #
# -------------------------------------- #

outpin = (8, 10, 12, 16, 18, 22, 24, 26)

for p in outpin:
        GPIO.setup(p, GPIO.OUT)

print "each of 8 pins will switch on for 1sec in sequence"

flash_on_time = 1
wait_off_time = 0.25

i = 1
for p in outpin:
        print "output", i, "on pin:"
        print p
        GPIO.output(p, 1)
        print "is on..."
        time.sleep(flash_on_time)
        GPIO.output(p, 0)
        print "...is off"
        time.sleep(wait_off_time)
        i = i+1


GPIO.cleanup()

print '- - - - End of Test - - - -'
