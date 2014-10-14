import argparse
import math

from pythonosc import dispatcher
from pythonosc import osc_server



import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
#  Pin Map - Power, Ground, and GPIO     #
# -------------------------------------- #
# 5v 3p Gd _8 10 12 Gd 16 18 Gd 22 24 26 # 
# 3p _3 _5 _7 Gd 11 13 15 3p 19 21 24 Gd #
# -------------------------------------- #

outpin = (8, 10, 12, 16, 18, 22, 24, 26)

for p in outpin:
        GPIO.setup(p, GPIO.OUT)



devmode = True

def print_volume_handler(unused_addr, args, volume):
  print("[{0}] ~ {1}".format(args[0], volume))

def print_compute_handler(unused_addr, args, volume):
  try:
    print("[{0}] ~ {1}".format(args[0], args[1](volume)))
  except ValueError: pass




def pinout_1_handler(unused_addr, args, value):
	p = 1
	if value == 0:
		v = 0
	else:
		v = 1
	GPIO.output(p, v)	
	if devmode:
		print("[{0}] ~ {1}".format(args[0], value))



	


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--ip",
      default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
      type=int, default=5005, help="The port to listen on")
  args = parser.parse_args()

  dispatcher = dispatcher.Dispatcher()
  dispatcher.map("/debug", print)
  dispatcher.map("/volume", print_volume_handler, "Volume")
  dispatcher.map("/logvolume", print_compute_handler, "Log volume", math.log)
  dispatcher.map("/pinout1", pinout_1_handler, "PinOut_1")

  server = osc_server.ThreadingOSCUDPServer(
      (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  server.serve_forever()

# how to make it not forever?
# would want to end with:
# GPIO.cleanup()
