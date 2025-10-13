import subprocess

proc_a = subprocess.Popen(["echo", " proc_a"], stdin=subprocess.PIPE,
    stdout=subprocess.PIPE)
proc_b = subprocess.Popen(["echo"," proc_b"], stdin=subprocess.PIPE,
    stdout=subprocess.PIPE)

try:
    outs, errs = proc_a.communicate(timeout=1)
except TimeoutExpired:
    proc_a.kill()
    outs, errs = proc_a.communicate()
    print(outs, errs)

try:
    outs, errs = proc_b.communicate(timeout=1)
except TimeoutExpired:
    proc_b.kill()
    outs, errs = proc_b.communicate()
    print(outs, errs)


#while True:
#    # check if either sub-process has finished
#    proc_a.poll()
#    proc_b.poll()
#
#    if proc_a.returncode is not None or proc_b.returncode is not None:
#        break
