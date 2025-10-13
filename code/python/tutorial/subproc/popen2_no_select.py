#!/usr/local/bin/python3
import subprocess, shlex
import sys, os
import threading
import queue
import select
import pdb

def read_output(name, pipe, q):
    """reads output from `pipe`, when line has been read, puts
line on Queue `q`"""

    #pdb.set_trace()
    if streamsReady[pipe]:
        for l in iter( pipe.readline, b''):
        #print('read input of {} - {}'.format( name, l)) 
            q.put(l)


cmds=[ "cf logs portal-cf-transport-service ",  "cf logs portal-cf-site-semantic-service"]
procs = [ subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE) for cmd in cmds ]
streams = [p.stdout for p in procs]
streams2Cmds = {k:v for (k,v) in zip(streams, cmds)}
streamsReady= {k:False for k in streams}
queues = {k:queue.Queue() for k in procs}
threads = { p:threading.Thread(target=read_output, args=(streams2Cmds[p.stdout], p.stdout, queues[p])) for p in procs}

for thread in threads:
    threads[thread].daemon = True
    threads[thread].start()

while True:
    # check if either sub-process has finished
    for p in procs:
        p.poll()

    if all( p.returncode is not None for p in procs):
        break

    for stream in streamsReady:
        streamsReady[stream] = False
    rstreams,_,_ = select.select(streams, [], [])
    for stream in rstreams:
        streamsReady[stream] = True
    # write output from procedure A (if there is any)
    for q in queues:
        try:
            l = queues[q].get(False)
            sys.stdout.write(l.decode())
        except queue.Empty:
            pass



