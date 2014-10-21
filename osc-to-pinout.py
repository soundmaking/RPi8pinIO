""" python3
	coding by sdf
	soundmaking.co.uk
"""

""" code marked 'added but not tested' 
	should be uncommented hen ready to test it...
	... other lines may beed to be commented out 
	when testing the new ones!
"""

devmode = True

import RPi.GPIO as GPIO
import time

import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server


GPIO.setmode(GPIO.BOARD)
#  Pin Map - Power, Ground, and GPIO     #
# -------------------------------------- #
# 5v 3p Gd _8 10 12 Gd 16 18 Gd 22 24 26 # 
# 3p _3 _5 _7 Gd 11 13 15 3p 19 21 24 Gd #
# -------------------------------------- #

# added but not tested 1 of 3 (changed pin out mapping)

#           8  7  6     5  4     3  2  1 # 
#  |  |  |  |  |  |  |  |  |  |  |  |  | #
# 5v 3p Gd _8 10 12 Gd 16 18 Gd 22 24 26 #

outpin = (26, 24, 22, 18, 16, 12, 10, 8)

# end of added but not tested 1 of 3 : comment below to test above """
""""
#           1  2  3     4  5     6  7  8 # 
#  |  |  |  |  |  |  |  |  |  |  |  |  | #
# 5v 3p Gd _8 10 12 Gd 16 18 Gd 22 24 26 #
outpin = (8, 10, 12, 16, 18, 22, 24, 26)
"""
for p in outpin:
        GPIO.setup(p, GPIO.OUT)
        GPIO.output(p, 1)


def set_relay(pin_, val_):
  if val_ == 0:
    v = 1
  else:
    v = 0
  GPIO.output(outpin[pin_-1], v)


def pinout_1_handler(unused_addr, args, value):
	set_relay(1, value)

def pinout_2_handler(unused_addr, args, value):
	set_relay(2, value)

def pinout_3_handler(unused_addr, args, value):
	set_relay(3, value)

def pinout_4_handler(unused_addr, args, value):
	set_relay(4, value)



""" # added but not tested 2 of 3 
def pinout_5_handler(unused_addr, args, value):
	set_relay(5, value)

def pinout_6_handler(unused_addr, args, value):
	set_relay(6, value)

def pinout_7_handler(unused_addr, args, value):
	set_relay(7, value)

def pinout_8_handler(unused_addr, args, value):
	set_relay(8, value)

# end of added but not tested 2 of 3  --- test at same time as 3 of 3 """



def kill_it(unused_addr, args, val):
	if val == 1:
		if devmode:
			print("shutting down...")
		GPIO.cleanup()
		server.shutdown()


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/debug", print)
#  dispatcher.map("/volume", print_volume_handler, "Volume")
#  dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)
  dispatcher.map("/pinout1", pinout_1_handler, "PinOut_1")
  dispatcher.map("/pinout2", pinout_2_handler, "PinOut_2")
  dispatcher.map("/pinout3", pinout_3_handler, "PinOut_3")
  dispatcher.map("/pinout4", pinout_4_handler, "PinOut_4")

  """ # added but not tested 3 of 3 
  dispatcher.map("/pinout5", pinout_5_handler, "PinOut_5")
  dispatcher.map("/pinout6", pinout_6_handler, "PinOut_6")
  dispatcher.map("/pinout7", pinout_7_handler, "PinOut_7")
  dispatcher.map("/pinout8", pinout_8_handler, "PinOut_8")
  
  # end of added but not tested 3 of 3 """ 


  dispatcher.map("/killit", kill_it, "Kill")

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()

