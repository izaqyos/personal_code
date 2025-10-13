"""
Tutorial:
    https://lyceum-allotments.github.io/2017/03/python-and-pipes-part-6-multiple-subprocesses-and-pipes/

Running the Suite

mkfifo proc_a_input
mkfifo proc_b_input
then you can run two_subprocesses_with_output_and_input.py. In another terminal, by piping input into proc_a_input or proc_b_input you should see the consequences of that input reflected in the output of the suite, for example:

    echo hi there > proc_a_input
in another terminal should give you the output:

A: what should proc A say?
B: what should proc B say?
A: Proc A says, "hi there"
A: what should proc A say?
and following this with:

    echo hi from b > proc_b_input
will give you the output:

A: what should proc A say?
B: what should proc B say?
A: Proc A says, "hi there"
A: what should proc A say?
B: Proc B says, "hi from b"
B: what should proc B say?

"""
# two_subprocesses_with_output_and_input.py

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

def read_input(write_pipe, in_pipe_name):
    """reads input from a pipe with name `read_pipe_name`,
writing this input straight into `write_pipe`"""
    while True:
        with open(in_pipe_name, "r") as f:
            write_pipe.write(f.read())

# start both `proc_a.py` and `proc_b.py`
proc_a = subprocess.Popen(["stdbuf", "-o0", "python2", "proc_a.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
proc_b = subprocess.Popen(["stdbuf", "-o0", "python2", "proc_b.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

# lists for storing the lines of output generated
pa_line_buffer = [] 
pb_line_buffer = [] 

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

# start a pair of threads to read input into procedures A and B
pa_input_thread = threading.Thread(target=read_input, args=(proc_a.stdin, "proc_a_input"))
pb_input_thread = threading.Thread(target=read_input, args=(proc_b.stdin, "proc_b_input"))
pa_input_thread.daemon = True
pb_input_thread.daemon = True
pa_input_thread.start()
pb_input_thread.start()

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
