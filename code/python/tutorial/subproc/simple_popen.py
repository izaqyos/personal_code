#!/usr/local/bin/python3
import subprocess, shlex
import sys, os

cmd="echo popen is alive"
cmdArgs=shlex.split(cmd)
print(cmdArgs)

process = subprocess.Popen(cmdArgs, stdout=subprocess.PIPE)
for line in iter(process.stdout.readline, b''):  
    sys.stdout.write(line.decode())

#while True:
#    line = process.stdout.readline()
#    if process.poll is not None and line == '':
#        break
#    if line:
#        print(line)
retval = process.poll()
print('sub proc ret val is {}'.format(retval))


