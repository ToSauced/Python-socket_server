import socket
import threading
from queue import Queue
import time
import os

# number of threads should always match # of jobs 
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1,2] # 1: running jobs, 2: accepting connections
queue = Queue()

# connected clients
all_connections = [] # for computers connection view
all_addresses = [] # for human connection view

def socket_create():
  try:
    global s
    s = socket.socket() # the actual connection/conversation between the computers
  except socket.error as msg:
    print("Socket Failed Connection (already bound?): " + str(msg))

# bind socket (channel) to a port, awaits connections here 
def socket_bind():
  try:
    global s
    s.bind(('', 55885)) # binds to current ip, and random ephermeral port
    s.listen(5)
        
  except socket.error as msg:
    print("[ERR0R] Socket binding error (ctrl+c to exit): " + str(msg) + "\n")
    time.sleep(5)
    socket_bind()

# Accept connections from multiple clients and save to list
def socket_accept():
  for connection in all_connections:
    connection.close()
    del all_connections[:]        
    del all_addresses[:]
    
  while 1:
    try:
      conn, address = s.accept()
      conn.setblocking(1) # I don't want any timeout, disconnects when interrupted
      all_connections.append(conn)
      all_addresses.append(address)
      print("\nConnection Established | Client: "+str(address[0])+" | Port: "+str(address[1]))
    except Exception as msg:
      print("Connection establishing failed: "+str(msg))

def main_console():
  print("Please wait for prompt to appear, type 'list' or 'select' to get started.") 
  time.sleep(3)
  while True: 
    cmd = input("socket-server >> ")
    if cmd == 'list': 
      results = ''
      total = 0
      for i, conn in enumerate(all_connections):
        try:
          conn.send(str.encode(' '))
          conn.recv(20480)
        except socket.error as msg:
        # remove client from connections if connection error
          del all_connections[i]
          del all_addresses[i]
          continue
        results += '[ID: ' + str(i) + '] IP: ' + str(all_addresses[i][0]) + ' | Port: ' + str(all_addresses[i][1]) + '\n'
        total=total+1
      print('-=+ Connected Machines ['+ str(total) +'] +=-' + '\n' + results)
    elif cmd == 'exit':
      print("..closing...")
      time.sleep(1)
      os._exit(0)
    elif cmd == 'help':
        print("List: List out connected clients\n")
    elif cmd == 'clear':
        os.system("cls" if os.name=="nt" else "clear")

#threading

def create_jobs():
  for x in JOB_NUMBER:
    queue.put(x) # schedule task
  queue.join()

def create_workers():
  for _ in range(NUMBER_OF_THREADS):
    t = threading.Thread(target=work)
    t.daemon = True # designates as a subprocess of this (dies on exit)
    t.start()
def work():
  while True:
    x = queue.get()
    # define task # operations
    if x == 1:
      socket_create()
      socket_bind()
      socket_accept()
    elif x == 2:
      main_console()
    queue.task_done()

if __name__ == '__main__':
    create_workers()
    create_jobs()
