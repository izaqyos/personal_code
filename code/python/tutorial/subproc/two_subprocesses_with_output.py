# two_subprocesses_with_output.py

import subprocess
import threading
import sys
import Queue


def read_output(pipe, q):
    """reads output from `pipe`, when line has been read, puts
line on Queue `q`"""

    while True:
        l = pipe.readline()
        q.put(l)

# start both `proc_a.py` and `proc_b.py`
proc_a = subprocess.Popen(["stdbuf", "-o0", "python2", "proc_a.py"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)
proc_b = subprocess.Popen(["stdbuf", "-o0", "python2", "proc_b.py"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# queues for storing output lines
pa_q = Queue.Queue()
pb_q = Queue.Queue()

# start a pair of threads to read output from procedures A and B
pa_t = threading.Thread(target=read_output, args=(proc_a.stdout, pa_q))
pb_t = threading.Thread(target=read_output, args=(proc_b.stdout, pb_q))
pa_t.daemon = True
pb_t.daemon = True
pa_t.start()
pb_t.start()

while True:
    # check if either sub-process has finished
    proc_a.poll()
    proc_b.poll()

    if proc_a.returncode is not None or proc_b.returncode is not None:
        break

    # write output from procedure A (if there is any)
    try:
        l = pa_q.get(False)
        sys.stdout.write("A: ")
        sys.stdout.write(l)
    except Queue.Empty:
        pass

    # write output from procedure B (if there is any)
    try:
        l = pb_q.get(False)
        sys.stdout.write("B: ")
        sys.stdout.write(l)
    except Queue.Empty:
        pass
