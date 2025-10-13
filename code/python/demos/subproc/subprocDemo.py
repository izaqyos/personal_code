#!/usr/local/bin/python3
import subprocess, shlex
import sys, os

cmd="cat "+ os.getcwd()+os.sep+"subprocDemo.py" 
#cmd="cf logs portal-cf-site-semantic-service"
cmdArgs=shlex.split(cmd)
print(cmdArgs)

with open('test.log', 'wb') as f:  
    process = subprocess.Popen(cmdArgs, stdout=subprocess.PIPE)
    for line in iter(process.stdout.readline, b''):  
        sys.stdout.write(line.decode())
        f.write(line)

#process = subprocess.Popen(cmdArgs, stdout=subprocess.PIPE)
#while True:
#    line = process.stdout.readline()
#    if process.poll is not None and line == '':
#        break
#    if line:
#        print(line)
#retval = process.poll()

