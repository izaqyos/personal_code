#!/usr/local/bin/python3
import subprocess, shlex
import sys, os
import threading
import queue

def read_output(name, pipe, q):
    """reads output from `pipe`, when line has been read, puts
line on Queue `q`"""
    while True:
        l = pipe.readline()
        #print('read input of {} - {}'.format( name, l)) 
        q.put(l)

cmds=[ "ls -l", "ls -a", "./print_nums.sh"]

p0  = subprocess.Popen(shlex.split(cmds[0]), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p1  = subprocess.Popen(shlex.split(cmds[1]), stdin=subprocess.PIPE, stdout=subprocess.PIPE)
#for line in iter(process.stdout.readline, b''):  
#    sys.stdout.write(line.decode())

p0q = queue.Queue()
p1q = queue.Queue()

p0_t = threading.Thread(target=read_output, args=('p0', p0.stdout, p0q))
p1_t = threading.Thread(target=read_output, args=('p1', p1.stdout, p1q))
#p0_t.daemon = True
#p1_t.daemon = True
p0_t.start()
p1_t.start()

while True:
    # check if either sub-process has finished
    p0.poll()
    p1.poll()

    if p0.returncode is not None or p1.returncode is not None:
        break

    # write output from procedure A (if there is any)
    try:
        l = p0q.get(False)
        sys.stdout.write("P0: ")
        sys.stdout.write(l.decode())
    except queue.Empty:
        pass

    # write output from procedure B (if there is any)
    try:
        l = p1q.get(False)
        sys.stdout.write("P1: ")
        sys.stdout.write(l.decode())
    except queue.Empty:
        pass
